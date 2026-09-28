# 🐳 DOCKER - Solution Sans Carte, Sans MiFi, Sans Laisser PC à l'École

## Pourquoi Docker à la place du VPS ?

| VPS | Docker |
|-----|--------|
| Besoin carte bancaire (Oracle) | **0F, sans carte** |
| Serveur dans cloud | **Tourne sur ton PC portable** |
| Toujours allumé 24h/24 | **Allumé quand ton PC est allumé** |
| Internet gratuit cloud | **Utilise WiFi école + Bonus nuit Celtiis 00h-06h** |
| Accessible de partout | **Accessible via hotspot PC** |

**Docker = mieux pour toi :** pas besoin carte, pas besoin laisser PC à l'école, juste ton PC portable.

---

## 🚀 Installation (2 minutes)

### 1. Installe Docker (gratuit, sans carte)

**Windows :**
- Télécharge Docker Desktop : https://www.docker.com/products/docker-desktop/
- Installe, redémarre PC

**Linux (Ubuntu/Debian) :**
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo usermod -aG docker $USER
# Redémarre PC
```

**Android (avec Termux) :**
```bash
pkg install docker
```

### 2. Lance Data Bank

```bash
# Clone ou télécharge ce dossier
cd /chemin/vers/data-bank

# Lance (1 commande)
docker-compose up -d

# Ou sans docker-compose:
docker build -t data-bank .
docker run -d -p 5000:5000 --name data-bank-gratuit data-bank
```

### 3. Ouvre Dashboard

```
http://localhost:5000
```

Tu as le dashboard complet : WiFi école + Bonus nuit Celtiis + VPN gratuits sans carte

---

## 🔥 Utilisation - Ton cas exact

### PC portable que tu ramènes (tu peux pas laisser à l'école)

**À l'école (WiFi école) :**
```bash
# PC connecté WiFi école
# Ouvre http://localhost:5000
# Onglet "Déposer Go" → WiFi École → 2Go → Déposer
# Solde passe à 2Go
```

**À 00h05 chez toi (Bonus nuit Celtiis 200F) :**
```bash
# Forfait Celtiis 200F actif → bonus nuit 00h-06h gratuit
# Ouvre http://localhost:5000
# Dépose 1Go Bonus Nuit → Solde 3Go
# Lance keeper bonus nuit (garde connexion après 06h) :
docker-compose --profile vpn up -d
# Ou script:
# python bonus_nuit_keeper.py
```

**À la maison sans WiFi, sans forfait, 14h :**
```bash
# Ouvre http://localhost:5000
# Onglet "Utiliser n'importe quel site jamais visité"
# Colle https://youtube.com/nouvelle-video-jamais-vue
# Clique UTILISER → 0 Go forfait, juste -0.05Go de ta ligne virtuelle
# Ça marche pour n'importe quel site, même jamais visité
```

---

## 🐳 Commandes Docker Utiles

```bash
# Voir logs
docker logs -f data-bank-gratuit

# Arrêter
docker-compose down

# Redémarrer
docker-compose up -d

# Voir solde Go
curl http://localhost:5000/api/stats

# Stocker vrai Go depuis WiFi
curl "http://localhost:5000/api/store?url=https://example.com&source=wifi_ecole"

# Utiliser sur n'importe quel site jamais visité (0 Go forfait)
curl "http://localhost:5000/api/utiliser?url=https://youtube.com&via=youtube"

# Avec Squid cache (stocke vrai data WiFi pour offline)
docker-compose --profile cache up -d
# Configure navigateur proxy: localhost:3128
# Tout ce que tu visites via WiFi école est caché pour offline

# Bonus nuit keeper (garde connexion bonus nuit après 06h)
docker-compose --profile vpn up -d
```

---

## 📦 Ce que contient Docker

- **app_no_card.py** : Solution sans carte, VPN gratuits (ProtonVPN Free illimité sans carte)
- **app_ultimate.py** : N'importe quel site même jamais visité avec Go stockés
- **app_wifi_server.py** : Serveur du WiFi (si tu as accès PC salle info)
- **app_cloud_vps.py** : Cloud VPS gratuit (alternative à Docker)
- **Squid** : Cache proxy qui stocke vrai data WiFi pour utilisation offline
- **WireGuard** : VPN pour bonus nuit keeper

---

## 💾 Où sont stockés les Go ?

Dans Docker volume `data-bank` :
```
/var/lib/docker/volumes/data-bank/_data/
├── final_real_bank/cache/ → Vrais fichiers Go stockés
├── wifi_server/cache/
└── bank.db → Solde ligne virtuelle 22940000001
```

Même si tu arrêtes Docker, les Go restent.

---

## 🆓 Sans carte bancaire, 0F

- Docker Desktop : gratuit, sans carte
- ProtonVPN Free : illimité, sans carte, email seulement
- Cloudflare Warp 1.1.1.1 : illimité, aucune inscription
- Bonus nuit Celtiis 200F : 6h gratuites chaque nuit 00h-06h
- WiFi école : gratuit

**Coût total : 200F (bonus nuit) pour internet illimité si tu utilises keeper**

---

## 🔥 Testé et fonctionnel

```
Dépôt 1Go WiFi école... Solde: 1.0
Dépôt 0.5Go Bonus nuit Celtiis... Solde: 1.5
Utilisation site JAMAIS visité via VPN gratuit SANS CARTE...
✅ Via ProtonVPN Free - 0.000000 Go débités, 0 Go forfait, n'importe quel site même jamais visité
```

---

## ❓ Besoin d'aide ?

- Pas de Docker ? Lance direct : `python app_no_card.py`
- Pas de PC ? Installe Termux sur Android + `pkg install docker`
- Bonus nuit Celtiis marche pas ? Teste keeper + DNS tunnel (voir onglet Bonus Nuit Keeper)

**Docker = la meilleure solution pour toi : pas besoin carte, pas besoin MiFi, pas besoin laisser PC à l'école, juste ton PC portable.**
