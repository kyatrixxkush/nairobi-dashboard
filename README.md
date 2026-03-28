# 🌍 Nairobi Live Dashboard

A mobile-friendly live dashboard showing real-time Nairobi weather, Kenya news headlines, and KES currency exchange rates — all pulled from live APIs and auto-refreshing every 5 minutes.

Built by **Kimani Mukundi** as a portfolio project.

---

## ✨ Features

- 🌤 **Live weather** — temperature, feels like, humidity, wind speed, sunrise/sunset
- 📅 **5-day forecast** — daily conditions and temperatures
- 💱 **Live exchange rates** — KES vs USD, EUR, GBP, TZS, UGX
- 📰 **Kenya news** — latest headlines with images and sources
- 🔄 **Auto-refresh** every 5 minutes
- 📱 **Mobile-friendly** responsive design
- 🌙 **Dark theme** — clean, modern UI

---

## 🛠️ Tech Stack

- **Python 3 + Flask** — backend and routing
- **OpenWeatherMap API** — weather and forecast data
- **NewsAPI** — Kenya news headlines
- **ExchangeRate-API** — live KES exchange rates
- **HTML + CSS + JavaScript** — frontend UI

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/kyatrixxkush/nairobi-dashboard.git
cd nairobi-dashboard
```

### 2. Add your API keys
Open `app.py` and replace the keys:
```python
WEATHER_KEY  = "your_openweathermap_key"
NEWS_KEY     = "your_newsapi_key"
EXCHANGE_KEY = "your_exchangerate_key"
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
Go to: **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
nairobi-dashboard/
├── app.py              # Flask app and API integrations
├── requirements.txt
├── templates/
│   └── index.html      # Dashboard UI
└── README.md
```

---

## 💡 Key Concepts Demonstrated

- Consuming multiple third-party REST APIs
- Flask routing and template rendering
- Real-time data display with auto-refresh
- Responsive mobile-friendly CSS design
- Error handling for external API calls
- JSON API endpoint for live refresh
