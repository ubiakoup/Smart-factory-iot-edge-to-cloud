# TP 08 — Grafana : Monitoring & Visualisation des données IoT

---

## Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Comprendre le rôle de Grafana dans une architecture IoT
* Déployer Grafana avec Docker
* Connecter Grafana à InfluxDB
* Comprendre les requêtes Flux
* Créer des dashboards temps réel
* Structurer un monitoring industriel
* Mettre en place des alertes simples

---

## Contexte

Dans notre architecture actuelle :

```text
PLC → OPC UA → MQTT → Node-RED → InfluxDB
````

👉 Les données sont maintenant :

* collectées ✔
* transportées ✔
* traitées ✔
* stockées ✔

---

## Problème

👉 Les données ne sont pas encore exploitables visuellement

❌ difficile à interpréter
❌ pas de monitoring
❌ pas d’alertes

---

## Solution

👉 Utiliser **Grafana**

---

## Pourquoi Grafana ?

Grafana permet de :

* visualiser les données en temps réel
* créer des dashboards industriels
* surveiller l’état des systèmes
* détecter des anomalies
* générer des alertes

---

# Partie 1 — Création du volume (IMPORTANT)

---

```bash
docker volume create grafana-storage
```

---

# Partie 2 — Déploiement Grafana

---

```bash
docker run -d \
  --name grafana \
  --network iiot-network \
  -p 3000:3000 \
  -v grafana-storage:/var/lib/grafana \
  --restart unless-stopped \
  grafana/grafana
```

---

## Vérification

```bash
docker ps
```

---

# Partie 3 — Accès à Grafana

---

Ouvrir dans votre navigateur :

```text
http://192.168.56.12:3000
```

---

## Connexion

* Username : admin
* Password : admin

👉 Changer le mot de passe au premier login

---

# Partie 4 — Ajouter InfluxDB comme Data Source

---

## Étapes

1. Aller dans **Connections → Data Sources**
2. Cliquer sur **Add data source**
3. Choisir **InfluxDB**

---

## Configuration

---

### URL

```text
http://influxdb:8086
```

---

👉 Important :

* utiliser le nom du conteneur (réseau Docker)
* ne pas utiliser localhost

---

### Paramètres

* Query Language : Flux
* Organisation : iiot
* Token : (token InfluxDB valide)
* Default Bucket : edge-GW

---

## Sauvegarde

Cliquer sur :

👉 **Save & Test**

---

## Résultat attendu

```text
Data source is working
```

---

# Partie 5 — Création d’un Dashboard

---

## Étapes

1. Aller dans **Dashboards → New Dashboard**
2. Cliquer sur **Add new panel**

---

## Exemple de requête Flux

```flux
from(bucket: "edge-GW")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "plc1_temperature_motor")
  |> aggregateWindow(every: 5s, fn: last)
```

---

## Visualisations possibles

* Time series (recommandé)
* Gauge
* Bar chart

---

# Partie 6 — Compréhension des requêtes

---

Une requête Flux permet de :

* sélectionner une source de données
* filtrer un capteur
* définir une période
* préparer l’affichage

---

# Partie 7 — Introduction à l’alerting

---

## Objectif

👉 Détecter des anomalies automatiquement

---

## Exemple

Créer une alerte si :

```text
température > 80°C
```

---

👉 Grafana peut envoyer des notifications (email, etc.)

---

# Exercice


## Exercice 1 — Dashboard multi-PLC (complet)

Créer un dashboard structuré par systèmes industriels :

---

### 🔧 PLC1 — Motor System

* temperature_motor
* vibration_motor
* motor_current
* motor_speed
* bearing_health

---

### 💧 PLC2 — Hydraulic System

* hydraulic_pressure
* hydraulic_temp
* flow_rate
* oil_level

---

### ⚡ PLC3 — Energy Monitoring

* voltage
* current
* energy
* power_factor

---

## Contraintes

* un panel = une mesure
* utiliser des Time series
* organiser par PLC
* nommer clairement les panels

---

## Export

Exporter le dashboard au format JSON :

1. Dashboard settings
2. JSON Model
3. Copier le contenu ou Exporter.

---

# Résultat attendu

---

* Grafana fonctionnel
* InfluxDB connecté
* dashboards complets
* visualisation temps réel
* export du Dashboard

---

# Hints

---

* vérifier docker ps
* vérifier réseau Docker
* vérifier token InfluxDB
* vérifier bucket
* vérifier requêtes Flux

---

# Vision globale

---

```text
PLC → OPC UA → MQTT → Node-RED → InfluxDB → Grafana
```

---
