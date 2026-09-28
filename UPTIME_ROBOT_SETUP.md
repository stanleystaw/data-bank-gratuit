# 🤖 UptimeRobot - Garder Render Allumé 24h/24 Gratuitement

## Pourquoi UptimeRobot ?

Render.com Free **s'endort après 15 minutes d'inactivité**.
- 1ère visite après sleep = 30 secondes d'attente (cold start)
- UptimeRobot ping toutes les 5 minutes → Render ne dort jamais → toujours rapide

**Coût : 0F, sans carte bancaire, gratuit à vie**

---

## Option 1: UptimeRobot.com (Recommandé - 2 min)

### 1. Crée compte UptimeRobot (gratuit, sans carte)

- Va sur https://uptimerobot.com
- Sign Up → avec Email (gratuit, sans carte)
- Confirme email

### 2. Crée Monitor

- Dashboard → "Add New Monitor"
- **Monitor Type:** HTTP(s)
- **Friendly Name:** `Data Bank Gratuit - Render`
- **URL:** `https://data-bank-gratuit.onrender.com`
- **Monitoring Interval:** 5 minutes
- **Alert Contacts:** Ton email
- Clique "Create Monitor"

### 3. C'est tout !

UptimeRobot va ping `https://data-bank-gratuit.onrender.com` toutes les 5 minutes → Render ne dort plus jamais.

**50 monitors gratuits** sur UptimeRobot Free.

---

## Option 2: GitHub Actions (Déjà configuré - 0F, sans inscription externe)

J'ai déjà créé `.github/workflows/uptime.yml` qui fait la même chose que UptimeRobot mais via GitHub Actions.

**Comment ça marche :**
- GitHub Actions gratuit (2000 minutes/mois gratuit)
- Cron toutes les 5 minutes : `*/5 * * * *`
- Ping `https://data-bank-gratuit.onrender.com/api/stats`
- Render reste allumé

**Aucune action de ta part, c'est déjà actif dans ton repo GitHub.**

Vérifie : https://github.com/stanleystaw/data-bank-gratuit/actions

---

## Option 3: Uptime Kuma (Self-hosted)

Si tu as un PC ou Raspberry Pi :

```bash
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1
```

Puis ajoute monitor pour `https://data-bank-gratuit.onrender.com`

---

## 📊 Résultat

| Sans UptimeRobot | Avec UptimeRobot |
|------------------|------------------|
| Sleep après 15min | **Jamais sleep** |
| 1ère visite = 30s attente | **Toujours <2s** |
| Gratuit mais lent | **Gratuit et rapide** |

**Recommandation : Active les 2 (UptimeRobot + GitHub Actions) pour double sécurité, 0F**

---

## 🔍 Vérifier que ça marche

- Va sur https://data-bank-gratuit.onrender.com
- Si tu vois dashboard instantanément (<2s) → UptimeRobot marche
- Si tu attends 30s → UptimeRobot pas encore actif, attends 5 min

Logs UptimeRobot : Dashboard UptimeRobot → Monitor → Logs (doit voir ping toutes les 5 min, status 200)
