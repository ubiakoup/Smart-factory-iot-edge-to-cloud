

##  Intégration GitHub Actions (CI/CD → Edge)

---

### 🎯 Rôle

GitHub Actions permet de transformer un simple :

```text
git push
```

en :

```text
événement MQTT envoyé vers l’Edge
```

👉 C’est le **déclencheur du système event-driven**.

---

## 🔄 Fonctionnement

```text
Git Push
   ↓
GitHub Actions
   ↓
mosquitto_pub (MQTT TLS)
   ↓
AWS IoT Core
   ↓
Edge (mqtt_listener)
```

---

## 🔐 Gestion des secrets

Les certificats ne doivent **jamais être dans le repo**.

👉 Ils sont stockés dans GitHub :

```text
Settings → Environments → Edge_Vagrant_Secrets
```

---

## Secrets utilisés

| Nom              | Description       |
| ---------------- | ----------------- |
| AWS_CERT         | certificat device |
| AWS_PRIVATE_KEY  | clé privée        |
| AWS_CA           | certificat racine |
| AWS_IOT_ENDPOINT | endpoint AWS      |

---

## ⚙️ Workflow final

```yaml
name: Deploy Edge via AWS IoT

on:
  push:
    branches:
      - main

jobs:
  trigger:
    runs-on: ubuntu-latest
    environment: Edge_Vagrant_Secrets 

    steps:

      - name: Install mosquitto
        run: |
          sudo apt-get update
          sudo apt-get install -y mosquitto-clients

      - name: Create cert files
        run: |
          echo "${{ secrets.AWS_CERT }}" > cert.pem
          echo "${{ secrets.AWS_PRIVATE_KEY }}" > private.key
          echo "${{ secrets.AWS_CA }}" > root-CA.crt

      - name: Send MQTT trigger
        run: |
          mosquitto_pub \
            -h "${{ secrets.AWS_IOT_ENDPOINT }}" \
            -p 8883 \
            --cafile root-CA.crt \
            --cert cert.pem \
            --key private.key \
            -t deploy/vagrant-edge-device \
            -m update
```

---

## 🧠 Explication

---

### 1. Déclencheur

```yaml
on:
  push:
    branches:
      - main
```

👉 chaque `git push` déclenche le workflow

---

### 2. Installation mosquitto

```bash
sudo apt-get install -y mosquitto-clients
```

👉 permet d’utiliser :

```text
mosquitto_pub
```

---

### 3. Création des certificats

```bash
echo "${{ secrets.AWS_CERT }}" > cert.pem
```

👉 reconstitue les fichiers TLS à partir des secrets

---

### 4. Envoi MQTT

```bash
mosquitto_pub ...
```

👉 envoie :

```text
message "update"
```

vers :

```text
deploy/vagrant-edge-device
```

---

## 🎯 Résultat final

```text
git push
→ GitHub Actions
→ MQTT message
→ Edge reçoit
→ deploy.sh exécuté
```

---

# 🧠 Pourquoi c’est CRUCIAL

Sans GitHub Actions :

```text
❌ pas d’événement
❌ pas de déclenchement
❌ pas d’event-driven réel
```

---

Avec :

```text
✔ CI/CD connecté à l’Edge
✔ automatisation complète
✔ architecture industrielle
```

---

