# TP 10 - Déploiement complet avec Docker Compose

---

## Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Déployer une architecture IoT complète avec Docker Compose
* Utiliser des variables d’environnement
* Gérer des secrets de manière sécurisée
* Comprendre les healthchecks
* Orchestrer plusieurs services

---

## Contexte

Jusqu’à présent :

* chaque service était lancé manuellement
* la configuration était fragmentée

👉 En environnement réel, on automatise tout avec Docker Compose.

---

# Architecture finale

```text id="x1k9p2"
OPC-UA → MQTT → Node-RED → InfluxDB → Grafana
```

---

# Partie 1 — Fichier `.env`

---

Créer un fichier :

```bash id="c2m8k1"
nano .env
```

---

## Contenu

```env id="z4k7p2"
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=admin
DOCKER_INFLUXDB_INIT_PASSWORD=admin123
DOCKER_INFLUXDB_INIT_ORG=iiot
DOCKER_INFLUXDB_INIT_BUCKET=edge-GW
INFLUXDB_TOKEN=my-super-token
```

---

# Partie 2 — Gestion des secrets (optionnel mais recommandé)

---

Créer le dossier :

```bash id="p8k2m3"
mkdir -p secrets
```

---

Créer le fichier :

```bash id="y2k9p1"
nano secrets/influx_token.txt
```

---

## Contenu

```text id="u7k3p1"
my-super-token
```

---

# Partie 3 — docker-compose.yml

---

Créer le fichier :

```bash id="n8k2p4"
nano docker-compose.yml
```

---

## Contenu complet

```yaml id="m2k9p3"
version: "3.8"

services:

  mosquitto:
    image: eclipse-mosquitto
    container_name: mqtt-broker
    ports:
      - "1883:1883"
    networks:
      - iiot-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mosquitto_pub", "-h", "localhost", "-t", "healthcheck", "-m", "ok"]
      interval: 30s
      timeout: 10s
      retries: 5

  influxdb:
    image: influxdb:2.7
    container_name: influxdb
    ports:
      - "8086:8086"
    volumes:
      - influxdb-data:/var/lib/influxdb2
      - ./secrets/influx_token.txt:/run/secrets/influx_token:ro
    environment:
      DOCKER_INFLUXDB_INIT_MODE: ${DOCKER_INFLUXDB_INIT_MODE}
      DOCKER_INFLUXDB_INIT_USERNAME: ${DOCKER_INFLUXDB_INIT_USERNAME}
      DOCKER_INFLUXDB_INIT_PASSWORD: ${DOCKER_INFLUXDB_INIT_PASSWORD}
      DOCKER_INFLUXDB_INIT_ORG: ${DOCKER_INFLUXDB_INIT_ORG}
      DOCKER_INFLUXDB_INIT_BUCKET: ${DOCKER_INFLUXDB_INIT_BUCKET}
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: ${INFLUXDB_TOKEN}
      # Option avancée :
      # DOCKER_INFLUXDB_INIT_ADMIN_TOKEN_FILE: /run/secrets/influx_token
    networks:
      - iiot-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8086/health"]
      interval: 30s
      timeout: 10s
      retries: 5

  grafana:
    image: grafana/grafana
    container_name: grafana
    depends_on:
      influxdb:
        condition: service_healthy
    ports:
      - "3000:3000"
    volumes:
      - grafana-storage:/var/lib/grafana
    networks:
      - iiot-network
    restart: unless-stopped

  node-red:
    image: nodered/node-red
    container_name: node-red
    depends_on:
      mosquitto:
        condition: service_healthy
      influxdb:
        condition: service_healthy
    ports:
      - "1880:1880"
    volumes:
      - ./node-red-data:/data
    networks:
      - iiot-network
    restart: unless-stopped

  data-collector:
    build: .
    container_name: opcua-data-collector
    depends_on:
      mosquitto:
        condition: service_healthy
    volumes:
      - ./config.yml:/app/config.yml
    networks:
      - iiot-network
    restart: unless-stopped

volumes:
  influxdb-data:
  grafana-storage:

networks:
  iiot-network:
    driver: bridge
```

---

# Partie 4 — Lancement

---

```bash id="f3k9p2"
docker compose up -d --build
```

---

# Partie 5 — Vérification

---

```bash id="k2p8m1"
docker compose ps
```

---

👉 Tous les services doivent être :

* running
* healthy

---

# Partie 6 — Accès aux services

---

| Service  | URL                   |
| -------- | --------------------- |
| Node-RED | http://localhost:1880 |
| InfluxDB | http://localhost:8086 |
| Grafana  | http://localhost:3000 |

---

# Partie 7 — Healthchecks

---

## Définition

Permet de vérifier l’état d’un service.

---

## Exemple MQTT

```yaml id="p2k8m1"
healthcheck:
  test: ["CMD", "mosquitto_pub", "-h", "localhost"]
```

---

## Exemple InfluxDB

```yaml id="x7k2p1"
test: ["CMD", "curl", "-f", "http://localhost:8086/health"]
```

---

👉 Permet de garantir :

* démarrage correct
* dépendances fiables

---

# Analyse

---

## Exercice 1

Pourquoi utiliser Docker Compose ?

---

## Exercice 2

Pourquoi utiliser un fichier `.env` ?

---

## Exercice 3

Pourquoi utiliser un fichier secret ?

---

## Exercice 4

Quel est le rôle des healthchecks ?

---

# Résultat attendu

* stack complète fonctionnelle
* services interconnectés
* architecture stable

---

# Conclusion

Docker Compose permet de déployer toute l’architecture en une seule commande.

👉 C’est une approche DevOps moderne.

---

## Prochaine étape

👉 CI/CD et Pull Model

---
