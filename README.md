# 🐅 Harimau Malaya Football Analytics & Tactical Workbench

An immersive, professional football intelligence and tactical analysis platform built for the **Malaysia National Football Team (Harimau Malaya)**, prospective heritage talents, and all-time legendary benchmarks.

Designed with an immersive **Football Manager (FM)** dark tactical UI, this system fuses verified data from **Transfermarkt**, **FotMob**, and **SofaScore** into a real-time Head Coach & Performance Analyst (PA) workbench.

---

## 🌟 Key Features

### 1. 🏟️ Tactical Board & Dynamic Starting XI Customizer (Coach Mode)
- **Interactive Lineup Customizer**: Freely assign and swap any of the 11 starting positions on the pitch (**4-3-3**, **3-4-3**, **4-2-3-1**).
- **FM-Style Pitch Board**: Deep tactical board with role tokens (`[GK]`, `[LB]`, `[CB]`, `[DM]`, `[IF]`, `[AF]`).
- **Real-Time Team Tactical Balance Indices**: Automatically calculates live team ratings whenever a player is swapped:
  - *Attacking Threat* (0–100)
  - *Defensive Solidity* (0–100)
  - *Pressing Intensity & Work Rate* (0–100)
  - *Passing Fluidity & Build-up* (0–100)
  - *Aerial Dominance* (0–100)
  - *Average Starting XI Age*

### 2. 👤 Player Profile, Face Portraits & 2D Tactical Heatmap
- **Verified Official Headshots**: Real player face portraits pulled directly from Transfermarkt CDN.
- **2D Touch & Action Density Heatmaps**: Authentic SofaScore / WhoScored density mesh mapped across pitch thirds:
  - Defensive 3rd %, Middle 3rd %, Attacking 3rd %.
  - Left Flank %, Central Channel %, Right Flank %.
- **FM Attribute Matrix**: Technical, Mental, and Physical attribute scores highlighted in classic Football Manager color tiers (Elite Neon Green, Good Sky Blue, Average Gold).
- **Form Progression**: 5-match form curve from FotMob against the 7.0 benchmark.

### 3. 🔄 Performance Analyst (PA) Swap & Substitution Delta
- Test substitutions side-by-side (e.g., swapping starter *Faisal Halim* for *Fergus Tierney* or *Luqman Hakim*).
- **Attribute Delta Matrix ($\Delta$)**: Quantifies exact variances in Pace, Shooting, Passing, Defending, Physicality, and Work Rate.
- **Automated PA Tactical Briefing**: Outlines tactical advantages gained vs tactical trade-offs and structural concessions.

### 4. 🏛️ Historical Legends & All-Time Benchmarks
- Benchmark active Harimau Malaya stars against all-time Malaysian legends:
  - **Mokhtar Dahari (SuperMokh)** – 89 international goals.
  - **Soh Chin Ann (Tauke)** – FIFA world-record 195 caps.
  - **Safiq Rahim** – AFF Suzuki Cup 2010 MVP & set-piece maestro.
  - **Safee Sali** – AFF 2010 Golden Boot winner.
  - **Aidil Zafuan**, **Brendan Gan**, **Amri Yahyah**, and **Badhri Radzi**.

### 5. 🌍 Global Prospects & Heritage Scouting Database
- In-depth scouting tracking for 17 youth starlets and diaspora/heritage prospects:
  - **Homegrown Stars**: Luqman Hakim (YSCC Yokohama), Mukhairi Ajmal, Sikh Izhan, Alif Ikmalrizal, Hakimi Abdullah, Haqimi Azim, T. Saravanan, Daniel Amier, Zhafri Yahya.
  - **Overseas Heritage**: Wan Kuzain (St. Louis City SC / MLS), Wan Kuzri (USA), Mats Deijl (Go Ahead Eagles / Eredivisie), Ferdy Druijf (Rapid Vienna), Richard Chin (England), Kobe Chong (England), Jaami Qureshi (Brighton Academy), Samuel Somerville.
- **Scouting Readiness Index (1–100)**: Algorithm evaluating league strength coefficient, playing minutes volume, recent ratings, and age curve.

### 6. 📊 Macro Analytics & Official 2026/27 Minutes Leaderboard
- Verified minutes distribution across Malaysia Super League, J1 League (Japan), Thai League 1 (Thailand), and Cyprus League.
- Age vs Market Value quadrant mapping.
- Instant CSV export for scouting reports.

---

## 📁 Directory Structure

```
harimaumalaya-dashboard-analysis/
├── app.py                         # Master Streamlit FM Application
├── requirements.txt               # Dependencies
├── .gitignore                     # Git Rules
├── README.md                      # Documentation
├── data/
│   ├── squad_asean_2026.json      # 23-Man ASEAN Cup Squad + Photos + 26/27 Mins
│   ├── malaysian_prospects.json   # 17 Global Prospects & Heritage Pool
│   └── legends_past_players.json  # 8 Historical Benchmarks & All-Time Legends
└── src/
    ├── data_collectors/           # Collectors & Aggregator
    │   ├── transfermarkt_collector.py
    │   ├── fotmob_collector.py
    │   ├── sofascore_collector.py
    │   └── aggregator.py
    ├── analytics/
    │   ├── metrics.py             # Scouting Readiness & Archetypes
    │   └── tactical_engine.py     # Team Balance & Player Swap Delta Engine
    └── visualizations/
        ├── pitch.py               # FM 2D Tactical Pitch Board
        ├── heatmap.py             # 2D Pitch Touch Density Heatmaps
        ├── radar.py               # Polygon & Comparison Radars
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

---

## 🇲🇾 2026/27 Squad Minutes Overview

| Player | Position | Club | League | 26/27 Mins |
|---|---|---|---|:---:|
| **Dion Cools** | Right-Back / CB | Cerezo Osaka | J1 League (Japan) | **720'** |
| **Arif Aiman** | Right Winger | Johor Darul Ta'zim | Malaysia Super League | **630'** |
| **Haziq Nadzli** | Goalkeeper | Kuching City FC | Malaysia Super League | **630'** |
| **Paulo Josué** | Centre-Forward | KL City FC | Malaysia Super League | **626'** |
| **Nooa Laine** | Central Midfield | Selangor FC | Malaysia Super League | **553'** |
| **Faisal Halim** | Left Winger | Selangor FC | Malaysia Super League | **541'** |
| **Bérgson** | Centre-Forward | Johor Darul Ta'zim | Malaysia Super League | **452'** |
| **Brad Tapp** | Centre-Back | Johor Darul Ta'zim | Malaysia Super League | **450'** |
| **Syihan Hazmi** | Goalkeeper | Johor Darul Ta'zim | Malaysia Super League | **450'** |
| **Ubaidullah Shamsul**| Centre-Back | Terengganu FC | Malaysia Super League | **447'** |
| **Quentin Cheng** | Right-Back | Selangor FC | Malaysia Super League | **443'** |
| **Azri Ghani** | Goalkeeper | Negeri Sembilan FC | Malaysia Super League | **379'** |
| **Nazmi Faiz** | Central Midfield | Kuching City FC | Malaysia Super League | **367'** |
| **Manuel Hidalgo** | Right Winger | Johor Darul Ta'zim | Malaysia Super League | **319'** |
| **Fergus Tierney** | Left Winger | Omonia 29th May | Cyprus League (Cyprus) | **319'** |
| **Syahir Bashah** | Central Midfield | Selangor FC | Malaysia Super League | **281'** |
| **La'Vere Corbin-Ong**| Left-Back | Johor Darul Ta'zim | Malaysia Super League | **278'** |
| **Harith Haiqal** | Centre-Back | Selangor FC | Malaysia Super League | **270'** |
| **Stuart Wilkin** | Central Midfield | Johor Darul Ta'zim | Malaysia Super League | **191'** |
| **Daniel Ting** | Left-Back | Ratchaburi FC | Thai League 1 (Thailand) | **107'** |
| **G. Pavithran** | Winger | Terengganu FC | Malaysia Super League | **100'** |
| **Hong Wan** | Defensive Midfield | Johor Darul Ta'zim | Malaysia Super League | **90'** |
| **Syahmi Safari** | Right-Back | Johor Darul Ta'zim | Malaysia Super League | **0'** |
