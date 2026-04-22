#  Corrigé — TP 10 Docker Compose & Provisioning

---

##  Principe clé

👉 On passe de :

```text
configuration manuelle ❌
```

à :

```text
infrastructure automatisée ✅
```

---

# ⚙️ 1 — Fichier `.env`

---

```env
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=admin
DOCKER_INFLUXDB_INIT_PASSWORD=admin123
DOCKER_INFLUXDB_INIT_ORG=iiot
DOCKER_INFLUXDB_INIT_BUCKET=edge-GW
INFLUXDB_TOKEN=my-super-token

GF_SMTP_ENABLED=true
GF_SMTP_HOST=smtp.gmail.com:587
GF_SMTP_USER=your_email@gmail.com
GF_SMTP_PASSWORD=your_app_password
GF_SMTP_FROM_ADDRESS=your_email@gmail.com
GF_SMTP_FROM_NAME=grafana
```

---

##  Explication

👉 Permet d’initialiser automatiquement InfluxDB
👉 Configure aussi l’envoi d’emails dans Grafana

---

# 2 — Secret InfluxDB

---

```bash
mkdir -p secrets
echo "my-super-token" > secrets/influx_token.txt
```

---

## Explication

👉 évite d’exposer le token dans le code
👉 bonne pratique DevOps

---

# 3 — Docker Compose COMPLET

---

![docker-compose](docker-compose.yml)
---

#  Explication des services

---

## MQTT

👉 broker simple (edge)

---

## InfluxDB

👉 base de données time-series
👉 initialisée automatiquement

---

## Grafana

👉 provisioning automatique :

* datasource
* dashboards
* alertes

---

## Node-RED

👉 traitement des données
👉 flow chargé automatiquement

---

## Data Collector

👉 OPC-UA → MQTT

---

# Réseau

---

👉 tous les services utilisent :

```text
iiot-network
```

✔ communication interne
✔ pas besoin d’IP

---

# 4 — Lancement

---

```bash
docker compose up -d
```

---

#  Vérification

---

## Grafana

👉 dashboards déjà présents
👉 alertes déjà configurées

---

## InfluxDB

👉 bucket automatiquement créé

---

## Node-RED

👉 flow chargé automatiquement

---

#  Réponses aux questions

---

## Question 1

👉 Docker Compose permet :

* déploiement rapide
* reproductibilité
* standardisation

---

## Question 2

👉 Provisioning Grafana :

* évite config manuelle
* déploiement automatique
* cohérence

---

## Question 3

👉 Automatisation :

* gain de temps
* réduction des erreurs
* passage à l’échelle

---

# Conclusion

---

👉 Tu as maintenant :

✔ une plateforme IIoT complète
✔ automatisée
✔ prête pour production

---
