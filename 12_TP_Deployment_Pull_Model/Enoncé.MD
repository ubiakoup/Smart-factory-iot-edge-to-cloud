#  TP12 – Restructuration du déploiement et mise en place du Pull Model

---

##  Objectifs

Dans ce TP, vous allez faire évoluer votre architecture afin de :

* Séparer clairement le **provisioning** et le **runtime**
* Comprendre les limites d’un déploiement basé uniquement sur Ansible
* Mettre en place un mécanisme de mise à jour automatique
* Rendre votre Edge **autonome et maintenable**

---

## Contexte

Dans le TP11, vous avez déployé une stack IIoT complète avec :

* Ansible
* Docker Compose
* Node-RED
* InfluxDB
* Grafana

👉 Le système fonctionne correctement.

Cependant, cette architecture présente une limite importante :

```text id="ctx1"
Les mises à jour dépendent d’Ansible
```

Cela signifie que :

* chaque modification nécessite de relancer le playbook
* le système n’est pas autonome
* le déploiement n’est pas adapté à un environnement réel

---

##  Problématique

Dans le TP11, Ansible est utilisé pour :

* configurer le système
* déployer les fichiers
* lancer la stack Docker

👉 On mélange donc deux responsabilités :

```text id="ctx2"
Configuration + Exécution
```

Or, dans une architecture industrielle, ces deux aspects doivent être séparés.

---

##  Objectif du TP

Faire évoluer l’architecture vers le modèle suivant :

```text id="ctx3"
Ansible → provisioning (une seule fois)
Pull Model → runtime (en continu)
```

---

## Rôle d’Ansible

Dans ce TP, Ansible doit être limité à :

* installer les outils nécessaires
* créer les dossiers
* gérer les permissions
* déployer les fichiers
* configurer les secrets

👉 Il ne doit plus gérer l’exécution de la stack.

---

## Principe du Pull Model

Le Pull Model consiste à laisser l’Edge :

* récupérer les mises à jour depuis un dépôt Git
* redéployer automatiquement la stack

👉 Le système devient autonome.

---

#  Partie 1 — Analyse

Réfléchissez au fonctionnement actuel du TP11.

**Questions :**

1. Pourquoi relancer Ansible à chaque modification n’est pas une bonne pratique ?
2. Quelle différence faites-vous entre provisioning et runtime ?
3. Quel est le risque si un seul outil gère tout ?

---

#  Partie 2 — Adaptation du playbook Ansible

Vous allez modifier le fichier `deploy_edge.yml`.

👉 L’objectif est de transformer Ansible en outil de provisioning uniquement.

---

## Travail demandé

### ✔️ Conserver

* préparation du système
* création des dossiers
* gestion des permissions
* déploiement des fichiers
* configuration des secrets

---

### ❌ Supprimer

* toute action liée à l’exécution de la stack
* toute commande lançant ou redéployant les containers

---

### ➕ Ajouter

* le déploiement du script de Pull Model
* la création du service systemd
* l’activation automatique de ce service

---

## 🧩 Résultat attendu

Après modification :

```text id="ctx4"
Ansible prépare uniquement l’environnement
```

et :

```text id="ctx5"
Le runtime est géré par le Pull Model
```

---

# 🔄 Partie 3 — Mise en place du Pull Model

Vous allez créer un script permettant à l’Edge de se mettre à jour automatiquement.

Ce script doit :

* se positionner dans le dossier du projet
* récupérer les dernières modifications depuis Git
* redéployer la stack Docker

👉 Ce script sera ensuite exécuté automatiquement.

---

#  Partie 4 — Automatisation avec systemd

Afin d’automatiser les mises à jour, vous allez :

* créer un service systemd
* exécuter le script de manière régulière
* assurer le redémarrage automatique en cas d’erreur

👉 Le système devient totalement autonome.

---

# Partie 5 — Vérification

Vérifiez que :

* le service systemd est actif
* le script s’exécute correctement
* la stack est mise à jour automatiquement

---

##  Point important

Toutes les opérations doivent être réalisées dans :

```bash id="ctx6"
/home/vagrant/edge-stack
```

👉 Ce répertoire est la **source de vérité** du projet.

---

#  Analyse finale

1. Pourquoi le Pull Model ne remplace-t-il pas Ansible ?
2. Pourquoi séparer provisioning et runtime ?
3. Quel est l’intérêt d’utiliser systemd ?
4. Pourquoi utiliser un seul répertoire projet ?

---

# ✅ Résultat attendu

À la fin du TP, vous devez obtenir :

* un Edge autonome
* une mise à jour automatique
* une architecture claire et maintenable
* une séparation propre des responsabilités

---

# 🚀 Conclusion

Vous avez transformé une stack fonctionnelle en un système :

```text id="ctx7"
✔ autonome
✔ évolutif
✔ maintenable
```
