# TP12 – Corrigé final : Restructuration du déploiement & Pull Model

---

#  Objectif du TP

Transformer une architecture couplée :

```text
Ansible → configure + déploie + exécute
```

en une architecture découplée :

```text
Ansible → provisioning (1 fois)
Pull Model → runtime (continu)
```

👉 L’objectif est de **séparer clairement les responsabilités**.

---

# 🧠 Partie 1 — Analyse

---

## Pourquoi relancer Ansible à chaque modification est une mauvaise pratique ?

* dépendance à un outil externe
* manque d’autonomie de l’Edge
* mises à jour lourdes
* difficilement scalable

👉 En industrie, un Edge doit être **autonome**.

---

## Provisioning vs Runtime

| Concept      | Rôle                                            |
| ------------ | ----------------------------------------------- |
| Provisioning | Préparer le système (install, dossiers, config) |
| Runtime      | Exécuter et mettre à jour les applications      |

👉 Mélanger les deux rend le système fragile.

---

## Risques d’un système non séparé

* couplage fort
* erreurs de déploiement
* écrasement de configuration
* maintenance complexe

---

#  Partie 2 — Adaptation du playbook Ansible

---

## Principe

👉 Ansible :

```text
✔ prépare la machine
✔ clone le projet
✔ installe le mécanisme de mise à jour
```

👉 MAIS :

```text
❌ ne gère plus le runtime au quotidien
```

---

## Playbook corrigé

```yaml
---
- name: "deploy Edge-Gateway services"
  hosts: edge
  become: true
  vars_files:
    - vars.yml

  pre_tasks:
    - name: Install docker compose plugin
      ansible.builtin.apt:
        name: docker-compose-plugin
        state: present
        update_cache: yes

  tasks:

    # Directories
    - name: Ensure directories exist
      file:
        path: "{{ item }}"
        state: directory
      loop:
        - /home/vagrant/edge-stack
        - /home/vagrant/edge-stack/secrets
        - /home/vagrant/data/influxdb
        - /home/vagrant/data/grafana

    # Permissions
    - name: Fix InfluxDB permissions
      file:
        path: /home/vagrant/data/influxdb
        owner: 1000
        group: 1000
        recurse: yes

    - name: Fix Grafana permissions
      file:
        path: /home/vagrant/data/grafana
        owner: 472
        group: 472
        recurse: yes

    # Clone project
    - name: Clone project repository
      git:
        repo: "{{ git_repo_url }}"
        dest: /home/vagrant/edge-stack
        version: main
        force: yes

    # Secrets
    - name: Copy secrets
      copy:
        src: ./files/secrets/influx_token.txt
        dest: /home/vagrant/edge-stack/secrets/influx_token.txt
        owner: root
        group: root
        mode: '0444'

    # ENV
    - name: Deploy .env file
      template:
        src: .env.j2
        dest: /home/vagrant/edge-stack/.env
        mode: '0400'

    # Pull script
    - name: Deploy pull-update script
      copy:
        src: ./files/pull-update.sh
        dest: /home/vagrant/pull-update.sh
        owner: vagrant
        group: vagrant
        mode: '0755'

    # systemd service
    - name: Deploy systemd service
      copy:
        src: ./files/iiot-pull.service
        dest: /etc/systemd/system/iiot-pull.service

    - name: Reload systemd
      command: systemctl daemon-reload

    - name: Enable pull service
      systemd:
        name: iiot-pull.service
        enabled: yes

    - name: Start pull service
      systemd:
        name: iiot-pull.service
        state: started

    # First deployment (IMPORTANT)
    - name: Initial docker compose up
      command: docker compose up -d --build
      args:
        chdir: /home/vagrant/edge-stack
```

---

##  À retenir

```text
Ansible prépare ET lance une première fois
Puis le Pull Model prend le relais
```

---

#  Partie 3 — Script Pull Model

---

## Script corrigé

```bash
#!/bin/bash

PROJECT_DIR="/home/vagrant/edge-stack"

echo "📁 Moving to project directory..."
cd $PROJECT_DIR || exit 1

echo "🔄 Pull latest version..."
git pull origin main || exit 1

echo "🚀 Re-deploying stack..."
docker compose up -d --build

echo "🧹 Cleanup (safe)..."
docker image prune -f

echo "✅ Update done"
```

---

## Explication

* `cd` → bon contexte
* `git pull` → récupération des changements
* `docker compose up` :

  * recrée uniquement les conteneurs modifiés
  * évite les doublons
  * conserve les volumes
* `prune` → nettoyage des images inutilisées

---

#  Partie 4 — Service systemd

---

## Service

```ini
[Unit]
Description=IIoT Pull Model Service
After=network.target

[Service]
User=vagrant
WorkingDirectory=/home/vagrant/edge-stack
ExecStart=/home/vagrant/pull-update.sh
Restart=always
RestartSec=300

[Install]
WantedBy=multi-user.target
```

---

## Explication

* `Restart=always` → relance après chaque exécution
* `RestartSec=300` → attente entre deux exécutions
* `WorkingDirectory` → cohérence du contexte

👉 Le script est exécuté en boucle contrôlée.

---

#  Partie 5 — Vérification

```bash
systemctl status iiot-pull.service
```

---

## Attendu

* service actif
* pas d’erreurs
* logs cohérents

---

# ⚠️ Erreurs fréquentes

---

## ❌ Garder Docker dans Ansible

👉 casse la séparation des rôles

---

## ❌ Mauvaise structure Git

👉 repo non exécutable directement

---

## ❌ Script exécuté au mauvais endroit

👉 `docker compose` échoue

---

## ❌ Mauvaise gestion des permissions

👉 script non exécuté

---

#  Bonne pratique

```text
Ne jamais stocker :
- .env
- tokens
- secrets
dans le repo Git
```

👉 Les secrets doivent rester côté Ansible.

---

# Conclusion pédagogique

---

## Avant

```text
Ansible fait tout
```

---

## Après

```text
Ansible → provisioning initial
Pull Model → mise à jour continue
```

---

## Résultat

* Edge autonome
* mises à jour automatiques
* architecture maintenable
* approche industrielle réaliste

---

#  Point clé

👉 Le Pull Model :

```text
✔ ne remplace pas Ansible
✔ ne configure pas la machine
✔ gère uniquement le runtime
```

---

