from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/recommendations')
def recommendations():

    stocks = [

        {
            "stock":"Marico",
            "signal":"BUY",
            "entry":"841",
            "target":"880",
            "stoploss":"824",
            "note":"Defensive FMCG momentum setup"
        },

        {
            "stock":"Triveni Turbine",
            "signal":"BUY",
            "entry":"607",
            "target":"642",
            "stoploss":"590",
            "note":"Strong continuation breakout"
        },

        {
            "stock":"Arvind",
            "signal":"BUY",
            "entry":"451",
            "target":"495",
            "stoploss":"429",
            "note":"Bullish textile setup"
        },

        {
            "stock":"Info Edge",
            "signal":"SELL",
            "entry":"Weak",
            "target":"Lower",
            "stoploss":"Avoid Fresh Buy",
            "note":"Brokerage bearish outlook"
        }

    ]

    random.shuffle(stocks)

    return jsonify(stocks)

if __name__ == '__main__':
    app.run(debug=True)
