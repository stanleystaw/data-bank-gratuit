# 🔥 Pourquoi 60,5 Go effacés ? Et comment fixer pour de vrai ?

## Pourquoi solde passé de 60,5 Go à 0 Go ?

**Render.com Free = stockage éphémère**
- SQLite `free.db` est stocké dans container Docker
- À chaque nouveau deploy (git push) ou quand Render sleep 15min et redémarre, container est recréé → SQLite effacé → solde 0 Go
- C'est ce qui vient d'arriver: tu avais 60,5 Go, on a poussé code UptimeRobot → nouveau deploy → SQLite effacé → 0 Go

**C'est normal sur Render Free sans disque persistant.**

## Solution 1: PostgreSQL Gratuit Render (Recommandé, 0F, Sans Carte, Persistant)

PostgreSQL Free Render garde data même après deploy.

### Étapes (2 min, sans carte) :

1. Va sur https://dashboard.render.com/new/database
2. Choisis **PostgreSQL**, Name: `data-bank-db`, Plan: **Free** (90 jours gratuit, sans carte), Région: Oregon
3. Clique Create Database, attends 2 min
4. Copie **Internal Database URL** (genre `postgres://user:pass@dpg-xxx.oregon-postgres.render.com/db`)
5. Va sur ton service https://dashboard.render.com/web/srv-dat6rjnlk1mc73egre00
6. Environment → Add Environment Variable → Key: `DATABASE_URL`, Value: colle Internal Database URL
7. Save Changes → Render redeploy automatique
8. Maintenant Go stockés dans PostgreSQL → **persistants, jamais effacés même après deploy**

**Coût : 0F, sans carte, 90 jours gratuit, après tu recrées DB gratuite**

### Code déjà prêt pour PostgreSQL

J'ai déjà modifié `no_card_solution/free_internet.py` pour détecter `DATABASE_URL` :
- Si `DATABASE_URL` existe → utilise PostgreSQL (persistant)
- Sinon → SQLite (éphémère)

Donc dès que tu ajoutes env var `DATABASE_URL` sur Render, ça passe en persistant automatiquement.

## Solution 2: Redéposer rapidement (si pas envie PostgreSQL)

Tu es en WiFi maintenant, tu peux redéposer 60,5 Go en 6 clics :

```
https://data-bank-gratuit.onrender.com/api/deposer?source=wifi_ecole&go=10
https://data-bank-gratuit.onrender.com/api/deposer?source=wifi_ecole&go=10
https://data-bank-gratuit.onrender.com/api/deposer?source=wifi_ecole&go=10
https://data-bank-gratuit.onrender.com/api/deposer?source=wifi_ecole&go=10
https://data-bank-gratuit.onrender.com/api/deposer?source=wifi_ecole&go=10
https://data-bank-gratuit.onrender.com/api/deposer?source=wifi_ecole&go=10
https://data-bank-gratuit.onrender.com/api/deposer?source=wifi_ecole&go=0.5
= 60,5 Go
```

6 clics = 60,5 Go de retour.

Mais à chaque deploy Render Free, ça s'effacera encore. Donc Solution 1 PostgreSQL mieux.

## Solution 3: Supabase (Gratuit sans carte, persistant à vie)

- Va sur https://supabase.com → Sign Up gratuit sans carte
- New Project → copie DATABASE_URL PostgreSQL
- Ajoute env var `DATABASE_URL` sur Render
- Persistant à vie, pas 90 jours

## Solution 4: Garder Render allumé avec UptimeRobot + ne plus deploy

- UptimeRobot ping toutes les 5min → évite sleep
- Ne fais plus git push → pas de nouveau deploy → SQLite reste
- Mais si Render redémarre serveur, quand même effacé

**Recommandation : Solution 1 PostgreSQL Free Render - 2 min, 0F, sans carte, persistant**

## Action immédiate pour toi maintenant (en WiFi) :

1. **Redépose 60,5 Go rapidement :** Clique 6 fois sur lien 10Go ci-dessus
2. **Puis fixe persistance :** Crée PostgreSQL Free Render + ajoute DATABASE_URL
3. **Après, tes Go ne s'effaceront plus jamais**

Veux-tu que je crée PostgreSQL Free pour toi via API Render ?
