"""
app.py - Nairobi Live Dashboard
Author: Kimani Mukundi
Description: A live dashboard showing Nairobi weather, currency rates and Kenya news.
"""

from flask import Flask, render_template, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# ── API KEYS ──
WEATHER_KEY  = "7e6b2c1d72e198278a43ca00507aea7e"
NEWS_KEY     = "13f7d17a1e834c2e884aeef426a6bf10"
EXCHANGE_KEY = "4aad03ead61644a8261d61d8"


# ─────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────

def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Nairobi,KE&appid={WEATHER_KEY}&units=metric"
        r = requests.get(url, timeout=5)
        d = r.json()
        return {
            "temp":        round(d["main"]["temp"]),
            "feels_like":  round(d["main"]["feels_like"]),
            "humidity":    d["main"]["humidity"],
            "description": d["weather"][0]["description"].title(),
            "icon":        d["weather"][0]["icon"],
            "wind":        round(d["wind"]["speed"] * 3.6, 1),  # m/s to km/h
            "city":        d["name"],
            "country":     d["sys"]["country"],
            "sunrise":     datetime.fromtimestamp(d["sys"]["sunrise"]).strftime("%H:%M"),
            "sunset":      datetime.fromtimestamp(d["sys"]["sunset"]).strftime("%H:%M"),
        }
    except Exception as e:
        return {"error": str(e)}


def get_forecast():
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q=Nairobi,KE&appid={WEATHER_KEY}&units=metric&cnt=24"
        r = requests.get(url, timeout=5)
        d = r.json()
        # Get one entry per day (every 8th = 24h apart)
        days = {}
        for item in d["list"]:
            date = item["dt_txt"][:10]
            if date not in days:
                days[date] = {
                    "date":  datetime.strptime(date, "%Y-%m-%d").strftime("%a %d %b"),
                    "temp":  round(item["main"]["temp"]),
                    "icon":  item["weather"][0]["icon"],
                    "desc":  item["weather"][0]["description"].title(),
                }
        return list(days.values())[:5]
    except Exception as e:
        return []


def get_currency():
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_KEY}/latest/KES"
        r = requests.get(url, timeout=5)
        d = r.json()
        rates = d["conversion_rates"]
        # How many KES per 1 unit of foreign currency
        return {
            "USD": round(1 / rates["USD"], 2),
            "EUR": round(1 / rates["EUR"], 2),
            "GBP": round(1 / rates["GBP"], 2),
            "TZS": round(1 / rates["TZS"], 2),
            "UGX": round(1 / rates["UGX"], 2),
            "updated": datetime.now().strftime("%H:%M"),
        }
    except Exception as e:
        return {"error": str(e)}


def get_news():
    try:
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q=Kenya&language=en&sortBy=publishedAt"
            f"&pageSize=10&apiKey={NEWS_KEY}"
        )
        r = requests.get(url, timeout=5)
        d = r.json()
        articles = []
        for a in d.get("articles", []):
            if a.get("title") and a.get("title") != "[Removed]":
                articles.append({
                    "title":       a["title"],
                    "source":      a["source"]["name"],
                    "url":         a["url"],
                    "publishedAt": a["publishedAt"][:10],
                    "image":       a.get("urlToImage"),
                    "description": a.get("description", "")[:120] + "..." if a.get("description") else "",
                })
        return articles[:8]
    except Exception as e:
        return []


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def index():
    weather  = get_weather()
    forecast = get_forecast()
    currency = get_currency()
    news     = get_news()
    now      = datetime.now().strftime("%A, %d %B %Y — %H:%M")
    return render_template("index.html",
                           weather=weather, forecast=forecast,
                           currency=currency, news=news, now=now)


@app.route("/api/refresh")
def refresh():
    """JSON endpoint for live refresh without page reload."""
    return jsonify({
        "weather":  get_weather(),
        "currency": get_currency(),
        "news":     get_news(),
        "time":     datetime.now().strftime("%A, %d %B %Y — %H:%M"),
    })


if __name__ == "__main__":
    print("✅ Nairobi Dashboard running → http://127.0.0.1:5000")
    app.run(debug=True)
