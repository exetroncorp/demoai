# IBM Bob IDE — Pack de 12 vidéos de formation
## Scénarios et scripts voix-off complets

> **Contenu strictement dérivé des sources fournies** (aucune connaissance externe injectée) :
> - Plan de formation des 12 vidéos (image fournie)
> - Documentation officielle : https://bob.ibm.com/docs/ide (page « Welcome to IBM Bob »)
> - Tutoriel Quickstart : https://bob.ibm.com/docs/ide/getting-started/quickstart
> - Changelog officiel (consulté le 02/09/2026 pour la vérification de compatibilité avec la version 2.1.0) : https://bob.ibm.com/docs/ide/changelog
>
> **Ce que sont ces documents** : pour chacune des 12 vidéos du plan de formation, ce pack fournit une fiche technique, un storyboard minuté (prêt à tourner en capture d'écran ou en montage « image par image » à partir de captures fixes) et le script voix-off intégral.

## Sommaire

| N° | Vidéo | N° | Vidéo |
|---|---|---|---|
| 1 | Découverte de l'interface BOB IDE | 7 | Review de code avec BOB |
| 2 | Les modes Ask, Plan et Agent | 8 | Literate Coding |
| 3 | Auto Approvals | 9 | Top 10 des commandes à connaître |
| 4 | Skills | 10 | Personnaliser le comportement de BOB |
| 5 | MCP (Model Context Protocol) | 11 | Démarrer un projet avec /init |
| 6 | Bien rédiger une demande à BOB | 12 | Première mission avec BOB |

Annexes : aide-mémoire des prompts officiels, glossaire, sources.

---

## Note de production (commune aux 12 vidéos)

### Format et ton

| Paramètre | Valeur |
|---|---|
| **Durée cible par vidéo** | 2 min à 2 min 30 (la durée précise figure sur chaque fiche technique ; la finale n° 12, plus dense, peut atteindre 3 min) |
| **Volume de voix-off** | ~310 à 490 mots par vidéo (rythme ≈ 150-170 mots/min ; la vidéo 4 est la plus courte, la finale n° 12 la plus dense) |
| **Ton** | Pédagogique et convivial, accessible à un public généraliste : chaque terme technique est expliqué en une phrase lors de sa première apparition |
| **Public** | Développeurs généralistes et grand public curieux |
| **Langue** | Français |

### Structure récurrente de chaque vidéo

1. **Accroche** (0:00 → 0:15) : une question ou une promesse concrète.
2. **Introduction** (0:15 → 0:30) : ce que l'on va apprendre, en une phrase.
3. **Corps** (0:30 → 2:00) : démonstration guidée dans l'interface, découpée en séquences.
4. **Récapitulatif** (≈ 2:00 → 2:15) : bandeau « À retenir » avec 3 puces maximum.
5. **Outro** (≈ 2:15 → 2:30) : teaser de la vidéo suivante + rappel de la playlist.

### Éléments visuels récurrents

- **Plaque de titre** (5 s) : numéro et titre de la vidéo sur fond sombre.
- **Zooms** sur chaque zone cliquée : le curseur est surligné et ralenti au moment des clics importants.
- **Encarts « À retenir »** : bandeau sombre, texte blanc, 3 puces maximum en fin de vidéo.
- **Surlignage des prompts** : tout texte tapé dans le chat Bob apparaît aussi en incrustation basse d'écran (lisibilité mobile).
- **Montage en images fixes** : chaque storyboard peut être tourné soit en capture d'écran animée, soit en diaporama de captures d'écran successives avec zoom et surlignage — les deux montages respectent la même time-line.

### Environnement de démonstration (identique pour toute la série)

| Élément | Valeur utilisée à l'écran |
|---|---|
| **Application** | IBM Bob — IDE autonome (une application à part entière, pas une extension d'éditeur) |
| **Dépôt de démonstration** | `https://github.com/IBM/bob-demo.git` (cloné depuis l'IDE) |
| **Dossier de travail** | `bob-get-started/express-todo-api-modern` — une API REST Express TypeScript de listes de tâches (to-do lists) |
| **Conteneur** | Docker, image Node 22, application servie sur le port 3000 |
| **Raccourci chat Bob** | Option + Commande + B (Mac) ou Ctrl + Alt + B (Windows) |
| **Avertissement à afficher une fois** (vidéo 1) | Les versions IDE v1.0.3 et v2.0.0 cesseront de fonctionner le 30 septembre 2026 : mettre à jour vers la version 2.0.2 ou plus récente (au moment du tournage, la dernière version publiée est la 2.1.0) |

### Compatibilité vérifiée avec la version 2.1.0 (août 2026)

Ce pack a été revérifié le 2 septembre 2026 contre la version 2.1.0, publiée en août 2026 d'après le changelog officiel. **Verdict : les 12 scénarios restent valides tels quels.** Les pages « Welcome to IBM Bob » et « Quickstart » n'ont pas changé de contenu, et aucune fonctionnalité mobilisée dans les vidéos — modes Ask / Plan / Agent, approbations et auto-approbation, /init, AGENTS.md, skills, MCP — n'a été retirée ni renommée. Seuls trois points méritent l'attention de l'équipe de tournage :

- **Séparateurs de progression dans le chat (nouveauté 2.1.0)** : chaque fois que Bob marque une tâche « en progrès », un séparateur stylisé affiche son libellé dans le chat. Ces encarts apparaîtront dans les captures des vidéos 11 et 12 (tâches multi-étapes) : c'est une aide de lecture normale, pas un défaut de capture.
- **Onglet Hooks dans les réglages (nouveauté 2.1.0)** : les hooks se pilotent désormais depuis un onglet dédié de Bob Settings — liste complète, recherche, bascule marche/arrêt. La vidéo 10 intègre cette ouverture.
- **Nouveautés hors plan de formation** : la 2.1.0 sait aussi lire et éditer des fichiers Office (.docx, .xlsx, .pptx) et interroger la documentation produit IBM (IBM i, z/OS, Db2, watsonx). Non couvertes par les 12 vidéos, ces capacités peuvent servir de teaser d'outro si vous le souhaitez.

---

# VIDÉO 1/12 — Découverte de l'interface BOB IDE

## Fiche technique

- **Objectif pédagogique** : savoir se repérer dans l'interface : chat, explorateur de fichiers, terminal, panneaux latéraux, historique des conversations.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① Qu'est-ce que Bob ? ② Le chat ③ L'explorateur et le terminal ④ L'historique des conversations ⑤ Première action : cloner un projet.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Écran figé de l'IDE avec un prompt tapé : « Explique ce que fait cette application » | « Et si votre éditeur de code pouvait simplement… comprendre votre projet ? » | « Et si votre IDE comprenait votre projet ? » |
| 0:15–0:35 | Présentation | Logo IBM Bob + page d'accueil | Bob = partenaire IA du cycle de vie du développement logiciel (SDLC) ; il s'intègre à vos workflows existants et travaille sur de vraies bases de code | « IBM Bob : votre partenaire IA SDLC » + bandeau « v2.0.2+ requise avant le 30/09/2026 (dernière version : 2.1.0) » |
| 0:35–0:55 | Le chat | Ouverture du panneau chat via l'icône Bob, puis raccourci Option+Cmd+B / Ctrl+Alt+B répété lentement | Le chat : on écrit des demandes en langage naturel dans le champ de saisie | « Option+Cmd+B (Mac) · Ctrl+Alt+B (Windows) » |
| 0:55–1:20 | Explorateur + terminal | Clic sur l'icône fichiers en haut à gauche → arborescence ; ouverture du terminal ; survol des panneaux latéraux | Explorateur de fichiers, terminal, panneaux latéraux : tout est au même endroit | « 1 éditeur · chat · fichiers · terminal » |
| 1:20–1:40 | Historique | Défilement de la liste des conversations ; clic sur le signe « + » en haut du chat | L'historique garde chaque conversation ; le « + » en ouvre une nouvelle | « + » = nouvelle conversation |
| 1:40–2:15 | Démo : clonage | Icône fichiers → Clone Repository → collage de l'URL `https://github.com/IBM/bob-demo.git` → choix de l'emplacement → Open → « Yes, I trust the authors » | Clonage du dépôt de démo directement depuis l'IDE, en quelques clics | URL du dépôt affichée en gros |
| 2:15–2:30 | Récap + outro | Bandeau « À retenir » + plaque de la vidéo 2 | Trois réflexes à retenir ; teaser : les modes Ask, Plan et Agent | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
Et si votre environnement de développement pouvait simplement… comprendre votre projet ? Bienvenue dans cette première vidéo consacrée à IBM Bob, l'IDE qui intègre un assistant IA directement dans votre flux de travail.

**[0:15 — Qu'est-ce que Bob ?]**
Avant de cliquer partout, une phrase pour situer le produit. IBM Bob est un partenaire IA du cycle de vie du développement logiciel — en anglais, un « SDLC partner ». Il s'ajoute à vos habitudes de travail et vous aide à avancer en confiance sur de vraies bases de code. Point important : Bob est une application autonome — un IDE à part entière, pas une extension d'éditeur. Et une précision pratique : les versions 1.0.3 et 2.0.0 de l'IDE cesseront de fonctionner le 30 septembre 2026 — mettez à jour vers la version 2.0.2 ou une version plus récente — actuellement, la 2.1.0.

**[0:35 — Le chat]**
Le cœur de Bob, c'est son interface de chat. Si elle n'est pas visible, cliquez sur l'icône Bob à côté de la barre de navigation, ou utilisez le raccourci clavier — Option + Commande + B sur Mac, Ctrl + Alt + B sur Windows. Dans le champ de saisie, on ne tape pas du code : on écrit des demandes en langage naturel. « Explique ce que fait cette application », « Crée un Dockerfile »… Bob comprend et agit.

**[0:55 — Explorateur, terminal, panneaux latéraux]**
Autour du chat, tout ce qu'on attend d'un IDE moderne. L'explorateur de fichiers, accessible par l'icône en haut à gauche du panneau Bob, affiche l'arborescence du projet. Le terminal exécute vos commandes, et les panneaux latéraux encadrent votre zone d'édition : votre code reste sous les yeux pendant que Bob travaille à côté.

**[1:20 — L'historique des conversations]**
Dernier repère : l'historique des conversations. Chaque échange avec Bob y reste accessible. En haut du chat, un signe « plus » ouvre une nouvelle conversation — chaque conversation neuve repart d'un contexte vierge.

**[1:40 — Première action : cloner un projet]**
Passons à un geste concret : récupérer un projet. Cliquez sur l'icône fichiers, en haut à gauche du panneau Bob, puis sur « Clone Repository », et collez l'adresse du dépôt de démonstration : github.com/IBM/bob-demo.git. Choisissez l'emplacement d'enregistrement, cliquez « Open » à la fin du clonage, puis « Yes, I trust the authors » si Bob demande confirmation. L'explorateur affiche les fichiers du projet, le chat reste ouvert à côté : vous êtes prêt à travailler.

**[2:15 — Récapitulatif]**
Trois choses à retenir de cet épisode. Un : Bob est un IDE autonome avec un assistant IA intégré. Deux : le chat s'ouvre avec Option + Commande + B ou Ctrl + Alt + B. Trois : on clone un dépôt depuis l'icône fichiers, sans jamais quitter l'application. Dans la prochaine vidéo, nous découvrons les trois modes de Bob — Ask, Plan et Agent — et surtout, quand utiliser chacun.

---

# VIDÉO 2/12 — Les modes Ask, Plan et Agent

## Fiche technique

- **Objectif pédagogique** : savoir quand utiliser Ask, Plan et Agent, avec la même demande traitée dans les trois modes.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① Trois personas ② Ask : explorer sans risque ③ Plan : concevoir avant de coder ④ Agent : construire ⑤ La même demande, trois comportements.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Trois cartes apparaissant une à une : ASK / PLAN / AGENT | « Trois modes, trois super-pouvoirs — et un seul bon réflexe : choisir le bon » | « Ask · Plan · Agent » |
| 0:15–0:35 | Concept | Zoom sur le sélecteur de mode, à gauche du champ de saisie | Les modes sont des personas spécialisés qui adaptent le comportement de Bob à la tâche | « Le sélecteur de mode » |
| 0:35–1:00 | Ask | Sélection de Ask dans le menu déroulant, puis frappe de `/ask` ; prompt « Explique ce que fait cette application et comment elle fonctionne » ; Bob répond | Ask lit les fichiers mais ne peut rien écrire : exploration en toute sécurité — le principe du moindre privilège | « Ask = lecture seule » |
| 1:00–1:30 | Plan | Sélection de Plan, puis `/plan` ; prompt de planification d'une UI React ; le plan s'affiche | Plan sert à concevoir avant d'implémenter : on examine l'approche avant tout code | « Plan = réfléchir avant d'agir » |
| 1:30–1:55 | Agent | Sélection de Agent, puis `/agent` ; Bob annonce les fichiers qu'il va créer/modifier et demande la permission | Agent écrit, modifie et refactorise du code — mais demande l'autorisation avant chaque opération | « Agent = passage à l'action » |
| 1:55–2:15 | Comparaison | Écran partagé : la même demande « ajoute une interface web » dans les 3 modes : réponse / plan / code | La même demande donne trois comportements : explication, feuille de route, réalisation | « 1 demande → 3 comportements » |
| 2:15–2:30 | Récap + outro | Bandeau « À retenir » + plaque vidéo 3 | Réflexe : explorer avec Ask, planifier avec Plan, construire avec Agent | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
Demander quelque chose à une IA, c'est facile. Encore faut-il lui parler avec le bon chapeau. Bob propose trois modes — Ask, Plan et Agent — et toute cette vidéo tient en une question : quand utiliser lequel ?

**[0:15 — Trois personas]**
Dans Bob, les modes sont des personas spécialisés : ils adaptent le comportement de l'assistant au scénario de développement en cours. On les change depuis le sélecteur de mode, ce menu déroulant situé à gauche du champ de saisie du chat. Et pour aller vite, chaque mode a aussi sa commande : on peut taper la commande directement dans le chat.

**[0:35 — Ask : explorer sans risque]**
Premier mode : Ask. Activez-le dans le sélecteur, ou tapez « slash ask » dans le chat. Sa règle est simple et rassurante : Ask ne peut que lire les fichiers, jamais les écrire. Bob ne peut rien casser dans ce mode. C'est parfait pour explorer un projet que vous découvrez. Demandez-lui par exemple : « Explique ce que fait cette application et comment elle fonctionne. » Bob parcourt le projet et vous répond, sans rien toucher. La documentation appelle ça le principe du moindre privilège : on ne donne que les permissions strictement nécessaires.

**[1:00 — Plan : concevoir avant de coder]**
Deuxième mode : Plan, activable via le sélecteur ou la commande « slash plan ». Ici, Bob conçoit avant d'implémenter. Vous lui décrivez un objectif — par exemple « propose un plan pour ajouter une interface web à cette application » — et il produit une feuille de route que vous pouvez relire, critiquer et faire corriger avant la moindre ligne de code. C'est le mode des grandes décisions d'architecture.

**[1:30 — Agent : construire]**
Troisième mode : Agent, via le sélecteur ou « slash agent ». C'est lui qui écrit, modifie et refactorise le code. Mais attention, « Agent » ne veut pas dire « carte blanche » : Bob demande votre permission avant chaque opération. Il vous montre ce qu'il s'apprête à faire, et c'est vous qui validez.

**[1:55 — La même demande, trois comportements]**
Pour bien sentir la différence, prenons la même demande : « ajoute une interface web à cette API ». En mode Ask, Bob vous explique comment l'application est construite et ce qu'il faudrait savoir. En mode Plan, il rédige un plan d'implémentation. En mode Agent, il crée les fichiers, conteneurise l'application et la démarre — après votre accord.

**[2:15 — Récapitulatif]**
Le réflexe à garder : explorer avec Ask, planifier avec Plan, construire avec Agent. Prochaine vidéo : les approbations automatiques — ce que Bob a le droit de faire tout seul, et comment garder le contrôle.

---

# VIDÉO 3/12 — Auto Approvals

## Fiche technique

- **Objectif pédagogique** : comprendre le workflow d'approbation, configurer l'auto-approbation, mesurer les risques et appliquer les bonnes pratiques.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① Le principe : rien sans vous ② Où se cache le réglage ③ La config recommandée : Read uniquement ④ Les types d'approbation ⑤ Risques et bonnes pratiques.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Curseur cliquant sur « Approve » plusieurs fois de suite, compteur d'approbations qui s'incrémente | « Bob peut-il agir sans vous ? Oui — mais seulement si vous le décidez » | « Qui décide ? Vous. » |
| 0:15–0:35 | Principe | Bob annonce une action, une demande d'approbation apparaît | Le workflow d'approbation : Bob propose, vous disposez — il demande l'autorisation avant chaque opération | Bob propose · vous décidez |
| 0:35–0:55 | Le réglage | Zoom coin inférieur droit → menu Permissions → bascule d'auto-approbation | L'auto-approbation se règle dans le menu Permissions, en bas à droite de la fenêtre | « Permissions ↘ coin bas-droit » |
| 0:55–1:25 | Config recommandée | Case « Read » seule cochée ; Bob lance une commande en lecture seule sans demander ; puis demande une écriture → validation manuelle | Avec Read seul : les commandes en lecture seule passent automatiquement ; tout ce qui modifie des fichiers ou tourne dans le terminal demande votre accord | « Read » seul ✓ |
| 1:25–1:50 | Types d'approbation | Succession d'encarts : « Approve todo tools », « Approve edit tools », « Approve skill tools », « Approve subagent tools », « I understand the risks » | Selon l'action, Bob demande d'approuver ses outils de tâches, d'édition, de skills ou de sous-agents ; pour exécuter des commandes : « I understand the risks » puis Approve | 4 × « Approve … » + « I understand the risks » |
| 1:50–2:15 | Risques & bonnes pratiques | Encart « bonnes pratiques » avec 3 puces | Risque : des commandes exécutées en votre nom. Pratiques : Read seul par défaut, relire les diffs, valider au cas par cas | Read par défaut · relire les diffs |
| 2:15–2:30 | Récap + outro | Bandeau « À retenir » + plaque vidéo 4 | Récap ; teaser : les skills | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
Une IA qui écrit du code, c'est bien. Une IA qui exécute des commandes sans vous demander votre avis, ça, c'est une autre histoire. Alors : Bob peut-il agir tout seul ? Réponse courte : oui — mais uniquement dans les limites que vous avez définies.

**[0:15 — Le principe : rien sans vous]**
Par défaut, Bob fonctionne selon un workflow d'approbation. À chaque fois qu'il veut agir — créer un fichier, modifier du code, lancer une commande — il s'arrête et vous montre ce qu'il compte faire. Vous validez, ou pas. Rien ne s'exécute en votre nom sans votre accord explicite.

**[0:35 — Où se cache le réglage]**
Ce réglage se trouve dans le menu Permissions, au coin inférieur droit de la fenêtre. Vous y trouverez la bascule d'auto-approbation — « auto-approval » en anglais. Autrement dit : la liste des catégories d'actions que Bob peut mener sans vous redemander la permission à chaque fois.

**[0:55 — La configuration recommandée]**
La configuration conseillée par le tutoriel officiel est minimale : ne cocher que « Read », la lecture. Avec ce seul réglage, Bob exécute automatiquement les commandes en lecture seule — consulter un fichier, inspecter le projet. Mais dès qu'une commande modifie des fichiers ou s'exécute dans le terminal, il revient vers vous pour demander l'autorisation. Résultat : pas de validation fastidieuse pour les actions innocentes, et un garde-fou systématique pour tout le reste.

**[1:25 — Les types d'approbation]**
Dans la pratique, vous croiserez plusieurs libellés d'approbation. Quand Bob organise son travail : « Approve todo tools for task ». Quand il édite des fichiers : « Approve edit tools for task ». Quand il fait appel à des compétences spécialisées : « Approve skill tools for task ». Quand il répartit le travail en sous-agents : « Approve subagent tools for task ». Et pour l'exécution de commandes, une étape explicite : cliquer « I understand the risks » — je comprends les risques — puis « Approve ». Ce double clic est volontaire : il vous fait marquer une pause de conscience.

**[1:50 — Risques et bonnes pratiques]**
Parlons franchement des risques : chaque commande approuvée est exécutée sur votre machine, en votre nom. D'où trois bonnes pratiques simples. Un : rester en lecture seule pour l'auto-approbation, et valider manuellement tout le reste. Deux : toujours relire les modifications proposées — les diffs — avant de cliquer. Trois : réfléchir à la portée de ce que vous autorisez, surtout sur des projets professionnels.

**[2:15 — Récapitulatif]**
À retenir : l'auto-approbation se règle dans le menu Permissions, en bas à droite ; la configuration sûre, c'est « Read » uniquement ; et « I understand the risks » est votre dernier point de contrôle. Prochaine vidéo : les skills — comment apprendre de nouveaux tours à Bob.

---

# VIDÉO 4/12 — Skills

## Fiche technique

- **Objectif pédagogique** : comprendre ce qu'est une skill, savoir quand en créer une, et voir Bob en action avec ses skills.
- **Durée cible** : 2 min 15.
- **Chapitrage** : ① L'idée en une image ② Qu'est-ce qu'une skill ? ③ Quand créer une skill ? ④ Démonstration : Bob mobilise ses skills.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Icône « boîte à outils » qui s'ouvre, plusieurs compétences qui s'emboîtent | « Votre assistant est doué. Ajoutez-lui des compétences sur mesure, et il devient redoutable » | « Des compétences sur mesure » |
| 0:15–0:45 | Définition | Schéma simple : Bob + skill = comportement spécialisé | Une skill étend Bob avec des connaissances et des comportements spécialisés : c'est un module qui enrichit ce qu'il sait faire | « Skill = savoir + savoir-faire » |
| 0:45–1:15 | Quand créer | Encart 2 colonnes : « répétez-vous ? » / « consignes maison ? » | Le bon signal : vous répétez souvent la même consigne ou la même méthode — plutôt que de la retaper, transformez-la en skill | Vous répétez ? → créez une skill |
| 1:15–1:55 | Démo | Dans le chat en mode Plan, prompt « Fais un plan pour ajouter une UI web React à cette application » ; Bob demande à utiliser ses skills → encart « Approve skill tools for task » → clic Approve | Au moment de produire un plan, Bob demande l'autorisation d'utiliser ses skills — c'est là qu'on les voit entrer en scène | « Approve skill tools for task » |
| 1:55–2:15 | Récap + outro | Bandeau « À retenir » + plaque vidéo 5 | Récap 3 puces ; teaser : MCP, le protocole qui connecte Bob au monde extérieur | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
Votre assistant IA est déjà doué. Mais imaginez que vous puissiez lui ajouter des compétences sur mesure, exactement celles dont votre équipe a besoin. C'est exactement l'idée des skills de Bob.

**[0:15 — Qu'est-ce qu'une skill ?]**
Une skill — une « compétence » en français — est un module qui étend Bob avec des connaissances et des comportements spécialisés. La documentation officielle résume les skills ainsi : elles ajoutent à Bob un savoir et un savoir-faire dédiés. Autrement dit, Bob sait déjà faire beaucoup de choses ; une skill lui apprend à le faire à votre manière, avec vos conventions, vos méthodes, votre vocabulaire métier.

**[0:45 — Quand créer une skill ?]**
Alors, quand créer une skill ? Le meilleur signal, c'est la répétition. Si vous vous surprenez à expliquer plusieurs fois la même chose à Bob — « nos composants s'écrivent toujours comme ceci », « nos rapports suivent toujours ce format », « respecte cette méthode pour nos revues » — c'est qu'une consigne mérite de devenir permanente. Plutôt que de la retaper à chaque conversation, vous la transformez en skill, et Bob l'applique ensuite systématiquement.

**[1:15 — Démonstration]**
Voyons une skill à l'œuvre, en situation. Demandez à Bob, en mode Plan, de préparer un plan pour ajouter une interface web React à votre application. Avant de se lancer, Bob vous annonce qu'il souhaite mobiliser ses outils de skills — et une demande d'approbation apparaît : « Approve skill tools for task ». Cliquez sur Approve. Bob entreprend alors son analyse en s'appuyant sur ses compétences spécialisées, et produit un plan beaucoup plus structuré. Retenez ce moment de l'approbation : même avec des skills, rien ne se fait sans votre feu vert — la règle d'or de la vidéo précédente s'applique toujours.

**[1:55 — Récapitulatif]**
Trois points à retenir. Un : une skill étend Bob avec des connaissances et comportements spécialisés. Deux : le bon moment pour en créer une, c'est quand vous vous répétez. Trois : l'usage des skills passe par votre approbation explicite. Prochaine vidéo : MCP, le Model Context Protocol — le protocole qui ouvre Bob vers vos outils externes.

---

# VIDÉO 5/12 — MCP (Model Context Protocol)

## Fiche technique

- **Objectif pédagogique** : définir MCP, comprendre ses cas d'usage, gérer des serveurs MCP depuis les réglages.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① Le problème que MCP résout ② Définition en une phrase ③ Intégré vs externe ④ Serveurs locaux ou distants ⑤ Gérer ses serveurs MCP.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Bob face à une porte fermée (icône verrou) → la porte s'ouvre sur des logos d'outils | « Bob parle déjà à votre projet. Et s'il parlait aussi à tous vos autres outils ? » | « Ouvrir Bob au monde » |
| 0:15–0:40 | Définition | Nom du protocole décomposé mot à mot : Model · Context · Protocol | MCP = Model Context Protocol : le cadre qui étend Bob avec des outils et intégrations personnalisés | Model · Context · Protocol |
| 0:40–1:05 | Intégré vs externe | Encart 2 colonnes : « outils intégrés » (fichiers, commandes) vs « outils externes » (via MCP) | Bob sait déjà lire/écrire des fichiers et exécuter des commandes ; MCP ajoute vos propres outils externes | Intégré ↔ externe |
| 1:05–1:30 | Transports | Schéma : machine locale ↔ nuage distant | Deux modèles de déploiement pour vos serveurs MCP : local, sur votre machine, ou distant | Local ou distant |
| 1:30–2:05 | Gestion | Ouverture du panneau de réglages → section serveurs MCP → Ajouter / Configurer / Retirer | La gestion des serveurs MCP se fait dans le panneau de configuration : ajouter, configurer, supprimer | Ajouter · Configurer · Retirer |
| 2:05–2:30 | Récap + outro | Bandeau « À retenir » + plaque vidéo 6 | Récap 3 puces ; teaser : bien rédiger une demande à Bob | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
Bob parle déjà couramment votre projet : il lit vos fichiers, écrit votre code, exécute vos commandes. Mais et s'il pouvait aussi parler à vos autres outils ? C'est précisément le rôle de MCP.

**[0:15 — Définition]**
MCP signifie Model Context Protocol — en français, « protocole de contexte de modèle ». Derrière ce nom technique se cache une idée simple : MCP est le cadre qui étend les capacités de Bob avec des outils et des intégrations personnalisés. C'est la prise universelle qui relie Bob au reste de votre écosystème.

**[0:40 — Intégré versus externe]**
Précisons ce que Bob sait déjà faire sans MCP. Il dispose d'outils intégrés : l'accès aux fichiers — lire et écrire dans votre projet — et l'exécution de commandes, directement depuis le chat. Ces deux briques suffisent pour l'essentiel du travail quotidien. MCP intervient quand vous voulez aller plus loin : connecter des outils externes, les vôtres, ceux de votre entreprise. Grâce au protocole, ces outils s'intègrent proprement dans la panoplie de Bob, qui peut ensuite les mobiliser comme ses propres outils.

**[1:05 — Serveurs locaux ou distants]**
Côté architecture, MCP vous laisse le choix entre deux modèles de déploiement, ce que la documentation appelle les « transports serveur ». Vous pouvez héberger un serveur MCP en local, sur votre propre machine — vos données restent alors chez vous. Ou opter pour un serveur distant, adapté aux outils partagés par une équipe ou fournis par un prestataire. Ce choix dépend de vos contraintes : sécurité, réseau, gestion.

**[1:30 — Gérer ses serveurs MCP]**
La bonne nouvelle, c'est que tout se pilote depuis l'interface : la gestion des serveurs MCP se fait directement dans le panneau de réglages de Bob. Trois actions suffisent : ajouter un serveur, le configurer — par exemple son transport — et le retirer quand vous n'en avez plus besoin. Ajoutez le serveur de votre choix, et Bob gagne immédiatement accès aux outils qu'il expose.

**[2:05 — Récapitulatif]**
Trois points à retenir. Un : MCP, c'est le Model Context Protocol, le cadre qui étend Bob avec des outils externes. Deux : deux modèles de déploiement existent, local ou distant. Trois : tout se gère depuis le panneau de configuration — ajouter, configurer, retirer. Prochaine vidéo, la plus rentable de toute la série : comment bien rédiger une demande à Bob pour obtenir exactement ce que vous voulez.

---

# VIDÉO 6/12 — Bien rédiger une demande à BOB

## Fiche technique

- **Objectif pédagogique** : passer d'un prompt vague à un prompt efficace : objectif, exigences, contraintes, destination.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① La règle d'or ② Mauvais prompt vs bon prompt ③ L'anatomie d'un prompt parfait ④ Bonus : imposer le format de réponse.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Deux bulles de chat : « Fais-moi un tableau » vs un long prompt structuré | « La différence entre un résultat moyen et un résultat parfait ? La façon de demander » | « Bien demander = bien obtenir » |
| 0:15–0:40 | Règle d'or | Encart citation officielle + exemple : « Crée un composant React qui affiche un tableau triable de données utilisateurs » | La règle d'or de la doc : plus la demande est spécifique, meilleurs sont les résultats | Spécifique > vague |
| 0:40–1:05 | Mauvais vs bon | Écran partagé : réponse au mauvais prompt (générique) vs au bon prompt (précis) | « Fais-moi un composant tableau » laisse tout dans le flou ; la version précise obtient exactement le bon composant | Flou vs précis |
| 1:05–1:55 | Anatomie | Prompt du quickstart affiché et surligné par blocs de couleur : objectif / exigences / contraintes / destination | La recette en 4 blocs : un objectif clair, des exigences numérotées, des contraintes explicites, une destination finale | Objectif · Exigences · Contraintes · Destination |
| 1:55–2:15 | Bonus format | Réponse de Bob en tableau 2 colonnes « Field / Value » suite à la demande de format | Précisez même le format de réponse attendu — Bob l'applique à la lettre | « Donne-moi la réponse en tableau » |
| 2:15–2:30 | Récap + outro | Bandeau « À retenir » + plaque vidéo 7 | Récap ; teaser : la revue de code avec Bob | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
La différence entre un résultat décevant et un résultat parfait tient souvent à une seule chose : la façon de demander. Cette vidéo est la plus rentable de toute la série — elle vous apprend à parler à Bob pour obtenir exactement ce que vous voulez.

**[0:15 — La règle d'or]**
La règle d'or vient directement de la documentation officielle : plus votre demande est spécifique, meilleurs seront les résultats. L'exemple donné par IBM est parfait : dites « Crée un composant React qui affiche un tableau triable de données utilisateurs », plutôt que « Fais-moi un composant tableau ». Même intention — mais dans le premier cas, la technologie, la fonctionnalité de tri et la nature des données sont explicites. Bob n'a plus rien à deviner.

**[0:40 — Mauvais prompt versus bon prompt]**
Prenons le mauvais prompt : « Fais-moi un composant tableau. » Bob doit choisir la technologie, deviner s'il faut du tri, une pagination, un style… Le résultat sera générique, et vous devrez itérer plusieurs fois. Avec le bon prompt, tout est déjà tranché : Bob livre directement la bonne pièce.

**[1:05 — L'anatomie d'un prompt parfait]**
Voyons la recette, telle que la pratique le tutoriel officiel — quatre blocs. Bloc un, l'objectif : « Ajoute une interface web React à cette application, avec Vite. » Bloc deux, les exigences, numérotées : afficher les tâches existantes via GET, en ajouter via POST, les marquer comme terminées via PUT. Bloc trois, les contraintes : ne pas modifier l'API existante, tout servir dans un seul conteneur Docker, rester simple — pas d'authentification, pas de bibliothèque d'état — et installer les dépendances dans le Dockerfile. Bloc quatre, la destination : « Enregistre le plan dans un fichier nommé ui-plan.md, à la racine du projet. » Objectif, exigences, contraintes, destination : avec ces quatre blocs, Bob travaille comme un collègue parfaitement briefé.

**[1:55 — Bonus : imposer le format de réponse]**
Dernier réflexe, souvent négligé : précisez le format de la réponse. Le tutoriel le montre sur un test d'API : après avoir exécuté une requête, on ajoute simplement « Donne-moi la réponse sous forme de tableau à deux colonnes : Champ et Valeur ». Bob obéit à la lettre, et la réponse devient immédiatement lisible.

**[2:15 — Récapitulatif]**
À retenir : spécifique vaut mieux que vague ; structurez en quatre blocs — objectif, exigences, contraintes, destination ; et imposez le format de réponse souhaité. Prochaine vidéo : la revue de code — comment Bob traque les problèmes de sécurité, de performance, et corrige même les builds cassés.

---

# VIDÉO 7/12 — Review de code avec BOB

## Fiche technique

- **Objectif pédagogique** : utiliser Bob pour analyser du code, détecter les problèmes (sécurité, performance), relire et corriger — y compris les builds cassés.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① Bob, relecteur de code ② La revue sans risque : mode Ask ③ Étude de cas réels : builds cassés ④ Sécurité, performance, pull requests.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Du code rouge avec une loupe qui détecte 3 anomalies surlignées | « Un collègue qui lit tout votre code, repère les failles et propose la correction — sans jamais se fatiguer » | « Votre relecteur inépuisable » |
| 0:15–0:40 | Bob relecteur | Encart des capacités : nettoyer/corriger du code existant, répondre aux questions sur la base de code | Bob sait nettoyer et corriger le code existant, et répondre à vos questions sur la base de code | Nettoyer · corriger · expliquer |
| 0:40–1:05 | Revue sans risque | Mode Ask activé ; prompt « Y a-t-il des problèmes de sécurité ou de performance dans ce projet ? » ; réponse structurée | En mode Ask — lecture seule — Bob audite le code sans pouvoir rien modifier : la revue la plus sûre | Ask = audit sans risque |
| 1:05–1:50 | Cas réels | Écran de build en échec → message de Bob : « Le build a échoué car npm ci exige un package-lock.json — je passe à npm install » ; second cas : index.html déplacé de public/ vers la racine pour Vite | Deux corrections réelles tirées du tutoriel : npm ci remplacé par npm install, et index.html déplacé là où Vite l'attend | npm ci → npm install · index.html → racine |
| 1:50–2:15 | Itération & PR | Boucle : erreur → diagnostic → correctif proposé → Approve ; mention de la relecture des diffs | L'itération fait partie du développement avec Bob : il montre l'erreur et propose la correction — vous validez | Erreur → correctif → Approve |
| 2:15–2:30 | Récap + outro | Bandeau « À retenir » + plaque vidéo 8 | Récap ; teaser : literate coding | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
Imaginez un collègue qui lit tout votre code, repère les failles, questionne vos choix techniques — et ne fatigue jamais. Bienvenue dans la revue de code avec Bob.

**[0:15 — Bob, relecteur de code]**
Parmi les capacités officielles de Bob, deux concernent directement la revue : nettoyer et corriger le code existant, et répondre à des questions sur votre base de code. Autrement dit, Bob ne se contente pas d'écrire : il lit, explique et remet en ordre. C'est un double regard permanent sur votre projet.

**[0:40 — La revue sans risque : mode Ask]**
Première méthode, la plus sûre : la revue en mode Ask. Vous vous souvenez de la vidéo 2 ? En mode Ask, Bob lit mais n'écrit jamais. C'est donc le cadre idéal pour un audit. Posez-lui vos questions de revue : « Ce code présente-t-il des risques de sécurité ? », « Où sont les points de performance sensibles ? ». Bob parcourt le projet et vous répond avec des références précises — sans qu'une seule ligne puisse changer.

**[1:05 — Étude de cas réels]**
Voyons maintenant la revue en action, sur deux incidents réels du tutoriel officiel. Premier cas : un build Docker échoue. Bob diagnostique : la commande « npm ci » exige un fichier package-lock.json, absent du projet. Sa correction : remplacer npm ci par npm install dans le Dockerfile — npm install, lui, n'a pas besoin de ce fichier pour installer les dépendances. Il vous propose le correctif, vous approuvez, le build repart. Deuxième cas : Vite, l'outil de construction, ne trouve pas index.html — le fichier est dans le dossier public alors que Vite l'attend à la racine. Bob identifie l'emplacement exact et déplace le fichier. Deux erreurs différentes, même méthode : diagnostic précis, correction proposée, validation humaine.

**[1:50 — Itération et pull requests]**
Ce qu'il faut comprendre, c'est que ces allers-retours ne sont pas des échecs : la documentation le dit explicitement — l'itération fait partie du développement avec Bob. Il montre l'erreur, propose une correction, vous décidez. Ce réflexe s'applique aussi aux pull requests : faites relire vos changements avant de les fusionner, et examinez toujours le diff proposé avant de cliquer.

**[2:15 — Récapitulatif]**
À retenir : Bob nettoie, corrige et répond aux questions sur votre code ; le mode Ask est le cadre idéal pour un audit sans risque ; et l'itération erreur-correction est le mode de travail normal avec un assistant IA. Prochaine vidéo : literate coding — écrire du code avec l'IA, directement dans l'éditeur.

---

# VIDÉO 8/12 — Literate Coding

## Fiche technique

- **Objectif pédagogique** : comprendre et pratiquer le « literate coding » : décrire une intention en langage naturel, laisser Bob éditer le code, relire le diff et sauvegarder.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① L'idée : parler au lieu de taper ② La boucle en 4 temps ③ Démo : restyler une interface ④ Le garde-fou : relire avant de sauver.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Clavier qui recule, micro qui s'avance ; phrase tapée : « Décris, ne tape pas » | « Et si le meilleur langage de programmation était… le vôtre ? » | « Décrire > Taper » |
| 0:15–0:40 | L'idée | Du texte naturel à gauche → code généré à droite | Transformer du langage naturel en code fonctionnel : c'est une capacité officielle de Bob | Naturel → code |
| 0:40–1:00 | La boucle | Infographie en 4 étapes fléchées : Décrire → Proposer → Relire → Sauver | La boucle du literate coding : décrire l'intention, recevoir la proposition, relire le diff, sauvegarder | Décrire → Proposer → Relire → Sauver |
| 1:00–1:50 | Démo : restyler l'UI | Page web sobre → encart « 3 polices au choix : Inter · Georgia · JetBrains Mono » → prompt « Mets à jour les styles : police Inter, fond bleu nuit, texte blanc » → diff des composants React → clic Save → page restylée | Démo officielle : on choisit police, couleur de fond et couleur de texte ; Bob modifie les styles ; on relit le diff et on clique Save | Inter · Georgia · JetBrains Mono |
| 1:50–2:15 | Garde-fou | Zoom sur le diff : lignes rouges/vertes ; flèche vers le bouton Save | La règle d'or : aucun Save sans lecture du diff — l'IA propose, vous décidez | Pas de Save sans lecture |
| 2:15–2:30 | Récap + outro | Bandeau « À retenir » + plaque vidéo 9 | Récap ; teaser : le top 10 des commandes | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
Et si le meilleur langage de programmation au monde était simplement… le vôtre ? C'est la promesse du literate coding : la programmation lettrée, où l'on décrit ce que l'on veut, et où l'éditeur — avec l'aide de Bob — l'écrit pour vous.

**[0:15 — L'idée]**
Transformer du langage naturel en code fonctionnel : c'est littéralement l'une des capacités officielles de Bob, inscrite dans sa documentation. Vous exprimez une intention — « affiche la liste des tâches », « change la police du site » — et Bob traduit cette intention en modifications concrètes de vos fichiers, directement dans l'éditeur. Le code reste du code ; c'est la saisie qui change.

**[0:40 — La boucle en quatre temps]**
Le literate coding avec Bob suit une boucle simple, en quatre temps. Temps un : décrire — formulez votre intention dans le chat, comme vous l'expliqueriez à un collègue. Temps deux : proposer — Bob rédige la modification et vous la présente. Temps trois : relire — examinez le diff, ce qu'il change exactement. Temps quatre : sauvegarder — cliquez Save si tout vous convient. Puis on recommence. Décrire, proposer, relire, sauver.

**[1:00 — Démonstration : restyler une interface]**
Prenons la démonstration du tutoriel officiel : personnaliser l'apparence d'une interface web. Pour la police, le tutoriel propose trois valeurs sûres : Inter, le grand classique des applications web ; Georgia, une police à empattements, chaleureuse et très lisible ; ou JetBrains Mono, à largeur fixe, pour un look d'outil de développeur. Dans le chat, la demande tient en trois lignes : « Mets à jour les styles de l'interface. Utilise la police Inter. Fond bleu nuit, texte blanc. » C'est tout. Bob propose alors des modifications sur les styles des composants React : couleurs de fond, police, couleur du texte. Le diff s'affiche — chaque ligne modifiée est visible, ce qui part, ce qui arrive. Un dernier examen, un clic sur Save… et en rafraîchissant la page, l'interface a changé de visage. Trois phrases en français, une page transformée : voilà le literate coding.

**[1:50 — Le garde-fou]**
Un mot d'avertissement pour finir, car la facilité peut endormir : la règle d'or reste « aucun Save sans lecture du diff ». Bob propose, mais c'est vous qui décidez. Prenez les deux ou trois secondes nécessaires pour vérifier ce que vous êtes sur le point d'accepter — surtout sur un projet professionnel.

**[2:15 — Récapitulatif]**
À retenir : le literate coding, c'est décrire en langage naturel ce que vous voulez ; la boucle est décrire, proposer, relire, sauver ; et jamais de sauvegarde sans relecture du diff. Prochaine vidéo : le top 10 des commandes à connaître — le condensé qui vous fera gagner du temps tous les jours.

---

# VIDÉO 9/12 — Top 10 des commandes à connaître

## Fiche technique

- **Objectif pédagogique** : mémoriser les commandes et gestes essentiels du chat Bob : commandes slash et raccourcis d'interface.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① La logique « slash » ② Le top 10 en accéléré ③ Comment retrouver la liste complète.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Clavier frappant `/` ; une liste de commandes se déploie | « Dix commandes, trente secondes pour les voir, une série pour les retenir » | « / : la clé magique » |
| 0:15–0:30 | La logique slash | Champ de chat, frappe de `/` + défilement de l'autocomplétion | Les commandes se tapent dans le champ de chat, commencent par une barre oblique | « / » = commande |
| 0:30–2:00 | Le top 10 | 10 vignettes de ~9 s chacune, une par commande, avec démo éclair | Présentation éclair des 10 commandes et gestes essentiels (voir script) | Compteur 1/10 → 10/10 |
| 2:00–2:15 | Retrouver la liste | Frappe de `/help` ; panneau d'aide | La liste complète vit dans la documentation et dans l'aide intégrée | /help · documentation |
| 2:15–2:30 | Récap + outro | Affiche récap « top 10 » en poster + plaque vidéo 10 | Récap ; teaser : personnaliser le comportement de Bob | « Gardez ce poster » |

## Script voix-off intégral

**[0:00 — Accroche]**
Dix commandes à connaître, une série de gestes qui deviennent des réflexes. Voici le top 10 des commandes de Bob — à garder sous la main.

**[0:15 — La logique slash]**
D'abord, la logique : les commandes de Bob se tapent directement dans le champ de chat, et commencent toutes par une barre oblique — le fameux « slash ». C'est le même principe que dans les messageries d'équipe. Voyons le top 10, en accéléré.

**[0:30 — Le top 10]**
Un : « slash init » — la commande la plus importante : elle initialise les fichiers de règles de votre projet. On lui consacre d'ailleurs une vidéo entière.
Deux : « slash ask » — bascule Bob en mode lecture seule : questions et exploration, sans risque.
Trois : « slash plan » — bascule en mode planification : Bob conçoit avant de coder.
Quatre : « slash agent » — bascule en mode agent : Bob écrit, modifie et refactorise, sous votre approbation.
Cinq : « slash review » — demande une revue de code : Bob analyse et traque les problèmes.
Six : « slash help » — l'aide intégrée : commandes, fonctionnement, réponses aux questions courantes.
Sept : « slash clear » — nettoie la conversation en cours pour repartir sur une base propre.
Huit : le bouton « plus », en haut du chat — ouvre une nouvelle conversation et efface le contexte : le réflexe à prendre entre deux grandes tâches, pour garder des échanges focalisés.
Neuf : la recherche — raccourci Commande K, noté ⌘ K : c'est le raccourci affiché en haut de la documentation de Bob, pour retrouver une page ou une notion en quelques secondes.
Dix : les commandes personnalisées — celles que vous créez vous-même, avec vos skills et vos règles, pour vos besoins spécifiques. Et pour découvrir les commandes IBM propres à votre environnement, le réflexe est simple : « slash help ».

**[2:00 — Retrouver la liste]**
Ce top 10 n'est pas figé : la liste complète des commandes vit dans la documentation officielle de Bob, et l'aide intégrée — « slash help » — vous la rappelle à tout moment. Prenez trente secondes pour la parcourir après cette vidéo.

**[2:15 — Récapitulatif]**
Si vous ne deviez en retenir que trois : « slash init » pour démarrer un projet, « slash ask / plan / agent » pour piloter les modes, et le « plus » pour repartir d'un contexte vierge. Prochaine vidéo : personnaliser le comportement de Bob — règles, hooks et instructions persistantes.

---

# VIDÉO 10/12 — Personnaliser le comportement de BOB

## Fiche technique

- **Objectif pédagogique** : comprendre comment rendre les consignes permanentes : instructions persistantes (AGENTS.md), règles par mode, hooks et bobignore.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① Le problème : Bob oublie ② Les instructions persistantes ③ Une règle par mode ④ Hooks et bobignore ⑤ Pratique : éditer ses règles.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Bob qui salue chaleureusement… puis oublie tout (bulle vide) | « Votre assistant a un défaut : il ne se souvient de rien. Voici comment y remédier » | « Bob oublie tout » |
| 0:15–0:45 | Le problème | Schéma : conversation 1 → mémoire vidée → conversation 2 repart de zéro | Bob est « sans état » (stateless) : sans consignes persistantes, il repart du début à chaque fois | Stateless = mémoire vide |
| 0:45–1:15 | Instructions persistantes | Explorateur : fichier AGENTS.md à la racine + dossier .bob contenant les fichiers de règles | La solution : des fichiers d'instructions persistantes, lus à chaque session — la structure du projet, les conventions, les objectifs | AGENTS.md + .bob/ |
| 1:15–1:45 | Une règle par mode | Zoom sur .bob : un fichier de règles pour Agent, un pour Plan, un pour Ask | Chaque mode a son propre fichier de règles : le comportement s'adapte ET se mémorise | Règles : Agent · Plan · Ask |
| 1:45–2:10 | Hooks & bobignore | Encart 2 cases : « Hooks : automatiser des réactions » / « bobignore : exclure des fichiers » ; ouverture éclair de l'onglet Hooks des réglages Bob (liste des hooks, bascule marche/arrêt) | Au-delà des règles : les hooks pour déclencher des actions — pilotés depuis l'onglet Hooks des réglages (nouveauté 2.1.0) — et bobignore pour tenir certains fichiers à l'écart | Hooks · bobignore |
| 2:10–2:30 | Récap + outro | Bandeau « À retenir » + plaque vidéo 11 | Récap ; teaser : /init en pratique | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
Votre assistant IA a un défaut secret : il oublie tout. Chaque conversation repart de zéro. Heureusement, Bob offre tout ce qu'il faut pour y remédier — et c'est l'objet de cette vidéo.

**[0:15 — Le problème : Bob oublie]**
Précisons le défaut, tel que le décrit la documentation : Bob est « sans état » — stateless, en anglais. Sans instructions persistantes, il repart du début à chaque fois. Vos conventions de code, vos préférences, l'architecture de votre projet : à chaque nouvelle conversation, il faut tout lui réexpliquer. Frustrant — et facile à corriger.

**[0:45 — Les instructions persistantes]**
La solution tient dans des fichiers d'instructions persistantes. Le plus important s'appelle AGENTS.md, placé à la racine du projet. Il indique à Bob la structure d'ensemble du projet, ses conventions et ses objectifs. Résultat : Bob écrit du code qui colle à votre projet, au lieu de deviner. Ces fichiers sont de simples fichiers texte — vous pouvez les ouvrir, les relire et les éditer à la main à tout moment. Vos consignes deviennent ainsi permanentes : expliquées une fois, appliquées toujours.

**[1:15 — Une règle par mode]**
Encore mieux : la personnalisation est affinée mode par mode. Dans le dossier .bob du projet vivent des fichiers de règles distincts — un pour le mode Agent, un pour le mode Plan, un pour le mode Ask. Chaque mode suit ainsi ses propres règles de conduite. Vous pouvez, par exemple, exiger une prudence maximale en mode Agent, celui qui modifie le code, et laisser le mode Ask plus libre dans ses explorations.

**[1:45 — Hooks et bobignore]**
Deux leviers complètent la panoplie, listés dans le plan de formation : les hooks — des points d'accroche pour déclencher automatiquement des actions au bon moment du flux de travail — et le fichier bobignore, qui tient à l'écart les fichiers que Bob ne doit pas toucher ni considérer. Notez que depuis la version 2.1.0, les hooks disposent d'un onglet dédié dans les réglages de Bob : tous y sont listés, avec recherche et bascule marche/arrêt — plus besoin d'être expert pour les piloter. Leur mise en œuvre détaillée dépasse le cadre de cette introduction : la documentation officielle vous les présente pas à pas. Retenez simplement qu'ils existent, et qu'ils complètent les règles persistantes.

**[2:10 — Récapitulatif]**
Trois points à retenir. Un : Bob est sans état — sans consignes persistantes, il repart de zéro. Deux : AGENTS.md et les fichiers de règles du dossier .bob rendent vos consignes permanentes, avec une règle par mode. Trois : hooks et bobignore complètent l'arsenal de personnalisation. Prochaine vidéo : la commande /init — celle qui crée tous ces fichiers pour vous, automatiquement.

---

# VIDÉO 11/12 — Démarrer un projet avec /init

## Fiche technique

- **Objectif pédagogique** : exécuter /init sur un projet réel, comprendre ce qu'il crée (AGENTS.md racine + règles par mode dans .bob) et pourquoi c'est indispensable.
- **Durée cible** : 2 min 30.
- **Chapitrage** : ① La commande en une phrase ② Démo pas à pas ③ Ce que Bob analyse ④ Les fichiers obtenus ⑤ Pourquoi c'est non négociable.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Frappe de `/init` en très gros ; cascade de fichiers qui apparaissent | « Une commande, quelques secondes — et Bob connaît votre projet par cœur » | « /init : le premier réflexe » |
| 0:15–0:30 | En une phrase | Overlay : /init → AGENTS.md + règles | /init initialise Bob dans votre projet : il crée le fichier AGENTS.md racine et les fichiers de règles | /init → AGENTS.md + .bob/ |
| 0:30–1:00 | Démo pas à pas | Projet bob-get-started/express-todo-api-modern ouvert → frappe `/init` dans le chat → demande d'autorisation « Approve todo tools for task » → clic | Sur un projet fraîchement cloné, on tape /init ; Bob demande la permission d'agir ; on approuve | « Approve todo tools for task » |
| 1:00–1:25 | Ce que Bob analyse | Bob parcourt l'arborescence (survol animé des fichiers détectés) | Bob analyse les fichiers du projet pour en décrire la structure, les conventions et les objectifs | Structure · conventions · objectifs |
| 1:25–1:50 | Les fichiers obtenus | Explorateur : AGENTS.md à la racine, dossier .bob et ses fichiers de règles Agent / Plan / Ask | Résultat : un AGENTS.md racine + un fichier de règles par mode dans .bob | AGENTS.md · .bob/ |
| 1:50–2:15 | Pourquoi | Rappel visuel « stateless » (vidéo 10) : sans AGENTS.md, Bob repart du début à chaque fois | Sans /init, Bob repart de zéro à chaque conversation ; avec, il est opérationnel immédiatement | Avec /init : opérationnel tout de suite |
| 2:15–2:30 | Récap + outro | Bandeau « À retenir » + plaque vidéo 12 | Récap ; teaser : la première mission complète | « À retenir » ×3 puces |

## Script voix-off intégral

**[0:00 — Accroche]**
Une commande. Quelques secondes. Et Bob connaît votre projet par cœur. Voici /init — le premier réflexe à prendre sur tout nouveau projet.

**[0:15 — La commande en une phrase]**
Que fait /init, exactement ? Il initialise Bob dans votre projet : il analyse vos fichiers et crée le jeu complet d'instructions persistantes — le fichier AGENTS.md à la racine, plus les fichiers de règles. Autrement dit, tout ce que nous avons vu en théorie dans la vidéo précédente, /init le fabrique pour vous.

**[0:30 — Démonstration pas à pas]**
Faisons-le en direct, comme dans le tutoriel officiel. Notre projet est le dépôt de démonstration IBM, fraîchement cloné : une API de listes de tâches, dans le dossier bob-get-started/express-todo-api-modern. Dans le chat Bob, tapez : slash init. Bob propose son plan d'action et demande l'autorisation de créer les fichiers — l'encart « Approve todo tools for task » apparaît. Cliquez sur Approve. C'est tout.

**[1:00 — Ce que Bob analyse]**
Pendant ces quelques secondes, Bob parcourt votre projet : il détecte les fichiers, identifie la structure, repère les conventions en usage et déduit les objectifs du projet. Ce n'est pas de la magie : c'est de la lecture — méthodique et complète — de votre base de code.

**[1:25 — Les fichiers obtenus]**
Une fois l'analyse terminée, l'explorateur affiche le résultat : à la racine, le fichier AGENTS.md, qui décrit la structure, les conventions et les objectifs du projet ; et dans le dossier .bob, les fichiers de règles — un par mode : Agent, Plan et Ask. Vous pouvez ouvrir chacun de ces fichiers, vérifier leur contenu, les corriger, les enrichir. Ils vous appartiennent.

**[1:50 — Pourquoi c'est non négociable]**
Dernier point, le plus important : pourquoi cette commande change tout. Rappelez-vous — Bob est sans état. Sans AGENTS.md, il repart du début à chaque conversation : il réapprend votre projet à chaque session, et brûle du temps — et des tokens — à redécouvrir ce qu'il devrait déjà savoir. Avec AGENTS.md, Bob démarre chaque échange en connaissance de cause, et écrit d'emblée du code conforme à vos conventions.

**[2:15 — Récapitulatif]**
À retenir : /init crée le fichier AGENTS.md racine et les règles par mode dans .bob ; Bob demande votre approbation avant d'agir ; et c'est le geste d'ouverture de tout projet avec Bob. Prochaine et dernière vidéo : votre première mission complète — de l'exploration au nettoyage, en passant par le plan, le build et la personnalisation.

---

# VIDÉO 12/12 — Première mission avec BOB

## Fiche technique

- **Objectif pédagogique** : dérouler une mission réelle de bout en bout — ici, ajouter une interface web à une API Express — en mobilisant tous les acquis : Ask, Plan, Agent, approbations, /init, itération.
- **Durée cible** : 2 min 30 à 3 min (la plus dense de la série).
- **Chapitrage** : ① La mission ② Explorer avec Ask ③ Construire avec Agent ④ Planifier puis implémenter ⑤ Personnaliser, nettoyer ⑥ Les réflexes de la série.

## Storyboard

| TC | Séquence | Visuel / Action à l'écran | Voix-off (synopsis) | Texte à l'écran |
|---|---|---|---|---|
| 0:00–0:15 | Accroche | Écran de fin de mission : une web app de to-dos qui tourne dans le navigateur | « Vous avez tout appris. Place à la première mission — une vraie, de bout en bout » | « Mission : ajouter une UI web » |
| 0:15–0:35 | Mise en place | Clone de github.com/IBM/bob-demo.git → dossier bob-get-started/express-todo-api-modern → `/init` → Approve | On clone le dépôt de démo, on entre dans le dossier, on initialise Bob avec /init | Clone → dossier → /init |
| 0:35–0:55 | Explorer (Ask) | Mode Ask ; prompt « Explique ce que fait cette application et comment elle fonctionne » | En lecture seule, on demande à Bob d'expliquer l'API : routes, fonctionnement | /ask · lecture seule |
| 0:55–1:15 | Construire (Agent) | Mode Agent ; prompt Dockerfile Node 22 port 3000 → approbations → correction npm ci → npm install → test curl POST → réponse en tableau Field/Value | Bob crée le Dockerfile, construit et démarre le conteneur, corrige le problème npm, et l'API est testée en direct | /agent · Node 22 · port 3000 |
| 1:15–1:30 | Nouvelle conversation | Clic sur « + » en haut du chat | On repart d'un contexte vierge avant la phase suivante — économie de tokens, contexte focalisé | « + » = contexte vierge |
| 1:30–1:55 | Plan puis implémentation | Mode Plan : plan React + Vite enregistré dans ui-plan.md, avec exigences et contraintes → relecture du plan → mode Agent : « Implémente le plan ui-plan.md, conteneurise, démarre » → approbations → corrections de build | Bob planifie l'interface et l'enregistre dans ui-plan.md ; on relit ; puis Bob l'implémente, la conteneurise et la démarre | /plan → ui-plan.md → /agent |
| 1:55–2:15 | Personnaliser & nettoyer | Navigateur sur localhost:3000/index.html → ajout d'une tâche → prompt styles (Inter, bleu nuit, blanc) → diff → Save → rebuild → prompt de nettoyage « Stoppe et supprime le conteneur » | On vérifie l'UI dans le navigateur, on personnalise les styles, on reconstruit, puis on nettoie le conteneur | localhost:3000/index.html |
| 2:15–2:30 | Récap final | Poster récap : Ask → Plan → Agent → Review + approbations + /init | Les réflexes de toute la série, en un poster — fin de la formation | « Vous êtes opérationnel » |

## Script voix-off intégral

**[0:00 — Accroche]**
Onze épisodes, autant de réflexes : modes, approbations, skills, MCP, prompts efficaces, /init… Il est temps de tout réunir pour votre première mission avec Bob : ajouter une interface web à une API existante.

**[0:15 — Mise en place]**
D'abord, la mise en place : clonez le dépôt de démonstration — github.com/IBM/bob-demo.git — depuis l'icône fichiers, puis demandez à Bob de vous placer dans le dossier bob-get-started/express-todo-api-modern (changement de répertoire : cliquez Run). Enfin, tapez /init et approuvez la création des fichiers AGENTS.md. Bob connaît le projet.

**[0:35 — Explorer avec Ask]**
Avant de toucher à quoi que ce soit : explorer. En mode Ask — lecture seule, zéro risque — demandez : « Explique ce que fait cette application et comment elle fonctionne. » Bob décrit l'API, ses routes, son fonctionnement. Vous savez sur quoi vous construisez.

**[0:55 — Construire avec Agent]**
Passons à l'action — avec le réglage de sûreté : menu Permissions, auto-approbation sur Read uniquement. Puis, en mode Agent, la demande structurée : « Crée un Dockerfile pour cette API avec Node 22, sur le port 3000. N'installe pas les dépendances localement : le Dockerfile s'en charge. Construis l'image et démarre le conteneur. » Bob annonce ses actions ; cliquez « I understand the risks », puis Approve. Un imprévu ? npm ci exige un package-lock.json, le build échoue. Bob propose de passer à npm install, vous approuvez, le build repart. L'API tourne : testez-la depuis le chat avec un curl qui ajoute une tâche — réponse en tableau à deux colonnes, Champ et Valeur : identifiant, titre, état, date de création. Ça fonctionne.

**[1:15 — Nouvelle conversation]**
Avant la phase suivante, un clic stratégique : le signe « plus », en haut du chat — contexte vierge. La planification ne sature pas votre budget de tokens, et l'implémentation reste focalisée sur le plan approuvé.

**[1:30 — Planifier puis implémenter]**
Le plat de résistance : en mode Plan, la demande en quatre blocs — objectif, exigences, contraintes, destination. Ajouter une interface web React avec Vite ; afficher les tâches via GET, en ajouter via POST, les cocher via PUT ; ne pas modifier l'API, tout servir dans un seul conteneur Docker, rester simple ; enregistrer le plan dans ui-plan.md. Relisez le plan, approuvez. Puis, en mode Agent : « Implémente le plan ui-plan.md, conteneurise l'application et démarre-la. » Bob lit le plan, crée les fichiers, corrige les échecs éventuels — comme index.html à déplacer pour Vite — et démarre le conteneur.

**[1:55 — Personnaliser et nettoyer]**
Ouvrez localhost:3000/index.html et ajoutez une tâche : l'interface dialogue avec l'API. Pour personnaliser, décrivez vos styles — police Inter, fond bleu nuit, texte blanc —, relisez le diff, cliquez Save, puis faites reconstruire le conteneur. À noter : l'API stocke ses données en mémoire — au redémarrage, la liste revient à son état initial. Enfin, le ménage : « Stoppe et supprime le conteneur et l'image Docker. » Bob demande l'approbation et libère votre machine.

**[2:15 — Récapitulatif final]**
Vous venez de dérouler une mission complète : explorer avec Ask, planifier avec Plan, construire avec Agent, relire et itérer, personnaliser, nettoyer — une approbation à chaque étape, et /init en tête de course. C'est exactement le flux du tutoriel officiel IBM — et désormais le vôtre. Merci d'avoir suivi cette série : votre prochaine mission n'attend qu'un prompt. Bien joué.

---

# ANNEXES

## Aide-mémoire : les prompts exacts du tutoriel officiel

| Situation | Prompt (traduit de la documentation) |
|---|---|
| Naviguer dans le projet | « Navigue vers le dossier bob-get-started/express-todo-api-modern. » |
| Explorer l'API (mode Ask) | « Explique ce que fait cette application et comment elle fonctionne. » |
| Créer le conteneur API (mode Agent) | « Crée un Dockerfile pour cette API avec Node 22, exécutée sur le port 3000. N'installe pas les dépendances localement — le Dockerfile gère toutes les installations. Une fois le Dockerfile créé, construis l'image et démarre le conteneur. » |
| Tester l'API | `curl -X POST http://localhost:3000/api/todos -H "Content-Type: application/json" -d '{"title": "Build a web UI"}'` + « Donne-moi la réponse sous forme de tableau à deux colonnes : Champ et Valeur. » |
| Arrêter le conteneur | « Stoppe et supprime le conteneur en cours d'exécution et l'image Docker. » |
| Planifier l'UI (mode Plan) | « Fais un plan pour ajouter une interface web React TypeScript à cette application de tâches, avec Vite. L'UI doit : afficher les tâches existantes via GET /api/todos ; ajouter des tâches via POST /api/todos ; marquer les tâches terminées via PUT /api/todos/:id. Contraintes : ne pas modifier l'API Express existante ; servir l'API et le frontend React dans un seul conteneur Docker (build multi-étapes) ; rester simple — pas d'authentification, pas de routage client, pas de bibliothèque d'état ; lancer npm install dans le Dockerfile. Enregistre le plan dans ui-plan.md, dans le répertoire du projet. » |
| Implémenter (mode Agent) | « Implémente le plan ui-plan.md pour construire l'interface web, conteneurise l'application avec Docker et démarre-la. N'installe pas les dépendances localement — le Dockerfile gère tout. » |
| Personnaliser les styles | « Mets à jour les styles de l'interface web : police Inter, fond bleu nuit, texte blanc. » |
| Reconstruire | « Reconstruis l'image Docker et redémarre le conteneur avec les styles mis à jour. » |

## Glossaire (fidèle aux sources)

| Terme | Définition en une phrase |
|---|---|
| **IBM Bob** | Partenaire IA du cycle de vie du développement logiciel (SDLC), qui s'ajoute à vos workflows et travaille sur de vraies bases de code ; application IDE autonome. |
| **Modes (Ask / Plan / Agent)** | Personas spécialisés : Ask lit sans écrire, Plan conçoit avant d'implémenter, Agent écrit, modifie et refactorise — sous approbation. |
| **Principe du moindre privilège** | Chaque mode ne reçoit que les permissions nécessaires à sa tâche — le mode Ask ne peut que lire. |
| **Auto-approbation** | Réglage du menu Permissions (bas droite) définissant ce que Bob exécute sans demander ; la config sûre est « Read » uniquement. |
| **AGENTS.md** | Fichier d'instructions persistantes créé par /init : structure, conventions et objectifs du projet. |
| **Dossier .bob** | Contient les fichiers de règles de Bob, un par mode (Agent, Plan, Ask). |
| **Stateless** | Bob ne conserve pas d'état entre les conversations : sans AGENTS.md, il repart du début à chaque fois. |
| **Skill** | Module qui étend Bob avec des connaissances et comportements spécialisés. |
| **MCP** | Model Context Protocol : cadre qui connecte des outils externes à Bob ; serveurs locaux ou distants, gérés depuis le panneau de configuration. |
| **Subagent** | Agent spécialisé que Bob peut créer pour paralléliser une tâche complexe — chaque création est approuvée par vous. |
| **Bob Shell** | L'assistance de Bob emportée dans le terminal, au-delà de l'éditeur. |
| **Bobalytics** | Le suivi de la consommation en Bobcoins et de la productivité. |

## Rappel des sources

1. Plan de formation « 12 vidéos » (image fournie par le commanditaire).
2. IBM Bob — Documentation IDE, page d'accueil : https://bob.ibm.com/docs/ide
3. IBM Bob — Quickstart : https://bob.ibm.com/docs/ide/getting-started/quickstart
4. IBM Bob — Changelog : https://bob.ibm.com/docs/ide/changelog (consulté le 2 septembre 2026 pour la vérification de compatibilité avec la version 2.1.0)

*Tous les faits, prompts, libellés d'interface, commandes et scénarios de ce pack sont issus des sources officielles ci-dessus : les trois premières pour la rédaction, le changelog uniquement pour la vérification de compatibilité avec la 2.1.0. Les notions listées par le plan de formation mais non détaillées dans les pages de documentation fournies (hooks, bobignore, /review, /help, /clear) sont présentées de manière volontairement générale, à approfondir dans la documentation officielle.*
