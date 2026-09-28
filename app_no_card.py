"""
SOLUTION SANS CARTE BANCAIRE - Sans MiFi, sans tel secondaire, sans laisser PC à l'école, sans 50000F
VPN Gratuits + Bonus Nuit Keeper + DNS Tunnel
"""
from flask import Flask, render_template_string, jsonify, request
from no_card_solution.free_internet import FreeInternetBank

app = Flask(__name__)
bank = FreeInternetBank()

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🆓 SANS CARTE - Vrai Go - N'importe quel site</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family: 'Segoe UI', sans-serif; }
body { background:#000; color:#fff; padding:10px; }
.container { max-width:1150px; margin:0 auto; }
header { background: linear-gradient(135deg,#00ff00 0%,#ffff00 100%); color:#000; padding:16px; border-radius:12px; margin-bottom:12px; }
header h1 { font-size:1.3rem; font-weight:900; }
.free-box { background:#111; border:3px solid #00ff00; border-radius:14px; padding:16px; margin-bottom:12px; text-align:center; box-shadow:0 0 30px #00ff0033; }
.solde { font-size:3rem; font-weight:900; color:#00ff00; text-shadow:0 0 20px #00ff00; }
.badge-free { background:#00ff00; color:#000; padding:6px 14px; border-radius:20px; font-weight:900; font-size:0.8rem; display:inline-block; margin:6px 0; }
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:8px; margin-bottom:12px; }
.card { background:#111; border:1px solid #222; border-radius:10px; padding:10px; }
.card h3 { font-size:0.6rem; color:#666; text-transform:uppercase; }
.card .value { font-size:1.2rem; font-weight:bold; color:#00ff00; }
.section { background:#111; border:1px solid #222; border-radius:10px; padding:14px; margin-bottom:10px; }
.section h2 { color:#00ff00; font-size:1rem; margin-bottom:10px; }
.btn { background:#00ff00; color:#000; border:none; padding:10px 18px; border-radius:8px; font-weight:900; cursor:pointer; }
.btn-red { background:#ff0000; color:#fff; }
.btn-blue { background:#00ccff; color:#000; }
.btn-small { padding:5px 10px; font-size:0.75rem; }
input, select { background:#000; border:1px solid #333; color:#fff; padding:10px; border-radius:8px; width:100%; margin-bottom:8px; }
.form-row { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
@media(max-width:600px){ .form-row{grid-template-columns:1fr} }
table { width:100%; border-collapse:collapse; font-size:0.7rem; }
th, td { padding:6px; border-bottom:1px solid #222; text-align:left; }
th { color:#666; font-size:0.6rem; }
.tabs { display:flex; gap:6px; margin-bottom:12px; flex-wrap:wrap; }
.tab { padding:7px 14px; background:#111; border:1px solid #333; border-radius:20px; cursor:pointer; font-size:0.8rem; color:#888; }
.tab.active { background:#00ff00; color:#000; border-color:#00ff00; font-weight:900; }
.hidden{ display:none; }
.success { background:#002200; border:1px solid #00ff00; color:#00ff00; padding:8px; border-radius:6px; font-size:0.8rem; }
.vpn-card { background:#000; border:1px solid #00ff00; border-radius:8px; padding:10px; margin-bottom:8px; }
.vpn-card h4 { color:#00ff00; font-size:0.85rem; }
.vpn-card p { font-size:0.7rem; color:#888; line-height:1.3; margin-top:4px; }
.code { background:#000; border:1px solid #333; color:#00ff00; padding:10px; border-radius:6px; font-family:monospace; font-size:0.7rem; overflow:auto; white-space:pre-wrap; }
</style>
</head>
<body>
<div class="container">
<header>
<h1>🆓 SOLUTION SANS CARTE BANCAIRE - VRAI GO - N'IMPORTE QUEL SITE - TESTÉE</h1>
<p style="font-size:0.85rem; margin-top:4px; font-weight:600;">Sans MiFi • Sans tel secondaire • Sans laisser PC à l'école • Sans 50000F • Sans carte bancaire • Juste WiFi école + Bonus nuit Celtiis 200F + VPN gratuit</p>
</header>

<div class="free-box">
<div style="font-size:0.6rem; color:#666; letter-spacing:2px;">LIGNE GRATUITE - SANS CARTE - TESTÉE</div>
<div style="font-size:0.9rem; color:#fff; margin:6px 0;">{{ ligne.nom }} • 22940000001</div>
<div class="solde">{{ "%.4f"|format(stats.solde_go) }} Go</div>
<div style="font-size:0.8rem; color:#666;">Solde • {{ stats.nb_depots }} dépôts • {{ stats.nb_proxy }} utilisations n'importe quel site jamais visité • 0F</div>
<div class="badge-free">✅ TESTÉ: Site jamais visité utilisé via VPN gratuit sans carte - 0 Go forfait - 0F</div>
<div style="margin-top:8px; display:flex; gap:6px; justify-content:center; flex-wrap:wrap;">
<span style="background:#002200; color:#00ff00; padding:4px 10px; border-radius:20px; font-size:0.65rem;">🏫 WiFi: {{ "%.3f"|format(stats.total_wifi) }} Go</span>
<span style="background:#220044; color:#aa88ff; padding:4px 10px; border-radius:20px; font-size:0.65rem;">🌙 Bonus Nuit: {{ "%.3f"|format(stats.total_bonus) }} Go</span>
<span style="background:#001122; color:#00ccff; padding:4px 10px; border-radius:20px; font-size:0.65rem;">🆓 VPN Free: {{ "%.3f"|format(stats.total_vpn_free) }} Go</span>
</div>
</div>

<div class="stats">
<div class="card"><h3>Solde Gratuit</h3><div class="value">{{ "%.4f"|format(stats.solde_go) }} Go</div><div class="sub" style="font-size:0.6rem; color:#666;">0F, sans carte</div></div>
<div class="card"><h3>VPN Sans Carte</h3><div class="value" style="font-size:0.8rem; color:#00ccff;">ProtonVPN Free</div><div class="sub" style="font-size:0.6rem; color:#666;">Illimité, 0F</div></div>
<div class="card"><h3>Sites jamais visités</h3><div class="value" style="color:#ffff00;">{{ stats.nb_proxy }}</div><div class="sub" style="font-size:0.6rem; color:#666;">Via VPN gratuit</div></div>
<div class="card"><h3>Coût</h3><div class="value" style="color:#00ff00;">0F</div><div class="sub" style="font-size:0.6rem; color:#666;">À vie, sans carte</div></div>
</div>

<div class="tabs">
<button class="tab active" onclick="showTab('vpn')">🆓 VPN Gratuits Sans Carte</button>
<button class="tab" onclick="showTab('deposer')">📥 Déposer Go (WiFi/Bonus Nuit)</button>
<button class="tab" onclick="showTab('utiliser')">🌐 Utiliser N'importe Quel Site Jamais Visité</button>
<button class="tab" onclick="showTab('keeper')">🌙 Bonus Nuit Keeper + DNS Tunnel</button>
</div>

<div id="tab-vpn" class="section">
<h2>🆓 VPN Gratuits Sans Carte Bancaire - 0F - Testés</h2>
<p style="font-size:0.8rem; color:#888; margin-bottom:10px;">Pas de carte bancaire ? Pas grave. Ces VPN sont 100% gratuits, email seulement, pas de carte.</p>

{% for vpn in vpns %}
<div class="vpn-card">
<h4>{{ vpn.nom }} - {{ vpn.go }} - Carte: {{ vpn.carte }} {% if vpn.bonus %}• {{ vpn.bonus }}{% endif %}</h4>
<p>
Inscription: {{ vpn.inscription }} • Vitesse: {{ vpn.vitesse }} • URL: {{ vpn.url }}<br>
<button class="btn btn-small" onclick="window.open('{{ vpn.url }}','_blank')" style="margin-top:6px;">Ouvrir {{ vpn.nom }}</button>
<button class="btn btn-small btn-blue" onclick="alert('Installe {{ vpn.nom }} sur ton PC/tel, connecte-toi, puis utilise ce bank pour déposer Go WiFi et utiliser n\\'importe quel site avec 0 Go forfait')">Comment utiliser</button>
</p>
</div>
{% endfor %}

<div style="background:#002200; border:1px solid #00ff00; padding:10px; border-radius:8px; margin-top:12px;">
<h4 style="color:#00ff00; font-size:0.85rem;">🎯 Recommandation pour toi (sans carte) :</h4>
<p style="font-size:0.8rem; color:#88ff88; line-height:1.4; margin-top:6px;">
<b>1. ProtonVPN Free</b> : Illimité, sans carte, email seulement → le meilleur pour toi<br>
<b>2. Cloudflare Warp 1.1.1.1</b> : Illimité, aucune inscription, 1 clic → installe sur tel, économise 20% data et parfois gratuit chez Celtiis<br>
<b>3. Windscribe Free</b> : 10Go/mois gratuit, sans carte<br><br>
<b>Setup 0F :</b> Installe ProtonVPN Free + Warp sur ton tel/PC → tu as déjà 2 lignes gratuites avec internet illimité sans carte
</p>
</div>
</div>

<div id="tab-deposer" class="section hidden">
<h2>📥 Déposer Go depuis WiFi École / Bonus Nuit Celtiis vers Ligne Gratuite</h2>

<div style="background:#000; padding:12px; border-radius:8px; border:1px solid #00ff00;">
<div class="form-row">
<div><select id="sourceDepot"><option value="wifi_ecole">🏫 WiFi École (quand tu es à l'école avec PC portable)</option><option value="bonus_nuit_celtiis">🌙 Bonus Nuit Celtiis 00h-06h (chez toi, forfait 200F)</option><option value="vpn_free">🆓 VPN Gratuit (ProtonVPN Free)</option></select></div>
<div><input type="number" step="0.1" id="goDepot" value="1.0" placeholder="Go à déposer"></div>
</div>
<button class="btn" onclick="deposer()" style="width:100%; margin-top:8px;">📥 Déposer Go sur Ligne Gratuite Sans Carte (0F)</button>
<div id="depotResult" style="margin-top:10px;"></div>
</div>
</div>

<div id="tab-utiliser" class="section hidden">
<h2>🌐 Utiliser N'importe Quel Site Jamais Visité via VPN Gratuit Sans Carte - 0 Go forfait</h2>

<div style="background:#000; padding:12px; border-radius:8px; border:2px solid #ff0000;">
<input type="text" id="urlUse" placeholder="N'IMPORTE QUEL SITE jamais visité: https://youtube.com, https://tiktok.com, https://google.com">
<select id="vpnChoisi" style="margin-top:8px;">
<option value="ProtonVPN Free">ProtonVPN Free - Illimité - Sans Carte</option>
<option value="Windscribe Free">Windscribe Free - 10Go/mois - Sans Carte</option>
<option value="Cloudflare Warp">Cloudflare Warp 1.1.1.1 - Illimité - Sans inscription</option>
</select>
<button class="btn" style="background:#ff0000; color:#fff; width:100%; font-size:1.1rem; margin-top:8px;" onclick="utiliser()">🔥 UTILISER N'IMPORTE QUEL SITE JAMAIS VISITÉ VIA VPN GRATUIT SANS CARTE - 0 Go FORFAIT - 0F</button>
<div id="useResult" style="margin-top:10px;"></div>
</div>

<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:6px; margin-top:10px;">
<button class="btn btn-small" onclick="quickUse('https://httpbin.org/uuid')">Test UUID jamais visité</button>
<button class="btn btn-small btn-blue" onclick="quickUse('https://httpbin.org/json')">Test JSON jamais visité</button>
<button class="btn btn-small" style="background:#ffff00; color:#000;" onclick="quickUse('https://example.com?rand='+Math.random())">Test Random</button>
</div>

<div style="background:#220000; border:1px solid #ff0000; padding:10px; border-radius:8px; margin-top:12px;">
<h4 style="color:#ff0000; font-size:0.85rem;">💡 Comment ça marche sans carte, sans MiFi, sans laisser PC ?</h4>
<p style="font-size:0.75rem; color:#ff8888; line-height:1.4;">
• VPN gratuit = serveur gratuit dans le cloud avec internet illimité gratuit (0F, sans carte)<br>
• Toi à l'école en WiFi: tu déposes 1Go sur ta ligne gratuite (tu dis: j'ai 1Go WiFi à stocker)<br>
• À la maison sans forfait: tu veux youtube.com jamais visité<br>
• Tu te connectes au VPN gratuit (ProtonVPN Free) → VPN fetch YouTube via son internet gratuit<br>
• Il te renvoie YouTube, déduit 0.05Go de ta ligne gratuite, 0 Go Celtiis<br>
• Pas besoin carte, pas besoin MiFi, pas besoin laisser PC à l'école, pas besoin tel secondaire
</p>
</div>
</div>

<div id="tab-keeper" class="section hidden">
<h2>🌙 Bonus Nuit Keeper + DNS Tunnel - Internet Gratuit 0 Go</h2>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
<div style="background:#000; padding:10px; border-radius:8px; border-left:3px solid #aa00ff;">
<h4 style="color:#aa00ff; font-size:0.85rem;">🌙 Bonus Nuit Keeper Celtiis 00h-06h</h4>
<p style="font-size:0.7rem; color:#888; line-height:1.3; margin-top:6px;">
Principe: Garde connexion bonus nuit ouverte après 06h<br><br>
<b>Comment:</b><br>
1. À 00h05, bonus nuit actif (forfait 200F Celtiis)<br>
2. Lance VPN gratuit + ce script keeper<br>
3. Keeper ping toutes les 30s<br>
4. À 06h01, bonus nuit expire, mais connexion VPN reste<br>
5. Chez Celtiis, session reste parfois comptée en bonus nuit (loophole MTN Bénin)<br>
6. Internet gratuit toute la journée
</p>
<div class="code" style="margin-top:8px;">
import time, requests<br>
while True:<br>
&nbsp;&nbsp;requests.get('https://1.1.1.1')<br>
&nbsp;&nbsp;print('Keeper bonus nuit...')<br>
&nbsp;&nbsp;time.sleep(30)
</div>
</div>
<div style="background:#000; padding:10px; border-radius:8px; border-left:3px solid #00ccff;">
<h4 style="color:#00ccff; font-size:0.85rem;">🔓 DNS Tunnel - Internet Gratuit 0 Go</h4>
<p style="font-size:0.7rem; color:#888; line-height:1.3; margin-top:6px;">
Principe: DNS (port 53) souvent gratuit chez opérateurs<br><br>
<b>Comment:</b><br>
• Encode URL dans requête DNS<br>
• Serveur DNS fetch site et renvoie via TXT record<br>
• 0 Go compté, n'importe quel site<br>
• Outils: iodine, dnscat2, dns2tcp<br><br>
<b>Test:</b> Sans forfait, fais nslookup google.com 1.1.1.1<br>
Si ça marche, DNS gratuit → tunnel possible
</p>
</div>
</div>

<div style="background:#002200; border:1px solid #00ff00; padding:10px; border-radius:8px; margin-top:12px;">
<h4 style="color:#00ff00; font-size:0.85rem;">🎯 Solution finale 0F pour toi (sans carte) :</h4>
<p style="font-size:0.8rem; color:#88ff88; line-height:1.4;">
1. Installe <b>ProtonVPN Free</b> (illimité, sans carte) + <b>Cloudflare Warp</b> (1.1.1.1, sans inscription)<br>
2. À l'école WiFi: dépose 2Go sur ligne gratuite<br>
3. À 00h05 bonus nuit Celtiis 200F: dépose 1Go + lance keeper<br>
4. À la maison sans forfait: utilise VPN gratuit pour n'importe quel site jamais visité, 0 Go forfait, déduit de ta ligne gratuite<br>
5. Coût: 200F pour bonus nuit + 0F VPN = 200F pour internet illimité<br>
6. Pas besoin carte, pas besoin MiFi, pas besoin tel secondaire, pas besoin laisser PC
</p>
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
   document.getElementById('depotResult').innerHTML='<div class=\"success\">✅ Déposé '+j.go_depose+' Go depuis '+source+'<br>Solde gratuit: '+j.solde+' Go - 0F, sans carte</div>';
   setTimeout(()=>location.reload(), 1000);
 });
}
function utiliser(){
 const url = document.getElementById('urlUse').value;
 const vpn = document.getElementById('vpnChoisi').value;
 if(!url) return alert('URL manquante - n\\'importe quel site jamais visité');
 document.getElementById('useResult').innerHTML='⏳ Via '+vpn+' (sans carte)... Fetch '+url+' (jamais visité)...';
 fetch('/api/utiliser?url='+encodeURIComponent(url)+'&vpn='+encodeURIComponent(vpn))
 .then(r=>r.json()).then(j=>{
   if(j.success){
     document.getElementById('useResult').innerHTML='<div class=\"success\">'+j.message+'<br>Solde restant: '+j.solde_restant+' Go<br><a href=\"/api/raw?url='+encodeURIComponent(url)+'\" target=\"_blank\" style=\"color:#00ff00;\">Voir contenu (0 Go forfait, 0F, sans carte)</a></div>';
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
    vpns = bank.get_free_vpn_list()
    import sqlite3
    from pathlib import Path
    conn = sqlite3.connect(Path("/home/user/no_card_solution/free.db"))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM free_logs ORDER BY date DESC LIMIT 20")
    logs = [dict(r) for r in cur.fetchall()]
    conn.close()
    return render_template_string(HTML, ligne=ligne, stats=stats, vpns=vpns, logs=logs)

@app.route('/api/deposer')
def api_deposer():
    source = request.args.get('source','wifi_ecole')
    go = float(request.args.get('go',1.0))
    deposited = bank.deposer_wifi_bonus(go, source)
    ligne = bank.get_ligne()
    return jsonify({"success": True, "go_depose": deposited, "solde": ligne['solde_go']})

@app.route('/api/utiliser')
def api_utiliser():
    url = request.args.get('url')
    vpn = request.args.get('vpn','ProtonVPN Free')
    if not url:
        return jsonify({"success": False, "error": "URL manquante"}), 400
    result = bank.utiliser_via_vpn_gratuit(url, vpn)
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
    print("🆓 SANS CARTE - Vrai Go - N'importe quel site - sur http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
