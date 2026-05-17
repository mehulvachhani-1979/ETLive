from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

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
.error{color:#f87171;margin:20px 0;}
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
<div id="error" class="error" style="display:none"></div>
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
    document.getElementById('error').style.display='none';
    document.getElementById('grid').innerHTML='';
    try {
        const response = await fetch('/api/recommendations');
        const data = await response.json();
        if(data.error){
            document.getElementById('error').innerText = data.error;
            document.getElementById('error').style.display='block';
        } else {
            document.getElementById('grid').innerHTML = data.map(createCard).join('');
        }
    } catch(e) {
        document.getElementById('error').innerText = 'Failed to load data. Please try again.';
        document.getElementById('error').style.display='block';
    }
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
    try:
        url = "https://munafasutra.com/nse/BestIntradayTips"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        stocks = []
        rows = soup.select("table tr")

        for row in rows[1:21]:  # skip header, get up to 20 rows
            cols = row.find_all("td")
            if len(cols) >= 5:
                name_tag = cols[0].find("a")
                name = name_tag.text.strip() if name_tag else cols[0].text.strip()
                # Clean name: remove NSE symbol part after " - "
                if " - " in name:
                    name = name.split(" - ")[0].strip()

                signal = cols[1].text.strip().upper()
                entry  = cols[2].text.strip()
                target = cols[3].text.strip()
                sl     = cols[5].text.strip() if len(cols) > 5 else cols[4].text.strip()

                stocks.append({
                    "stock": name,
                    "signal": signal,
                    "entry": entry,
                    "target": target,
                    "stoploss": sl,
                    "note": "Live NSE Intraday Tip — MunafaSutra"
                })

        if not stocks:
            return jsonify({"error": "No data scraped. Site may have changed structure."})

        return jsonify(stocks)

    except Exception as e:
        return jsonify({"error": f"Scraping failed: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=False)
