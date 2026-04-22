# TP 10 — Industrialisation avec Docker Compose & Provisioning automatique

---

## Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Concevoir une architecture IoT complète avec Docker Compose
* Automatiser le déploiement de tous les services
* Comprendre le rôle du provisioning (Grafana, InfluxDB, Node-RED)
* Déployer une plateforme IIoT en une seule commande

---

##  Contexte

Jusqu’ici, vous avez mis en place :

* MQTT ✔
* Node-RED ✔
* InfluxDB ✔
* Grafana ✔
* Alerting ✔

👉 MAIS toutes ces configurations ont été faites **manuellement**

---

## Problème

* déploiement long
* non reproductible
* erreurs humaines possibles

---

## Objectif du TP

👉 Construire une architecture **automatisée et industrialisée**

```text
PLC → OPC UA → MQTT → Node-RED → InfluxDB → Grafana
```

---

# Partie 1 — Structuration du projet

---

##  Objectif

Organiser correctement les fichiers pour permettre le provisioning automatique.

---

## À faire

Créer l’arborescence suivante :

```bash
10_TP_Deployment_Docker_Compose/
```

Puis organiser :

* un dossier `grafana/provisioning`
* un dossier `grafana/dashboards`
* un dossier `node-red`
* un dossier `secrets`

---

## Question

👉 Pourquoi structurer les fichiers avant Docker Compose ?

---

# Partie 2 — Configuration InfluxDB

---

## Objectif

Automatiser l’initialisation de :

* organisation
* bucket
* token

---

## À faire

Créer un fichier :

```bash
.env
```

---

## Question

👉 Pourquoi ne pas configurer InfluxDB à la main ?

---

# Partie 3 — Gestion des secrets

---

## Objectif

Sécuriser le token InfluxDB

---

## À faire

Créer un fichier :

```bash
secrets/influx_token.txt
```

---

## Question

👉 Pourquoi utiliser un secret au lieu d’une variable classique ?

---

# Partie 4 — Création du Docker Compose

---

## Objectif

Créer un fichier :

```bash
docker-compose.yml
```

---

## Contraintes

Votre docker-compose doit contenir :

---

###  MQTT

* image Mosquitto
* réseau commun
* port 1883

---

### InfluxDB

* initialisation via `.env`
* volume pour persistance
* healthcheck

---

### Grafana

* connexion à InfluxDB
* provisioning automatique :

  * datasource
  * dashboards
  * alertes
* configuration SMTP

---

### Node-RED

* connecté à MQTT et InfluxDB
* chargement automatique du flow

---

### Data Collector

* connecté à MQTT
* utilisation du fichier config.yml

---

### Réseau

* réseau Docker unique

---

## Question

👉 Pourquoi tous les services doivent être sur le même réseau ?

---

# Partie 5 — Déploiement

---

## Lancer l’infrastructure :

```bash
docker compose up -d
```

---

## Vérifier :

* les conteneurs sont UP
* les services sont accessibles

---

# Partie 6 — Validation

---

## Vérifier :

### Node-RED

👉 interface accessible

### InfluxDB

👉 bucket existant

### Grafana

👉 datasource configurée automatiquement
👉 dashboards chargés
👉 alertes présentes

---

# Analyse

---

## Question 1

Pourquoi Docker Compose est indispensable dans un projet IoT ?

---

## Question 2

Quel est l’intérêt du provisioning Grafana ?

---

## Question 3

Pourquoi automatiser toute l’infrastructure ?

---

# Résultat attendu

---

✔ plateforme déployée en 1 commande
✔ aucune configuration manuelle
✔ dashboards disponibles
✔ alertes actives

---

# 🔭 Vision finale

---

```text
ONE COMMAND → FULL IIoT PLATFORM
```

---

