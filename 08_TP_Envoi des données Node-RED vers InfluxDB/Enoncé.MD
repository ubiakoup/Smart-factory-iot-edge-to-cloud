# TP 07 — Envoi des données Node-RED vers InfluxDB

---

## Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Envoyer des données depuis Node-RED vers InfluxDB
* Comprendre le format des données time-series
* Vérifier que les données sont bien stockées

---

## Contexte

Dans l’architecture actuelle :

```text
OPC UA → Data Collector → MQTT → Node-RED → InfluxDB
```

👉 Les données arrivent déjà dans Node-RED.

👉 Il faut maintenant les stocker dans InfluxDB.

---

## Objectif

👉 Connecter Node-RED à InfluxDB

👉 et envoyer les données transformées

---

# Partie 1 — Installer le node InfluxDB

---

Dans Node-RED :

1. Menu → **Manage Palette**
2. Onglet **Install**
3. Installer :

```text id="p9x3a1"
node-red-contrib-influxdb
```

---

# Partie 2 — Mise à jour du flow

---

## Objectif

Ajouter un node permettant d’envoyer les données vers InfluxDB.

---

## Flow attendu

```text id="flow-influx"
MQTT → Function → InfluxDB OUT
```

---

👉 Ajouter un node :

👉 **influxdb out**

---

# Partie 3 — Configuration

---

Configurer le node **influxdb out** :

* URL : `http://influxdb:8086`
* Token : (défini dans .env)
* Organisation : `iiot`
* Bucket : `edge-GW`

---

## Important

👉 Le conteneur Node-RED doit être dans :

```text id="net-check"
iiot-network
```

👉 pour accéder à InfluxDB

---

# Partie 4 — Format des données (IMPORTANT)

---

Le node Function doit envoyer :

```json id="payload-format"
{
  "measurement": "plc1_temperature_motor",
  "value": 45.2,
  "timestamp": 1710000000
}
```

---

👉 Ce format est compatible avec InfluxDB

---

# Partie 5 — Vérification

---

## Aller dans InfluxDB

```text id="influx-ui"
http://192.168.56.12:8086
```

---

## Data Explorer

👉 Vérifier que :

* les mesures apparaissent
* les valeurs évoluent dans le temps

---

# Résultat attendu

* données visibles dans InfluxDB
* flow Node-RED fonctionnel
* pipeline complet

---

# Hints

---

* vérifier token
* vérifier bucket
* vérifier réseau Docker
* vérifier logs Node-RED

---

# Vision architecture finale

---

```text id="arch-final"
PLC → OPC UA → MQTT → Node-RED → InfluxDB
```

---

# Conclusion

Node-RED envoie maintenant les données vers InfluxDB.

👉 Le stockage est opérationnel.

---

## Prochaine étape

👉 Visualisation avec Grafana

---
