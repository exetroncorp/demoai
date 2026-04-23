#!/usr/bin/env python3
"""Rootless Docker/Podman-compatible shim using skopeo + umoci + proot.

This command is designed for constrained environments where user namespaces,
KVM, and elevated capabilities are unavailable.

Usage examples:
  ./dockpodman.py pull alpine:latest
  ./dockpodman.py run --rm -it alpine:latest sh

For drop-in behavior, symlink this binary as `docker` and/or `podman`.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import socketserver
import subprocess
import sys
import tempfile
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

STATE_DIR = Path(os.environ.get("DOCKPODMAN_STATE", Path.home() / ".local" / "share" / "dockpodman"))
OCI_LAYOUT = STATE_DIR / "images"
BUNDLES = STATE_DIR / "bundles"
BUILDS = STATE_DIR / "builds"
CONTAINERS = STATE_DIR / "containers"


class DockpodmanError(RuntimeError):
    pass


def run(cmd: Sequence[str], capture: bool = False) -> subprocess.CompletedProcess:
    kwargs = {"check": False, "text": True}
    if capture:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE
    result = subprocess.run(list(cmd), **kwargs)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip() if capture else ""
        raise DockpodmanError(f"Command failed ({result.returncode}): {' '.join(cmd)}\n{stderr}")
    return result


def tool_exists(tool: str) -> bool:
    return shutil.which(tool) is not None


def ensure_prereqs() -> None:
    missing = [t for t in ("skopeo", "umoci", "proot") if not tool_exists(t)]
    if missing:
        raise DockpodmanError(f"Missing required tool(s): {', '.join(missing)}")


def ensure_dirs() -> None:
    OCI_LAYOUT.mkdir(parents=True, exist_ok=True)
    BUNDLES.mkdir(parents=True, exist_ok=True)
    BUILDS.mkdir(parents=True, exist_ok=True)
    CONTAINERS.mkdir(parents=True, exist_ok=True)


def sanitize_image(image: str) -> str:
    # docker.io/library/alpine:latest -> docker.io_library_alpine_latest
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", image)


def default_tag(image: str) -> str:
    if ":" in image.rsplit("/", 1)[-1]:
        return image
    return f"{image}:latest"


def oci_ref(image: str) -> str:
    image = default_tag(image)
    return f"oci:{OCI_LAYOUT / sanitize_image(image)}:latest"


def pull(image: str) -> None:
    image = default_tag(image)
    print(f"Pulling {image} ...")
    dest = OCI_LAYOUT / sanitize_image(image)
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    run(["skopeo", "copy", "--insecure-policy", f"docker://{image}", oci_ref(image)])


def ensure_unpacked(image: str) -> Path:
    image = default_tag(image)
    bundle = BUNDLES / sanitize_image(image)
    if bundle.exists() and (bundle / "rootfs").exists():
        return bundle

    if not (OCI_LAYOUT / sanitize_image(image)).exists():
        pull(image)

    bundle.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=str(BUNDLES)) as tmp:
        tmp_path = Path(tmp) / "bundle"
        run(["umoci", "unpack", "--rootless", "--image", oci_ref(image).split("oci:", 1)[1], str(tmp_path)])
        if bundle.exists():
            shutil.rmtree(bundle)
        shutil.move(str(tmp_path), bundle)
    return bundle


def parse_exec_form(value: str) -> List[str]:
    value = value.strip()
    if value.startswith("["):
        parsed = json.loads(value)
        if not isinstance(parsed, list):
            raise DockpodmanError(f"Invalid exec form: {value}")
        return [str(x) for x in parsed]
    return ["/bin/sh", "-c", value]


def parse_dockerfile(path: Path) -> List[Tuple[str, str]]:
    instructions: List[Tuple[str, str]] = []
    raw = path.read_text()
    logical = ""
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.endswith("\\"):
            logical += stripped[:-1] + " "
            continue
        logical += stripped
        parts = logical.split(maxsplit=1)
        op = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        instructions.append((op.upper(), rest.strip()))
        logical = ""
    if logical:
        parts = logical.split(maxsplit=1)
        op = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        instructions.append((op.upper(), rest.strip()))
    return instructions


def parse_from(value: str) -> Tuple[str, Optional[str]]:
    parts = value.split()
    if not parts:
        raise DockpodmanError("FROM requires an image")
    idx = 0
    while idx < len(parts) and parts[idx].startswith("--"):
        idx += 1
    if idx >= len(parts):
        raise DockpodmanError(f"FROM missing image: {value}")
    image = parts[idx]
    alias = None
    if len(parts) >= idx + 3 and parts[idx + 1].upper() == "AS":
        alias = parts[idx + 2]
    return image, alias


def parse_copy(value: str) -> Tuple[Optional[str], List[str], str]:
    tokens = shlex.split(value)
    from_stage = None
    i = 0
    while i < len(tokens) and tokens[i].startswith("--"):
        tok = tokens[i]
        if tok.startswith("--from="):
            from_stage = tok.split("=", 1)[1]
        else:
            raise DockpodmanError(f"Unsupported COPY flag: {tok}")
        i += 1
    body = tokens[i:]
    if len(body) < 2:
        raise DockpodmanError(f"Invalid COPY args: {value}")
    srcs = body[:-1]
    dst = body[-1]
    return from_stage, srcs, dst


def normalize_run_instruction(value: str) -> str:
    tokens = shlex.split(value)
    i = 0
    while i < len(tokens) and tokens[i].startswith("--"):
        i += 1
    if i >= len(tokens):
        return ""
    return " ".join(tokens[i:])


def stage_exec(stage: Dict[str, object], cmd: List[str]) -> None:
    rootfs = Path(stage["bundle"]) / "rootfs"
    full = ["proot", "-R", str(rootfs), "-0"]
    workdir = stage.get("workdir")
    if workdir:
        full.extend(["-w", str(workdir)])
    full.extend(cmd)
    run(full)


def abs_in_root(path: str, workdir: str) -> str:
    if path.startswith("/"):
        return path
    return str(Path(workdir) / path)


def copy_into_stage(stage: Dict[str, object], src_path: Path, dst_path: str) -> None:
    rootfs = Path(stage["bundle"]) / "rootfs"
    target = rootfs / dst_path.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    if src_path.is_dir():
        if target.exists() and target.is_file():
            target.unlink()
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(src_path, target)
    else:
        shutil.copy2(src_path, target)


def resolve_stage(stage_ref: str, stages: List[Dict[str, object]], aliases: Dict[str, Dict[str, object]]) -> Dict[str, object]:
    if stage_ref in aliases:
        return aliases[stage_ref]
    if stage_ref.isdigit():
        idx = int(stage_ref)
        if idx < 0 or idx >= len(stages):
            raise DockpodmanError(f"COPY --from index out of range: {stage_ref}")
        return stages[idx]
    raise DockpodmanError(f"Unknown stage in COPY --from: {stage_ref}")


def build_image(context: str, dockerfile: str, tag: str) -> None:
    context_dir = Path(context).resolve()
    dockerfile_path = Path(dockerfile).resolve()
    if not context_dir.exists():
        raise DockpodmanError(f"Build context does not exist: {context_dir}")
    if not dockerfile_path.exists():
        raise DockpodmanError(f"Dockerfile not found: {dockerfile_path}")

    instructions = parse_dockerfile(dockerfile_path)
    stages: List[Dict[str, object]] = []
    aliases: Dict[str, Dict[str, object]] = {}
    current: Optional[Dict[str, object]] = None
    build_tmp = Path(tempfile.mkdtemp(dir=str(BUILDS)))
    try:
        for op, value in instructions:
            if op == "FROM":
                image, alias = parse_from(value)
                image = default_tag(image)
                pull(image)
                stage_name = alias or f"stage{len(stages)}"
                stage_layout = build_tmp / f"{stage_name}_layout"
                src_layout = OCI_LAYOUT / sanitize_image(image)
                if stage_layout.exists():
                    shutil.rmtree(stage_layout)
                shutil.copytree(src_layout, stage_layout)
                stage_ref = f"{stage_layout}:latest"
                bundle = build_tmp / f"{stage_name}_bundle"
                run(["umoci", "unpack", "--rootless", "--image", stage_ref, str(bundle)])
                current = {
                    "name": stage_name,
                    "layout": stage_layout,
                    "bundle": bundle,
                    "workdir": "/",
                    "cmd": None,
                    "entrypoint": None,
                }
                stages.append(current)
                aliases[stage_name] = current
            elif current is None:
                raise DockpodmanError(f"{op} appears before any FROM")
            elif op == "WORKDIR":
                current["workdir"] = abs_in_root(value, str(current["workdir"]))
                stage_exec(current, ["/bin/mkdir", "-p", str(current["workdir"])])
            elif op == "RUN":
                run_cmd = normalize_run_instruction(value)
                if not run_cmd:
                    raise DockpodmanError(f"Unsupported RUN format: {value}")
                stage_exec(current, ["/bin/sh", "-c", run_cmd])
            elif op == "COPY":
                from_stage, srcs, dst = parse_copy(value)
                dst_abs = abs_in_root(dst, str(current["workdir"]))
                for src in srcs:
                    if from_stage:
                        from_obj = resolve_stage(from_stage, stages, aliases)
                        from_root = Path(from_obj["bundle"]) / "rootfs"
                        matches = list(from_root.glob(src.lstrip("/")))
                    else:
                        matches = list(context_dir.glob(src))
                    if not matches:
                        raise DockpodmanError(f"COPY source not found: {src}")
                    for m in matches:
                        copy_into_stage(current, m, dst_abs)
            elif op == "CMD":
                current["cmd"] = parse_exec_form(value)
            elif op == "ENTRYPOINT":
                current["entrypoint"] = parse_exec_form(value)

        if not stages:
            raise DockpodmanError("Dockerfile has no FROM stage")

        final = stages[-1]
        run(["umoci", "repack", "--image", f"{final['layout']}:latest", str(final["bundle"])])

        final_dest = OCI_LAYOUT / sanitize_image(default_tag(tag))
        if final_dest.exists():
            shutil.rmtree(final_dest)
        shutil.move(str(final["layout"]), final_dest)
    finally:
        shutil.rmtree(build_tmp, ignore_errors=True)


def parse_run_args(args: List[str]) -> Tuple[Dict[str, object], str, List[str]]:
    opts: Dict[str, object] = {
        "rm": False,
        "interactive": False,
        "tty": False,
        "detach": False,
        "name": None,
        "workdir": None,
        "env": {},
        "volumes": [],
    }

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--rm":
            opts["rm"] = True
        elif arg in ("-i", "--interactive"):
            opts["interactive"] = True
        elif arg in ("-t", "--tty"):
            opts["tty"] = True
        elif arg in ("-d", "--detach"):
            opts["detach"] = True
        elif arg == "--name":
            i += 1
            opts["name"] = args[i]
        elif arg in ("-it", "-ti"):
            opts["interactive"] = True
            opts["tty"] = True
        elif arg in ("-w", "--workdir"):
            i += 1
            opts["workdir"] = args[i]
        elif arg in ("-e", "--env"):
            i += 1
            kv = args[i]
            if "=" not in kv:
                raise DockpodmanError(f"Invalid env format: {kv}; expected KEY=VALUE")
            k, v = kv.split("=", 1)
            opts["env"][k] = v
        elif arg in ("-v", "--volume"):
            i += 1
            opts["volumes"].append(args[i])
        elif arg in ("--pull", "--platform", "--network", "--user", "--entrypoint"):
            i += 1
        elif arg.startswith("-"):
            raise DockpodmanError(
                f"Unsupported run flag: {arg}. Supported: --rm, -i, -t, -d, -it, -w, -e, -v, --name"
            )
        else:
            image = arg
            cmd = args[i + 1 :] if i + 1 < len(args) else []
            return opts, image, cmd
        i += 1

    raise DockpodmanError("Missing image name for run")


def run_with_opts(opts: Dict[str, object], image: str, cmd: List[str], capture: bool = False) -> Tuple[int, str, str]:
    bundle = ensure_unpacked(image)
    rootfs = bundle / "rootfs"

    if not cmd:
        cmd = ["/bin/sh"]

    proot_cmd = ["proot", "-R", str(rootfs), "-0"]

    workdir = opts["workdir"]
    if workdir:
        proot_cmd.extend(["-w", str(workdir)])

    for vol in opts["volumes"]:
        proot_cmd.extend(["-b", vol])

    env = os.environ.copy()
    env.update(opts["env"])

    proot_cmd.extend(cmd)
    if opts.get("detach"):
        proc = subprocess.Popen(proot_cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rc = 0
        out, err = str(proc.pid), ""
    elif opts["tty"] or opts["interactive"]:
        proc = subprocess.run(proot_cmd, env=env)
        rc = proc.returncode
        out, err = "", ""
    else:
        proc = subprocess.run(proot_cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = proc.stdout or ""
        err = proc.stderr or ""
        if not capture:
            if out:
                print(out, end="")
            if err:
                print(err, file=sys.stderr, end="")
        rc = proc.returncode

    if opts["rm"]:
        shutil.rmtree(bundle, ignore_errors=True)
    return rc, out, err


def run_container(args: List[str]) -> int:
    opts, image, cmd = parse_run_args(args)
    rc, _, _ = run_with_opts(opts, image, cmd, capture=False)
    return rc


def images() -> None:
    rows = []
    if OCI_LAYOUT.exists():
        for item in sorted(OCI_LAYOUT.iterdir()):
            if item.is_dir():
                rows.append({"Repository": item.name, "Tag": "latest", "Storage": str(item)})

    if not rows:
        return

    print("REPOSITORY\tTAG\tSTORAGE")
    for row in rows:
        print(f"{row['Repository']}\t{row['Tag']}\t{row['Storage']}")


def inspect(image: str) -> None:
    image = default_tag(image)
    out = run(["skopeo", "inspect", f"docker://{image}"], capture=True)
    meta = json.loads(out.stdout)
    print(json.dumps(meta, indent=2))


def rmi(image: str) -> None:
    image = default_tag(image)
    safe = sanitize_image(image)
    shutil.rmtree(OCI_LAYOUT / safe, ignore_errors=True)
    shutil.rmtree(BUNDLES / safe, ignore_errors=True)


def load_containers() -> Dict[str, Dict[str, object]]:
    db = CONTAINERS / "containers.json"
    if not db.exists():
        return {}
    return json.loads(db.read_text())


def save_containers(data: Dict[str, Dict[str, object]]) -> None:
    db = CONTAINERS / "containers.json"
    db.write_text(json.dumps(data, indent=2))


def find_container(containers: Dict[str, Dict[str, object]], ident: str) -> Optional[str]:
    if ident in containers:
        return ident
    for cid, meta in containers.items():
        if meta.get("name") == ident:
            return cid
    return None


def docker_api_handler_factory() -> type[BaseHTTPRequestHandler]:
    class DockerAPIHandler(BaseHTTPRequestHandler):
        server_version = "dockpodman-api/0.1"

        def _send(self, code: int, payload: object = None, content_type: str = "application/json") -> None:
            self.send_response(code)
            self.send_header("Api-Version", "1.41")
            if content_type:
                self.send_header("Content-Type", content_type)
            self.end_headers()
            if payload is None:
                return
            if isinstance(payload, (dict, list)):
                self.wfile.write(json.dumps(payload).encode("utf-8"))
            elif isinstance(payload, str):
                self.wfile.write(payload.encode("utf-8"))
            else:
                self.wfile.write(payload)

        def _path(self) -> str:
            return self.path.split("?", 1)[0]

        def _query(self) -> Dict[str, str]:
            q = {}
            if "?" not in self.path:
                return q
            raw = self.path.split("?", 1)[1]
            for part in raw.split("&"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    q[k] = v
            return q

        def _read_json(self) -> Dict[str, object]:
            size = int(self.headers.get("Content-Length", "0"))
            if size == 0:
                return {}
            body = self.rfile.read(size).decode("utf-8")
            if not body:
                return {}
            return json.loads(body)

        def do_GET(self) -> None:  # noqa: N802
            p = self._path()
            if p == "/_ping":
                self._send(200, "OK", content_type="text/plain")
                return
            if p in ("/version", "/v1.41/version"):
                self._send(
                    200,
                    {
                        "ApiVersion": "1.41",
                        "Version": "0.1.0",
                        "MinAPIVersion": "1.24",
                    },
                )
                return
            if p in ("/images/json", "/v1.41/images/json"):
                items = []
                if OCI_LAYOUT.exists():
                    for item in OCI_LAYOUT.iterdir():
                        if item.is_dir():
                            items.append({"Id": item.name, "RepoTags": [item.name.replace("_latest", ":latest")]})
                self._send(200, items)
                return
            if p in ("/containers/json", "/v1.41/containers/json"):
                containers = load_containers()
                out = []
                for cid, c in containers.items():
                    out.append(
                        {
                            "Id": cid,
                            "Names": ["/" + str(c.get("name", cid[:12]))],
                            "Image": c.get("image"),
                            "State": c.get("state", "created"),
                            "Status": c.get("state", "created"),
                        }
                    )
                self._send(200, out)
                return
            if p.startswith("/containers/") or p.startswith("/v1.41/containers/"):
                parts = p.strip("/").split("/")
                if parts[0].startswith("v1.41"):
                    parts = parts[1:]
                if len(parts) >= 3 and parts[2] == "json":
                    ident = parts[1]
                    containers = load_containers()
                    cid = find_container(containers, ident)
                    if not cid:
                        self._send(404, {"message": "No such container"})
                        return
                    c = containers[cid]
                    self._send(
                        200,
                        {
                            "Id": cid,
                            "Name": "/" + str(c.get("name", cid[:12])),
                            "Config": {"Image": c.get("image"), "Cmd": c.get("cmd"), "Env": c.get("env", [])},
                            "State": {"Status": c.get("state", "created")},
                        },
                    )
                    return
                if len(parts) >= 3 and parts[2] == "logs":
                    ident = parts[1]
                    containers = load_containers()
                    cid = find_container(containers, ident)
                    if not cid:
                        self._send(404, {"message": "No such container"})
                        return
                    self._send(200, str(containers[cid].get("logs", "")), content_type="text/plain")
                    return
            self._send(404, {"message": f"Unhandled endpoint {p}"})

        def do_POST(self) -> None:  # noqa: N802
            p = self._path()
            if p in ("/images/create", "/v1.41/images/create"):
                query = self._query()
                image = query.get("fromImage") or query.get("fromSrc")
                if not image:
                    self._send(400, {"message": "fromImage required"})
                    return
                pull(image)
                self._send(200, '{"status":"Pulled"}', content_type="application/json")
                return

            if p in ("/containers/create", "/v1.41/containers/create"):
                query = self._query()
                req = self._read_json()
                image = str(req.get("Image", ""))
                if not image:
                    self._send(400, {"message": "Image required"})
                    return
                cmd = req.get("Cmd") or []
                if isinstance(cmd, str):
                    cmd = [cmd]
                cid = uuid.uuid4().hex[:12]
                name = query.get("name") or cid
                containers = load_containers()
                containers[cid] = {
                    "id": cid,
                    "name": name,
                    "image": image,
                    "cmd": cmd,
                    "env": req.get("Env") or [],
                    "workdir": req.get("WorkingDir") or None,
                    "binds": ((req.get("HostConfig") or {}).get("Binds") or []),
                    "state": "created",
                    "logs": "",
                    "created": int(time.time()),
                }
                save_containers(containers)
                self._send(201, {"Id": cid, "Warnings": []})
                return

            if "/containers/" in p and p.endswith("/start"):
                parts = p.strip("/").split("/")
                if parts[0].startswith("v1.41"):
                    parts = parts[1:]
                ident = parts[1]
                containers = load_containers()
                cid = find_container(containers, ident)
                if not cid:
                    self._send(404, {"message": "No such container"})
                    return
                meta = containers[cid]
                opts: Dict[str, object] = {
                    "rm": False,
                    "interactive": False,
                    "tty": False,
                    "workdir": meta.get("workdir"),
                    "env": {},
                    "volumes": meta.get("binds", []),
                }
                for env in meta.get("env", []):
                    if "=" in env:
                        k, v = env.split("=", 1)
                        opts["env"][k] = v
                rc, out, err = run_with_opts(opts, str(meta["image"]), list(meta.get("cmd") or []), capture=True)
                meta["state"] = "exited" if rc == 0 else "error"
                meta["logs"] = out + err
                meta["exitCode"] = rc
                containers[cid] = meta
                save_containers(containers)
                self._send(204, None, content_type="")
                return
            self._send(404, {"message": f"Unhandled endpoint {p}"})

        def log_message(self, fmt: str, *args: object) -> None:
            return

    return DockerAPIHandler


class UnixHTTPServer(socketserver.UnixStreamServer):
    allow_reuse_address = True


def serve_api(bind: str) -> None:
    handler = docker_api_handler_factory()
    if bind.startswith("unix://"):
        sock_path = bind[len("unix://") :]
        try:
            os.unlink(sock_path)
        except FileNotFoundError:
            pass
        server: object = UnixHTTPServer(sock_path, handler)
        print(f"Listening on unix socket {sock_path}")
        try:
            server.serve_forever()
        finally:
            try:
                os.unlink(sock_path)
            except FileNotFoundError:
                pass
    else:
        host = "127.0.0.1"
        port = 2375
        if bind.startswith("tcp://"):
            _, addr = bind.split("://", 1)
            host, port_s = addr.rsplit(":", 1)
            port = int(port_s)
        elif ":" in bind:
            host, port_s = bind.rsplit(":", 1)
            port = int(port_s)
        server = ThreadingHTTPServer((host, port), handler)
        print(f"Listening on tcp://{host}:{port}")
        server.serve_forever()


def load_compose_file(path: str) -> Dict[str, object]:
    compose_path = Path(path)
    if not compose_path.exists():
        raise DockpodmanError(f"Compose file not found: {compose_path}")
    raw = compose_path.read_text()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except Exception as exc:
            raise DockpodmanError(
                "Compose parsing needs JSON-formatted compose file or PyYAML installed for YAML files"
            ) from exc
        data = yaml.safe_load(raw)
    if not isinstance(data, dict) or "services" not in data:
        raise DockpodmanError("Compose file must define top-level 'services'")
    return data


def topo_services(services: Dict[str, Dict[str, object]]) -> List[str]:
    ordered: List[str] = []
    temp: set[str] = set()
    perm: set[str] = set()

    def visit(name: str) -> None:
        if name in perm:
            return
        if name in temp:
            raise DockpodmanError(f"Cycle in depends_on at service '{name}'")
        temp.add(name)
        deps = services.get(name, {}).get("depends_on", [])
        if isinstance(deps, dict):
            deps = list(deps.keys())
        for dep in deps:
            if dep in services:
                visit(dep)
        temp.remove(name)
        perm.add(name)
        ordered.append(name)

    for svc in services.keys():
        visit(svc)
    return ordered


def parse_env_map(env: object) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if isinstance(env, list):
        for item in env:
            if isinstance(item, str) and "=" in item:
                k, v = item.split("=", 1)
                out[k] = v
    elif isinstance(env, dict):
        for k, v in env.items():
            out[str(k)] = str(v)
    return out


def compose_project_name(compose_path: str) -> str:
    return sanitize_image(Path(compose_path).resolve().parent.name or "default")


def compose_up(compose_file: str, detach: bool) -> None:
    compose_path = Path(compose_file).resolve()
    compose_dir = compose_path.parent
    data = load_compose_file(compose_file)
    services = data["services"]
    if not isinstance(services, dict):
        raise DockpodmanError("Compose services must be a mapping")

    project = compose_project_name(compose_file)
    containers = load_containers()
    project_state: Dict[str, str] = {}

    for name in topo_services(services):  # type: ignore[arg-type]
        svc = services[name]
        if not isinstance(svc, dict):
            continue
        image = svc.get("image")
        if not image and "build" in svc:
            build_cfg = svc["build"]
            if isinstance(build_cfg, str):
                context = str((compose_dir / build_cfg).resolve())
                dockerfile = str((Path(context) / "Dockerfile").resolve())
            elif isinstance(build_cfg, dict):
                ctx_rel = Path(str(build_cfg.get("context", ".")))
                context = str((ctx_rel if ctx_rel.is_absolute() else (compose_dir / ctx_rel)).resolve())
                df_rel = Path(str(build_cfg.get("dockerfile", "Dockerfile")))
                dockerfile = str((df_rel if df_rel.is_absolute() else (Path(context) / df_rel)).resolve())
            else:
                raise DockpodmanError(f"Invalid build config for service {name}")
            image = f"{project}_{name}:latest"
            build_image(context=context, dockerfile=dockerfile, tag=str(image))
        if not image:
            raise DockpodmanError(f"Service {name} needs image or build")

        cid = uuid.uuid4().hex[:12]
        cname = f"{project}_{name}_1"
        cmd = svc.get("command") or []
        if isinstance(cmd, str):
            cmd = ["/bin/sh", "-c", cmd]
        env_map = parse_env_map(svc.get("environment", []))
        binds = svc.get("volumes", [])
        if not isinstance(binds, list):
            binds = []
        opts: Dict[str, object] = {
            "rm": False,
            "interactive": False,
            "tty": False,
            "detach": detach,
            "workdir": svc.get("working_dir"),
            "env": env_map,
            "volumes": binds,
        }
        rc, out, err = run_with_opts(opts, str(image), list(cmd), capture=True)
        state = "running" if detach and rc == 0 else ("exited" if rc == 0 else "error")
        containers[cid] = {
            "id": cid,
            "name": cname,
            "service": name,
            "project": project,
            "image": image,
            "cmd": cmd,
            "env": [f"{k}={v}" for k, v in env_map.items()],
            "binds": binds,
            "state": state,
            "logs": out + err,
            "exitCode": rc,
            "created": int(time.time()),
        }
        project_state[name] = cid

    save_containers(containers)
    (CONTAINERS / f"compose_{project}.json").write_text(json.dumps(project_state, indent=2))


def compose_ps(compose_file: str) -> None:
    project = compose_project_name(compose_file)
    state_file = CONTAINERS / f"compose_{project}.json"
    if not state_file.exists():
        return
    state = json.loads(state_file.read_text())
    containers = load_containers()
    print("NAME\tSERVICE\tSTATE\tIMAGE")
    for svc, cid in state.items():
        meta = containers.get(cid, {})
        print(f"{meta.get('name', cid)}\t{svc}\t{meta.get('state', 'unknown')}\t{meta.get('image', '')}")


def compose_down(compose_file: str) -> None:
    project = compose_project_name(compose_file)
    state_file = CONTAINERS / f"compose_{project}.json"
    if not state_file.exists():
        return
    state = json.loads(state_file.read_text())
    containers = load_containers()
    for _, cid in state.items():
        containers.pop(cid, None)
    save_containers(containers)
    state_file.unlink(missing_ok=True)


def print_help() -> None:
    print(
        """dockpodman: rootless Docker/Podman-compatible shim

Commands:
  pull IMAGE                Pull image from registry into local OCI layout
  build [-f FILE] -t TAG CTX Build image from Dockerfile context
  run [flags] IMAGE [CMD]   Run image via proot
  serve [--host BIND]       Expose Docker-compatible API over tcp/unix
  compose [opts] CMD        Compose subset: up/down/ps
  images                    List locally cached images
  inspect IMAGE             Show remote image metadata (skopeo inspect)
  rmi IMAGE                 Remove local cached image/bundle
  --version                 Show tool versions

Run flags supported:
  --rm, -i/--interactive, -t/--tty, -d/--detach, -it, -w/--workdir, -e/--env, -v/--volume
  --name, --pull, --platform, --network, --user, --entrypoint
"""
    )


def print_version() -> None:
    print("dockpodman 0.1.0")
    for tool in ("skopeo", "umoci", "proot"):
        try:
            out = run([tool, "--version"], capture=True)
            line = (out.stdout or out.stderr).splitlines()[0] if (out.stdout or out.stderr) else "unknown"
        except Exception:
            line = "unavailable"
        print(f"{tool}: {line}")


def main(argv: List[str]) -> int:
    if len(argv) <= 1 or argv[1] in ("-h", "--help", "help"):
        print_help()
        return 0
    if argv[1] == "--version":
        print_version()
        return 0

    ensure_dirs()
    ensure_prereqs()

    cmd = argv[1]
    args = argv[2:]

    if cmd == "pull":
        if not args:
            raise DockpodmanError("pull requires IMAGE")
        pull(args[0])
        return 0
    if cmd == "build":
        dockerfile = "Dockerfile"
        tag = None
        context = "."
        i = 0
        while i < len(args):
            a = args[i]
            if a in ("-f", "--file"):
                i += 1
                dockerfile = args[i]
            elif a in ("-t", "--tag"):
                i += 1
                tag = args[i]
            elif a.startswith("-"):
                raise DockpodmanError(f"Unsupported build flag: {a}")
            else:
                context = a
            i += 1
        if not tag:
            raise DockpodmanError("build requires -t/--tag")
        build_image(context=context, dockerfile=dockerfile, tag=tag)
        return 0
    if cmd == "run":
        return run_container(args)
    if cmd == "serve":
        bind = "tcp://127.0.0.1:2375"
        i = 0
        while i < len(args):
            if args[i] in ("--host", "-H"):
                i += 1
                bind = args[i]
            else:
                raise DockpodmanError(f"Unsupported serve flag: {args[i]}")
            i += 1
        serve_api(bind)
        return 0
    if cmd == "compose":
        compose_file = "docker-compose.yml"
        i = 0
        while i < len(args) and args[i].startswith("-"):
            if args[i] in ("-f", "--file"):
                i += 1
                compose_file = args[i]
            else:
                raise DockpodmanError(f"Unsupported compose option: {args[i]}")
            i += 1
        if i >= len(args):
            raise DockpodmanError("compose requires a command (up/down/ps)")
        sub = args[i]
        rest = args[i + 1 :]
        if sub == "up":
            detach = "-d" in rest or "--detach" in rest
            compose_up(compose_file, detach=detach)
            return 0
        if sub == "ps":
            compose_ps(compose_file)
            return 0
        if sub == "down":
            compose_down(compose_file)
            return 0
        raise DockpodmanError(f"Unsupported compose command: {sub}")
    if cmd == "images":
        images()
        return 0
    if cmd == "inspect":
        if not args:
            raise DockpodmanError("inspect requires IMAGE")
        inspect(args[0])
        return 0
    if cmd == "rmi":
        if not args:
            raise DockpodmanError("rmi requires IMAGE")
        rmi(args[0])
        return 0

    raise DockpodmanError(f"Unsupported command: {cmd}")


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except DockpodmanError as err:
        print(f"error: {err}", file=sys.stderr)
        raise SystemExit(1)
