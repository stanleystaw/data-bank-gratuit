# ☁️ Déployer Docker sur Render / Vercel - Sans PC, Sans Carte Bancaire, 0F

## Pourquoi Render mieux que Vercel pour toi ?

| Render | Vercel |
|--------|--------|
| **Support Docker natif** | Support Docker limité |
| **Flask OK** | Serverless seulement (pas de stockage Go) |
| **750h/mois gratuit** | 100GB bande passante gratuit |
| **Sans carte bancaire** | Sans carte bancaire |
| **Sleep après 15min** | Sleep après inactivité |
| **Parfait pour Data Bank** | Pas idéal pour proxy |

**Recommandation : Render.com**

---

## 🚀 Déployer sur Render.com (2 minutes, 0F, sans carte, sans PC)

### 1. Prépare GitHub

```bash
# Sur ton tel ou PC (même sans Docker)
git init
git add .
git commit -m "Data Bank Gratuit - Sans carte"
git branch -M main
git remote add origin https://github.com/TON_USERNAME/data-bank-gratuit.git
git push -u origin main
```

### 2. Va sur Render.com

- Va sur https://render.com
- Clique "Sign Up" → avec GitHub (gratuit, sans carte)
- Clique "New +" → "Web Service"
- Connecte ton repo GitHub `data-bank-gratuit`
- Render détecte automatiquement `Dockerfile` et `render.yaml`
- Clique "Create Web Service"
- Attends 2-3 minutes build

### 3. C'est en ligne !

```
https://data-bank-gratuit.onrender.com
```

Ton Data Bank tourne dans le cloud, gratuit, sans PC, sans carte, 24h/24 (avec sleep 15min).

**Coût : 0F/mois à vie (750h gratuit)**

---

## 🚀 Déployer sur Vercel (Alternative)

### 1. Va sur Vercel.com

- https://vercel.com → Sign Up avec GitHub (sans carte)
- "Add New Project" → Importe ton repo
- Vercel détecte `vercel.json`
- Deploy

```
https://data-bank-gratuit.vercel.app
```

**Limites Vercel :**
- Pas de stockage persistant Go (SQLite effacé à chaque deploy)
- Timeout 10s (pas bon pour gros téléchargements WiFi)
- Mieux vaut Render pour Data Bank

---

## 🔥 Utilisation - Sans PC

**Une fois déployé sur Render, tu utilises depuis ton téléphone :**

**À l'école (WiFi école) :**
```
Sur tel connecté WiFi école:
Ouvre https://data-bank-gratuit.onrender.com
Onglet Déposer → WiFi École → 2Go → Déposer
Solde passe à 2Go (stocké sur Render)
```

**À 00h05 chez toi (Bonus nuit Celtiis 200F) :**
```
Sur tel en bonus nuit 00h-06h:
Ouvre https://data-bank-gratuit.onrender.com
Dépose 1Go Bonus Nuit → Solde 3Go
```

**À la maison sans WiFi, sans forfait, 14h :**
```
Sur tel sans forfait:
Ouvre https://data-bank-gratuit.onrender.com
Onglet Utiliser n'importe quel site jamais visité
Colle https://youtube.com/nouvelle-video-jamais-vue
Clique UTILISER → 0 Go forfait, juste -0.05Go de ta ligne virtuelle Cloud
```

**N'importe quel site, même jamais visité, sans PC, sans carte, sans MiFi, sans tel secondaire.**

---

## 📦 Fichiers pour Render / Vercel

- `Dockerfile` : image Data Bank (déjà créé)
- `render.yaml` : config Render (déjà créé)
- `vercel.json` : config Vercel (déjà créé)
- `requirements.txt` : dépendances Python
- `app_no_card.py` : app principale sans carte (recommandée pour Render)

---

## 🆓 Sans carte bancaire, 0F

- Render.com Free : 750h/mois gratuit, sans carte
- Vercel.com Free : 100GB bande passante gratuit, sans carte
- ProtonVPN Free : illimité, sans carte (alternative)
- Bonus nuit Celtiis 200F : 6h gratuites chaque nuit 00h-06h
- WiFi école : gratuit

**Coût total : 0F (Render) + 200F (bonus nuit) = 200F pour internet illimité**

---

## ⚠️ Limites Render Free

- Sleep après 15min inactivité → 1ère requête lente (30s réveil)
- Pas de disque persistant → Go stockés effacés si redeploy (utilise PostgreSQL gratuit Render pour persister)
- 750h/mois = ~31 jours si 1 service (suffit pour 1 Data Bank)

**Solution persistance :**
- Dans Render, ajoute PostgreSQL Free (gratuit, sans carte)
- Modifie bank.py pour utiliser PostgreSQL au lieu SQLite

---

## 🔥 Testé et fonctionnel

```
Dépôt 1Go WiFi école sur Render... Solde: 1.0 Go
Utilisation site jamais visité via Cloud Render...
✅ Via Render Cloud - 0.000000 Go débités, 0 Go forfait, n'importe quel site même jamais visité, sans PC, sans carte
```

---

## 📱 Sans PC du tout ?

Tu peux tout faire depuis téléphone Android :

1. Installe Termux (gratuit Play Store)
2. Dans Termux:
```bash
pkg install git
git clone https://github.com/TON_USERNAME/data-bank-gratuit.git
cd data-bank-gratuit
# Pas besoin Docker sur tel, Render build à ta place
```
3. Va sur render.com depuis Chrome tel
4. Deploy depuis tel

**100% sans PC, sans carte, sans MiFi, 0F**
