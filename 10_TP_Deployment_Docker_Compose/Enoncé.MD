# TP 10 - Déploiement complet avec Docker Compose

---

## Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Déployer toute une architecture IoT avec Docker Compose
* Comprendre la notion de services multi-conteneurs
* Utiliser les healthchecks
* Gérer les dépendances entre services
* Industrialiser une stack complète

---

## Contexte

Jusqu’à présent, nous avons :

* lancé chaque conteneur manuellement
* configuré chaque service séparément

👉 En entreprise, cette approche n’est pas scalable.

👉 On utilise Docker Compose pour orchestrer toute la stack.

---

# Architecture finale

```text
OPC-UA → MQTT → Node-RED → InfluxDB → Grafana
```

---

# Partie 1 — Création du docker-compose.yml

---

Créer le fichier :

```bash
nano docker-compose.yml
```

---

## Contenu

```yaml
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
    networks:
      - iiot-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8086/health"]

  grafana:
    image: grafana/grafana
    container_name: grafana
    depends_on:
      - influxdb
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
  node-red-data:

networks:
  iiot-network:
    driver: bridge
```

---

# Partie 2 — Lancer la stack

---

```bash
docker compose up -d --build
```

---

# Partie 3 — Vérification

---

```bash
docker compose ps
```

---

👉 Tous les services doivent être :

* running
* healthy

---

# Partie 4 — Accès aux services

---

| Service  | URL                   |
| -------- | --------------------- |
| Node-RED | http://localhost:1880 |
| InfluxDB | http://localhost:8086 |
| Grafana  | http://localhost:3000 |

---

# Partie 5 — Comprendre les Healthchecks

---

## Définition

Un healthcheck permet de vérifier si un service fonctionne correctement.

---

## Exemple MQTT

```yaml
healthcheck:
  test: ["CMD", "mosquitto_pub", "-h", "localhost", "-t", "healthcheck", "-m", "ok"]
```

---

👉 Vérifie que le broker répond

---

## Exemple InfluxDB

```yaml
test: ["CMD", "curl", "-f", "http://localhost:8086/health"]
```

---

👉 Vérifie que l’API est disponible

---

## Pourquoi c’est important ?

* éviter démarrage trop rapide
* gérer dépendances
* améliorer la stabilité

---

# Partie 6 — Dépendances intelligentes

---

```yaml
depends_on:
  mosquitto:
    condition: service_healthy
```

---

👉 Node-RED attend que MQTT soit prêt

---

# Analyse

---

## Exercice 1

Pourquoi utiliser Docker Compose ?

---

## Exercice 2

Quel est le rôle des healthchecks ?

---

## Exercice 3

Pourquoi utiliser depends_on ?

---

## Exercice 4

Quelle différence avec docker run ?

---

# Résultat attendu

* stack complète déployée
* services interconnectés
* architecture fonctionnelle

---

# Hints

* vérifier logs : docker compose logs
* vérifier ports
* vérifier network

---

# Conclusion

Docker Compose permet de déployer une architecture complète en une seule commande.

👉 C’est la base des environnements DevOps modernes.

---

## Prochaine étape

👉 Déploiement avec Ansible / CI-CD

---
