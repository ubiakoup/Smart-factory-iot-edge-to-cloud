# TP 06 - Setup Node-RED (Data Processing)

---

## Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Comprendre le rôle de Node-RED dans une architecture IoT
* Déployer Node-RED avec Docker
* Se connecter à MQTT
* Créer un flow de traitement de données
* Visualiser des données en temps réel

---

## Contexte

Dans une architecture IoT :

* les données sont collectées (OPC-UA)
* transportées (MQTT)

👉 Mais elles doivent être :

* transformées
* filtrées
* enrichies

👉 C’est le rôle de **Node-RED**

---

# Introduction à Node-RED

---

## Qu’est-ce que Node-RED ?

Node-RED est un outil de programmation visuelle basé sur des flows.

👉 On connecte des blocs entre eux pour créer des pipelines de données.

---

## Exemple de flow

```text id="c2z8y1"
MQTT → Processing → Output
```

---

## Avantages

* visuel
* rapide
* adapté IoT
* intégration facile

---

# Partie 1 — Lancer Node-RED

---

## Lancer le conteneur

```bash id="v7q1hk"
docker run -d \
  --name node-red \
  --network iiot-network \
  -p 1880:1880 \
  -v node-red-data:/data \
  --restart unless-stopped \
  nodered/node-red
```

---

## Vérifier

```bash id="m1k9a2"
docker ps
```

---

# Partie 2 — Accéder à Node-RED

---

Ouvrir dans le navigateur :

```text id="l5k8s9"
http://localhost:1880
```

---

👉 Interface Node-RED accessible

---

# Partie 3 — Connexion à MQTT

---

## Ajouter un node MQTT IN

1. Drag & Drop : **mqtt in**
2. Configurer :

* Server : `mqtt-broker`
* Port : `1883`

---

## Topic

```text id="t4h2l7"
factory/+/+
```

---

👉 Permet d’écouter toutes les données

---

# Partie 4 — Traitement des données

---

## Ajouter un node debug

Relier :

```text id="g6h3p1"
MQTT IN → DEBUG
```

---

## Résultat

👉 Voir les données en temps réel

---

# Partie 5 — Exemple de flow

---

```text id="k8f4x2"
MQTT → Function → Debug
```

---

## Node Function (optionnel)

Exemple :

```javascript id="z1n3p5"
msg.payload = {
    value: msg.payload,
    timestamp: new Date()
};
return msg;
```

---

👉 Ajoute un timestamp

---

# Partie 6 — Compréhension globale

---

## Flux complet

```text id="r2m8k1"
OPC-UA → Data Collector → MQTT → Node-RED
```

---

# Analyse

---

## Exercice 1

Quel est le rôle de Node-RED ?

---

## Exercice 2

Pourquoi utiliser un outil visuel ?

---

## Exercice 3

Que fait le node MQTT IN ?

---

## Exercice 4

Quel est le rôle du node Function ?

---

# Résultat attendu

* Node-RED accessible
* MQTT connecté
* Données visibles

---

# Hints

* vérifier réseau Docker
* vérifier broker MQTT
* vérifier topic
* vérifier logs

---

# Vision globale

```text id="n5k7r1"
Data → MQTT → Node-RED → Processing
```

---

# Conclusion

Node-RED permet de traiter les données en temps réel.

👉 C’est le cerveau de l’Edge Gateway.

---

## Prochaine étape

👉 Stockage avec InfluxDB

---
