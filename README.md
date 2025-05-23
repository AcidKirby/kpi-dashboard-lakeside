# 📊 KPI Dashboard – Lake Side Mania

Dit project is een interactief dashboard dat de prestaties van het bedienend personeel vergelijkt met die van een serveerrobot op basis van zes KPI’s. Het dashboard is ontwikkeld tijdens sprint **DP22** in samenwerking tussen **Eninio** en **Arion**.

## 🎯 Doel van het dashboard
Het doel is om de effectiviteit en efficiëntie van personeel en robot inzichtelijk te maken op basis van real-time gegevens uit het restaurant van Lake Side Mania. De visualisaties ondersteunen de besluitvorming over mogelijke technologische implementaties in de bediening.

---

## 🔍 KPI's die in dit dashboard worden weergegeven

| # | KPI | Verantwoordelijke |
|---|-----|--------------------|
| 1 | **Bezorgsnelheid in seconden** (Robot vs Personeel) | Timothy |
| 2 | **Aantal opgepikte orders per uur** | Tim |
| 3 | **Aantal fouten per dag (<6 score)** | Johannes |
| 4 | **Klanttevredenheid jongeren (≤ 45 jaar)** | Eninio |
| 5 | **Kosten per dag – personeel vs robot** | Jaden |
| 6 | **Beschikbaarheid personeel vs robot** | Arion |

---

## 🗂️ Mappenstructuur

```
/kpi-dashboard-lakeside/
├── data/                   # Ingevoerde data (Excel, JSON)
│   ├── besteldata-2.xlsx
│   └── robot_restaurant_log.json
├── scripts/                # Python-scripts per KPI
│   ├── kpi1_bezorgsnelheid.py
│   ├── ...
├── visuals/                # PNG-afbeeldingen van de grafieken
│   ├── 01_bezorgsnelheid.png
│   ├── ...
├── dashboard_mockup.pdf   # High fidelity ontwerp van het dashboard
└── README.md              # Dit bestand
```

---

## 🛠️ Tools gebruikt

- Python (Pandas, Matplotlib, Seaborn)
- Jupyter Notebook / PyCharm
- Figma (voor het dashboardontwerp)
- GitHub (samenwerking en versiebeheer)

---

## 📎 Link naar ontwerp

👉 **TBA**

---

## 👥 Samenwerking

- **Timothy**: Data-analyse, Python-scripts, grafieken, technische implementatie  
- **Arion**: Ontwerp dashboard, structuur mock-up, documentatie

---

## 🧠 Inzichten

- De robot is gemiddeld sneller en consistenter dan personeel.
- Jongere klanten zijn net iets meer tevreden over robotservice.
- Kosten per dag liggen lager bij de robot, maar beschikbaarheid is iets minder door storingen.
- Het dashboard ondersteunt de business case uit het projectplan.

---

## 📬 Contact

Voor vragen of feedback: neem contact op met **Eninio & Arion** via het Windesheim leerteam.
