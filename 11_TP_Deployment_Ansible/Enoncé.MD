# 🚀 TP 11 — Déploiement IIoT avec Ansible (Vagrant Edition)

---

## 🎯 Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Comprendre le rôle d’Ansible dans une architecture DevOps
* Configurer une communication SSH dans un environnement Vagrant
* Définir un inventaire Ansible
* Écrire un playbook de déploiement
* Automatiser entièrement une stack IoT
* Déployer plusieurs machines sans connexion manuelle

---

## 🧠 Contexte

Jusqu’ici, vous avez déployé votre architecture IoT :

```text
PLC → OPC UA → MQTT → Node-RED → InfluxDB → Grafana
````

👉 MAIS :

* déploiement manuel ❌
* répétitif ❌
* non scalable ❌

---

## ❌ Problème

Dans un environnement multi-machines :

* connexion manuelle à chaque VM
* erreurs humaines possibles
* difficile à reproduire
* non industrialisable

---

## ✅ Solution

👉 Utiliser **Ansible**

---

## 🧱 Infrastructure

| Machine          | Rôle          | IP            |
| ---------------- | ------------- | ------------- |
| Ansible Server   | Orchestrateur | 192.168.56.10 |
| Edge Gateway     | Stack IoT     | 192.168.56.12 |
| OPC UA Simulator | PLC           | 192.168.56.11 |

---

# ⚠️ IMPORTANT — Spécificité Vagrant

👉 Chaque machine virtuelle Vagrant possède sa propre clé SSH

👉 Donc :

❌ `ssh-copy-id` ne fonctionne pas
❌ connexion SSH classique impossible

---

## ✅ Approche utilisée

👉 Nous allons :

* Utiliser le dossier partagé Vagrant
* Accéder aux clés générées automatiquement
* Les utiliser depuis la machine Ansible

---

# 📁 Partie 1 — Accès aux clés Vagrant

---

## ⚠️ IMPORTANT — Accès au dossier `.vagrant`

Le dossier `.vagrant` est généré automatiquement par Vagrant.

---

## ❌ Mauvaise pratique

Ne pas utiliser directement :

```text
./.vagrant
```

👉 Pourquoi ?

* dépend du système host (Windows / Linux)
* non portable
* source d’erreurs

---

## ✅ Bonne pratique

Utiliser le dossier partagé Projects et creer un dossier vagrant puis y copier le dossier .vagrant

```text
/vagrant/.vagrant
```

👉 Ce chemin est :

* accessible depuis la VM Ansible
* stable
* identique pour tous

---

## 🧠 À retenir

```text
Host (Windows) → 11_TP_Deployment_Ansible\vagrant\.vagrant
VM (Linux) → Projects/vagrant/.vagrant
```

---

# 🔐 Partie 2 — Configuration SSH (VM Ansible)

---

## 🎯 Objectif

Permettre à Ansible de se connecter aux machines

---

## Étape 1 — Copier les clés

Sur la VM Ansible :

```bash
cp /vagrant/.vagrant/machines/iot-edge/virtualbox/private_key ~/.ssh/edge_key

cp /vagrant/.vagrant/machines/iot-opcua-plc-simulator/virtualbox/private_key ~/.ssh/opcua_plc_simulator_key
```

---

## Étape 2 — Corriger les permissions (CRITIQUE)

```bash
chmod 600 ~/.ssh/edge_key
chmod 600 ~/.ssh/opcua_plc_simulator_key
```

👉 Sinon erreur :

```text
UNPROTECTED PRIVATE KEY FILE
```

---

## Étape 3 — Tester SSH

```bash
ssh -i ~/.ssh/edge_key vagrant@192.168.56.12

ssh -i ~/.ssh/opcua_plc_simulator_key vagrant@192.168.56.11
```

👉 Connexion attendue sans erreur

---

# 🧾 Partie 3 — Inventaire Ansible

---

Créer le fichier `hosts.yml` :

```yaml
---
all:
  vars:
    ansible_user: vagrant
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no'

  children:
    edge:
      hosts:
        client1:
          ansible_host: 192.168.56.12
          ansible_ssh_private_key_file: /home/vagrant/.ssh/edge_key

    opcua_plc_simulator:
      hosts:
        client2:
          ansible_host: 192.168.56.11
          ansible_ssh_private_key_file: /home/vagrant/.ssh/opcua_plc_simulator_key
```

---

# 🔍 Partie 4 — Test de connectivité

---

```bash
ansible all -i hosts.yml -m ping
```

---

## ✅ Résultat attendu

```text
client1 | SUCCESS
client2 | SUCCESS
```

---

# 🚀 Partie 5 — Playbook de déploiement

---

## 🎯 Objectif

Créer un playbook permettant de :

* préparer les dossiers
* copier les fichiers
* configurer l’environnement
* lancer Docker Compose

---

## Contraintes

Le playbook doit :

* s’exécuter sur le groupe **edge**
* utiliser `become: true`
* créer les dossiers nécessaires
* copier les fichiers du projet
* déployer `.env`
* gérer les permissions (Node-RED, Grafana, InfluxDB)
* lancer :

```bash
docker compose up -d --build
```

---

# 📁 Partie 6 — Organisation du projet

---

```bash
Ansible/
├── ansible.cfg
├── hosts.yml
├── deploy_edge.yml
├── deploy_opcua_plc_simulator.yml
├── vars.yml
│
├── group_vars/
│   ├── edge.yml
│
├── opcua-plc-simulator/
│   ├── opcua_plc_simulation.py
│   ├── requirements.txt
|
├── templates/
│   ├── .env.j2
|
|
├── files/
│   ├── docker-compose.yml
│   ├── config.yml
│   ├── data_collector.py
│   ├── Dockerfile
│   ├── requirements.txt
│   │
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   │
│   ├── node-red/
│   │   └── flows.json
│   │
│   └── secrets/
│       └── influx_token.txt
```
## installer posix sur le serveur Ansible
```bash
ansible-galaxy collection install ansible.posix
```
---

# 🚀 Partie 7 — Déploiement 

## Déploiement sur L'edge
---

```bash
ansible-playbook -i hosts.yml deploy_edge.yml
```

---
## Déploiement sur le Simulateur(opcua-plc-simulator)

---

```bash
ansible-playbook -i hosts.yml deploy_opcua_plc_simulator.yml
```

---


## 🎯 Résultat attendu

👉 Déploiement automatique complet :

* MQTT ✔
* Node-RED ✔
* InfluxDB ✔
* Grafana ✔
* Alerting ✔

---

# 🔍 Vérifications

---

| Service  | URL                                                    |
| -------- | ------------------------------------------------------ |
| Node-RED | [http://192.168.56.12:1880](http://192.168.56.12:1880) |
| InfluxDB | [http://192.168.56.12:8086](http://192.168.56.12:8086) |
| Grafana  | [http://192.168.56.12:3000](http://192.168.56.12:3000) |

---

## Attendu

* données visibles ✔
* dashboards chargés ✔
* alertes actives ✔

---

# 🧠 Analyse

---

## Question 1

Pourquoi les clés SSH sont indispensables avec Ansible ?

---

## Question 2

Pourquoi `ssh-copy-id` ne fonctionne pas avec Vagrant ?

---

## Question 3

Quel est l’intérêt d’un inventaire ?

---

## Question 4

Pourquoi utiliser un playbook ?

---

## Question 5

Quel est l’avantage d’Ansible par rapport à Docker Compose seul ?

---

# 🏁 Résultat final

---

* déploiement automatisé ✔
* aucune connexion manuelle ✔
* reproductibilité ✔
* infrastructure scalable ✔

---

# 🔭 Vision finale

---

```text
1 commande → déploiement complet → multi-machines
```

---

# 🏁 Conclusion

Ansible permet :

👉 d’automatiser entièrement le déploiement
👉 de standardiser les environnements
👉 de passer à l’échelle industrielle

---
