# OPC UA Industrial Simulator – Smart Factory

---

## Présentation du projet

Ce projet implémente un simulateur industriel basé sur le protocole OPC UA.

Il permet de reproduire le comportement de plusieurs automates industriels (PLC) générant des données en temps réel.

Le simulateur est conçu pour être utilisé dans des architectures IIoT (Industrial Internet of Things), notamment pour :

* le monitoring industriel
* la maintenance prédictive
* les tests d’architectures Edge / Cloud

---

## Architecture du simulateur

Le système simule trois PLC industriels :

| PLC  | Système simulé    |
| ---- | ----------------- |
| PLC1 | Motor System      |
| PLC2 | Hydraulic System  |
| PLC3 | Energy Monitoring |

Au total, **plusieurs capteurs industriels** sont simulés et exposés via un serveur OPC UA.

---

## PLC1 — Motor System

Ce PLC représente un moteur industriel.

### Capteurs simulés

* Temperature
* Vibration
* MotorCurrent
* MotorSpeed
* BearingHealth

### Cas d’usage

Ces capteurs sont utilisés pour :

* le monitoring d’état (condition monitoring)
* la maintenance prédictive
* le diagnostic machine

---

## PLC2 — Hydraulic System

Ce PLC simule un système hydraulique industriel.

### Capteurs simulés

* Pressure
* Temperature
* FlowRate
* OilLevel

### Cas d’usage

* surveillance de la pression
* suivi de la température de l’huile
* analyse du débit
* détection de fuite ou de panne

---

## PLC3 — Energy Monitoring

Ce PLC permet de superviser la consommation énergétique.

### Capteurs simulés

* Voltage
* Current
* EnergyConsumption
* PowerFactor

### Cas d’usage

* optimisation énergétique
* analyse de charge
* suivi de consommation

---

## Modes de simulation

Le simulateur propose trois modes de fonctionnement.

---

### Mode 1 — Normal Operation

Dans ce mode, les machines fonctionnent normalement.

Caractéristiques :

* température stable
* vibration faible
* courant stable
* vitesse constante
* bearing health proche de 100 %

Exemple :

* Temperature : 41 °C
* Vibration : 0.35 g
* Motor Current : 8 A
* Motor Speed : 1500 RPM
* Bearing Health : 98 %

---

### Mode 2 — Progressive System Failure

Ce mode simule une dégradation progressive du système.

Comportement :

* température augmente
* vibration augmente
* courant augmente
* vitesse diminue
* bearing health diminue

Exemple :

* Temperature : 55 °C
* Vibration : 1.8 g
* Motor Current : 11 A
* Motor Speed : 1420 RPM
* Bearing Health : 70 %

Ce mode reproduit une **dégradation mécanique progressive**.

---

### Mode 3 — Bearing Failure

Ce mode simule une panne critique de roulement.

Caractéristiques :

* vibration fortement élevée
* température élevée
* courant élevé
* vitesse instable
* bearing health chute rapidement

Exemple :

* Temperature : 65 °C
* Vibration : 3.5 g
* Motor Current : 12 A
* Motor Speed : 1380 RPM
* Bearing Health : 25 %

Seuil critique :

* vibration > 3 g
* bearing health < 30 %

→ panne imminente

---

## Logique de simulation

Les données générées ne sont pas totalement aléatoires.

Le simulateur utilise une logique de type :

```
previous_value + variation progressive
```

Cela permet de reproduire :

* l’inertie thermique
* l’inertie mécanique
* le bruit industriel

Les capteurs évoluent donc de manière réaliste, comme dans une vraie machine.

---

## Fonctionnement du code

Le script Python :

1. crée un serveur OPC UA
2. définit un namespace
3. crée plusieurs objets (PLC)
4. ajoute des variables (capteurs)
5. met à jour les valeurs en continu

---

## Structure OPC UA

Le serveur expose les données sous forme d’arbre :

```
Objects
 ├── PLC1_Motor_System
 │    ├── Temperature
 │    ├── Vibration
 │    ├── MotorCurrent
 │    ├── MotorSpeed
 │
 ├── PLC2_Hydraulic_System
 │    ├── Pressure
 │    ├── Temperature
 │
 ├── PLC3_Energy_Monitoring
      ├── Voltage
      ├── Current
      ├── EnergyConsumption
```

---

## Simulation des pannes

Le mode "fault" utilise un compteur qui augmente dans le temps :

```
fault_counter += 1
```

Cela permet de simuler une dégradation progressive.

### Exemple : Température moteur

```
temp = 40 + (fault_counter * 0.8) + bruit
```

Résultat :

* la température augmente progressivement
* comportement réaliste

---

## Objectif du simulateur

Ce simulateur permet de tester :

* des architectures OPC UA
* des pipelines IoT
* des systèmes de monitoring
* des cas de maintenance prédictive


## Conclusion

Ce simulateur OPC UA fournit un environnement industriel réaliste dans lequel plusieurs PLC et capteurs génèrent des données dynamiques.

Il constitue la base d’une architecture IoT complète permettant d’expérimenter :

* le monitoring industriel
* la détection d’anomalies
* la maintenance prédictive
* les architectures Edge et Cloud

---
