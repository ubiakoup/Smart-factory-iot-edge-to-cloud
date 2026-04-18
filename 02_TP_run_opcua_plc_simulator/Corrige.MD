# Corrigé - TP 01 Setup OT et simulation OPC-UA

---

## Compréhension globale

Dans ce TP, nous avons mis en place un environnement permettant de simuler une couche OT (Operational Technology).

Cette couche représente les machines industrielles (PLC) qui produisent des données.

Grâce à Python et au protocole OPC-UA, nous avons pu simuler ces machines et exposer leurs données.

---

## Vérification de l’environnement

Si toutes les étapes ont été correctement suivies :

* Python est installé
* Un environnement virtuel est actif
* Les dépendances sont installées
* Le script OPC-UA se lance sans erreur

---

## Exercice 1

### Pourquoi utilise-t-on un environnement virtuel ?

Un environnement virtuel permet de :

* isoler les dépendances d’un projet
* éviter les conflits entre versions de librairies
* ne pas impacter le système global

👉 Cela garantit que le projet reste reproductible et stable.

---

## Exercice 2

### Quel est le rôle de la bibliothèque OPC-UA ?

La bibliothèque OPC-UA permet de :

* créer un serveur OPC-UA
* exposer des données industrielles
* simuler un automate industriel (PLC)

👉 Elle joue un rôle clé dans la communication entre les machines et les systèmes informatiques.

---

## Exercice 3

### Que représente le simulateur PLC ?

Le simulateur PLC représente :

* une machine industrielle
* un automate réel

Il génère des données telles que :

* température
* vibration
* courant
* pression

👉 Ces données seront utilisées dans les prochains TP.

---

## Exercice 4

### Pourquoi simuler un environnement OT ?

Dans un contexte réel :

* les machines industrielles sont coûteuses
* elles ne sont pas toujours accessibles
* elles peuvent être dangereuses

👉 La simulation permet :

* de reproduire un environnement réel
* de tester sans risque
* d’apprendre plus facilement

---

## Compréhension du fonctionnement

Le script Python :

1. génère des données (simulation machine)
2. crée un serveur OPC-UA
3. expose les données
4. permet à d’autres systèmes de les lire

👉 Il constitue la source de données de toute l’architecture.

---

## Point important

Lors de l’exécution du script, il est possible de voir le message :

```text
cryptography is not installed, use of crypto disabled
```

👉 Cela signifie que la bibliothèque `cryptography` n’est pas installée.

Dans ce cas :

```bash
python -m pip install cryptography
```

👉 Cette bibliothèque permet d’activer la sécurité (TLS).

---

## Conclusion

Ce TP met en place la première brique du système :

👉 la génération de données industrielles

Ces données seront ensuite :

* collectées
* transportées
* stockées
* visualisées

dans les prochains TP.

---
