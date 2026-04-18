# TP 01 - Setup de l’environnement OT et simulation OPC-UA

---

## Objectifs pédagogiques

À la fin de ce TP, vous serez capable de :

* Installer un environnement Python propre
* Créer et utiliser un environnement virtuel
* Installer des dépendances Python
* Comprendre le rôle d’un serveur OPC-UA
* Lancer un simulateur de PLC

---

## Contexte

Dans une architecture IoT industrielle, la couche OT (Operational Technology) représente les machines et les capteurs.

Dans un environnement réel, ces machines sont des automates industriels (PLC).

Dans ce TP, nous allons simuler ces automates à l’aide d’un programme Python qui expose des données via le protocole OPC-UA.

---

## Installation de Python (si nécessaire)

Si Python n’est pas installé sur votre machine, suivez les instructions ci-dessous.

---

### Sur Windows (méthode recommandée)

1. Ouvrir le Microsoft Store
2. Rechercher **Python 3**
3. Installer la version proposée (ex : Python 3.11 ou plus)

---

### Alternative via PowerShell (Windows)

```bash
winget install Python.Python.3
```

---

### Vérification de l’installation

```bash
python --version
```

> Si la commande `python` ne fonctionne pas, essayez avec `py`

---

### Sur Linux

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

### Sur macOS

```bash
brew install python
```

---

## Instructions

---

### 1. Vérification de Python

```bash
python --version
```

---

### 2. Vérification de pip

```bash
python -m pip --version
```

---

### 3. Création d’un environnement virtuel

```bash
python -m venv venv
```

---

### 4. Activation de l’environnement virtuel

#### Windows

```bash
.\venv\Scripts\Activate.ps1
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

### 5. Installation des dépendances

```bash
python -m pip install --upgrade pip
python -m pip install opcua cryptography
```

---

### 6. Vérification des installations

```bash
python -m pip list
```

---

### 7. Lancement du simulateur PLC

Un script Python est fourni dans le projet.

```bash
python opcua_plc_simulation.py
```

---

## Analyse

Répondez aux questions suivantes :

---

### Exercice 1

Pourquoi utilise-t-on un environnement virtuel ?

---

### Exercice 2

Quel est le rôle de la bibliothèque OPC-UA dans ce projet ?

---

### Exercice 3

Que représente le simulateur PLC dans l’architecture globale ?

---

### Exercice 4

Pourquoi simuler un environnement OT plutôt que d’utiliser de vraies machines ?

---

## Résultat attendu

À la fin de ce TP :

* L’environnement Python est correctement configuré
* Le simulateur OPC-UA fonctionne
* Vous comprenez le rôle de la couche OT

---

## Bonnes pratiques

* Toujours utiliser un environnement virtuel
* Installer les dépendances avec `python -m pip`
* Ne jamais installer les dépendances globalement

---

## Note importante

Si une erreur liée à `pip` ou à l’environnement virtuel apparaît, il est recommandé de supprimer et recréer l’environnement virtuel.

---
