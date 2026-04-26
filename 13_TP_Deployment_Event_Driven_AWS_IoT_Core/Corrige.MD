#  TP13 – Corrigé final

##  Passage à une architecture Event-Driven avec AWS IoT Core

---

# 🎯 Objectif du TP

Faire évoluer l’architecture du TP12 pour passer de :

```text
Polling (Edge vérifie)
```

à :

```text
Event-driven (le système déclenche)
```

👉 Objectif final :

```text
git push → déclenche automatiquement un déploiement sur l’Edge
```

---

#  Partie 1 — Analyse (Lien avec TP12)

---

##  Rappel TP12

Dans le TP12, nous avions :

```text
Edge → git pull toutes les 5 minutes → deploy si changement
```

👉 basé sur :

* script `pull-update.sh`
* service systemd
* boucle de polling

---

##  Ce qui fonctionnait

* Edge autonome
* mise à jour automatique
* système simple

---

## ❗ Problème fondamental

```text
Le système vérifie même quand il n’y a rien à faire
```

---

##  Conséquences

* CPU inutile
* trafic réseau inutile
* latence (jusqu’à 5 min)
* inefficacité à grande échelle

---

## Problème architectural

```text
L’Edge prend l’initiative → ce n’est pas optimal
```

---

##  Nouveau paradigme

```text
Ce n’est plus le device qui demande
→ c’est le système qui déclenche
```

---

# 🔄 Partie 2 — Passage à l’Event-Driven

---

##  Avant (Polling)

```text
Edge → "y a-t-il une mise à jour ?"
```

---

## Après (Event-driven)

```text
Git push → événement → déclenchement immédiat
```

---

## Concept clé

```text
On passe d’un système qui vérifie
→ à un système qui réagit
```

---

#  Partie 3 — Architecture finale

```text
Git Push
   ↓
GitHub Actions
   ↓
MQTT Publish (TLS)
   ↓
AWS IoT Core
   ↓
Edge (subscriber sécurisé)
   ↓
mqtt_listener.sh
   ↓
deploy.sh
   ↓
Docker Compose
```

---

#  Partie 4 — Contraintes industrielles

---

##  Réalité terrain

```text
Un Edge n’a PAS d’IP publique
```

---

## 👉 Solution

```text
✔ Edge initie la connexion vers le cloud
✔ le cloud envoie les événements
```

---

## 👉 Rôle de MQTT

* communication bidirectionnelle
* léger et temps réel
* adapté IoT

---

# 🛠️ Partie 5 — AWS IoT Core

---

## Création du device

* créer un Thing : `vagrant-edge-device`
* générer :

  * certificat (`.cert.pem`)
  * clé privée (`.private.key`)
  * CA (`root-CA.crt`)

---

## Endpoint

```text
AWS IoT Core → Settings → Endpoint
```

---

## Policy MQTT

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Subscribe",
      "Resource": "arn:aws:iot:*:*:topicfilter/deploy/edge"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Receive",
      "Resource": "arn:aws:iot:*:*:topic/deploy/edge"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Publish",
      "Resource": "arn:aws:iot:*:*:topic/deploy/edge"
    }
  ]
}
```

👉 (à restreindre par topic en production)

---

# Partie 6 — Script `deploy.sh`

---

##  Rôle

```text
Mettre à jour le code et redéployer la stack
```

---

##  Logique

* récupérer dernier commit
* comparer avec l’ancien
* déployer uniquement si nécessaire
* rollback si erreur

---

##  Implémentation

```bash
#!/bin/bash

set -euo pipefail

LOG_FILE="/home/vagrant/deploy.log"
PROJECT_DIR="/home/vagrant/edge-stack"

# -------------------------------
# Logging
# -------------------------------
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" | tee -a "$LOG_FILE"
}

log "Starting deployment"

# -------------------------------
# Go to project directory
# -------------------------------
cd "$PROJECT_DIR" || {
    log "❌ Failed to access project directory"
    exit 1
}

# -------------------------------
# Save current commit (rollback)
# -------------------------------
OLD_COMMIT=$(git rev-parse HEAD)
log "Current commit: $OLD_COMMIT"

# -------------------------------
# Pull latest code
# -------------------------------
log "🔄 Pulling latest version..."
sleep 2  # Simulate delay for testing anti-spam
git pull origin main

NEW_COMMIT=$(git rev-parse HEAD)
log "New commit: $NEW_COMMIT"

# -------------------------------
# Check if update needed
# -------------------------------
if [ "$OLD_COMMIT" = "$NEW_COMMIT" ]; then
    log "✅ No changes detected, skipping deployment"
    exit 0
fi

# -------------------------------
# Deploy
# -------------------------------
log " Deploying new version..."

if docker compose up -d --build; then
    log "✅ Deployment successful"
else
    log "❌ Deployment failed → rolling back..."

    git reset --hard "$OLD_COMMIT"

    docker compose up -d --build

    log "↩️ Rollback applied"
    exit 1
fi

# -------------------------------
# Cleanup
# -------------------------------
log "🧹 Cleaning unused images..."
docker image prune -f

log "✅ Deployment finished successfully"

```

---

# 📡 Partie 7 — MQTT Listener

---

## Rôle

```text
Transformer un message MQTT en action système
```

---

## Fonctionnement

* écoute AWS IoT
* reçoit message `update`
* déclenche `deploy.sh`

---

## ⚠️ Problème réel

```text
Plusieurs commits peuvent arriver rapidement
```

---

##  Solution implémentée

| Mécanisme | Rôle                         |
| --------- | ---------------------------- |
| LOCK      | empêche concurrence          |
| PENDING   | mémorise événements          |
| LOOP      | converge vers dernier commit |
| COOLDOWN  | évite spam                   |

---

##  Script final (résumé)

```bash
#!/bin/bash

set -euo pipefail

# -------------------------------
# CONFIG
# -------------------------------
BROKER="aee5b2mogflua-ats.iot.us-east-1.amazonaws.com"
CERT_DIR="/home/vagrant/certs"
DEVICE="vagrant-edge-device"

TOPIC="deploy/vagrant-edge-device"

LOCK_FILE="/tmp/deploy.lock"
PENDING_UPDATE="/tmp/deploy.pending"
LAST_RUN_FILE="/tmp/last_deploy_time"
LOG_FILE="/home/vagrant/mqtt_listener.log"

COOLDOWN=30

# -------------------------------
# LOG FUNCTION
# -------------------------------
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" | tee -a "$LOG_FILE"
}

# -------------------------------
# CLEANUP
# -------------------------------
cleanup() {
    rm -f "$LOCK_FILE"
}
trap cleanup EXIT

log "Starting MQTT listener..."

# -------------------------------
# MAIN LOOP
# -------------------------------
while true; do

    log "Connecting to AWS IoT..."

    while read -r msg
    do
        [ -z "$msg" ] && continue

        log "Message reçu: $msg"

        if [ "$msg" != "update" ]; then
        log "Message ignoré"
        continue
    fi

        if [ -f "$LOCK_FILE" ]; then
            log "Deploy en cours → pending"
            touch "$PENDING_UPDATE"
            continue
        fi

        if [ -f "$LAST_RUN_FILE" ]; then
            LAST_RUN=$(cat "$LAST_RUN_FILE")
            NOW=$(date +%s)
            DIFF=$((NOW - LAST_RUN))

            if [ "$DIFF" -lt "$COOLDOWN" ]; then
                log "Cooldown actif ($DIFF sec) → ignoré"
                continue
            fi
        fi

        touch "$LOCK_FILE"
        date +%s > "$LAST_RUN_FILE"

        while true; do

            log "🚀 Déploiement..."

            if timeout 300 /home/vagrant/deploy.sh; then
                log "✅ Déploiement OK"
            else
                log "❌ Déploiement échoué"
            fi

            if [ ! -f "$PENDING_UPDATE" ]; then
                break
            fi

            log "🔁 Pending détecté → nouveau cycle"
            rm -f "$PENDING_UPDATE"

        done

        rm -f "$LOCK_FILE"

    done < <(mosquitto_sub \
      -h "$BROKER" \
      -p 8883 \
      --cafile "$CERT_DIR/root-CA.crt" \
      --cert "$CERT_DIR/$DEVICE.cert.pem" \
      --key "$CERT_DIR/$DEVICE.private.key" \
      -t "$TOPIC")

    log "MQTT déconnecté → reconnexion dans 5s..."
    sleep 5

done
```

---

#  Partie 8 — systemd

---

## 🎯 Rôle

```text
Garantir que le listener fonctionne en continu
```

---

## Configuration

```ini
[Unit]
Description=MQTT Listener AWS (Edge Deployment)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=vagrant

ExecStart=/bin/bash /home/vagrant/mqtt_listener.sh

# 🔥 robustesse réseau
Restart=on-failure
RestartSec=5

# 🔥 limites anti-bug
StartLimitBurst=5
StartLimitIntervalSec=60

# 🔐 sécurité
NoNewPrivileges=true
PrivateTmp=true

# 🔧 ressources
MemoryMax=500M
CPUQuota=80%
TasksMax=50
LimitNOFILE=1024

# 📝 logs
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

#  Partie 9 — GitHub Actions

---

## 🎯 Rôle

```text
Relier CI/CD → Edge
```

---

## Fonctionnement

```text
git push → GitHub Actions → MQTT publish
```

---

## Exemple

```yaml
mosquitto_pub \
  -h AWS_ENDPOINT \
  -p 8883 \
  --cert cert.pem \
  --key private.key \
  -t deploy/vagrant-edge-device \
  -m update
```

---

#  Partie 10 — Test global

---

## Scénario

```text
git push → MQTT → Edge → deploy
```

---

## Résultat attendu

* déclenchement immédiat
* pas de polling
* système réactif

---

#  Partie 11 — Réponses attendues

---

## 1. Pourquoi polling non adapté ?

* inefficace
* latence
* non scalable

---

## 2. Pourquoi MQTT ?

* léger
* temps réel
* adapté IoT

---

## 3. Pourquoi Edge initie la connexion ?

* pas d’IP publique
* sécurité réseau

---

## 4. Rôle GitHub Actions ?

* déclencheur d’événement
* lien CI/CD → Edge

---

# 🚀 Conclusion

---

## Avant (TP12)

```text
Edge autonome mais basé sur polling
```

---

## Après (TP13)

```text
Edge piloté par événements
```

---

## Résultat

```text
✔ temps réel
✔ scalable
✔ sécurisé
✔ architecture industrielle
```

---

# 💬 À retenir

```text
Le polling est simple
mais l’event-driven est la norme industrielle
```

---
