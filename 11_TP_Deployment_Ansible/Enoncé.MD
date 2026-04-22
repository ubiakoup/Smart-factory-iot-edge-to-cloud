#  TP 11 — Déploiement IIoT avec Ansible

---

##  Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Comprendre le rôle d’Ansible dans une architecture DevOps
* Configurer une communication SSH sécurisée
* Définir un inventaire Ansible
* Écrire un playbook de déploiement
* Automatiser entièrement une stack IoT
* Déployer plusieurs machines sans connexion manuelle

---

##  Contexte

Jusqu’ici, vous avez déployé votre architecture IoT :

```text
PLC → OPC UA → MQTT → Node-RED → InfluxDB → Grafana
```

👉 MAIS :

* déploiement manuel ❌
* répétitif ❌
* non scalable ❌

---

## Problème

* connexion manuelle à chaque machine
* erreurs humaines possibles
* difficile à reproduire
* impossible à déployer à grande échelle

---

## Solution

👉 Utiliser **Ansible**

---

##  Principe

```text
1 serveur Ansible → déploie → plusieurs machines
```

---

## Infrastructure

| Machine          | Rôle          | IP            |
| ---------------- | ------------- | ------------- |
| Ansible Server   | Orchestrateur | 192.168.56.10 |
| Edge Gateway     | Stack IoT     | 192.168.56.12 |
| OPC UA Simulator | PLC           | 192.168.56.11 |

---

# Partie 1 — Configuration SSH (OBLIGATOIRE)

---

## Objectif

Permettre à Ansible de se connecter **sans mot de passe**

---

## Étape 1 — Générer une clé SSH

Sur le serveur Ansible :

```bash
ssh-keygen -t rsa -b 4096
```

---

## Étape 2 — Copier la clé sur les machines

### Edge Gateway

```bash
ssh-copy-id vagrant@192.168.56.12
```

### PLC Simulator

```bash
ssh-copy-id vagrant@192.168.56.11
```

---

## Étape 3 — Tester la connexion

```bash
ssh vagrant@192.168.56.12
```

👉 Connexion sans mot de passe attendue

---

# Partie 2 — Inventaire Ansible

---

## Objectif

Déclarer les machines à gérer

---

## Fichier : `hosts.yml`

Créer un inventaire contenant :

* groupe **edge**
* groupe **opcua_plc_simulator**
* IP des machines

---

#  Partie 3 — Test de connectivité

---

## Commande

```bash
ansible all -i hosts.yml -m ping
```

---

## Résultat attendu

```text
SUCCESS
```

---

# Partie 4 — Playbook de déploiement

---

## Objectif

Créer un playbook permettant de :

* préparer les dossiers
* copier les fichiers
* configurer l’environnement
* lancer Docker Compose

---

## Fichier : `deploy.yml`

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

# Partie 5 — Organisation du projet

---

## Objectif

Structurer les fichiers pour Ansible

---

### Arborescence attendue

```bash
Ansible/
├── ansible.cfg
├── hosts.yml
├── deploy.yml
├── vars.yml
│
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

---

# Partie 6 — Déploiement

---

## Commande

```bash
ansible-playbook -i hosts.yml deploy.yml
```

---

## Résultat attendu

👉 Déploiement automatique complet :

* MQTT ✔
* Node-RED ✔
* InfluxDB ✔
* Grafana ✔
* Alerting ✔

---

# Vérifications

---

## Accès aux services

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
* emails reçus ✔

---

# Analyse

---

## Question 1

Pourquoi SSH key est indispensable pour Ansible ?

---

## Question 2

Quel est l’intérêt d’un inventaire ?

---

## Question 3

Pourquoi utiliser un playbook ?

---

## Question 4

Quel est l’avantage d’Ansible par rapport à Docker Compose seul ?

---

#  Résultat attendu

---

* déploiement automatisé ✔
* aucune connexion manuelle ✔
* reproductibilité ✔
* infrastructure scalable ✔

---

#  Vision finale

---

```text
1 commande → déploiement complet → multi-machines
```

---

#  Conclusion

Ansible permet :

👉 d’automatiser entièrement le déploiement
👉 de standardiser les environnements
👉 de passer à l’échelle industrielle

---

