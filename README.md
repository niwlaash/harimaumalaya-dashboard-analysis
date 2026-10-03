# 🐅 Harimau Malaya Performance Intelligence Hub

A professional, editorial-grade football intelligence and tactical analysis platform built for the **Malaysia National Football Team (Harimau Malaya)**, recent international call-up pools (2023–2026 cycle), and domestic/overseas prospects.

Inspired by premier performance analysis and data platforms like **The Analyst (Opta)**, **FBref / StatsBomb**, and **Wyscout**, this system fuses verified data from **Transfermarkt**, **FotMob**, and **SofaScore** into a real-time Head Coach & Performance Analyst (PA) workbench.

---

## 🌟 Key Features

### 1. 🏟️ Tactical Board & Starting XI Customizer
- **Interactive Lineup Customizer**: Freely assign and swap any of the 11 starting positions on the pitch (**4-3-3**, **3-4-3**, **4-2-3-1**).
- **Opta-Inspired Tactical Pitch**: Clean, high-density editorial pitch with position roles (`[GK]`, `[LB]`, `[CB]`, `[DM]`, `[CF]`, `[RW]`).
- **Real-Time Team Tactical Balance Indices**: Automatically calculates live team metrics whenever a player is swapped:
  - *Attacking Threat* (0–100)
  - *Defensive Solidity* (0–100)
  - *Pressing Index* (0–100)
  - *Build-Up Fluidity* (0–100)
  - *Aerial Dominance* (0–100)
  - *Average Starting XI Age*

### 2. 👤 Player Profile, Headshots & 2D Action Heatmaps
- **Verified Official Headshots**: Real player face portraits pulled directly from Transfermarkt CDN.
- **2D Touch & Action Density Heatmaps**: Authentic SofaScore / WhoScored density mesh mapped across pitch thirds:
  - Defensive 3rd %, Middle 3rd %, Attacking 3rd %.
  - Left Flank %, Central Channel %, Right Flank %.
- **Performance Radar**: Multi-attribute polygon chart and per-90 metrics.
- **Form Curve**: 5-match form curve from FotMob against the 7.0 benchmark.

### 3. 🔄 Performance Analyst (PA) Substitution & Call-Up Delta
- Compare starter (Player OUT) vs rotation option / new call-up (Player IN) side-by-side.
- **Attribute Delta Matrix ($\Delta$)**: Quantifies exact variances in Pace, Shooting, Passing, Defending, Physicality, and Work Rate.
- **Automated PA Tactical Briefing**: Outlines tactical advantages gained vs tactical trade-offs and structural concessions.

### 4. 🇲🇾 Recent Internationals Pool (2023–2026 Cycle)
- Senior players who represented Malaysia over the last 3 years (AFC Asian Cup Qatar, World Cup Qualifiers, Merdeka Cup) who remain in the active selection pool:
  - **Matthew Davies** (Johor Darul Ta'zim) – Starting RB & Vice-Captain in Asian Cup.
  - **Dominic Tan** (Sabah FC) – Starting CB in Asian Cup.
  - **Shahrul Saad** (Johor Darul Ta'zim) – Experienced central defender (56 caps).
  - **Junior Eldstål** (Johor Darul Ta'zim) – Physical aerial defender (1.91m).
  - **Syamer Kutty Abba** (Penang FC) – Starting DM in Asian Cup.
  - **Safawi Rasid** (Terengganu FC) – Active top scorer with 21 international goals.
  - **Akhyar Rashid** (Terengganu FC) – Dynamic 1v1 dribbler & transitional outlet.
  - **Darren Lok** (Sabah FC) – Relentless pressing forward in Asian Cup.
  - **Romel Morales** (Johor Darul Ta'zim) – Scored dramatic 90+15' equalizer vs South Korea in Asian Cup.
  - **Brendan Gan** (KL City FC) – Veteran midfield engine & leader.
  - **Endrick dos Santos** (Ho Chi Minh City FC / JDT) – Asian Cup naturalized midfielder.
  - **Azam Azmi** (Terengganu FC / JDT) – Starting RB in World Cup Qualifiers.

### 5. 🔭 National Prospect & Heritage Scouting (In-League & Foreign)
- In-depth scouting tracking for 17 youth starlets and diaspora/heritage prospects:
  - **Domestic League (MSL)**: Mukhairi Ajmal (Selangor FC), Sikh Izhan (Penang FC), Alif Ikmalrizal (Penang FC), Hakimi Abdullah (Terengganu FC), Haqimi Azim (KL City FC), T. Saravanan (Sri Pahang FC), Daniel Amier (Kuching City), Zhafri Yahya (KL City FC).
  - **Foreign Leagues**: Luqman Hakim (YSCC Yokohama, J3), Wan Kuzain (St. Louis City SC, MLS), Wan Kuzri (USA), Mats Deijl (Go Ahead Eagles, Eredivisie), Ferdy Druijf (Rapid Vienna, Austria), Richard Chin (England), Kobe Chong (England), Jaami Qureshi (Brighton Academy), Samuel Somerville (Selangor FC).
- **Scouting Readiness Index (1–100)**: Quantitative algorithm evaluating league strength coefficient, playing minutes volume, recent ratings, and age curve.

### 6. 📊 Performance Metrics & Minutes Tracker
- Verified minutes distribution across Malaysia Super League, J1 League (Japan), Thai League 1 (Thailand), and Cyprus League.
- Age vs Market Value quadrant mapping.
- Instant CSV export for scouting reports.

---

## 📁 Directory Structure

```
harimaumalaya-dashboard-analysis/
├── app.py                         # Master Streamlit Application
├── requirements.txt               # Dependencies
├── .gitignore                     # Git Rules
├── README.md                      # Documentation
├── data/
│   ├── squad_asean_2026.json      # 23-Man ASEAN Cup Squad + Photos + 26/27 Mins
│   ├── past_internationals_3yrs.json # 12 Senior Internationals (2023-2026 Cycle)
│   └── malaysian_prospects.json   # 17 Global Prospects & Heritage Pool
└── src/
    ├── data_collectors/           # Collectors & Aggregator
    │   ├── transfermarkt_collector.py
    │   ├── fotmob_collector.py
    │   ├── sofascore_collector.py
    │   └── aggregator.py
    ├── analytics/
    │   ├── metrics.py             # Performance Scoring & Archetypes
    │   └── tactical_engine.py     # Team Balance & Player Swap Delta Engine
    └── visualizations/
        ├── pitch.py               # Opta 2D Tactical Pitch Board
        ├── heatmap.py             # 2D Pitch Touch Density Heatmaps
        ├── radar.py               # Attribute & Comparison Radars
        └── charts.py              # Statistical Charts
```

---

## 🚀 Quickstart

```bash
git clone https://github.com/niwlaash/harimaumalaya-dashboard-analysis.git
cd harimaumalaya-dashboard-analysis
pip install -r requirements.txt
streamlit run app.py
```
Open `http://localhost:8501` in your browser.
