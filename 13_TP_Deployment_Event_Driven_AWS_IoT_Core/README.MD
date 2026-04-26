# 🚀 Smart Factory IoT – Edge Deployment (Event-Driven AWS IoT)

## 🎯 Overview

Ce TP implémente une architecture IoT industrielle permettant de déployer automatiquement une stack Edge via un mécanisme **event-driven sécurisé**.

👉 L’objectif est de remplacer un modèle polling (inefficace) par un système :

* autonome
* réactif
* scalable
* sécurisé

---

## 🧱 Architecture

```
GitHub (Code push)
        ↓
GitHub Actions (CI/CD)
        ↓
MQTT Publish (TLS)
        ↓
AWS IoT Core (Broker sécurisé)
        ↓
Edge Device (Subscriber)
        ↓
mqtt_listener.sh
        ↓
deploy.sh
        ↓
Docker Compose Stack
```

---

## ⚙️ Technologies utilisées

* AWS IoT Core (MQTT TLS + certificats X.509)
* GitHub Actions (CI/CD)
* Docker / Docker Compose
* Ansible (provisioning uniquement)
* Linux / systemd
* Bash scripting avancé

---

## 🔄 Évolution de l’architecture

### ❌ Avant (TP12 – Polling)

```
Edge → git pull toutes les 5 min
```

* inefficace
* latence élevée
* consommation inutile

---

### ✅ Après (TP13 – Event-Driven)

```
Git push → MQTT → Edge → Deploy immédiat
```

* instantané
* scalable
* cloud-native

---

## 🧠 Fonctionnement du système

Le Edge écoute un topic MQTT sécurisé :

```
deploy/vagrant-edge-device
```

Lorsqu’un message `update` est reçu :

1. Vérifie si un déploiement est en cours (LOCK)
2. Si oui → marque un update en attente (PENDING)
3. Lance `deploy.sh`
4. Après déploiement :

   * relance si update en attente
   * sinon s’arrête

---

## 🔒 Mécanismes clés

### 🔐 Lock (anti-concurrence)

Empêche plusieurs déploiements simultanés.

### 🧠 Pending (mémoire)

Garantit qu’aucun update n’est perdu.

### 🔁 Coalescing

Permet de converger vers le dernier commit sans déployer chaque version.

### ⏱️ Cooldown

Évite le spam MQTT.

### 🔄 Retry automatique

Reconnexion MQTT en cas de perte réseau.

---

## 🚀 Script principal

👉 `mqtt_listener.sh`

Fonctionnalités :

* écoute MQTT sécurisé (TLS)
* gestion concurrence
* gestion événements
* robustesse production

---

## 🧪 Exemple de comportement

```
Commit A
Commit B
Commit C
```

Résultat :

```
Deploy A
→ Pending détecté
→ Deploy C
```

👉 Optimisation : seuls les états nécessaires sont appliqués.

---

## 🔐 Sécurité

* authentification X.509
* TLS obligatoire (port 8883)
* policy AWS restrictive (topics limités)
* séparation provisioning / runtime

---

## 📦 Déploiement

### 1. Provisioning

```bash
ansible-playbook deploy_edge.yml
```

### 2. Runtime automatique

```bash
systemctl status mqtt_listener.service
```

---

## 🧠 Concepts avancés utilisés

* Event-driven architecture
* Concurrency control
* Idempotent deployment
* Distributed systems design
* GitOps (simplifié)

---

## 🚀 Améliorations possibles

* ACK MQTT (Edge → Cloud)
* versioning dans messages (JSON)
* multi-device orchestration
* monitoring Grafana
* rollback intelligent

---

## 💬 Conclusion

Ce projet démontre une approche réaliste d’un déploiement IoT industriel :

✔ autonome
✔ sécurisé
✔ scalable
✔ maintenable

---

🔥 Niveau : DevOps / IoT Engineering
