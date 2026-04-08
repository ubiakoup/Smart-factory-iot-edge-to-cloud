# Corrigé - TP 06 Node-RED

---

## Étape 1 — Lancement

```bash id="x8f2v1"
docker run -d \
  --name node-red \
  --network iiot-network \
  -p 1880:1880 \
  -v node-red-data:/data \
  nodered/node-red
```

---

## Vérification

```bash id="w4j9s3"
docker ps
```

---

## Accès

```text id="u1p7k3"
http://localhost:1880
```

---

## Étape 2 — MQTT

Configurer :

* Broker : mqtt-broker
* Port : 1883

---

## Topic

```text id="g2n8l4"
factory/+/+
```

---

## Étape 3 — Flow

```text id="p7x2k1"
MQTT IN → DEBUG
```

---

👉 Données visibles en temps réel

---

## Étape 4 — Function node

```javascript id="k3f9z2"
msg.payload = {
    value: msg.payload,
    timestamp: new Date()
};
return msg;
```

---

## Exercice 1

### Rôle Node-RED

* traitement
* transformation
* orchestration

---

## Exercice 2

### Avantage visuel

* rapide
* simple
* intuitif

---

## Exercice 3

### MQTT IN

* reçoit les données

---

## Exercice 4

### Function

* transforme les données

---

## Problèmes fréquents

---

### Pas de données

* vérifier MQTT
* vérifier topic

---

### Node-RED inaccessible

* vérifier port 1880

---

### Connexion échoue

* vérifier réseau Docker

---

## Conclusion

Node-RED fonctionne correctement.

👉 prêt pour :

* InfluxDB
* Grafana

---

## Prochaine étape

👉 Stockage avec InfluxDB

---
