# 🎯 RailWeb – Railway Route Planner Backend API

**RailWeb** is a lightweight, clean backend API for **Indian railway route planning**.  
It focuses on **fast, precise route suggestions** and a smooth integration experience for apps and tools — without clutter, ads, or unnecessary complexity.

---

## 🎯 The Mission

Most railway route planners are either:
- bloated websites,  
- confusing apps, or  
- closed‑source services.

**RailWeb** is built to do **one job well**:
- Let users find **all possible routes** between any two Indian railway stations  
- With **valid train numbers, classes, and transfer recommendations**  
- While feeling **simple, developer‑friendly, and reliable**.

It is designed as a **learning‑focused, ethical, and open tool** for creators and hobbyists.

---

## 🚀 Features

🚉 **Multi‑Route Suggestions** – Discover all possible station‑to‑station routes  
📘 **Train‑Level Details** – Train numbers, classes, validities  
🔁 **Smart Transfer Logic** – Suggests realistic transfer points between trains  
💡 **Cost‑Aware Routes** – Prioritizes cheaper and faster options  
🌊 **Multiple Travel Modes** – AC, sleeper, local, and more (if available)  

🎨 **Developer‑Friendly JSON API**  
- Clean, consistent JSON responses  
- Simple HTTP requests from any app or frontend  
- Easy to integrate in Unity, React, Android, etc.

🧠 **Offline‑First Design**  
- Uses local text files for station and route data  
- No heavy external APIs required  
- Fast, local calculations  

🧼 **Clean & Minimal Structure**  
- No ads, no crapware  
- Single `app.py` Flask backend  
- Simple `algorithm.py` for core logic  

And much more under the hood.

---

## ⚠️ Ethical Use Disclaimer

🚨 **RailWeb does NOT support misuse.**

This software is intended for:
- Educational and learning purposes  
- Personal railway‑planning experiments  
- Publicly available, non‑copyrighted timetable data  

The developer is **not responsible** for misuse of this software.  

Please respect railway data sources and official terms.

---

## 📸 Screenshots (Example)

| View | Description |
|------|-------------|
| `app.py` | Core Flask backend with routes |
| `algorithm.py` | Clean route‑finding logic with `find_routes()` |
| `stations.txt` / `routes.txt` | Simple data files for station and route information |
| Postman / API Test | Example `POST /find-route` request and JSON output |

> *(You can add actual screenshots later and update this table.)*

---

## 🛠 Tech Stack

- **Language:** Python  
- **Backend:** Flask  
- **API Style:** RESTful JSON  
- **Data Format:** Plain text files (`stations.txt`, `routes.txt`)  
- **Dev Tools:** Postman (testing), Unity (client‑side integration)

---

## ⚙️ Local Setup

```bash
git clone https://github.com/yourusername/railweb.git
cd railweb
python -m venv venv
venv\Scripts\activate     # on Windows
pip install -r requirements.txt
python app.py
```

The API will launch at:  
`http://127.0.0.1:5000`

Example API call:

```bash
curl -X POST http://127.0.0.1:5000/find-route \
  -H "Content-Type: application/json" \
  -d '{"source": "SRE", "destination": "DDN"}'
```

---

## 👥 Contributing

1. Fork the repository  
2. Create your feature branch: `git checkout -b feature-name`  
3. Commit your changes  
4. Push to your branch  
5. Open a Pull Request 🚀  

We welcome:
- new route‑logic improvements  
- better JSON formatting  
- better docs or README examples  

---

## 📄 License

[MIT License](LICENSE)

---

Made with ❤️ by **Shikeb Khan**
