# 📘 TP13 – Énoncé : Déploiement Event-Driven (Trigger par événement)

---

# Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Comprendre les limites du Pull Model
* Mettre en place un déclenchement par événement
* Déployer une stack à la demande
* Utiliser MQTT comme trigger
* Implémenter une logique Event-Driven sur un Edge

---

#  Contexte

Dans le TP12, vous avez mis en place un Pull Model :

```text
Edge → git pull → docker compose
```

👉 Mais ce modèle présente une limite :

```text
❌ vérification périodique (polling)
❌ latence inutile
❌ consommation inutile
```

---

#  Nouvelle approche : Event-Driven

👉 L’Edge ne vérifie plus en boucle
👉 Il réagit uniquement lorsqu’un événement arrive

---

#  Architecture

```text
Dev → git push → Event → MQTT → Edge → Deploy
```

---

#  Principe

1. Un événement est envoyé (ex: MQTT)
2. L’Edge reçoit cet événement
3. L’Edge déclenche le déploiement

---

#  Partie 1 — Préparer le script de déploiement

---

Créer le script :

```bash
nano /home/vagrant/deploy.sh
```

---

Contenu :

```bash
#!/bin/bash

PROJECT_DIR="/home/vagrant/edge-stack"

echo "📁 Moving to project directory..."
cd $PROJECT_DIR || exit 1

echo "🔄 Pull latest version..."
git pull origin main || exit 1

echo "🚀 Deploying..."
docker compose up -d --build

echo "✅ Done"
```

---

Rendre exécutable :

```bash
chmod +x /home/vagrant/deploy.sh
```

---

# 📡 Partie 2 — Subscriber MQTT

---

Créer le script :

```bash
nano /home/vagrant/mqtt-listener.sh
```

---

Contenu :

```bash
#!/bin/bash

echo "📡 Listening for deploy events..."

mosquitto_sub -h localhost -t deploy/edge | while read msg
do
    echo "📨 Event received: $msg"

    if [ "$msg" = "update" ]; then
        echo "🚀 Trigger deployment..."
        /home/vagrant/deploy.sh
    fi
done
```

---

Rendre exécutable :

```bash
chmod +x /home/vagrant/mqtt-listener.sh
```

---

# ⚙️ Partie 3 — Service systemd

---

Créer le service :

```bash
sudo nano /etc/systemd/system/iiot-event.service
```

---

Contenu :

```ini
[Unit]
Description=IIoT Event Driven Deployment
After=network.target

[Service]
User=vagrant
ExecStart=/home/vagrant/mqtt-listener.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

---

Activer :

```bash
sudo systemctl daemon-reload
sudo systemctl enable iiot-event.service
sudo systemctl start iiot-event.service
```

---

# 🧪 Partie 4 — Test

---

Envoyer un événement :

```bash
mosquitto_pub -h localhost -t deploy/edge -m update
```

---

👉 Attendu :

* réception du message
* déclenchement du script
* mise à jour de la stack

---

# 🔍 Analyse

---

## Exercice 1

Pourquoi ce modèle est-il plus efficace que le Pull Model ?

---

## Exercice 2

Quelle est la différence entre polling et event-driven ?

---

## Exercice 3

Quels sont les avantages en environnement industriel ?

---

---

# 📘 TP13 – Corrigé : Event-Driven Deployment

---

# 🧠 Analyse

---

## Pourquoi Event-Driven ?

```text
✔ pas de boucle inutile
✔ réaction immédiate
✔ consommation minimale
✔ scalable
```

---

## Polling vs Event

| Polling           | Event-Driven        |
| ----------------- | ------------------- |
| vérifie en boucle | attend un événement |
| latence           | immédiat            |
| consommation CPU  | faible              |
| inefficace        | optimisé            |

---

# ⚙️ Script de déploiement

👉 identique au TP12 mais déclenché à la demande

---

# 📡 MQTT Listener

👉 rôle :

```text
✔ écouter un topic
✔ déclencher une action
```

---

# ⚙️ systemd

👉 permet :

* démarrage automatique
* résilience
* redémarrage en cas d’erreur

---

# ⚠️ Points importants

---

## ❌ Ne pas utiliser localhost si broker en container

👉 utiliser :

```text
mqtt-broker
```

---

## ❌ Ne pas oublier docker dans le script

👉 sinon aucun déploiement

---

## ❌ Permissions script

👉 sinon rien ne s’exécute

---

# 🔐 Bonnes pratiques

---

* sécuriser MQTT (auth / TLS)
* limiter les topics
* éviter les déclenchements non contrôlés

---

# 🧠 Conclusion

---

## Avant (TP12)

```text
Edge vérifie régulièrement
```

---

## Maintenant (TP13)

```text
Edge réagit uniquement aux événements
```

---

## Résultat

* système réactif
* zéro polling
* architecture moderne

---
