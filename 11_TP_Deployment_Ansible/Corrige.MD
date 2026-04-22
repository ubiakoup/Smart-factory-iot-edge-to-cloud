# Corrigé — TP 10 Ansible (Déploiement IIoT)

---

#  1. Configuration SSH (solution attendue)

---

## Génération de clé

```bash
ssh-keygen -t rsa -b 4096
```

---

## Copie vers les machines

```bash
ssh-copy-id vagrant@192.168.56.12
ssh-copy-id vagrant@192.168.56.11
```

---

## Vérification

```bash
ssh vagrant@192.168.56.12
```

✔ Connexion sans mot de passe

---

#  2. Inventory — `hosts.yml`

---

## Solution correcte

```yaml
all:
  vars:
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no'

edge:
  hosts:
    client:
      ansible_host: 192.168.56.12

opcua_plc_simulator:
  hosts:
    client:
      ansible_host: 192.168.56.11
```

---

## Points importants

* séparation par groupes ✔
* IP définies ✔
* SSH simplifié ✔

---

# 3. Test Ansible

---

```bash
ansible all -i hosts.yml -m ping
```

---

## Résultat attendu

```text
SUCCESS
```

---

#  4. Playbook — `deploy.yml`

---

## Solution complète

```yaml
- name: deploy Edge-Gateway services
  hosts: edge
  become: true
  vars_files:
    - vars.yml

  pre_tasks:
    - name: Install docker compose plugin
      apt:
        name: docker-compose-plugin
        state: present
        update_cache: yes

  tasks:

    - name: Ensure directories exist
      file:
        path: "{{ item }}"
        state: directory
      loop:
        - /home/edge/edge-stack
        - /home/edge/data/node-red
        - /home/edge/edge-stack/secrets

    - name: Fix Node-RED permissions
      file:
        path: /home/edge/data/node-red
        owner: 1000
        group: 1000
        recurse: yes

    - name: Fix InfluxDB permissions
      file:
        path: /home/edge/data/influxdb
        owner: 1000
        group: 1000
        recurse: yes

    - name: Fix Grafana permissions
      file:
        path: /home/edge/data/grafana
        owner: 472
        group: 472
        recurse: yes

    - name: Copy edge gateway stack
      synchronize:
        src: ./files/
        dest: /home/edge/edge-stack/
        rsync_opts:
          - "--exclude=.env"
          - "--exclude=secrets"

    - name: Remove influx_token if exists
      file:
        path: /home/edge/edge-stack/secrets/influx_token.txt
        state: absent

    - name: Copy secrets
      copy:
        src: ./files/secrets/influx_token.txt
        dest: /home/edge/edge-stack/secrets/influx_token.txt
        owner: root
        group: root
        mode: '0444'

    - name: Deploy .env file
      template:
        src: .env.j2
        dest: /home/edge/edge-stack/.env
        mode: '0400'

    - name: Copy Node-RED flow if not exists
      copy:
        src: ./files/node-red/flows.json
        dest: /home/edge/data/node-red/flows.json
        owner: 1000
        group: 1000
        mode: '0644'
        force: no

    - name: Run docker compose
      command: docker compose up -d --build
      args:
        chdir: /home/edge/edge-stack
```

---

#  5. Explication rapide (essentiel uniquement)

---

### `pre_tasks`

👉 installe Docker Compose automatiquement

---

###  `file`

👉 crée dossiers + fixe permissions
👉 critique pour :

* Node-RED (UID 1000)
* Grafana (UID 472)

---

### `synchronize`

👉 copie rapide du projet (rsync)
👉 évite copier `.env` et secrets

---

### `template`

👉 génère `.env` dynamiquement

---

### `copy`

👉 injecte :

* secrets sécurisés
* flow Node-RED

---

### `command`

```bash
docker compose up -d --build
```

👉 lance toute la stack automatiquement

---

# 6. Déploiement final

---

```bash
ansible-playbook -i hosts.yml deploy.yml
```

---

#  7. Résultat attendu

---

✔ Stack complète lancée
✔ Aucun SSH manuel
✔ Services opérationnels

---

#  8. Vérification

---

```bash
docker ps
```

---

## Accès

* Node-RED → [http://192.168.56.12:1880](http://192.168.56.12:1880)
* InfluxDB → [http://192.168.56.12:8086](http://192.168.56.12:8086)
* Grafana → [http://192.168.56.12:3000](http://192.168.56.12:3000)

---

# 9. Erreurs fréquentes

---

###  SSH ne fonctionne pas

👉 refaire :

```bash
ssh-copy-id
```

---

### Permissions Grafana

👉 UID doit être :

```text
472
```

---

###  Node-RED vide

👉 vérifier :

```bash
flows.json
```

---

###  InfluxDB erreur

👉 vérifier :

* token
* volume

---

# 10. Réponses attendues (Analyse)

---

### Question 1

👉 SSH key = connexion automatique sécurisée

---

### Question 2

👉 Inventory = liste des machines

---

### Question 3

👉 Playbook = automatisation des tâches

---

### Question 4

👉 Ansible > Docker Compose

| Docker Compose | Ansible        |
| -------------- | -------------- |
| local          | multi-machines |
| manuel         | automatisé     |
| limité         | scalable       |

---
