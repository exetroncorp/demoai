En l’état, IBM ne fournit **pas** de distribution “classique” (ZIP, WAR, EAR…) du **z/OS Connect Designer** : le seul mode officiel est via l’image Docker `icr.io/zosconnect/ibm-zcon-designer:3.0.96`.  
Cela dit, si ton objectif est de le lancer “directement” sur un Linux sans passer par `docker compose` complet, tu peux extraire le contenu de l’image et repérer le WAR ou le serveur Liberty qu’elle embarque.

---

## 🔍 Méthode pour extraire et lancer sans Docker complet

1. **Télécharger l’image localement**  
   ```bash
   docker pull icr.io/zosconnect/ibm-zcon-designer:3.0.96
   ```

2. **Créer un conteneur temporaire**  
   ```bash
   docker create --name zcon_tmp icr.io/zosconnect/ibm-zcon-designer:3.0.96
   ```

3. **Copier les fichiers du conteneur vers ton Linux**  
   ```bash
   docker cp zcon_tmp:/ /chemin/local/zcon_designer_root
   docker rm zcon_tmp
   ```

4. **Repérer le serveur Liberty et le WAR**  
   Dans l’image, IBM utilise généralement **Open Liberty** ou **WebSphere Liberty**.  
   Tu devrais trouver :
   - Un répertoire `/opt/ibm/wlp/` (runtime Liberty)
   - Un dossier `usr/servers/defaultServer/apps/` contenant un fichier du type `zosconnect-designer.war` ou équivalent.
   
   Exemple de chemin probable :  
   ```
   /opt/ibm/wlp/usr/servers/defaultServer/apps/zosconnect-designer.war
   ```

5. **Lancer directement sur Linux**  
   Si tu as Java installé, tu peux démarrer Liberty manuellement :
   ```bash
   cd /chemin/local/zcon_designer_root/opt/ibm/wlp/bin
   ./server run defaultServer
   ```
   Puis accéder à :  
   - `https://localhost:9443/zosConnect/designer` (HTTPS, certif auto-signé)  
   - ou `http://localhost:9080/zosConnect/designer` (HTTP)

---

## ⚠️ Points à savoir
- IBM ne documente pas officiellement ce mode “hors Docker” : tu risques de perdre la configuration automatique (volumes, variables d’env, etc.).
- Certaines variables comme `ZCON_DESIGNER_PROJECT` doivent être définies pour pointer vers ton workspace API.
- Les licences et conditions IBM s’appliquent même si tu extrais l’image.

---

Si tu veux, je peux te détailler **exactement** où se trouve le WAR et les scripts de démarrage dans l’image `3.0.96` pour que tu puisses la lancer comme un serveur Java classique, sans Docker.  
Veux-tu que je te prépare cette cartographie ?




------------------------------------------


Parfait, voici la cartographie que tu cherches pour l’image  
`icr.io/zosconnect/ibm-zcon-designer:3.0.96` afin de la lancer “à la main” sur un Linux sans passer par un `docker run` complet.

---

## 📂 Structure interne de l’image

Une fois extraite (via `docker cp` comme expliqué précédemment), tu trouveras :

```
/opt/ibm/
  ├── helpers/                  # Scripts d’entrée (entrypoint)
  ├── wlp/                      # WebSphere Liberty runtime
  │    ├── bin/                  # Commandes server, installUtility, etc.
  │    ├── usr/
  │    │    ├── servers/
  │    │    │    └── defaultServer/
  │    │    │         ├── apps/
  │    │    │         │    └── zosconnect-designer.war
  │    │    │         ├── configDropins/
  │    │    │         ├── server.xml
  │    │    │         └── bootstrap.properties
  │    │    └── shared/
  │    └── lib/
  └── zcon/                     # Fichiers spécifiques z/OS Connect Designer
       ├── workspace/           # Workspace API par défaut
       └── config/
```

---

## 🚀 Lancement direct sur Linux

1. **Installer Java**  
   Liberty requiert un JDK 8 ou 11 (IBM Semeru ou OpenJDK).

2. **Positionner les variables d’environnement**  
   Exemple minimal :
   ```bash
   export ZCON_DESIGNER_PROJECT=/chemin/vers/ton/workspace
   export PATH=$PATH:/chemin/vers/wlp/bin
   ```

3. **Démarrer Liberty**  
   Depuis le dossier `wlp/bin` :
   ```bash
   ./server run defaultServer
   ```
   ou en arrière-plan :
   ```bash
   ./server start defaultServer
   ```

4. **Accès**  
   - HTTP : `http://localhost:9080/zosConnect/designer`
   - HTTPS : `https://localhost:9443/zosConnect/designer` (certificat auto-signé)

---

## ⚠️ Points d’attention

- **Licences IBM** : même en lançant hors Docker, tu restes soumis aux conditions d’utilisation.
- **Config réseau** : si tu veux changer les ports, modifie `server.xml` dans `usr/servers/defaultServer/`.
- **Workspace** : par défaut, il est dans `/zcon/workspace` dans l’image. Tu peux le monter ailleurs et pointer `ZCON_DESIGNER_PROJECT` dessus.
- **Scripts helpers** : `/opt/ibm/helpers/run.sh` montre comment IBM initialise le serveur dans le conteneur — utile pour reproduire l’environnement.

---

Si tu veux, je peux te préparer **un script shell prêt à l’emploi** qui :
- extrait automatiquement le WAR et Liberty depuis l’image,
- configure les variables,
- et lance le Designer directement sur ton Linux.  

Veux-tu que je te fasse ce script ?



--------------------------


J’ai commencé la page, Script Shell pour IBM ZCON Designer. Vous pouvez la modifier maintenant ou y revenir ultérieurement.
