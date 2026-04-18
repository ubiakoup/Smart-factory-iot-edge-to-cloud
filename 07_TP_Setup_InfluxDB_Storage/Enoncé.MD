# TP 07 - Setup InfluxDB (Stockage des données)

---

## Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Comprendre le rôle d’une base de données time-series
* Déployer InfluxDB avec Docker
* Configurer InfluxDB (org, bucket, token)
* Assurer la persistance des données
* Préparer l’intégration avec Node-RED

---

## Contexte

Dans notre architecture IoT :

* les données sont collectées (OPC-UA)
* transportées (MQTT)
* traitées (Node-RED)

👉 Elles doivent être stockées de manière fiable.

---

## Pourquoi InfluxDB ?

InfluxDB est une base de données spécialisée pour :

* données temporelles (time-series)
* IoT
* monitoring industriel

---

# Partie 1 — Configuration (.env)

---

Créer un fichier `.env` :

```bash id="6r3e92"
nano .env
```

---

## Contenu

```env id="v8n5ru"
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=admin
DOCKER_INFLUXDB_INIT_PASSWORD=admin123
DOCKER_INFLUXDB_INIT_ORG=iiot
DOCKER_INFLUXDB_INIT_BUCKET=edge-GW
INFLUXDB_TOKEN=my-super-token
```

---

# Partie 2 — Création du volume (CRITIQUE)

---

```bash id="h9j2x7"
docker volume create influxdb-data
```

---

## Pourquoi ?

👉 Ce volume permet de :

* conserver les données
* éviter la perte lors d’un redémarrage

---

# Partie 3 — Lancer InfluxDB

---

```bash id="n2k8q4"
docker run -d \
  --name influxdb \
  --network iiot-network \
  -p 8086:8086 \
  -v influxdb-data:/var/lib/influxdb2 \
  --env-file .env \
  --restart unless-stopped \
  influxdb:2.7
```

---

# Partie 4 — Vérification

---

```bash id="9l2v8k"
docker ps
```

---

# Partie 5 — Accès à l’interface

---

Ouvrir dans votre navigateur :

```text id="6h2p9n"
http://localhost:8086
```

---

## Connexion

* Username : admin
* Password : admin123
* Organisation : iiot
* Bucket : edge-GW

---

# Partie 6 — Concepts importants

---

## Organisation (Org)

Structure logique du projet

---

## Bucket

👉 Base de données contenant les mesures

---

## Token

👉 Clé sécurisée pour accès API

---

## Time-series

👉 Données avec timestamp

---

# Partie 7 — Intégration future

---

Flux global :

```text id="j3r8k1"
OPC-UA → MQTT → Node-RED → InfluxDB
```

---

👉 Node-RED enverra les données vers InfluxDB

---

# Analyse

---

## Exercice 1

Pourquoi InfluxDB est adapté à l’IoT ?

---

## Exercice 2

Pourquoi utiliser un volume Docker ?

---

## Exercice 3

Quel est le rôle du bucket edge-GW ?

---

## Exercice 4

Pourquoi utiliser un token ?

---

# Résultat attendu

* InfluxDB fonctionnel
* Interface accessible
* Données persistées

---

# Hints

* vérifier docker ps
* vérifier volume
* vérifier .env
* vérifier logs

---

# Vision globale

```text id="p4h7k1"
Data → Node-RED → InfluxDB (persistant)
```

---

# Conclusion

InfluxDB permet de stocker les données de manière fiable.

👉 Élément essentiel pour le monitoring industriel.

---

## Prochaine étape

👉 Visualisation avec Grafana

---
