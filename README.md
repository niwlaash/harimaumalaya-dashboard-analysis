# 🐅 Harimau Malaya Football Analytics & Scouting Dashboard

An advanced, multi-tiered football intelligence platform built for the **Malaysia National Football Team (Harimau Malaya)** and the entire prospective Malaysian player universe.

This project delivers comprehensive statistical profiling, tactical pitch visualization, per-90 metrics, form progression, and heritage scouting by fusing data from **Transfermarkt**, **FotMob**, and **SofaScore**.

---

## 🌟 Key Features

### 1. 🏟️ Tactical Squad Overview & Interactive Pitch
- **Tactical Pitch View**: Visualizes starting XI and depth chart in multiple formations (**4-3-3**, **3-4-3**, **4-2-3-1**).
- **Verified 2026/27 Playing Time**: Tracks exact cumulative club and national team minutes across the Malaysia Super League, J1 League (Japan), Thai League 1 (Thailand), and Cyprus League.
- **Squad KPI Banners**: Instant tracking of squad size, overseas player representation, goal contributions, and market values.

### 2. 👤 Player Deep Dive & Form Progression
- **Bio & Demographics**: Verified DOB, height, citizenship, preferred foot, and contract expiry.
- **Form Trend Tracker**: 5-match moving rating curve from FotMob and SofaScore.
- **Radar Profile**: Multi-attribute polygon chart (Pace, Shooting, Passing, Dribbling, Defending, Physicality).
- **Per-90 Statistical Percentiles**: Goals/90, Assists/90, Key Passes/90, Duels Won %, and Aerial Dominance.
- **Tactical Archetype Classifier**: Automatically groups players into roles (e.g. *Inverted Playmaker*, *Deep-Lying Regista*, *Ball-Playing Defender*, *Box-to-Box Engine*).

### 3. ⚔️ Head-to-Head Comparison Matrix
- Compare 2 or 3 players simultaneously (e.g., **Arif Aiman vs Faisal Halim vs Manuel Hidalgo**).
- Overlaid radar comparisons and side-by-side metric tables.

### 4. 🌍 Heritage & Prospect Scouting System
- Tracks domestic U23 starlets and eligible Malaysian diaspora/heritage players in Europe, North America, Australia, and Asia.
- **Eligibility Classification**:
  - Homegrown / Malaysian Born (e.g. Luqman Hakim, Mukhairi Ajmal, Sikh Izhan, Alif Ikmalrizal)
  - Heritage - Parents Malaysian (e.g. Wan Kuzain, Wan Kuzri)
  - Heritage - Grandparents / Ancestry (e.g. Richard Chin, Kobe Chong, Mats Deijl, Ferdy Druijf)
- **Scouting Readiness Index (1–100)**: Quantitative formula accounting for league coefficient, regular match minutes, recent ratings, and age peak curve.

### 5. 📈 Macro Analytics & Playing Time Distribution
- Cumulative minutes leaderboard.
- Goal contributions distribution (Goals vs Assists).
- Age vs Market Value quadrant mapping.
- Instant CSV export.

---

## 🛠️ Data Architecture & Collection Strategy

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│      TRANSFERMARKT      │     │         FOTMOB          │     │        SOFASCORE        │
│  • Biological & Demog.  │     │  • Per-Match Ratings    │     │  • Attribute Radars     │
│  • Verified 26/27 Mins  │     │  • xG / xA Metrics      │     │  • Positional Heatmaps  │
│  • Market Values        │     │  • Shot / Action Maps   │     │  • Per-90 Percentiles   │
└────────────┬────────────┘     └────────────┬────────────┘     └────────────┬────────────┘
             │                               │                               │
             └───────────────────────┬───────┴───────────────────────────────┘
                                     ▼
                         ┌───────────────────────┐
                         │    DATA AGGREGATOR    │
                         │  • Normalization      │
                         │  • Cache Layer        │
                         │  • Metric Enrichment  │
                         └───────────┬───────────┘
                                     ▼
                         ┌───────────────────────┐
                         │  STREAMLIT DASHBOARD  │
                         └───────────────────────┘
```

1. **Transfermarkt (`src/data_collectors/transfermarkt_collector.py`)**:
   - Primary source for biometrics, market valuation, transfer history, and official playing minutes.
   - Built with caching (`data/cache/transfermarkt/`) and request header spoofing.
2. **FotMob (`src/data_collectors/fotmob_collector.py`)**:
   - Ingests match-by-match ratings (6.0 – 10.0 scale) and expected metrics ($xG$, $xA$).
3. **SofaScore (`src/data_collectors/sofascore_collector.py`)**:
   - Provides attribute overviews, duel percentages, and touch maps.

---

## 📁 Project Directory Structure

```
harimaumalaya-dashboard-analysis/
├── app.py                      # Master Streamlit Application
├── requirements.txt            # Python Dependencies
├── .gitignore                  # Git Ignore Rules
├── README.md                   # Project Documentation
├── data/
│   ├── squad_asean_2026.json   # 23-Man ASEAN Cup 2026 Verified Roster
│   └── malaysian_prospects.json# Youth & Heritage Scouting Database
└── src/
    ├── data_collectors/
    │   ├── transfermarkt_collector.py
    │   ├── fotmob_collector.py
    │   ├── sofascore_collector.py
    │   └── aggregator.py
    ├── analytics/
    │   └── metrics.py          # Scouting Readiness & Archetypes
    └── visualizations/
        ├── pitch.py            # Plotly 2D Football Pitch
        ├── radar.py            # Attribute & Comparison Radars
        └── charts.py           # Minutes & Distribution Visuals
```

---

## 🚀 Quickstart & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/niwlaash/harimaumalaya-dashboard-analysis.git
cd harimaumalaya-dashboard-analysis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard
```bash
streamlit run app.py
```
Access the dashboard at `http://localhost:8501`.

---

## 🇲🇾 2026/27 Verified Squad Summary

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

---

## 📄 License
MIT License. Built for Malaysian football research and analytics.
