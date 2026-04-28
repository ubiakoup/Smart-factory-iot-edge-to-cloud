# TP15 – Traitement temps réel avec AWS IoT, Lambda et SNS

---

#  Objectifs

Dans ce TP, vous allez faire évoluer votre architecture afin de :

* traiter les données IoT en **temps réel**
* introduire une logique métier côté cloud
* déclencher des actions automatiques
* utiliser **AWS Lambda (Python)**
* envoyer des notifications via **SNS**
* construire un système IoT réactif et intelligent

---

#  Contexte (Lien avec TP14)

Dans le TP14, vous avez construit un pipeline :

```text id="ctx1"
Edge → MQTT → AWS IoT → S3
```

👉 Résultat :

* données centralisées ✔
* historisation ✔
* data lake ✔

---

##  Limite

```text id="ctx2"
Les données sont stockées… mais aucune action n’est déclenchée
```

---

## Exemple concret

```text id="ctx3"
Température moteur = 95°C
→ aucune alerte
→ aucun traitement
→ aucun opérateur prévenu
```

---

#  Problématique

```text id="ctx4"
Comment réagir immédiatement à une donnée critique ?
```

---

👉 Dans un environnement industriel :

```text id="ctx5"
Certaines données doivent déclencher des actions en temps réel
```

---

#  Changement de paradigme

---

##  Avant (TP14)

```text id="ctx6"
Stockage des données
```

---

## ✅ Maintenant (TP15)

```text id="ctx7"
Traitement temps réel + réaction automatique
```

---

# Objectif du TP

Mettre en place une architecture :

```text id="ctx8"
Edge → AWS IoT → Lambda → SNS → Notification
```

---

# Architecture cible

```text id="ctx9"
MQTT Broker (Edge)
        ↓
MQTT Bridge
        ↓
AWS IoT Core
        ↓
IoT Rule
        ↓
Lambda (Python)
        ↓
SNS
        ↓
Email / Notification
```

---

#  Concepts introduits

* Event-driven processing
* AWS Lambda (serverless)
* SNS (alerting)
* logique métier cloud
* traitement temps réel

---

#  Point important

```text id="ctx10"
Vous ne stockez plus seulement les données
→ vous les exploitez immédiatement
```

---

#  Partie 1 — Création d’une fonction Lambda

---

## 🎯 Objectif

Créer une fonction capable de :

```text id="ctx11"
recevoir et analyser les données IoT
```

---

## Travail demandé

* créer une fonction Lambda (Python)
* configurer son runtime
* comprendre la structure des événements reçus

---

##  Résultat attendu

```text id="ctx12"
La fonction reçoit les données depuis AWS IoT
```

---

# Partie 2 — Logique métier

---

## 🎯 Objectif

Définir une règle métier permettant de détecter une anomalie.

---

## Exemple

```text id="ctx13"
Si température > seuil → alerte
```

---

## Travail demandé

* extraire les données du message
* analyser la valeur
* définir une condition

---

## Résultat attendu

```text id="ctx14"
La fonction détecte les situations anormales
```

---

#  Partie 3 — SNS (Notification)

---

## 🎯 Objectif

Envoyer une notification automatique.

---

## Travail demandé

* créer un topic SNS
* créer un abonnement (email)
* confirmer la souscription

---

##  Résultat attendu

```text id="ctx15"
Une notification est envoyée en cas d’anomalie
```

---

#  Partie 4 — IoT Rule

---

## 🎯 Objectif

Relier AWS IoT à Lambda.

---

## Travail demandé

* créer une IoT Rule
* écrire une requête SQL
* transmettre les données à Lambda

---

## Résultat attendu

```text id="ctx16"
Chaque message MQTT déclenche Lambda
```

---

#  Partie 5 — Test complet

---

## Scénario attendu

```text id="ctx17"
publish MQTT → AWS IoT → Lambda → SNS → email
```

---

## Travail demandé

* envoyer une valeur normale avec la simulation en mode normal
* envoyer une valeur critique avec la simulation en mode failure ou bearing failure
* observer le comportement

---

##  Résultat attendu

```text id="ctx18"
✔ aucune alerte si valeur normale
✔ alerte envoyée si seuil dépassé
```

---

# Analyse

Répondez aux questions suivantes :

1. Pourquoi Lambda est adaptée au traitement temps réel ?
2. Quelle différence entre TP14 (S3) et TP15 (Lambda) ?
3. Pourquoi utiliser SNS pour les alertes ?
4. Quel est l’intérêt d’un système event-driven ?

---

# Points de vigilance

* format des messages JSON
* permissions IAM
* configuration IoT Rule
* gestion des erreurs

---

# ✅ Résultat attendu

À la fin du TP :

```text id="ctx19"
✔ traitement temps réel
✔ logique métier
✔ alerting automatique
✔ architecture réactive
```

---

#  Conclusion

---

## Avant

```text id="ctx20"
données stockées uniquement
```

---

## Après

```text id="ctx21"
données analysées et exploitées en temps réel
```

---

## Résultat

```text id="ctx22"
✔ système intelligent
✔ réactif
✔ industriel
```

---

#  Transition

```text id="ctx23"
TP16 → analyse avancée (Timestream)
```

---

#  À retenir

```text id="ctx24"
Collecter des données est utile
→ mais réagir à ces données est essentiel
```

---
