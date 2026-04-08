# Corrigé - TP 02 Setup Edge Gateway (Raspberry Pi)

---

## Compréhension globale

Dans ce TP, nous avons mis en place la couche Edge de notre architecture IoT.

Le Raspberry Pi agit comme une **passerelle (gateway)** entre :

* la couche OT (machines / simulateur OPC-UA)
* la couche IT / Cloud

Il permet de récupérer, traiter et transmettre les données.

---

## Validation des étapes

---

### Installation du système

Le Raspberry Pi OS doit être :

* correctement installé
* accessible
* configuré avec SSH activé

---

### Connexion SSH

La connexion doit fonctionner :

```bash
ssh edge@IP_RASPBERRY
```

👉 Si la connexion réussit, cela signifie que :

* le Raspberry est accessible sur le réseau
* SSH est correctement configuré

---

### Mise à jour système

```bash
sudo apt-get update
```

👉 Permet de :

* sécuriser le système
* éviter des problèmes de dépendances
* préparer l’installation de futurs outils (Docker)

---

## Exercice 1

### Quel est le rôle de l’Edge Gateway ?

L’Edge Gateway sert de pont entre :

* les machines industrielles (OT)
* les systèmes informatiques (IT / Cloud)

Elle permet de :

* collecter les données
* les transformer
* les transmettre

👉 Elle est essentielle dans toute architecture IoT.

---

## Exercice 2

### Pourquoi utiliser un Raspberry Pi ?

Le Raspberry Pi est utilisé car :

* il est peu coûteux
* il consomme peu d’énergie
* il fonctionne sous Linux
* il est facilement déployable

👉 Il est idéal pour simuler un environnement industriel réel.

---

## Exercice 3

### Pourquoi vérifier la connectivité réseau ?

Parce que toute l’architecture repose sur la communication réseau.

Sans réseau :

* le Raspberry ne peut pas accéder au serveur OPC-UA
* aucune donnée ne peut circuler
* le système ne fonctionne pas

👉 C’est l’un des points les plus critiques du projet.

---

## Exercice 4

### Différence entre Raspberry Pi physique et machine virtuelle

| Raspberry Pi réel              | Machine virtuelle             |
| ------------------------------ | ----------------------------- |
| Matériel réel                  | Simulation                    |
| Plus proche du terrain         | Plus simple à mettre en place |
| Accès aux interfaces physiques | Limité                        |
| Meilleure représentativité     | Moins réaliste                |

👉 La VM est utile pour apprendre, mais le Raspberry réel est recommandé.

---

## Vérification réseau

---

### Vérification des IP

Les deux machines doivent être dans le même réseau.

Exemple valide :

* PC : 192.168.0.10
* Raspberry : 192.168.0.25

👉 même réseau → communication possible

---

### Test Ping

```bash
ping IP_PC
```

👉 Permet de vérifier que les machines se voient sur le réseau.

---

### Test OPC-UA (port 4840)

```bash
nc -zv IP_PC 4840
```

👉 Permet de vérifier que :

* le serveur OPC-UA est actif
* le port est accessible

---

## Problèmes courants

---

### 1. SSH ne fonctionne pas

Causes possibles :

* mauvaise IP
* SSH non activé
* Raspberry non connecté au réseau

---

### 2. Ping ne fonctionne pas

Cause :

* firewall Windows

Solution :

```bash
netsh advfirewall firewall add rule name="Allow ICMPv4 Ping" protocol=icmpv4:8,any dir=in action=allow
```

---

### 3. nc ne fonctionne pas

Cause :

* netcat non installé

Solution :

```bash
sudo apt-get install netcat -y
```

---

### 4. Réseaux différents

Exemple :

* PC : 192.168.0.X
* Raspberry : 192.168.1.X

👉 Impossible de communiquer

Solution :

* connecter les deux au même WiFi
* ou vérifier configuration réseau

---

## Vision globale

```text
PC (OPC-UA Server) → Edge Gateway (Raspberry Pi)
```

👉 Le Raspberry récupère les données de la couche OT.

---

## Conclusion

Dans ce TP, nous avons :

* mis en place un Edge Gateway
* validé la connectivité réseau
* préparé l’environnement pour les prochaines étapes

👉 Le système est maintenant prêt pour :

* Docker
* déploiement des services
* pipeline IoT complet

---
