#!/usr/bin/env python3
"""
Exporte les tickets Jira d'un projet vers un fichier JSON.

Hypothèse : Jira Server / Data Center avec auth par Personal Access Token
(Bearer). Si tu es sur Jira Cloud, l'auth et l'endpoint sont différents
python jira_export.py --project ABC --unresolved --jql "issuetype != Epic"
python jira_export.py --project ABC --unresolved --output tickets_en_cours.json
(Basic Auth email + API token, /rest/api/3/search).

Usage :
    python jira_export.py --url https://jira.monentreprise.com --project ABC --pat "xxxx"

Ou via variables d'env (mieux, pour ne pas laisser le PAT dans l'historique shell) :
    export JIRA_URL="https://jira.monentreprise.com"
    export JIRA_PROJECT="ABC"
    export JIRA_PAT="xxxx"
    python jira_export.py

Dépendance : pip install requests
"""

import argparse
import json
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

PAGE_SIZE = 100       # Jira plafonne maxResults autour de 100 de toute façon
MAX_RETRIES = 5
RETRY_BACKOFF = 3     # secondes, multiplié par le numéro de tentative


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export des tickets Jira vers un JSON")
    parser.add_argument("--url", default=os.environ.get("JIRA_URL"),
                         help="URL de base de l'instance Jira (ex: https://jira.monentreprise.com)")
    parser.add_argument("--project", default=os.environ.get("JIRA_PROJECT"),
                         help="Clé du projet (ex: ABC)")
    parser.add_argument("--pat", default=os.environ.get("JIRA_PAT"),
                         help="Personal Access Token (Bearer). Mieux via la variable JIRA_PAT.")
    parser.add_argument("--jql", default=None,
                         help="JQL additionnel, combiné au projet (ex: 'status != Closed')")
    parser.add_argument("--unresolved", action="store_true",
                         help="Ne garde que les tickets non résolus (resolution = Unresolved) — pour avoir tous les tickets en cours")
    parser.add_argument("--fields", default="*all",
                         help="Champs à récupérer, séparés par des virgules (défaut: *all, "
                              "peut être lourd sur 500 tickets — ex: 'summary,status,assignee,created,updated')")
    parser.add_argument("--output", default="tickets.json",
                         help="Fichier de sortie JSON (défaut: tickets.json)")
    parser.add_argument("--no-verify-ssl", action="store_true",
                         help="Désactive la vérif SSL (utile si certif d'entreprise/proxy pose souci). À éviter si possible.")
    args = parser.parse_args()

    if not args.url or not args.project or not args.pat:
        parser.error("--url, --project et --pat sont requis (ou via JIRA_URL / JIRA_PROJECT / JIRA_PAT)")
    return args


def fetch_all_issues(
    base_url: str,
    pat: str,
    project: str,
    extra_jql: Optional[str],
    fields: str,
    verify_ssl: bool = True,
    unresolved: bool = False,
) -> List[Dict[str, Any]]:
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {pat}",
        "Accept": "application/json",
    })

    jql = f"project = {project}"
    if unresolved:
        jql += " AND resolution = Unresolved"
    if extra_jql:
        jql += f" AND {extra_jql}"
    jql += " ORDER BY created ASC"

    search_url = f"{base_url.rstrip('/')}/rest/api/2/search"

    all_issues: List[Dict[str, Any]] = []
    start_at = 0
    total: Optional[int] = None

    while total is None or start_at < total:
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": PAGE_SIZE,
            "fields": fields,
        }

        resp = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = session.get(search_url, params=params, verify=verify_ssl, timeout=30)
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", RETRY_BACKOFF * attempt))
                    log.warning("Rate limité (429), attente %ss...", wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                break
            except requests.exceptions.RequestException as exc:
                log.warning("Erreur réseau (tentative %s/%s) : %s", attempt, MAX_RETRIES, exc)
                if attempt == MAX_RETRIES:
                    log.error("Échec définitif à startAt=%s", start_at)
                    raise
                time.sleep(RETRY_BACKOFF * attempt)
        else:
            raise RuntimeError("Nombre max de tentatives atteint sans succès")

        data = resp.json()
        total = data.get("total", 0)
        issues = data.get("issues", [])
        all_issues.extend(issues)

        log.info("Récupéré %s/%s tickets...", len(all_issues), total)

        if not issues:
            break
        start_at += len(issues)

    return all_issues


def main() -> None:
    args = parse_args()
    verify_ssl = not args.no_verify_ssl

    log.info("Connexion à %s, projet %s", args.url, args.project)
    try:
        issues = fetch_all_issues(
            base_url=args.url,
            pat=args.pat,
            project=args.project,
            extra_jql=args.jql,
            fields=args.fields,
            verify_ssl=verify_ssl,
            unresolved=args.unresolved,
        )
    except requests.exceptions.HTTPError as exc:
        body = exc.response.text[:500] if exc.response is not None else ""
        status = exc.response.status_code if exc.response is not None else "?"
        log.error("Erreur HTTP %s : %s", status, body)
        sys.exit(1)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)

    log.info("%s tickets écrits dans %s", len(issues), args.output)


if __name__ == "__main__":
    main()
