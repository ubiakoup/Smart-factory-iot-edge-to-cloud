#  TP15 – Corrigé

##  AWS IoT → Lambda → SNS

---

# 🎯 Objectif

Mettre en place un système capable de :

```text id="c1"
analyser les données IoT et déclencher des alertes en temps réel
```

---

# Architecture finale

```text id="c2"
Edge → MQTT → AWS IoT → IoT Rule → Lambda → SNS → Email
```

---

#  Partie 1 — IoT Rule

---

## SQL

```sql id="c3"
SELECT 
  topic(2) as plc,
  topic(3) as metric,
  value,
  timestamp
FROM 'factory/+/+'
```

---

# Partie 2 — Lambda

---

## Fonction

```python id="c4"
import boto3
import json
import time

sns = boto3.client("sns")

TOPIC_ARN = "arn:aws:sns:us-east-1:315824631771:factory-alerts"

RANGES = {
    "temperature_motor": (0, 40),
    "vibration_motor": (0, 2.5),
    "motor_current": (8, 12),
    "motor_speed": (1300, 1500),
    "voltage": (210, 230)
}

COOLDOWN = 60
LAST_ALERT = {}

def lambda_handler(event, context):

    metric = event.get("metric")
    plc = event.get("plc")

    try:
        value = float(event.get("value", 0))
    except:
        return {"status": "error"}

    if metric not in RANGES:
        return {"status": "ignored"}

    min_v, max_v = RANGES[metric]

    key = f"{plc}_{metric}"
    now = time.time()

    if value < min_v or value > max_v:

        if key in LAST_ALERT:
            if now - LAST_ALERT[key] < COOLDOWN:
                return {"status": "cooldown"}

        LAST_ALERT[key] = now

        message = json.dumps({
            "plc": plc,
            "metric": metric,
            "value": value,
            "expected_min": min_v,
            "expected_max": max_v
        })

        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject="Factory Alert"
        )

    return {"status": "ok"}
```

---

# Partie 3 — SNS

---

* Topic : `factory-alerts`
* Type : Standard
* Subscription : Email

---

# Partie 4 — IAM

---

## Policy ajoutée

```json id="c5"
{
  "Effect": "Allow",
  "Action": "sns:Publish",
  "Resource": "arn:aws:sns:us-east-1:315824631771:factory-alerts"
}
```

---

#  Partie 5 — Test

---

## Normal

```json id="c6"
"value": 25
```

👉 pas d’alerte

---

## Anomalie

```json id="c7"
"value": 90
```

👉 email reçu

---

#  Limites

```text id="c8"
LAST_ALERT n’est pas persisté
```

👉 solution production :

```text id="c9"
DynamoDB / Redis
```

---

#  Résultat final

```text id="c10"
✔ détection anomalies
✔ alerting temps réel
✔ architecture réactive
✔ base industrielle
```

---

#  Conclusion

```text id="c11"
Le système ne se contente plus de stocker les données
→ il agit en temps réel
```

---
