# Corrigé - TP 07 InfluxDB

---

## Étape 1 — Création du fichier .env

```env id="w3m8n2"
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=admin
DOCKER_INFLUXDB_INIT_PASSWORD=admin123
DOCKER_INFLUXDB_INIT_ORG=iiot
DOCKER_INFLUXDB_INIT_BUCKET=edge-GW
INFLUXDB_TOKEN=my-super-token
```

---

## Étape 2 — Création du volume

```bash id="2k8p7v"
docker volume create influxdb-data
```

---

## Étape 3 — Lancement du conteneur

```bash id="8d1k3v"
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

## Étape 4 — Vérification

```bash id="6j3k9v"
docker ps
```

---

## Étape 5 — Accès

```text id="l2p7k3"
http://localhost:8086
```

---

## Exercice 1

### Pourquoi InfluxDB ?

* optimisé pour time-series
* performant
* adapté IoT

---

## Exercice 2

### Pourquoi volume ?

* persistance
* sécurité des données

---

## Exercice 3

### Bucket edge-GW

* stockage des données de l’Edge

---

## Exercice 4

### Token

* sécurisation des accès

---

## Problèmes fréquents

---

### Données perdues

👉 volume non utilisé

---

### Container KO

```bash id="9k2d8v"
docker logs influxdb
```

---

### Interface inaccessible

* vérifier port 8086

---

## Vérification du volume

```bash id="3k8p2v"
docker volume ls
docker inspect influxdb
```

---

## Vision globale

```text id="8j2k4p"
Node-RED → InfluxDB → stockage
```

---

## Conclusion

InfluxDB est correctement configuré et persistant.

👉 prêt pour visualisation avec Grafana

---

## Prochaine étape

👉 Grafana

---
