

#  NOTICE DE DEBUG — EDGE IoT (MQTT + AWS + systemd)

---

#  1. Vérifier le service systemd

```bash
systemctl status mqtt_listener.service
```

👉 **But :**

* vérifier si le service est actif
* voir les processus liés
* détecter redémarrages ou crash

---

```bash
journalctl -u mqtt_listener.service -f
```

👉 **But :**

* suivre les logs en temps réel
* voir si le message MQTT est reçu
* vérifier le déclenchement du deploy

---

```bash
sudo systemctl restart mqtt_listener.service
```

👉 **But :**

* appliquer les modifications du script
* redémarrer proprement le service

---

```bash
sudo systemctl daemon-reload
```

👉 **But :**

* recharger config systemd après modification du service

---

#  2. Vérifier les processus Linux

```bash
ps aux | grep mqtt
```

👉 **But :**

* détecter les processus en double
* vérifier si mosquitto_sub tourne

---

```bash
pkill -f mqtt_listener.sh
pkill -f mosquitto_sub
```

👉 **But :**

* tuer les anciens processus zombies
* éviter duplication

---

```bash
pstree -p
```

👉 **But :**

* visualiser l’arbre des processus
* comprendre parent / enfant (bash, subshell, mqtt)

---

#  3. Tester MQTT (connexion & réception)

```bash
mosquitto_sub \
  -h <endpoint> \
  -p 8883 \
  --cafile root-CA.crt \
  --cert device.cert.pem \
  --key private.key \
  -t deploy/vagrant-edge-device \
  -d
```

👉 **But :**

* tester la connexion TLS à AWS IoT
* vérifier SUBACK (autorisation)
* voir les messages reçus

---

```bash
mosquitto_pub \
  -h <endpoint> \
  -p 8883 \
  --cafile root-CA.crt \
  --cert device.cert.pem \
  --key private.key \
  -t deploy/vagrant-edge-device \
  -m "update"
```

👉 **But :**

* tester l’envoi d’un message MQTT
* valider le pipeline complet

---

#  4. Tester AWS IoT (console)

👉 MQTT Test Client :

* Topic :

```text
deploy/vagrant-edge-device
```

* Message :

```text
update
```

👉 **But :**

* vérifier que AWS envoie bien le message
* tester sans GitHub Actions

---

#  5. Vérifier les permissions AWS IoT
---

```markdown
⚠️ Recommandation :
Toujours commencer avec une policy permissive pour le debugging,
puis restreindre progressivement vers une policy minimale sécurisée.
```
---
👉 Policy minimale :

```json
{
  "Effect": "Allow",
  "Action": "iot:*",
  "Resource": "*"
}
```
👉 **But :**

* éliminer les erreurs de permission
* tester rapidement sans blocage

ou encore
👉 Policy stricte:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Subscribe",
      "Resource": "arn:aws:iot:*:*:topicfilter/deploy/vagrant-edge-device"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Receive",
      "Resource": "arn:aws:iot:*:*:topic/deploy/vagrant-edge-device"
    }
    
  ]
}
```
👉 **But :**

* principe du least privilege
* sécuriser l’accès au strict nécessaire
* limiter l’exposition du device

---

#  6. Vérifier les logs applicatifs

```bash
tail -f /home/vagrant/mqtt_listener.log

journalctl -u mqtt_listener.service -f
```

👉 **But :**

* voir les messages MQTT reçus
* vérifier le déclenchement du deploy

---

```bash
tail -f /home/vagrant/deploy.log
```

👉 **But :**

* suivre l’exécution du déploiement
* détecter erreurs Docker / Git

---

# 🐳 7. Vérifier Docker

```bash
docker ps
```

👉 **But :**

* vérifier que les containers tournent

---

```bash
docker compose logs -f
```

👉 **But :**

* debug runtime (Node-RED, collector, etc.)

---

```bash
docker image prune -f
```

👉 **But :**

* nettoyer les images inutiles

---

# 🌿 8. Vérifier Git (déploiement)

```bash
git pull origin main
```

👉 **But :**

* récupérer la dernière version

---

```bash
git rev-parse HEAD
```

👉 **But :**

* vérifier le commit actuel

---

```bash
git reset --hard <commit>
```

👉 **But :**

* rollback en cas d’échec

---

# ⚙️ 9. Vérifier ressources système

```bash
free -h
```

👉 **But :**

* vérifier RAM disponible

---

```bash
top
```

👉 **But :**

* voir CPU / processus actifs

---

```bash
dmesg -T | grep -i error
```

👉 **But :**

* détecter erreurs kernel (OOM, crash)

---

# 🧪 10. Tester le script manuellement

```bash
bash /home/vagrant/mqtt_listener.sh
```

👉 **But :**

* isoler problème systemd vs script

---

```bash
bash /home/vagrant/deploy.sh
```

👉 **But :**

* tester le déploiement indépendamment

---

# 🧠 11. Vérifications critiques à retenir

| Vérification        | Pourquoi                         |
| ------------------- | -------------------------------- |
| Topic MQTT exact    | MQTT ne tolère aucune erreur     |
| Message = `update`  | script filtre strict             |
| Certificat attaché  | sinon aucun message              |
| Policy AWS correcte | sinon SUBACK mais pas de message |
| Service actif       | sinon rien ne tourne             |
| Logs                | seule source de vérité           |

---

# 🚀 🧾 Résumé du workflow complet

```text
Git push
   ↓
GitHub Actions
   ↓
AWS IoT (MQTT)
   ↓
mqtt_listener.sh
   ↓
deploy.sh
   ↓
Docker update
```

---

# 🔥 Conclusion

👉 Avec ces commandes tu peux debug :

* MQTT
* AWS IoT
* systemd
* Bash
* Docker
* Git

👉 et diagnostiquer n’importe quel problème en **quelques minutes**

