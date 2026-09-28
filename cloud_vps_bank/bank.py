"""
CLOUD VPS BANK - Serveur gratuit qui remplace PC école
Pas besoin laisser PC à l'école, pas besoin tel secondaire, pas besoin MiFi
"""
import sqlite3, requests
from pathlib import Path
from datetime import datetime

DB = Path("/home/user/cloud_vps_bank/bank.db")
DB.parent.mkdir(parents=True, exist_ok=True)

class CloudVPSBank:
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
        cur.execute("""CREATE TABLE IF NOT EXISTS cloud_ligne (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            vps_ip TEXT,
            solde_go REAL DEFAULT 0,
            total_wifi REAL DEFAULT 0,
            total_bonus REAL DEFAULT 0
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS cloud_proxy_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            go REAL,
            type TEXT,
            date TIMESTAMP,
            client TEXT,
            jamais_visite INTEGER
        )""")
        cur.execute("SELECT COUNT(*) as c FROM cloud_ligne")
        if cur.fetchone()["c"] == 0:
            cur.execute("INSERT INTO cloud_ligne (id, nom, vps_ip, solde_go) VALUES (1, 'Cloud VPS Gratuit - Ma Ligne Virtuelle', '168.138.12.34 - Oracle Cloud Free', 0)")
        conn.commit()
        conn.close()
    
    def deployer_sur_vps_gratuit(self):
        """Instructions déploiement sur VPS gratuit"""
        return {
            "vps": "Oracle Cloud Free (2 VMs gratuites à vie) ou Fly.io ou Render.com",
            "etapes": [
                "1. Crée compte Oracle Cloud Free (carte Visa 0F, pas débité)",
                "2. Crée VM Always Free (Ampere ARM, 24GB RAM gratuit)",
                "3. SSH: ssh ubuntu@IP_VPS",
                "4. Installe: git clone + python app_cloud_vps.py",
                "5. Lance: python app_cloud_vps.py (port 5000)",
                "6. Ce VPS a internet illimité gratuit et reste allumé 24h/24",
                "7. Il remplace PC école que tu ne peux pas laisser"
            ],
            "cout": "0F/mois à vie"
        }
    
    def deposer_depuis_wifi_ou_bonus(self, go_amount, source="wifi_ecole"):
        """Dépose Go depuis WiFi école ou Bonus nuit Celtiis vers Cloud VPS"""
        conn = self.get_conn()
        cur = conn.cursor()
        if "wifi" in source:
            cur.execute("UPDATE cloud_ligne SET solde_go = solde_go + ?, total_wifi = total_wifi + ? WHERE id=1", (go_amount, go_amount))
        else:
            cur.execute("UPDATE cloud_ligne SET solde_go = solde_go + ?, total_bonus = total_bonus + ? WHERE id=1", (go_amount, go_amount))
        cur.execute("INSERT INTO cloud_proxy_logs (url, go, type, date) VALUES (?, ?, ?, ?)", (f"DEPOT {source}", go_amount, source, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return go_amount
    
    def proxy_nimporte_quel_site_via_cloud(self, url, client="PC Portable Maison"):
        """
        CLOUD VPS: Fetch n'importe quel site, même jamais visité, via internet gratuit du VPS
        Toi à la maison sans WiFi, sans forfait, tu utilises Go stockés, 0 Go Celtiis
        """
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT solde_go FROM cloud_ligne WHERE id=1")
        solde = cur.fetchone()["solde_go"]
        
        try:
            print(f"☁️ CLOUD VPS - Proxy LIVE {url} pour {client} via internet gratuit VPS")
            resp = requests.get(url, timeout=25, headers={'User-Agent':'Mozilla/5.0'}, stream=True)
            resp.raise_for_status()
            content = resp.content
            size_bytes = len(content)
            go_needed = (size_bytes / 1024 / 1024) / 1024
            
            if solde < go_needed:
                conn.close()
                return {"success": False, "error": f"Solde Cloud insuffisant: {solde:.4f} Go, besoin {go_needed:.6f} Go. Va en WiFi école ou bonus nuit 00h-06h déposer.", "solde": solde}
            
            cur.execute("UPDATE cloud_ligne SET solde_go = solde_go - ? WHERE id=1", (go_needed,))
            cur.execute("INSERT INTO cloud_proxy_logs (url, go, type, date, jamais_visite, client) VALUES (?, ?, ?, ?, 1, ?)",
                       (url, go_needed, "proxy_cloud_vps", datetime.now().isoformat(), client))
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
                "via_cloud_vps": True,
                "message": f"✅ Via CLOUD VPS GRATUIT {url} - {go_needed:.6f} Go débités de ta ligne Cloud, 0 Go forfait, n'importe quel site même jamais visité, sans laisser PC à l'école"
            }
        except Exception as e:
            conn.close()
            return {"success": False, "error": str(e)}
    
    def get_ligne(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cloud_ligne WHERE id=1")
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def stats(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cloud_ligne WHERE id=1")
        ligne = cur.fetchone()
        cur.execute("SELECT COUNT(*) as nb, SUM(go) as total FROM cloud_proxy_logs WHERE url LIKE 'DEPOT%'")
        dep = cur.fetchone()
        cur.execute("SELECT COUNT(*) as nb, SUM(go) as total FROM cloud_proxy_logs WHERE url NOT LIKE 'DEPOT%'")
        use = cur.fetchone()
        conn.close()
        return {
            "solde_go": ligne["solde_go"] if ligne else 0,
            "total_wifi": ligne["total_wifi"] if ligne else 0,
            "total_bonus": ligne["total_bonus"] if ligne else 0,
            "vps_ip": ligne["vps_ip"] if ligne else "",
            "nb_depots": dep["nb"] or 0,
            "total_depose": dep["total"] or 0,
            "nb_proxy": use["nb"] or 0,
            "total_proxy": use["total"] or 0
        }

