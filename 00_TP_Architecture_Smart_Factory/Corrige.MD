# Corrigé - TP 00 Architecture Smart Factory

---

## Compréhension globale

Une architecture IoT industrielle permet de connecter le monde industriel (OT) au monde informatique (IT) afin de collecter, traiter et exploiter les données issues des machines.

L’objectif est de transformer ces données en informations utiles pour améliorer la production, la maintenance et la prise de décision.

---

## Exercice 1 — Analyse de l’architecture

### 1. Combien de couches observe-t-on ?

On observe **3 couches principales** :

* Couche OT
* Couche Edge
* Couche Cloud

---

### 2. Rôle de chaque couche

#### Couche OT (Operational Technology)

Elle représente le monde industriel :

* machines
* capteurs
* automates (PLC)

👉 Rôle : produire les données

---

#### Couche Edge Gateway

Elle agit comme un intermédiaire entre OT et IT.

👉 Rôle :

* collecter les données (OPC-UA)
* transmettre les données (MQTT)
* transformer les données (Node-RED)
* stocker localement (InfluxDB)
* visualiser (Grafana)

---

#### Couche Cloud

👉 Rôle :

* centraliser les données
* analyser les données
* générer des alertes
* exploiter les données à grande échelle

---

## Exercice 2 — Flux de données

### 1. D’où viennent les données ?

Les données proviennent des machines industrielles (PLC) situées dans la couche OT.

---

### 2. Par quelles étapes passent-elles ?

Les données suivent le chemin suivant :

* génération dans les PLC
* exposition via OPC-UA
* collecte par un Data Collector
* transmission via MQTT
* traitement dans Node-RED
* stockage dans InfluxDB
* visualisation dans Grafana
* envoi vers le Cloud

---

### 3. Où sont-elles stockées ?

Les données sont stockées localement dans **InfluxDB** (base de données time-series).

Elles peuvent également être envoyées dans le **cloud** pour stockage long terme.

---

### 4. Où sont-elles visualisées ?

Les données sont visualisées dans **Grafana**, sous forme de dashboards.

---

## Exercice 3 — Identification des technologies

| Technologie | Rôle                                                |
| ----------- | --------------------------------------------------- |
| OPC-UA      | Permet de récupérer les données des machines        |
| MQTT        | Permet de transporter les données de manière légère |
| Node-RED    | Permet de transformer et manipuler les données      |
| InfluxDB    | Permet de stocker les données                       |
| Grafana     | Permet de visualiser les données                    |

---

## Exercice 4 — Réflexion

### 1. Pourquoi ne pas envoyer directement les données vers le cloud ?

Parce que :

* latence réseau
* dépendance à Internet
* surcharge du réseau
* besoin de traitement local

👉 L’Edge permet de filtrer et traiter les données avant envoi.

---

### 2. Rôle d’un système intermédiaire (Edge Gateway)

Il permet de :

* sécuriser les échanges
* traiter les données localement
* réduire la charge réseau
* garantir la continuité même sans Internet

---

### 3. Problèmes sans cette architecture

Sans Edge :

* saturation du réseau
* latence élevée
* perte de données
* dépendance totale au cloud

---

## Bonus — Industrie 4.0 et IT/OT

### 1. Pourquoi l’intégration IT/OT est importante ?

Elle permet de connecter les machines aux systèmes informatiques afin d’exploiter les données.

---

### 2. Autres piliers de l’Industrie 4.0

* IoT industriel
* Big Data
* Cloud Computing
* Intelligence artificielle
* Cybersécurité
* Robotique

---

### 3. Différence entre IT et OT

* OT : machines, capteurs, automates
* IT : logiciels, cloud, applications

---

### 4. Pourquoi l’intégration IT/OT prend de l’ampleur ?

* besoin de digitalisation
* optimisation des processus
* réduction des coûts
* compétitivité

---

### 5. Relation Smart Factory / Industrie 4.0

La Smart Factory est une application concrète de l’Industrie 4.0.

---

### 6. Cas d’usage de l’intégration IT/OT

#### Maintenance prédictive

Anticiper les pannes grâce aux données.

---

#### Monitoring en temps réel

Surveiller les machines en continu.

---

#### Détection d’anomalies

Détecter les comportements anormaux.

---

#### Optimisation énergétique

Réduire la consommation d’énergie.

---

#### Traçabilité

Suivre la production de bout en bout.

---

#### Exploitation cloud / IA

Analyser les données à grande échelle.

---

#### Centralisation multi-sites

Superviser plusieurs usines depuis un seul système.

---

## Conclusion

Ce TP permet de comprendre les bases d’une architecture IoT industrielle.

Il constitue une étape essentielle avant de passer à l’implémentation technique dans les TP suivants.
