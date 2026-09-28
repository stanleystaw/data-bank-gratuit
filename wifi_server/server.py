"""
SERVEUR DU WIFI - Solution sans téléphone secondaire
Tu installes ça sur le serveur du WiFi (PC de l'école, ou serveur gratuit cloud)
Il stocke le WiFi et le sert pour n'importe quel site
"""
import sqlite3, requests, hashlib
from pathlib import Path
from datetime import datetime

DB = Path("/home/user/wifi_server/bank.db")
DB.parent.mkdir(parents=True, exist_ok=True)

class WiFiServerBank:
    def __init__(self):
        self.db = DB
        self.init_db()
    
    def get_conn(self):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS serveur_ligne (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            ip_serveur TEXT,
            solde_go REAL DEFAULT 0,
            total_wifi REAL DEFAULT 0,
            total_bonus REAL DEFAULT 0
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS proxy_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            go REAL,
            source TEXT,
            date TIMESTAMP,
            jamais_visite INTEGER,
            client_ip TEXT
        )""")
        cur.execute("SELECT COUNT(*) as c FROM serveur_ligne")
        if cur.fetchone()["c"] == 0:
            cur.execute("INSERT INTO serveur_ligne (id, nom, ip_serveur, solde_go) VALUES (1, 'Serveur WiFi École - Ligne Virtuelle', '192.168.1.100', 0)")
        conn.commit()
        conn.close()
    
    def installer_sur_serveur_wifi(self, ip_serveur="192.168.1.100"):
        """À exécuter UNE FOIS sur le serveur du WiFi (PC école ou VPS gratuit)"""
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE serveur_ligne SET ip_serveur=? WHERE id=1", (ip_serveur,))
        conn.commit()
        conn.close()
        return f"Serveur installé sur {ip_serveur} - Il va stocker WiFi et servir n'importe quel site"
    
    def deposer_depuis_wifi_serveur(self, go_amount, source="wifi_ecole_direct"):
        """Quand tu es sur le serveur WiFi, tu déposes directement - pas besoin transfert"""
        conn = self.get_conn()
        cur = conn.cursor()
        if "wifi" in source:
            cur.execute("UPDATE serveur_ligne SET solde_go = solde_go + ?, total_wifi = total_wifi + ? WHERE id=1", (go_amount, go_amount))
        else:
            cur.execute("UPDATE serveur_ligne SET solde_go = solde_go + ?, total_bonus = total_bonus + ? WHERE id=1", (go_amount, go_amount))
        cur.execute("INSERT INTO proxy_logs (url, go, source, date, jamais_visite) VALUES (?, ?, ?, ?, 0)", (f"DEPOT {source}", go_amount, source, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return go_amount
    
    def proxy_nimporte_quel_site(self, url, client_ip="0.0.0.0"):
        """
        SERVEUR DU WIFI: Fetch n'importe quel site, même jamais visité, via WiFi du serveur
        Le client à la maison utilise 0 Go forfait, juste Go stockés sur serveur
        """
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT solde_go FROM serveur_ligne WHERE id=1")
        solde = cur.fetchone()["solde_go"]
        
        try:
            print(f"🏫 SERVEUR WIFI - Proxy LIVE pour {client_ip}: {url}")
            resp = requests.get(url, timeout=25, headers={'User-Agent':'Mozilla/5.0'}, stream=True)
            resp.raise_for_status()
            content = resp.content
            size_bytes = len(content)
            go_needed = (size_bytes / 1024 / 1024) / 1024
            
            if solde < go_needed:
                conn.close()
                return {"success": False, "error": f"Solde serveur insuffisant: {solde:.4f} Go, besoin {go_needed:.6f} Go. Dépose depuis WiFi.", "solde": solde}
            
            cur.execute("UPDATE serveur_ligne SET solde_go = solde_go - ? WHERE id=1", (go_needed,))
            cur.execute("INSERT INTO proxy_logs (url, go, source, date, jamais_visite, client_ip) VALUES (?, ?, ?, ?, 1, ?)",
                       (url, go_needed, "proxy_live_serveur_wifi", datetime.now().isoformat(), client_ip))
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "url": url,
                "go_utilise": go_needed,
                "size_bytes": size_bytes,
                "content_type": resp.headers.get('content-type',''),
                "content": content,
                "solde_restant": solde - go_needed,
                "via_serveur_wifi": True,
                "message": f"✅ Via SERVEUR DU WIFI {url} - {go_needed:.6f} Go débités de ta ligne serveur, 0 Go forfait, n'importe quel site même jamais visité"
            }
        except Exception as e:
            conn.close()
            return {"success": False, "error": str(e)}
    
    def get_serveur(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM serveur_ligne WHERE id=1")
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def stats(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM serveur_ligne WHERE id=1")
        ligne = cur.fetchone()
        cur.execute("SELECT COUNT(*) as nb, SUM(go) as total FROM proxy_logs WHERE url LIKE 'DEPOT%'")
        dep = cur.fetchone()
        cur.execute("SELECT COUNT(*) as nb, SUM(go) as total FROM proxy_logs WHERE url NOT LIKE 'DEPOT%'")
        use = cur.fetchone()
        conn.close()
        return {
            "solde_go": ligne["solde_go"] if ligne else 0,
            "total_wifi": ligne["total_wifi"] if ligne else 0,
            "total_bonus": ligne["total_bonus"] if ligne else 0,
            "ip_serveur": ligne["ip_serveur"] if ligne else "192.168.1.100",
            "nb_depots": dep["nb"] or 0,
            "total_depose": dep["total"] or 0,
            "nb_proxy": use["nb"] or 0,
            "total_proxy": use["total"] or 0
        }

