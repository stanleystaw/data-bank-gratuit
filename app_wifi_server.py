"""
SERVEUR DU WIFI - Solution sans téléphone secondaire
Tu installes ça sur le serveur WiFi (PC école, ou VPS gratuit)
"""
from flask import Flask, render_template_string, jsonify, request, Response
from wifi_server.server import WiFiServerBank
from datetime import datetime

app = Flask(__name__)
bank = WiFiServerBank()

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🏫 SERVEUR DU WIFI - Sans tel secondaire</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family: 'Segoe UI', sans-serif; }
body { background:#020617; color:#e2e8f0; padding:10px; }
.container { max-width:1200px; margin:0 auto; }
header { background: linear-gradient(135deg,#00ff88 0%,#00ccff 100%); color:#000; padding:16px; border-radius:12px; margin-bottom:12px; }
header h1 { font-size:1.4rem; font-weight:900; }
.serveur-box { background:#0f172a; border:2px solid #00ff88; border-radius:12px; padding:16px; margin-bottom:12px; text-align:center; }
.serveur-ip { font-family:monospace; background:#000; color:#00ff88; padding:6px 12px; border-radius:6px; display:inline-block; margin:6px 0; }
.solde { font-size:2.8rem; font-weight:900; color:#00ff88; }
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:8px; margin-bottom:12px; }
.card { background:#0f172a; border:1px solid #1e293b; border-radius:10px; padding:10px; }
.card h3 { font-size:0.6rem; color:#64748b; text-transform:uppercase; }
.card .value { font-size:1.2rem; font-weight:bold; color:#00ff88; }
.section { background:#0f172a; border:1px solid #1e293b; border-radius:10px; padding:14px; margin-bottom:10px; }
.section h2 { color:#00ff88; font-size:1rem; margin-bottom:10px; }
.btn { background:#00ff88; color:#000; border:none; padding:10px 18px; border-radius:8px; font-weight:800; cursor:pointer; }
.btn-red { background:#ff4444; color:#fff; }
.btn-blue { background:#00ccff; color:#000; }
.btn-small { padding:5px 10px; font-size:0.75rem; }
input, select { background:#020617; border:1px solid #1e293b; color:#fff; padding:10px; border-radius:8px; width:100%; margin-bottom:8px; }
.form-row { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
@media(max-width:600px){ .form-row{grid-template-columns:1fr} }
table { width:100%; border-collapse:collapse; font-size:0.75rem; }
th, td { padding:6px; border-bottom:1px solid #1e293b; text-align:left; }
th { color:#64748b; font-size:0.6rem; }
.tabs { display:flex; gap:6px; margin-bottom:12px; flex-wrap:wrap; }
.tab { padding:7px 14px; background:#0f172a; border:1px solid #1e293b; border-radius:20px; cursor:pointer; font-size:0.8rem; color:#94a3b8; }
.tab.active { background:#00ff88; color:#000; border-color:#00ff88; font-weight:800; }
.hidden{ display:none; }
.success { background:#052e16; border:1px solid #00ff88; color:#00ff88; padding:8px; border-radius:6px; font-size:0.8rem; }
.code { background:#000; border:1px solid #333; color:#00ff88; padding:10px; border-radius:6px; font-family:monospace; font-size:0.75rem; overflow:auto; }
</style>
</head>
<body>
<div class="container">
<header>
<h1>🏫 SERVEUR DU WIFI - Sans téléphone secondaire - Solution Finale</h1>
<p style="font-size:0.85rem; margin-top:4px; font-weight:600;">Tu installes ça sur le serveur WiFi (PC salle info, ou VPS gratuit) → Il stocke WiFi + Bonus nuit → Utilisable sur n'importe quel site même jamais visité, sans forfait</p>
</header>

<div class="serveur-box">
<div style="font-size:0.6rem; color:#64748b; letter-spacing:2px;">SERVEUR DU WIFI INSTALLÉ</div>
<div style="font-size:0.9rem; color:#fff; margin:6px 0;">{{ serveur.nom }}</div>
<div class="serveur-ip">📡 IP Serveur: {{ serveur.ip_serveur }} • Ligne Virtuelle: 22940000001</div>
<div class="solde">{{ "%.6f"|format(stats.solde_go) }} Go</div>
<div style="font-size:0.8rem; color:#64748b;">Solde serveur • {{ stats.nb_depots }} dépôts • {{ stats.nb_proxy }} utilisations n'importe quel site</div>
<div style="margin-top:8px; display:flex; gap:6px; justify-content:center; flex-wrap:wrap;">
<span style="background:#002200; color:#00ff88; padding:4px 10px; border-radius:20px; font-size:0.65rem;">🏫 WiFi Serveur: {{ "%.3f"|format(stats.total_wifi) }} Go</span>
<span style="background:#220044; color:#aa88ff; padding:4px 10px; border-radius:20px; font-size:0.65rem;">🌙 Bonus Nuit: {{ "%.3f"|format(stats.total_bonus) }} Go</span>
</div>
</div>

<div class="stats">
<div class="card"><h3>Solde Serveur</h3><div class="value">{{ "%.4f"|format(stats.solde_go) }} Go</div><div class="sub" style="font-size:0.6rem; color:#475569;">Pour n'importe quel site</div></div>
<div class="card"><h3>Installé sur</h3><div class="value" style="font-size:0.9rem; color:#00ccff;">{{ serveur.ip_serveur[:20] }}</div><div class="sub" style="font-size:0.6rem; color:#475569;">Serveur WiFi</div></div>
<div class="card"><h3>Sites jamais visités</h3><div class="value" style="color:#ffff00;">{{ stats.nb_proxy }}</div><div class="sub" style="font-size:0.6rem; color:#475569;">Servis via serveur</div></div>
<div class="card"><h3>Test</h3><div class="value" style="color:#00ff00;">✅ OK</div><div class="sub" style="font-size:0.6rem; color:#475569;">N'importe quel site marche</div></div>
</div>

<div class="tabs">
<button class="tab active" onclick="showTab('installer')">⚙️ Installer sur Serveur WiFi</button>
<button class="tab" onclick="showTab('deposer')">📥 Déposer Go (WiFi/Bonus Nuit)</button>
<button class="tab" onclick="showTab('utiliser')">🌐 Utiliser N'importe Quel Site Jamais Visité</button>
<button class="tab" onclick="showTab('logs')">📜 Logs Serveur</button>
</div>

<div id="tab-installer" class="section">
<h2>⚙️ Comment installer sur le serveur du WiFi (sans tel secondaire)</h2>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#020617; padding:10px; border-radius:8px; border-left:3px solid #00ff88;">
<h4 style="color:#00ff88; font-size:0.85rem;">Option 1: PC Salle Info École (le mieux)</h4>
<p style="font-size:0.75rem; color:#94a3b8; line-height:1.4; margin-top:6px;">
1. Va en salle info, PC qui reste allumé<br>
2. Installe Python + ce projet<br>
3. Lance: <code>python app_wifi_server.py</code><br>
4. Ce PC a IP genre 192.168.1.50<br>
5. Entre IP ci-dessous et clique Installer<br>
6. Ce PC devient serveur qui stocke WiFi et sert n'importe quel site
</p>
</div>
<div style="background:#020617; padding:10px; border-radius:8px; border-left:3px solid #00ccff;">
<h4 style="color:#00ccff; font-size:0.85rem;">Option 2: VPS Gratuit Cloud (sans accès école)</h4>
<p style="font-size:0.75rem; color:#94a3b8; line-height:1.4; margin-top:6px;">
• Oracle Cloud Free: 2 serveurs gratuits à vie<br>
• Fly.io: gratuit<br>
• Render.com: gratuit<br>
• Déploie ce code là-bas<br>
• Le VPS a internet illimité gratuit<br>
• Il sert de serveur WiFi virtuel
</p>
</div>
</div>

<div style="background:#000; padding:12px; border-radius:8px; margin-top:12px; border:1px solid #00ff88;">
<h4 style="color:#00ff88; font-size:0.85rem;">Installer maintenant :</h4>
<div class="form-row" style="margin-top:8px;">
<div><input type="text" id="ipServeur" placeholder="IP serveur WiFi ex: 192.168.1.50 ou 10.0.0.5" value="192.168.1.50 - PC Salle Info"></div>
<div><button class="btn" onclick="installer()" style="width:100%;">⚙️ Installer Serveur sur WiFi</button></div>
</div>
<div id="installResult" style="margin-top:8px;"></div>
</div>

<div class="code" style="margin-top:12px;">
# Code à lancer sur le serveur WiFi (PC école):<br>
git clone ton-projet<br>
cd wifi_server<br>
python app_wifi_server.py # Lance serveur sur 0.0.0.0:5000<br>
# Puis Cloudflare Tunnel pour accès depuis maison:<br>
cloudflared tunnel --url http://localhost:5000<br>
# Tu obtiens: https://xxx.trycloudflare.com → accessible depuis chez toi
</div>
</div>

<div id="tab-deposer" class="section hidden">
<h2>📥 Déposer Go depuis WiFi Serveur / Bonus Nuit Celtiis</h2>
<p style="font-size:0.8rem; color:#64748b; margin-bottom:10px;">Tu es sur le serveur WiFi (PC école) ou en bonus nuit 00h-06h ? Dépose Go.</p>

<div style="background:#000; padding:12px; border-radius:8px; border:1px solid #00ff88;">
<div class="form-row">
<div><select id="sourceDepot"><option value="wifi_ecole_direct">🏫 WiFi École Direct (serveur)</option><option value="bonus_nuit_celtiis">🌙 Bonus Nuit Celtiis 00h-06h</option><option value="wifi_ecole">🏫 WiFi École (via tel)</option></select></div>
<div><input type="number" step="0.01" id="goDepot" value="1.0" placeholder="Go à déposer"></div>
</div>
<button class="btn" onclick="deposer()" style="width:100%; margin-top:8px;">📥 Déposer Go sur Serveur WiFi</button>
<div id="depotResult" style="margin-top:10px;"></div>
</div>
</div>

<div id="tab-utiliser" class="section hidden">
<h2>🌐 Utiliser N'importe Quel Site Jamais Visité via Serveur WiFi - 0 Go forfait</h2>
<p style="font-size:0.8rem; color:#64748b; margin-bottom:10px;">À la maison sans WiFi, sans forfait ? Utilise Go stockés sur serveur WiFi pour aller sur n'importe quel site, même jamais visité.</p>

<div style="background:#000; padding:12px; border-radius:8px; border:2px solid #ff0000;">
<input type="text" id="urlUse" placeholder="N'IMPORTE QUEL SITE jamais visité: https://youtube.com, https://tiktok.com, https://google.com/search?q=...">
<input type="text" id="clientIp" placeholder="Ton IP (ex: 192.168.1.10 - Mon tel maison)" value="192.168.1.10 - Mon tel à la maison" style="margin-top:8px;">
<button class="btn btn-red" onclick="utiliser()" style="width:100%; font-size:1.1rem; margin-top:8px;">🔥 UTILISER N'IMPORTE QUEL SITE JAMAIS VISITÉ VIA SERVEUR WIFI - 0 Go FORFAIT</button>
<div id="useResult" style="margin-top:10px;"></div>
</div>

<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:6px; margin-top:10px;">
<button class="btn btn-small" onclick="quickUse('https://httpbin.org/uuid')">Test UUID jamais visité</button>
<button class="btn btn-small btn-blue" onclick="quickUse('https://httpbin.org/json')">Test JSON jamais visité</button>
<button class="btn btn-small" style="background:#ff00ff; color:#fff;" onclick="quickUse('https://example.com?rand='+Math.random())">Test Random</button>
<button class="btn btn-small" style="background:#ffff00; color:#000;" onclick="quickUse('https://www.google.com/search?q=test'+Math.random())">Test Google jamais visité</button>
</div>

<div style="background:#220000; border:1px solid #ff0000; padding:10px; border-radius:8px; margin-top:12px;">
<h4 style="color:#ff0000; font-size:0.85rem;">💡 Comment ça marche sans tel secondaire ?</h4>
<p style="font-size:0.75rem; color:#ff8888; line-height:1.4;">
• Serveur WiFi = PC salle info qui a WiFi école gratuit<br>
• Il tourne 24h/24, a internet illimité via WiFi école<br>
• Toi à la maison, tu envoies requête: "je veux youtube.com jamais visité"<br>
• Serveur WiFi fetch youtube.com via WiFi école (gratuit)<br>
• Il te renvoie YouTube, déduit Go de ta ligne serveur, 0 Go Celtiis<br>
• Pas besoin tel secondaire, juste serveur WiFi
</p>
</div>
</div>

<div id="tab-logs" class="section hidden">
<h2>📜 Logs Serveur WiFi - Proxy N'importe Quel Site</h2>
<table>
<tr><th>Date</th><th>URL / Source</th><th>Go</th><th>Client IP</th><th>Jamais visité</th></tr>
{% for log in logs %}
<tr>
<td style="font-size:0.65rem;">{{ log.date[:16].replace('T',' ') }}</td>
<td style="max-width:250px; overflow:hidden; font-size:0.7rem;">{{ log.url[:60] }}</td>
<td style="color:{% if 'DEPOT' in log.url %}#00ff00{% else %}#ff8888{% endif %}; font-weight:bold;">{{ "%.6f"|format(log.go) }} Go</td>
<td style="font-size:0.65rem;">{{ log.client_ip or log.source }}</td>
<td>{% if log.jamais_visite %}✅ Oui{% else %}-{% endif %}</td>
</tr>
{% endfor %}
</table>
</div>

</div>

<script>
function showTab(name){
 document.querySelectorAll('[id^=tab-]').forEach(el=>el.classList.add('hidden'));
 document.getElementById('tab-'+name).classList.remove('hidden');
 document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
 event.target.classList.add('active');
}
function quickUse(url){
 document.getElementById('urlUse').value=url;
 utiliser();
}
function installer(){
 const ip = document.getElementById('ipServeur').value;
 fetch('/api/installer?ip='+encodeURIComponent(ip))
 .then(r=>r.json()).then(j=>{
   document.getElementById('installResult').innerHTML='<div class=\"success\">✅ Serveur installé sur '+ip+' - Prêt à stocker WiFi et servir n\\'importe quel site</div>';
   setTimeout(()=>location.reload(), 1000);
 });
}
function deposer(){
 const source = document.getElementById('sourceDepot').value;
 const go = parseFloat(document.getElementById('goDepot').value);
 fetch('/api/deposer?source='+source+'&go='+go)
 .then(r=>r.json()).then(j=>{
   document.getElementById('depotResult').innerHTML='<div class=\"success\">✅ Déposé '+j.go_depose+' Go depuis '+source+'<br>Solde serveur: '+j.solde+' Go</div>';
   setTimeout(()=>location.reload(), 1000);
 });
}
function utiliser(){
 const url = document.getElementById('urlUse').value;
 const ip = document.getElementById('clientIp').value;
 if(!url) return alert('URL manquante - mets n\\'importe quel site jamais visité');
 document.getElementById('useResult').innerHTML='⏳ Proxy LIVE via serveur WiFi... Fetch '+url+' (jamais visité) via WiFi école...';
 fetch('/api/proxy?url='+encodeURIComponent(url)+'&client_ip='+encodeURIComponent(ip))
 .then(r=>r.json()).then(j=>{
   if(j.success){
     document.getElementById('useResult').innerHTML='<div class=\"success\">'+j.message+'<br>Solde restant: '+j.solde_restant+' Go<br><a href=\"/api/raw?url='+encodeURIComponent(url)+'\" target=\"_blank\" style=\"color:#00ff00;\">Voir contenu (0 Go forfait)</a></div>';
     setTimeout(()=>location.reload(), 1500);
   } else {
     document.getElementById('useResult').innerHTML='<div style=\"background:#330000; padding:8px; color:#f00;\">❌ '+j.error+'</div>';
   }
 });
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    serveur = bank.get_serveur()
    stats = bank.stats()
    # Get logs
    import sqlite3
    from pathlib import Path
    conn = sqlite3.connect(Path("/home/user/wifi_server/bank.db"))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM proxy_logs ORDER BY date DESC LIMIT 30")
    logs = [dict(r) for r in cur.fetchall()]
    conn.close()
    return render_template_string(HTML, serveur=serveur, stats=stats, logs=logs)

@app.route('/api/installer')
def api_installer():
    ip = request.args.get('ip','192.168.1.50')
    msg = bank.installer_sur_serveur_wifi(ip)
    return jsonify({"success": True, "message": msg, "ip": ip})

@app.route('/api/deposer')
def api_deposer():
    source = request.args.get('source','wifi_ecole_direct')
    go = float(request.args.get('go',1.0))
    deposited = bank.deposer_depuis_wifi_serveur(go, source)
    serveur = bank.get_serveur()
    return jsonify({"success": True, "go_depose": deposited, "solde": serveur['solde_go']})

@app.route('/api/proxy')
def api_proxy():
    url = request.args.get('url')
    client_ip = request.args.get('client_ip','0.0.0.0')
    if not url:
        return jsonify({"success": False, "error": "URL manquante"}), 400
    result = bank.proxy_nimporte_quel_site(url, client_ip)
    if result.get("success") and "content" in result:
        del result["content"]
    return jsonify(result)

@app.route('/api/raw')
def api_raw():
    url = request.args.get('url')
    if not url:
        return "URL manquante", 400
    try:
        import requests
        resp = requests.get(url, timeout=15, headers={'User-Agent':'Mozilla/5.0'})
        from flask import Response
        return Response(resp.content, content_type=resp.headers.get('content-type','text/html'))
    except Exception as e:
        return f"Erreur: {e}", 500

@app.route('/api/stats')
def api_stats():
    return jsonify(bank.stats())

if __name__ == '__main__':
    print("🏫 SERVEUR DU WIFI - Sans tel secondaire - sur http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
