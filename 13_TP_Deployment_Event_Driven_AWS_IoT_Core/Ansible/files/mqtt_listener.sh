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