# Corrigé - TP 10 Docker Compose

---

## Étape 1 — .env

```env id="v2k8p1"
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=admin
DOCKER_INFLUXDB_INIT_PASSWORD=admin123
DOCKER_INFLUXDB_INIT_ORG=iiot
DOCKER_INFLUXDB_INIT_BUCKET=edge-GW
INFLUXDB_TOKEN=my-super-token
```

---

## Étape 2 — Secrets

```bash id="y8k2p1"
mkdir -p secrets
echo "my-super-token" > secrets/influx_token.txt
```

---

## Étape 3 — Lancement

```bash id="p3k9m2"
docker compose up -d --build
```

---

## Vérification

```bash id="k4p8m1"
docker compose ps
```

---

## Logs

```bash id="z8k2p1"
docker compose logs
```

---

## Exercice 1

Docker Compose :

* orchestre plusieurs services
* simplifie le déploiement

---

## Exercice 2

.env :

* évite le hardcoding
* centralise la config

---

## Exercice 3

Secrets :

* sécurise les tokens

---

## Exercice 4

Healthchecks :

* vérifie état service
* améliore stabilité

---

## Problèmes fréquents

---

### Service KO

```bash id="k9p2m1"
docker compose logs influxdb
```

---

### Pas de données

* vérifier Node-RED
* vérifier MQTT

---

### Grafana vide

* vérifier InfluxDB
* vérifier bucket

---

## Conclusion

La stack IoT est entièrement automatisée.

---

## Vision finale

```text id="k1p9m3"
Smart Factory déployée automatiquement 🚀
```

---
