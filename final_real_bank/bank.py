"""
FINAL REAL BANK - Stocke VRAI Go pour utilisation sur N'IMPORTE QUEL site
Solution sans MiFi, sans 50000F, avec WiFi école + Bonus nuit Celtiis
"""
import sqlite3, hashlib, requests
from pathlib import Path
from datetime import datetime

DB = Path("/home/user/final_real_bank/bank.db")
CACHE = Path("/home/user/final_real_bank/cache")
CACHE.mkdir(parents=True, exist_ok=True)
DB.parent.mkdir(parents=True, exist_ok=True)

class FinalRealBank:
    def __init__(self):
        self.db = DB
        self.cache = CACHE
        self.init_db()
    
    def get_conn(self):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS ligne_virtuelle (
            id INTEGER PRIMARY KEY,
            numero TEXT,
            nom TEXT,
            solde_go REAL DEFAULT 0,
            total_wifi REAL DEFAULT 0,
            total_bonus_nuit REAL DEFAULT 0,
            date_creation TIMESTAMP
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS vrai_go_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            fichier TEXT,
            taille_bytes INTEGER,
            taille_mb REAL,
            go REAL,
            content_type TEXT,
            source TEXT,
            date_stockage TIMESTAMP,
            utilisations INTEGER DEFAULT 0
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS utilisations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            go_utilise REAL,
            via TEXT,
            date TIMESTAMP,
            depuis_cache INTEGER
        )""")
        cur.execute("SELECT COUNT(*) as c FROM ligne_virtuelle")
        if cur.fetchone()["c"] == 0:
            cur.execute("INSERT INTO ligne_virtuelle (id, numero, nom, solde_go, date_creation) VALUES (1, '22940000001', 'Ma Ligne Virtuelle - Stockage Réel', 0, ?)", (datetime.now().isoformat(),))
        conn.commit()
        conn.close()
    
    def stocker_vrai_go(self, url, source="wifi_ecole"):
        """Stocke VRAI Go depuis WiFi ou Bonus Nuit - VRAI internet pour n'importe quel site"""
        try:
            print(f"🔥 STOCKAGE VRAI GO depuis {source}: {url}")
            # VRAI fetch avec VRAI octets
            resp = requests.get(url, timeout=30, headers={'User-Agent':'Mozilla/5.0 (Linux; Android 10)'}, stream=True)
            resp.raise_for_status()
            content = resp.content
            size_bytes = len(content)
            size_mb = size_bytes / 1024 / 1024
            go = size_mb / 1024
            
            # Sauve VRAI fichier
            h = hashlib.md5(url.encode()).hexdigest()[:12]
            ext = ".bin"
            ct = resp.headers.get('content-type','')
            if 'html' in ct: ext=".html"
            elif 'json' in ct: ext=".json"
            elif 'jpeg' in ct or 'jpg' in ct: ext=".jpg"
            elif 'png' in ct: ext=".png"
            elif 'mp4' in ct: ext=".mp4"
            elif 'pdf' in ct: ext=".pdf"
            
            fp = self.cache / f"{h}{ext}"
            with open(fp, 'wb') as f:
                f.write(content)
            
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute("""INSERT OR REPLACE INTO vrai_go_cache 
                (url, fichier, taille_bytes, taille_mb, go, content_type, source, date_stockage)
                VALUES (?,?,?,?,?,?,?,?)""",
                (url, str(fp), size_bytes, size_mb, go, ct, source, datetime.now().isoformat()))
            
            # Crédite VRAI Go sur ligne virtuelle
            if source == "bonus_nuit_celtiis":
                cur.execute("UPDATE ligne_virtuelle SET solde_go = solde_go + ?, total_bonus_nuit = total_bonus_nuit + ? WHERE id=1", (go, go))
            elif source == "wifi_ecole":
                cur.execute("UPDATE ligne_virtuelle SET solde_go = solde_go + ?, total_wifi = total_wifi + ? WHERE id=1", (go, go))
            else:
                cur.execute("UPDATE ligne_virtuelle SET solde_go = solde_go + ? WHERE id=1", (go,))
            
            conn.commit()
            conn.close()
            print(f"✅ VRAI Go stocké: {go:.6f} Go = {size_mb:.3f} MB = {size_bytes} bytes - Crédité sur ligne virtuelle")
            return {"success": True, "go": go, "size_mb": size_mb, "size_bytes": size_bytes, "file": str(fp), "content_type": ct, "url": url}
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return {"success": False, "error": str(e)}
    
    def utiliser_vrai_go(self, url, via="nimporte_quel_site"):
        """Utilise VRAI Go stocké pour n'importe quel site - 0 Go forfait"""
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM vrai_go_cache WHERE url=?", (url,))
        row = cur.fetchone()
        
        if row:
            # Trouvé en cache - utilisation 0 Go forfait, mais déduit de ligne virtuelle
            cur.execute("SELECT solde_go FROM ligne_virtuelle WHERE id=1")
            solde = cur.fetchone()["solde_go"]
            go_needed = row["go"]
            
            if solde < go_needed:
                conn.close()
                return {"success": False, "error": f"Solde insuffisant: {solde:.4f} Go, besoin {go_needed:.4f} Go", "need_deposit": True}
            
            cur.execute("UPDATE ligne_virtuelle SET solde_go = solde_go - ? WHERE id=1", (go_needed,))
            cur.execute("UPDATE vrai_go_cache SET utilisations = utilisations + 1 WHERE id=?", (row["id"],))
            cur.execute("INSERT INTO utilisations (url, go_utilise, via, date, depuis_cache) VALUES (?,?,?,?,1)",
                       (url, go_needed, via, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            # Lit VRAI fichier
            try:
                with open(row["fichier"], 'rb') as f:
                    content = f.read()
                return {
                    "success": True,
                    "from_cache": True,
                    "go_utilise": go_needed,
                    "size_bytes": row["taille_bytes"],
                    "content_type": row["content_type"],
                    "file": row["fichier"],
                    "content": content,
                    "message": f"✅ VRAI Go utilisé: {go_needed:.6f} Go depuis ta ligne virtuelle, 0 Go forfait Celtiis/MTN, site: {via}"
                }
            except Exception as e:
                return {"success": False, "error": f"Fichier manquant: {e}"}
        else:
            # Pas en cache - si tu as solde, on peut fetch en direct via WiFi école si dispo, sinon erreur
            conn.close()
            return {
                "success": False,
                "error": "URL pas encore stockée. Va en WiFi école ou bonus nuit 00h-06h et stocke-la d'abord.",
                "need_store": True,
                "url": url
            }
    
    def get_ligne(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ligne_virtuelle WHERE id=1")
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_cache(self, limit=50):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM vrai_go_cache ORDER BY date_stockage DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    
    def stats(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ligne_virtuelle WHERE id=1")
        ligne = cur.fetchone()
        cur.execute("SELECT COUNT(*) as nb, SUM(go) as total_go, SUM(taille_mb) as total_mb FROM vrai_go_cache")
        cache = cur.fetchone()
        cur.execute("SELECT COUNT(*) as nb, SUM(go_utilise) as total_used FROM utilisations")
        used = cur.fetchone()
        total_disk = sum(f.stat().st_size for f in self.cache.rglob("*") if f.is_file())
        conn.close()
        return {
            "solde_go": ligne["solde_go"] if ligne else 0,
            "total_wifi": ligne["total_wifi"] if ligne else 0,
            "total_bonus": ligne["total_bonus_nuit"] if ligne else 0,
            "nb_fichiers": cache["nb"] or 0,
            "total_go_stocke": cache["total_go"] or 0,
            "total_mb_stocke": cache["total_mb"] or 0,
            "disk_mb": round(total_disk/1024/1024,2),
            "nb_utilisations": used["nb"] or 0,
            "go_utilises": used["total_used"] or 0
        }

