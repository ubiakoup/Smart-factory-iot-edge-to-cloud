
#  Smart Factory IoT – Event-Driven Edge Deployment (AWS IoT Core)

---

# 🎯 Objectif du projet

Ce projet implémente une architecture IoT industrielle permettant de déclencher automatiquement un déploiement Edge via un simple :

```text
git push → deploy automatique sur l’Edge
```

---

#  Contexte (TP12 → TP13)

---

##  Avant (TP12 – Pull Model)

```text
Edge → vérifie Git toutes les 5 min
```

### Limites :

* latence
* consommation inutile
* non scalable

---

## Maintenant (TP13 – Event-Driven)

```text
Git push → événement → déploiement immédiat
```

👉 changement de paradigme :

```text
On ne vérifie plus → on réagit
```

---

# 🧱 Architecture globale

```text
GitHub (push)
        ↓
GitHub Actions (CI/CD)
        ↓
MQTT Publish (TLS)
        ↓
AWS IoT Core
        ↓
Edge Device (subscriber)
        ↓
mqtt_listener.sh
        ↓
deploy.sh
        ↓
Docker Compose
```

---

# 🔐 Contraintes industrielles

```text
✔ Edge sans IP publique
✔ communication sortante uniquement
✔ sécurité TLS obligatoire
```

👉 solution :

```text
Edge → connecté au cloud
Cloud → envoie les événements
```

---

# ⚙️ Fonctionnement global

1. Développeur fait un `git push`
2. GitHub Actions s’exécute
3. Envoi d’un message MQTT sécurisé
4. AWS IoT Core transmet
5. Edge reçoit
6. `deploy.sh` est exécuté

---

# ☁️ GitHub Actions (CI/CD → Edge)

---

## 🎯 Rôle

Transformer :

```text
git push
```

en :

```text
événement MQTT
```

---

## 🔐 Secrets utilisés

| Secret           | Description |
| ---------------- | ----------- |
| AWS_CERT         | certificat  |
| AWS_PRIVATE_KEY  | clé privée  |
| AWS_CA           | CA          |
| AWS_IOT_ENDPOINT | endpoint    |

---

## ⚙️ Workflow

```yaml
name: Deploy Edge via AWS IoT

on:
  push:
    branches:
      - main

jobs:
  trigger:
    runs-on: ubuntu-latest
    environment: Edge_Vagrant_Secrets 

    steps:

      - name: Install mosquitto
        run: |
          sudo apt-get update
          sudo apt-get install -y mosquitto-clients

      - name: Create cert files
        run: |
          echo "${{ secrets.AWS_CERT }}" > cert.pem
          echo "${{ secrets.AWS_PRIVATE_KEY }}" > private.key
          echo "${{ secrets.AWS_CA }}" > root-CA.crt

      - name: Send MQTT trigger
        run: |
          mosquitto_pub \
            -h "${{ secrets.AWS_IOT_ENDPOINT }}" \
            -p 8883 \
            --cafile root-CA.crt \
            --cert cert.pem \
            --key private.key \
            -t deploy/vagrant-edge-device \
            -m update
```

---

# 🔐 AWS IoT Core

---

## Création du device

* Thing : `vagrant-edge-device`
* certificats :

  * `.cert.pem`
  * `.private.key`
  * `root-CA.crt`

---

## Policy minimale

```json
{
  "Effect": "Allow",
  "Action": ["iot:Connect","iot:Subscribe","iot:Receive","iot:Publish"],
  "Resource": "*"
}
```

---

# ⚙️ Script `deploy.sh`

---

## 🎯 Rôle

* mettre à jour le code
* déployer la stack
* rollback si erreur

---

## 🔥 Version production

```bash
#!/bin/bash
set -euo pipefail

PROJECT_DIR="/home/vagrant/edge-stack"

cd "$PROJECT_DIR" || exit 1

OLD_COMMIT=$(git rev-parse HEAD)

git pull origin main

NEW_COMMIT=$(git rev-parse HEAD)

if [ "$OLD_COMMIT" = "$NEW_COMMIT" ]; then
    exit 0
fi

docker compose up -d --build
```

---

# 📡 Script `mqtt_listener.sh`

---

## 🎯 Rôle

* écouter MQTT
* déclencher deploy
* gérer les événements

---

## 🔑 Concepts clés

| Concept  | Description                  |
| -------- | ---------------------------- |
| LOCK     | empêche concurrence          |
| PENDING  | mémorise update              |
| LOOP     | converge vers dernier commit |
| COOLDOWN | évite spam                   |

---

## 🔥 Logique

```bash
if deploy en cours → pending

while true:
    deploy
    si pending → redeploy
    sinon stop
```

---

# ⚙️ Service systemd

```ini
[Unit]
Description=MQTT Listener AWS
After=network-online.target

[Service]
User=vagrant
ExecStart=/home/vagrant/mqtt_listener.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

---

# 🧪 Test complet

```text
git push
→ GitHub Actions
→ MQTT
→ Edge
→ deploy
```

---

# 🧠 Concepts avancés

* Event-driven architecture
* MQTT sécurisé (TLS)
* Concurrency control
* Idempotence
* GitOps simplifié
* Distributed systems

---

# ⚠️ Problèmes rencontrés

* mauvaise policy AWS
* certificats incorrects
* endpoint manquant
* permissions Linux
* concurrence non gérée

---

# 🚀 Résultat final

```text
✔ déploiement instantané
✔ architecture scalable
✔ système robuste
✔ Edge autonome
✔ sécurité cloud
```

---

# 💬 Conclusion

---

## Avant

```text
Polling inefficace
```

---

## Après

```text
Event-driven industriel
```

---

## Résultat

```text
✔ rapide
✔ fiable
✔ maintenable
✔ production-ready
```

