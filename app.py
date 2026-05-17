from flask import Flask, jsonify
import random

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Live ET Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0f172a;color:white;font-family:Arial;padding:25px;}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:25px;}
.title{font-size:32px;font-weight:bold;color:#38bdf8;}
.sub{color:#94a3b8;margin-top:5px;}
.refresh-btn{background:#2563eb;border:none;color:white;padding:12px 20px;border-radius:12px;cursor:pointer;font-size:16px;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px;}
.card{background:#111827;border-radius:20px;padding:20px;border:1px solid rgba(255,255,255,0.08);}
.stock{font-size:24px;font-weight:bold;margin-bottom:10px;}
.signal{display:inline-block;padding:6px 14px;border-radius:50px;margin-bottom:18px;font-size:13px;font-weight:bold;}
.buy{background:#14532d;color:#4ade80;}
.sell{background:#7f1d1d;color:#f87171;}
.row{display:flex;justify-content:space-between;margin-bottom:12px;border-bottom:1px dashed rgba(255,255,255,0.08);padding-bottom:10px;}
.target{color:#22c55e;}
.sl{color:#ef4444;}
.note{margin-top:15px;color:#cbd5e1;line-height:1.5;}
.loader{display:none;margin-bottom:20px;color:#38bdf8;}
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="title">ET LIVE STOCK DASHBOARD</div>
        <div class="sub">Live Recommendation Feed</div>
    </div>
    <button onclick="loadData()" class="refresh-btn">Refresh</button>
</div>
<div class="loader" id="loader">Fetching latest recommendations...</div>
<div class="grid" id="grid"></div>
<script>
function createCard(item){
    return `
    <div class="card">
        <div class="stock">${item.stock}</div>
        <div class="signal ${item.signal.toLowerCase()}">${item.signal}</div>
        <div class="row"><span>Entry</span><span>${item.entry}</span></div>
        <div class="row"><span>Target</span><span class="target">${item.target}</span></div>
        <div class="row"><span>Stoploss</span><span class="sl">${item.stoploss}</span></div>
        <div class="note">${item.note}</div>
    </div>`;
}
async function loadData(){
    document.getElementById('loader').style.display='block';
    const response = await fetch('/api/recommendations');
    const data = await response.json();
    document.getElementById('grid').innerHTML = data.map(createCard).join('');
    document.getElementById('loader').style.display='none';
}
loadData();
</script>
</body>
</html>"""


@app.route('/')
def home():
    return HTML


@app.route('/api/recommendations')
def recommendations():
    stocks = [
        {"stock":"Marico","signal":"BUY","entry":"841","target":"880","stoploss":"824","note":"Defensive FMCG momentum setup"},
        {"stock":"Triveni Turbine","signal":"BUY","entry":"607","target":"642","stoploss":"590","note":"Strong continuation breakout"},
        {"stock":"Arvind","signal":"BUY","entry":"451","target":"495","stoploss":"429","note":"Bullish textile setup"},
        {"stock":"Info Edge","signal":"SELL","entry":"Weak","target":"Lower","stoploss":"Avoid Fresh Buy","note":"Brokerage bearish outlook"}
    ]
    random.shuffle(stocks)
    return jsonify(stocks)


if __name__ == '__main__':
    app.run(debug=False)
