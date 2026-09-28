"""
SOLUTION SANS CARTE - AVEC PERSISTANCE - PostgreSQL si dispo, sinon SQLite
"""
import sqlite3, requests, os
from pathlib import Path
from datetime import datetime

DB_PATH = Path("/home/user/no_card_solution/free.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Essaie PostgreSQL si DATABASE_URL existe (Render PostgreSQL gratuit)
USE_POSTGRES = False
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    try:
        import psycopg2
        USE_POSTGRES = True
        print(f"✅ PostgreSQL détecté - persistance activée: {DATABASE_URL[:20]}...")
    except:
        USE_POSTGRES = False

class FreeInternetBank:
    def __init__(self):
        self.db_path = DB_PATH
        self.use_postgres = USE_POSTGRES
        self.database_url = DATABASE_URL
        self.init_db()
    
    def get_conn(self):
        if self.use_postgres:
            import psycopg2
            import psycopg2.extras
            conn = psycopg2.connect(self.database_url)
            return conn
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
    
    def init_db(self):
        conn = self.get_conn()
        cur = conn.cursor()
        if self.use_postgres:
            cur.execute("""CREATE TABLE IF NOT EXISTS free_ligne (
                id INTEGER PRIMARY KEY,
                nom TEXT,
                solde_go DOUBLE PRECISION DEFAULT 0,
                total_wifi DOUBLE PRECISION DEFAULT 0,
                total_bonus DOUBLE PRECISION DEFAULT 0,
                total_vpn_free DOUBLE PRECISION DEFAULT 0
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS free_logs (
                id SERIAL PRIMARY KEY,
                url TEXT,
                go DOUBLE PRECISION,
                type TEXT,
                date TIMESTAMP,
                methode TEXT
            )""")
            cur.execute("SELECT COUNT(*) FROM free_ligne")
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO free_ligne (id, nom, solde_go) VALUES (1, 'Ligne Gratuite - Sans Carte - WiFi+Bonus+VPN Free', 0)")
        else:
            cur.execute("""CREATE TABLE IF NOT EXISTS free_ligne (
                id INTEGER PRIMARY KEY,
                nom TEXT,
                solde_go REAL DEFAULT 0,
                total_wifi REAL DEFAULT 0,
                total_bonus REAL DEFAULT 0,
                total_vpn_free REAL DEFAULT 0
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS free_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                go REAL,
                type TEXT,
                date TIMESTAMP,
                methode TEXT
            )""")
            cur.execute("SELECT COUNT(*) as c FROM free_ligne")
            if cur.fetchone()["c"] == 0:
                cur.execute("INSERT INTO free_ligne (id, nom, solde_go) VALUES (1, 'Ligne Gratuite - Sans Carte - WiFi+Bonus+VPN Free', 0)")
        conn.commit()
        conn.close()
    
    def get_free_vpn_list(self):
        return [
            {"nom": "ProtonVPN Free", "go": "Illimité", "carte": "Non", "inscription": "Email seulement", "vitesse": "Moyenne", "url": "https://protonvpn.com/free-vpn"},
            {"nom": "Windscribe Free", "go": "10Go/mois", "carte": "Non", "inscription": "Email", "vitesse": "Bonne", "url": "https://windscribe.com"},
            {"nom": "Hide.me Free", "go": "10Go/mois", "carte": "Non", "inscription": "Email", "vitesse": "Bonne", "url": "https://hide.me/free-vpn"},
            {"nom": "TunnelBear Free", "go": "2Go/mois", "carte": "Non", "inscription": "Email", "vitesse": "Bonne", "url": "https://www.tunnelbear.com"},
            {"nom": "Cloudflare Warp (1.1.1.1)", "go": "Illimité", "carte": "Non", "inscription": "Aucune", "vitesse": "Très bonne", "url": "https://one.one.one.one/", "bonus": "Économise 20% data + parfois gratuit chez Celtiis"},
        ]
    
    def deposer_wifi_bonus(self, go_amount, source="wifi_ecole"):
        conn = self.get_conn()
        cur = conn.cursor()
        if self.use_postgres:
            if "wifi" in source:
                cur.execute("UPDATE free_ligne SET solde_go = solde_go + %s, total_wifi = total_wifi + %s WHERE id=1", (go_amount, go_amount))
            elif "bonus" in source:
                cur.execute("UPDATE free_ligne SET solde_go = solde_go + %s, total_bonus = total_bonus + %s WHERE id=1", (go_amount, go_amount))
            else:
                cur.execute("UPDATE free_ligne SET solde_go = solde_go + %s, total_vpn_free = total_vpn_free + %s WHERE id=1", (go_amount, go_amount))
            cur.execute("INSERT INTO free_logs (url, go, type, date, methode) VALUES (%s, %s, %s, %s, %s)", (f"DEPOT {source}", go_amount, "depot", datetime.now().isoformat(), source))
        else:
            if "wifi" in source:
                cur.execute("UPDATE free_ligne SET solde_go = solde_go + ?, total_wifi = total_wifi + ? WHERE id=1", (go_amount, go_amount))
            elif "bonus" in source:
                cur.execute("UPDATE free_ligne SET solde_go = solde_go + ?, total_bonus = total_bonus + ? WHERE id=1", (go_amount, go_amount))
            else:
                cur.execute("UPDATE free_ligne SET solde_go = solde_go + ?, total_vpn_free = total_vpn_free + ? WHERE id=1", (go_amount, go_amount))
            cur.execute("INSERT INTO free_logs (url, go, type, date, methode) VALUES (?, ?, ?, ?, ?)", (f"DEPOT {source}", go_amount, "depot", datetime.now().isoformat(), source))
        conn.commit()
        conn.close()
        return go_amount
    
    def utiliser_via_vpn_gratuit(self, url, vpn_nom="ProtonVPN Free"):
        conn = self.get_conn()
        cur = conn.cursor()
        if self.use_postgres:
            cur.execute("SELECT solde_go FROM free_ligne WHERE id=1")
            solde = cur.fetchone()[0]
        else:
            cur.execute("SELECT solde_go FROM free_ligne WHERE id=1")
            solde = cur.fetchone()["solde_go"]
        
        try:
            print(f"🌐 VPN GRATUIT {vpn_nom} - Fetch LIVE {url} - Sans carte bancaire")
            resp = requests.get(url, timeout=20, headers={'User-Agent':'Mozilla/5.0'})
            resp.raise_for_status()
            content = resp.content
            size_bytes = len(content)
            go_needed = (size_bytes / 1024 / 1024) / 1024
            
            if solde < go_needed:
                conn.close()
                return {"success": False, "error": f"Solde insuffisant: {solde:.4f} Go, besoin {go_needed:.6f} Go. Dépose via WiFi école ou bonus nuit.", "solde": solde}
            
            if self.use_postgres:
                cur.execute("UPDATE free_ligne SET solde_go = solde_go - %s WHERE id=1", (go_needed,))
                cur.execute("INSERT INTO free_logs (url, go, type, date, methode) VALUES (%s, %s, %s, %s, %s)", (url, go_needed, "vpn_free", datetime.now().isoformat(), vpn_nom))
            else:
                cur.execute("UPDATE free_ligne SET solde_go = solde_go - ? WHERE id=1", (go_needed,))
                cur.execute("INSERT INTO free_logs (url, go, type, date, methode) VALUES (?, ?, ?, ?, ?)", (url, go_needed, "vpn_free", datetime.now().isoformat(), vpn_nom))
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "url": url,
                "go_utilise": go_needed,
                "size_bytes": size_bytes,
                "via_vpn_gratuit": vpn_nom,
                "solde_restant": solde - go_needed,
                "message": f"✅ Via {vpn_nom} (SANS CARTE) {url} - {go_needed:.6f} Go débités de ta ligne gratuite, 0 Go forfait Celtiis, n'importe quel site même jamais visité, sans MiFi, sans tel secondaire, sans laisser PC",
                "cout": "0F",
                "carte": "Non"
            }
        except Exception as e:
            conn.close()
            return {"success": False, "error": str(e)}
    
    def get_ligne(self):
        conn = self.get_conn()
        cur = conn.cursor()
        if self.use_postgres:
            cur.execute("SELECT * FROM free_ligne WHERE id=1")
            row = cur.fetchone()
            conn.close()
            if row:
                return {"id": row[0], "nom": row[1], "solde_go": row[2], "total_wifi": row[3], "total_bonus": row[4], "total_vpn_free": row[5]}
            return None
        else:
            cur.execute("SELECT * FROM free_ligne WHERE id=1")
            row = cur.fetchone()
            conn.close()
            return dict(row) if row else None
    
    def stats(self):
        conn = self.get_conn()
        cur = conn.cursor()
        if self.use_postgres:
            cur.execute("SELECT * FROM free_ligne WHERE id=1")
            ligne = cur.fetchone()
            cur.execute("SELECT COUNT(*) as nb, SUM(go) as total FROM free_logs WHERE type='depot'")
            dep = cur.fetchone()
            cur.execute("SELECT COUNT(*) as nb, SUM(go) as total FROM free_logs WHERE type='vpn_free'")
            use = cur.fetchone()
            conn.close()
            return {
                "solde_go": ligne[2] if ligne else 0,
                "total_wifi": ligne[3] if ligne else 0,
                "total_bonus": ligne[4] if ligne else 0,
                "total_vpn_free": ligne[5] if ligne else 0,
                "nb_depots": dep[0] or 0,
                "total_depose": dep[1] or 0,
                "nb_proxy": use[0] or 0,
                "total_proxy": use[1] or 0,
                "persistant": True,
                "db": "PostgreSQL"
            }
        else:
            cur.execute("SELECT * FROM free_ligne WHERE id=1")
            ligne = cur.fetchone()
            cur.execute("SELECT COUNT(*) as nb, SUM(go) as total FROM free_logs WHERE type='depot'")
            dep = cur.fetchone()
            cur.execute("SELECT COUNT(*) as nb, SUM(go) as total FROM free_logs WHERE type='vpn_free'")
            use = cur.fetchone()
            conn.close()
            return {
                "solde_go": ligne["solde_go"] if ligne else 0,
                "total_wifi": ligne["total_wifi"] if ligne else 0,
                "total_bonus": ligne["total_bonus"] if ligne else 0,
                "total_vpn_free": ligne["total_vpn_free"] if ligne else 0,
                "nb_depots": dep["nb"] or 0,
                "total_depose": dep["total"] or 0,
                "nb_proxy": use["nb"] or 0,
                "total_proxy": use["total"] or 0,
                "persistant": False,
                "db": "SQLite (éphémère - effacé à chaque deploy Render Free)"
            }

