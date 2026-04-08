# TP 02 - Setup Edge Gateway (Raspberry Pi)

---

## Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Installer un système Raspberry Pi OS
* Configurer un Raspberry Pi comme Edge Gateway
* Accéder à distance via SSH
* Vérifier la connectivité réseau avec la couche OT
* Comprendre le rôle de l’Edge Gateway

---

## Contexte

Dans une architecture IoT industrielle, l’Edge Gateway est un composant central.

Elle permet de :

* collecter les données depuis les machines (OT)
* traiter les données localement
* transmettre les données vers le cloud

Dans ce TP, nous allons préparer notre environnement Edge basé sur Raspberry Pi.

---

## Prérequis

* Un ordinateur (Windows, Linux ou macOS)
* Connexion Internet
* (Optionnel) Raspberry Pi + carte microSD
* (Alternative) VirtualBox

---

# Partie 1 — Installation du Raspberry Pi OS

---

## Étape 1 — Télécharger Raspberry Pi Imager

Télécharger :

https://www.raspberrypi.com/software/

---

## Étape 2 — Préparer la carte microSD

* Insérer la carte microSD dans votre PC
* Utiliser un adaptateur si nécessaire

---

## Étape 3 — Flasher l’image

1. Ouvrir Raspberry Pi Imager
2. Choisir :

   * OS : Raspberry Pi OS Lite (recommandé)
   * Storage : carte microSD

---

## Étape 4 — Configuration avancée (TRÈS IMPORTANT)

Avant de flasher, cliquer sur ⚙️ (Advanced Options) :

Configurer :

* Username : `edge`
* Password : `<choisir un mot de passe sécurisé>`
* Activer SSH ✅
* Configurer le WiFi (SSID + Password)

---

## Étape 5 — Flasher

* Lancer le flash
* Attendre la fin

---

# Partie 2 — Démarrage et accès

---

## Étape 6 — Démarrer le Raspberry Pi

* Insérer la carte SD
* Brancher alimentation
* Attendre le démarrage

---

## Étape 7 — Trouver l’adresse IP

---

### Option 1 — Via routeur

* Accéder à votre box Internet
* Voir les appareils connectés

---

### Option 2 — Depuis le PC

#### Windows

```bash
arp -a
```

#### Linux / Mac

```bash
arp -a
```

---

### Option 3 — Advanced IP Scanner (Windows - recommandé)

Télécharger :

https://www.advanced-ip-scanner.com/

---

### Étapes

1. Installer et lancer **Advanced IP Scanner**
2. Cliquer sur **Scan**
3. Identifier le Raspberry Pi

---

### Exemple

```text
192.168.0.25   raspberrypi   Raspberry Pi Foundation
```

---

### Conseil

Débranchez puis rebranchez le Raspberry pour identifier facilement son IP.

---

## Étape 8 — Connexion SSH

```bash
ssh edge@IP_RASPBERRY
```

Exemple :

```bash
ssh edge@192.168.0.25
```

---

## Étape 9 — Mise à jour système

```bash
sudo apt-get update
```

---

# Partie 3 — Vérification réseau (CRITIQUE)

---

## Point important

Votre PC (serveur OPC-UA) et votre Raspberry Pi doivent être dans le **même réseau**.

👉 Sans connectivité réseau, toute l’architecture IoT ne pourra pas fonctionner.
👉 C’est l’un des points les plus critiques du projet.

---

## Vérification des IP

### Sur le PC

#### Windows

```bash
ipconfig
```

#### Linux / Mac

```bash
ifconfig
```

---

### Sur le Raspberry

```bash
ip a
```

---

## Exemple valide

* PC : 192.168.0.10
* Raspberry : 192.168.0.25

👉 même réseau → OK

---

## Exemple invalide

* PC : 192.168.0.10
* Raspberry : 192.168.1.20

👉 réseaux différents → KO

---

## Test de connectivité

### Ping

```bash
ping IP_PC
```

---

### Installation de netcat (si nécessaire)

#### Raspberry / Linux

```bash
sudo apt-get install netcat -y
```

#### macOS

```bash
brew install netcat
```

---

### Test port OPC-UA

```bash
nc -zv IP_PC 4840
```

Exemple :

```bash
nc -zv 192.168.0.141 4840
```

---

## Important (Windows Firewall)

```bash
netsh advfirewall firewall add rule name="Allow ICMPv4 Ping" protocol=icmpv4:8,any dir=in action=allow
```

---

# Partie 4 — Alternative sans Raspberry Pi (VirtualBox)

---

## Important

Utiliser une image basée sur **Raspberry Pi OS Desktop (x86)** pour rester cohérent avec le Raspberry Pi réel.

Télécharger :

https://downloads.raspberrypi.org/rpd_x86/images/

---

## Étape 1 — Installer VirtualBox

https://www.virtualbox.org/

---

## Étape 2 — Créer la machine virtuelle

* RAM : 2 GB minimum
* CPU : 2 cores
* Disque : 20 GB
* Type : Linux

---

## Étape 3 — Configuration réseau (TRÈS IMPORTANT)

Configurer :

👉 **Mode Bridge Adapter**

---

## Étape 4 — Vérification réseau

```bash
ip a
```

---

## Étape 5 — Connexion SSH

```bash
ssh user@IP_VM
```

---

## Limites

* Pas exactement équivalent au Raspberry réel
* Différences réseau possibles
* Pas de matériel physique

---

# Analyse

---

## Exercice 1

Quel est le rôle de l’Edge Gateway ?

---

## Exercice 2

Pourquoi utiliser un Raspberry Pi ?

---

## Exercice 3

Pourquoi vérifier la connectivité réseau ?

---

## Exercice 4

Différence entre Raspberry réel et VM ?

---

# Résultat attendu

* Raspberry accessible en SSH
* Réseau fonctionnel
* Communication validée avec OT

---

# Hints

* SSH ne fonctionne pas → vérifier IP
* Ping échoue → vérifier firewall
* nc échoue → vérifier serveur OPC-UA
* Toujours vérifier le réseau en premier

---

# Vision globale

PC (OPC-UA Server) → Edge Gateway (Raspberry Pi)

👉 Le Raspberry agit comme un pont entre le monde OT et le monde IT.

---

# Conclusion

Ce TP met en place la couche Edge.

Prochaine étape :

* Installation Docker
* Déploiement des services
* Construction de l’architecture IoT complète

---
