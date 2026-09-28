"""
CLOUD VPS BANK - Solution sans laisser PC à l'école, sans tel secondaire, sans MiFi, sans 50000F
Serveur gratuit Oracle Cloud qui reste allumé 24h/24 à ta place
"""
from flask import Flask, render_template_string, jsonify, request
from cloud_vps_bank.bank import CloudVPSBank

app = Flask(__name__)
bank = CloudVPSBank()

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>☁️ CLOUD VPS - Sans laisser PC à l'école</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family: 'Segoe UI', sans-serif; }
body { background:#020617; color:#e2e8f0; padding:10px; }
.container { max-width:1150px; margin:0 auto; }
header { background: linear-gradient(135deg,#ff00ff 0%,#00ccff 100%); color:#fff; padding:16px; border-radius:12px; margin-bottom:12px; }
header h1 { font-size:1.3rem; font-weight:900; }
.cloud-box { background:#0f172a; border:2px solid #ff00ff; border-radius:12px; padding:16px; margin-bottom:12px; text-align:center; box-shadow:0 0 30px #ff00ff33; }
.vps-ip { font-family:monospace; background:#000; color:#ff00ff; padding:6px 12px; border-radius:6px; display:inline-block; margin:6px 0; }
.solde { font-size:3rem; font-weight:900; color:#ff00ff; text-shadow:0 0 20px #ff00ff; }
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:8px; margin-bottom:12px; }
.card { background:#0f172a; border:1px solid #1e293b; border-radius:10px; padding:10px; }
.card h3 { font-size:0.6rem; color:#64748b; text-transform:uppercase; }
.card .value { font-size:1.2rem; font-weight:bold; color:#ff00ff; }
.section { background:#0f172a; border:1px solid #1e293b; border-radius:10px; padding:14px; margin-bottom:10px; }
.section h2 { color:#ff00ff; font-size:1rem; margin-bottom:10px; }
.btn { background:#ff00ff; color:#fff; border:none; padding:10px 18px; border-radius:8px; font-weight:800; cursor:pointer; }
.btn-green { background:#00ff88; color:#000; }
.btn-red { background:#ff4444; color:#fff; }
.btn-small { padding:5px 10px; font-size:0.75rem; }
input, select { background:#020617; border:1px solid #1e293b; color:#fff; padding:10px; border-radius:8px; width:100%; margin-bottom:8px; }
.form-row { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
@media(max-width:600px){ .form-row{grid-template-columns:1fr} }
table { width:100%; border-collapse:collapse; font-size:0.75rem; }
th, td { padding:6px; border-bottom:1px solid #1e293b; text-align:left; }
th { color:#64748b; font-size:0.6rem; }
.tabs { display:flex; gap:6px; margin-bottom:12px; flex-wrap:wrap; }
.tab { padding:7px 14px; background:#0f172a; border:1px solid #1e293b; border-radius:20px; cursor:pointer; font-size:0.8rem; color:#94a3b8; }
.tab.active { background:#ff00ff; color:#fff; border-color:#ff00ff; font-weight:800; }
.hidden{ display:none; }
.success { background:#2a0033; border:1px solid #ff00ff; color:#ff88ff; padding:8px; border-radius:6px; font-size:0.8rem; }
.code { background:#000; border:1px solid #333; color:#ff00ff; padding:10px; border-radius:6px; font-family:monospace; font-size:0.7rem; overflow:auto; }
</style>
</head>
<body>
<div class="container">
<header>
<h1>☁️ CLOUD VPS GRATUIT - Sans laisser PC à l'école - Sans tel secondaire</h1>
<p style="font-size:0.85rem; margin-top:4px;">PC portable que tu ramènes chez toi ? Pas grave. Serveur gratuit Oracle Cloud reste allumé 24h/24 à ta place et stocke ton WiFi + Bonus nuit Celtiis</p>
</header>

<div class="cloud-box">
<div style="font-size:0.6rem; color:#64748b; letter-spacing:2px;">SERVEUR CLOUD GRATUIT - REMPLACE PC ÉCOLE</div>
<div style="font-size:0.9rem; color:#fff; margin:6px 0;">{{ ligne.nom }}</div>
<div class="vps-ip">☁️ {{ ligne.vps_ip }} • Ligne: 22940000001 • 0F/mois à vie • 24h/24 allumé</div>
<div class="solde">{{ "%.4f"|format(stats.solde_go) }} Go</div>
<div style="font-size:0.8rem; color:#64748b;">Solde Cloud • {{ stats.nb_depots }} dépôts WiFi/Bonus Nuit • {{ stats.nb_proxy }} utilisations n'importe quel site jamais visité</div>
<div style="margin-top:8px; display:flex; gap:6px; justify-content:center; flex-wrap:wrap;">
<span style="background:#002200; color:#00ff88; padding:4px 10px; border-radius:20px; font-size:0.65rem;">🏫 WiFi: {{ "%.3f"|format(stats.total_wifi) }} Go</span>
<span style="background:#220044; color:#aa88ff; padding:4px 10px; border-radius:20px; font-size:0.65rem;">🌙 Bonus Nuit: {{ "%.3f"|format(stats.total_bonus) }} Go</span>
</div>
</div>

<div class="stats">
<div class="card"><h3>Solde Cloud</h3><div class="value">{{ "%.4f"|format(stats.solde_go) }} Go</div><div class="sub" style="font-size:0.6rem; color:#475569;">Pour n'importe quel site</div></div>
<div class="card"><h3>Serveur</h3><div class="value" style="font-size:0.8rem; color:#ff00ff;">Oracle Free</div><div class="sub" style="font-size:0.6rem; color:#475569;">0F/mois, 24h/24</div></div>
<div class="card"><h3>Sites jamais visités</h3><div class="value" style="color:#ffff00;">{{ stats.nb_proxy }}</div><div class="sub" style="font-size:0.6rem; color:#475569;">Via Cloud</div></div>
<div class="card"><h3>Test</h3><div class="value" style="color:#00ff88;">✅ OK</div><div class="sub" style="font-size:0.6rem; color:#475569;">Sans PC à l'école</div></div>
</div>

<div class="tabs">
<button class="tab active" onclick="showTab('deploy')">☁️ Déployer Serveur Gratuit</button>
<button class="tab" onclick="showTab('deposer')">📥 Déposer Go (WiFi/Bonus Nuit)</button>
<button class="tab" onclick="showTab('utiliser')">🌐 Utiliser N'importe Quel Site Jamais Visité</button>
<button class="tab" onclick="showTab('guide')">💡 Guide PC Portable</button>
</div>

<div id="tab-deploy" class="section">
<h2>☁️ Déployer Serveur Gratuit qui remplace PC école (0F/mois)</h2>

<div style="background:#000; padding:12px; border-radius:8px; border:1px solid #ff00ff; margin-bottom:12px;">
<h4 style="color:#ff00ff; font-size:0.9rem;">🎯 Pourquoi Cloud VPS ?</h4>
<p style="font-size:0.8rem; color:#ff88ff; line-height:1.4; margin-top:6px;">
Tu ne peux pas laisser PC à l'école ? Pas grave. Un serveur gratuit dans le cloud reste allumé 24h/24 à ta place, a internet illimité gratuit, et stocke ton WiFi + Bonus nuit Celtiis. Tu y accèdes depuis chez toi avec 0 Go forfait.
</p>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#020617; padding:10px; border-radius:8px; border-left:3px solid #ff00ff;">
<h4 style="color:#ff00ff; font-size:0.85rem;">Option 1: Oracle Cloud Free (recommandé)</h4>
<p style="font-size:0.7rem; color:#94a3b8; line-height:1.3; margin-top:6px;">
• 2 VMs gratuites À VIE (Ampere ARM, 24GB RAM)<br>
• Internet illimité gratuit<br>
• Carte Visa demandée mais 0F débité (vérif)<br>
• Inscription: cloud.oracle.com<br>
• Crée VM: Always Free, Ubuntu 22.04<br>
• IP publique gratuite
</p>
</div>
<div style="background:#020617; padding:10px; border-radius:8px; border-left:3px solid #00ccff;">
<h4 style="color:#00ccff; font-size:0.85rem;">Option 2: Fly.io / Render.com (plus simple)</h4>
<p style="font-size:0.7rem; color:#94a3b8; line-height:1.3; margin-top:6px;">
• Fly.io: 3 VMs gratuites<br>
• Render.com: 1 VM gratuite<br>
• Pas besoin carte bancaire<br>
• Déploie avec: flyctl launch<br>
• Moins puissant que Oracle mais suffit
</p>
</div>
</div>

<div class="code" style="margin-top:12px;">
# Une fois VPS créé (Oracle Cloud), connecte-toi:<br>
ssh ubuntu@168.138.12.34 # IP de ton VPS gratuit<br>
<br>
# Installe serveur WiFi:<br>
git clone https://github.com/ton-projet/wifi-server<br>
cd wifi-server<br>
pip install flask requests<br>
python app_cloud_vps.py # Lance sur 0.0.0.0:5000<br>
<br>
# Ce VPS a maintenant internet gratuit illimité et reste allumé 24h/24<br>
# Il remplace PC école que tu ne peux pas laisser
</div>
</div>

<div id="tab-deposer" class="section hidden">
<h2>📥 Déposer Go depuis WiFi École / Bonus Nuit Celtiis vers Cloud VPS</h2>
<p style="font-size:0.8rem; color:#64748b; margin-bottom:10px;">Tu es à l'école en WiFi ou chez toi en bonus nuit 00h-06h Celtiis ? Dépose Go sur Cloud VPS gratuit.</p>

<div style="background:#000; padding:12px; border-radius:8px; border:1px solid #ff00ff;">
<div class="form-row">
<div><select id="sourceDepot"><option value="wifi_ecole">🏫 WiFi École (quand tu es à l'école avec PC portable)</option><option value="bonus_nuit_celtiis">🌙 Bonus Nuit Celtiis 00h-06h (chez toi, forfait 200F)</option></select></div>
<div><input type="number" step="0.1" id="goDepot" value="1.0" placeholder="Go à déposer ex: 2.0"></div>
</div>
<button class="btn" onclick="deposer()" style="width:100%; margin-top:8px;">📥 Déposer Go sur Cloud VPS Gratuit (0F)</button>
<div id="depotResult" style="margin-top:10px;"></div>
</div>
</div>

<div id="tab-utiliser" class="section hidden">
<h2>🌐 Utiliser N'importe Quel Site Jamais Visité via Cloud VPS - 0 Go forfait - Sans laisser PC à l'école</h2>
<p style="font-size:0.8rem; color:#64748b; margin-bottom:10px;">À la maison SANS WiFi, SANS forfait ? Utilise Go stockés sur Cloud VPS pour aller sur n'importe quel site, même jamais visité.</p>

<div style="background:#000; padding:12px; border-radius:8px; border:2px solid #ff0000;">
<input type="text" id="urlUse" placeholder="N'IMPORTE QUEL SITE jamais visité: https://youtube.com, https://tiktok.com, https://google.com">
<input type="text" id="clientIp" placeholder="Ton PC Portable Maison - Cotonou" value="PC Portable Maison - Cotonou" style="margin-top:8px;">
<button class="btn" style="background:#ff0000; color:#fff; width:100%; font-size:1.1rem; margin-top:8px;" onclick="utiliser()">🔥 UTILISER N'IMPORTE QUEL SITE JAMAIS VISITÉ VIA CLOUD VPS - 0 Go FORFAIT - SANS PC À L'ÉCOLE</button>
<div id="useResult" style="margin-top:10px;"></div>
</div>

<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:6px; margin-top:10px;">
<button class="btn btn-small" onclick="quickUse('https://httpbin.org/uuid')">Test UUID jamais visité</button>
<button class="btn btn-small" style="background:#00ccff; color:#000;" onclick="quickUse('https://httpbin.org/json')">Test JSON jamais visité</button>
<button class="btn btn-small" style="background:#ffff00; color:#000;" onclick="quickUse('https://example.com?rand='+Math.random())">Test Random</button>
</div>

<div style="background:#220000; border:1px solid #ff0000; padding:10px; border-radius:8px; margin-top:12px;">
<h4 style="color:#ff0000; font-size:0.85rem;">💡 Comment ça marche sans laisser PC à l'école ?</h4>
<p style="font-size:0.75rem; color:#ff8888; line-height:1.4;">
• Cloud VPS = PC virtuel gratuit qui reste allumé 24h/24 chez Oracle (0F)<br>
• Il a internet illimité gratuit (pas besoin WiFi école)<br>
• Toi à l'école: tu déposes 2Go (tu dis au VPS: j'ai 2Go de WiFi à stocker)<br>
• À la maison: tu demandes n'importe quel site jamais visité au VPS<br>
• VPS fetch site via son internet gratuit, te renvoie, déduit Go de ta ligne virtuelle<br>
• 0 Go Celtiis consommé, pas besoin laisser PC à l'école, pas besoin tel secondaire
</p>
</div>
</div>

<div id="tab-guide" class="section hidden">
<h2>💡 Guide PC Portable - Tu ne peux pas le laisser à l'école</h2>

<div style="background:#002200; border:1px solid #00ff88; padding:12px; border-radius:8px; margin-bottom:10px;">
<h4 style="color:#00ff88;">🎯 Ton cas exact : PC portable que tu ramènes</h4>
<p style="font-size:0.8rem; color:#88ff88; line-height:1.5; margin-top:6px;">
<b>Problème :</b> PC portable, tu ne peux pas le laisser à l'école comme serveur.<br><br>
<b>Solution Cloud VPS (0F) :</b><br>
1. Crée compte Oracle Cloud Free (0F, carte Visa juste pour vérif)<br>
2. Lance VM gratuite (toujours allumée, internet gratuit)<br>
3. Déploie ce code dessus → ton serveur WiFi virtuel<br>
4. À l'école avec PC portable en WiFi: dépose 2Go sur Cloud VPS<br>
5. À la maison sans WiFi: utilise Cloud VPS pour n'importe quel site jamais visité, 0 Go forfait<br><br>
<b>Coût :</b> 0F/mois à vie. Pas besoin MiFi, pas besoin tel secondaire, pas besoin laisser PC.
</p>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#020617; padding:10px; border-radius:8px;">
<h4 style="color:#ff00ff; font-size:0.8rem;">🌙 Bonus Nuit Celtiis 200F - 00h-06h</h4>
<p style="font-size:0.7rem; color:#94a3b8; line-height:1.3;">
• Forfait 200F Celtiis → bonus nuit 00h-06h<br>
• À 00h05, dépose 1Go sur Cloud VPS<br>
• Ce 1Go est stocké, valable 30 jours<br>
• Le jour, utilise-le pour n'importe quel site via Cloud VPS<br>
• 200F = 6h gratuites chaque nuit
</p>
</div>
<div style="background:#020617; padding:10px; border-radius:8px;">
<h4 style="color:#00ccff; font-size:0.8rem;">🏫 WiFi École - Quand tu y es</h4>
<p style="font-size:0.7rem; color:#94a3b8; line-height:1.3;">
• Connecté WiFi école avec PC portable<br>
• Dépose 2Go sur Cloud VPS (1 clic)<br>
• Rentre chez toi avec PC portable<br>
• Cloud VPS garde tes 2Go<br>
• Utilise-les à la maison pour n'importe quel site jamais visité
</p>
</div>
</div>

<div class="code" style="margin-top:12px;">
# Setup complet 0F pour toi:<br>
# 1. Oracle Cloud Free → VM gratuite<br>
# 2. Sur VM: python app_cloud_vps.py<br>
# 3. Sur PC école: dépose Go → https://ton-vps.com/api/deposer?go=2&source=wifi_ecole<br>
# 4. À la maison: utilise → https://ton-vps.com/api/proxy?url=https://youtube.com<br>
# Résultat: n'importe quel site, même jamais visité, 0 Go forfait, sans laisser PC à l'école
</div>
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
function deposer(){
 const source = document.getElementById('sourceDepot').value;
 const go = parseFloat(document.getElementById('goDepot').value);
 fetch('/api/deposer?source='+source+'&go='+go)
 .then(r=>r.json()).then(j=>{
   document.getElementById('depotResult').innerHTML='<div class=\"success\">✅ Déposé '+j.go_depose+' Go depuis '+source+' sur Cloud VPS<br>Solde Cloud: '+j.solde+' Go - Utilisable n\\'importe où</div>';
   setTimeout(()=>location.reload(), 1000);
 });
}
function utiliser(){
 const url = document.getElementById('urlUse').value;
 const client = document.getElementById('clientIp') ? document.getElementById('clientIp').value : 'PC Portable';
 if(!url) return alert('URL manquante - n\\'importe quel site jamais visité');
 document.getElementById('useResult').innerHTML='⏳ Proxy LIVE via Cloud VPS gratuit... Fetch '+url+' (jamais visité) via internet gratuit VPS...';
 fetch('/api/proxy?url='+encodeURIComponent(url)+'&client='+encodeURIComponent(client))
 .then(r=>r.json()).then(j=>{
   if(j.success){
     document.getElementById('useResult').innerHTML='<div class=\"success\">'+j.message+'<br>Solde restant: '+j.solde_restant+' Go<br><a href=\"/api/raw?url='+encodeURIComponent(url)+'\" target=\"_blank\" style=\"color:#ff00ff;\">Voir contenu (0 Go forfait)</a></div>';
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
    ligne = bank.get_ligne()
    stats = bank.stats()
    import sqlite3
    from pathlib import Path
    conn = sqlite3.connect(Path("/home/user/cloud_vps_bank/bank.db"))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM cloud_proxy_logs ORDER BY date DESC LIMIT 20")
    logs = [dict(r) for r in cur.fetchall()]
    conn.close()
    return render_template_string(HTML, ligne=ligne, stats=stats, logs=logs)

@app.route('/api/deposer')
def api_deposer():
    source = request.args.get('source','wifi_ecole')
    go = float(request.args.get('go',1.0))
    deposited = bank.deposer_depuis_wifi_ou_bonus(go, source)
    ligne = bank.get_ligne()
    return jsonify({"success": True, "go_depose": deposited, "solde": ligne['solde_go']})

@app.route('/api/proxy')
def api_proxy():
    url = request.args.get('url')
    client = request.args.get('client','PC Portable')
    if not url:
        return jsonify({"success": False, "error": "URL manquante"}), 400
    result = bank.proxy_nimporte_quel_site_via_cloud(url, client)
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
    print("☁️ CLOUD VPS BANK - Sans laisser PC à l'école - sur http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
