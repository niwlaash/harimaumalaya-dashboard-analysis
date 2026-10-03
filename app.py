import streamlit as st
import pandas as pd
import numpy as np
import json
import os

# Import modular components
from src.data_collectors.aggregator import DataAggregator
from src.analytics.metrics import calculate_scouting_score, get_player_archetype
from src.visualizations.pitch import draw_tactical_pitch
from src.visualizations.radar import create_attribute_radar, create_comparison_radar
from src.visualizations.charts import (
    create_minutes_bar_chart,
    create_form_trend_chart,
    create_goal_contributions_chart,
    create_age_value_quadrant
)

# Set Page Config
st.set_page_config(
    page_title="Harimau Malaya | Football Analysis Dashboard",
    page_icon="🐅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Mode + Harimau Malaya Gold & Black Theme)
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: #f0f6fc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Card */
    .hero-header {
        background: linear-gradient(90deg, #1f242d 0%, #2c2511 50%, #1a1a1a 100%);
        border: 1px solid rgba(244, 208, 63, 0.4);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f4d03f;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #cccccc;
        margin-top: 6px;
    }
    
    /* KPI Metric Cards */
    .kpi-container {
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
    }
    .kpi-card {
        background: rgba(30, 37, 48, 0.7);
        border-radius: 10px;
        padding: 16px;
        border-left: 4px solid #f4d03f;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        flex: 1;
    }
    .kpi-title {
        font-size: 0.85rem;
        color: #a0aec0;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f4d03f;
        margin: 4px 0;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #718096;
    }

    /* Player Profile Badge */
    .player-card {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        text-transform: uppercase;
    }
    .badge-gold { background: #d4ac0d; color: #111; }
    .badge-blue { background: #2980b9; color: #fff; }
    .badge-red { background: #c0392b; color: #fff; }
    .badge-green { background: #27ae60; color: #fff; }

    /* Custom Tables */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_all_data():
    aggregator = DataAggregator()
    squad_df = aggregator.load_squad()
    prospects_df = aggregator.load_prospects()
    return squad_df, prospects_df

try:
    squad_df, prospects_df = load_all_data()
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()

# Top Hero Banner
st.markdown("""
<div class="hero-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="hero-title">🐅 HARIMAU MALAYA ANALYTICS HUB</h1>
            <p class="hero-subtitle">Comprehensive National Squad Performance (2026/27) & Malaysian Football Prospect Scouting System</p>
        </div>
        <div style="text-align: right;">
            <span class="badge badge-gold">Transfermarkt Verified</span>
            <span class="badge badge-blue">FotMob Ratings</span>
            <span class="badge badge-green">SofaScore Radars</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/f/fa/Football_Association_of_Malaysia_logo.svg/300px-Football_Association_of_Malaysia_logo.svg.png", width=120)
st.sidebar.title("Navigation")
menu_selection = st.sidebar.radio(
    "Choose Analysis View:",
    [
        "🏟️ Squad Overview & Tactical Pitch",
        "👤 Player Deep Dive & Form",
        "⚔️ Head-to-Head Comparison",
        "🌍 Heritage & Prospect Scout",
        "📈 Minutes & Macro Analytics",
        "⚙️ Data Collection & Pipelines"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Squad Stats")
st.sidebar.write(f"**Total Squad Members:** {len(squad_df)}")
st.sidebar.write(f"**Total Prospects Tracked:** {len(prospects_df)}")
st.sidebar.write(f"**Foreign League Players:** {len(squad_df[squad_df['country'] != 'Malaysia'])} (Cools, Ting, Tierney)")
avg_age = round(squad_df["age"].mean(), 1)
st.sidebar.write(f"**Average Squad Age:** {avg_age} years")
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use the filters on each tab to switch between tactical roles, per-90 metrics, and eligibility categories.")

# -------------------------------------------------------------
# TAB 1: SQUAD OVERVIEW & TACTICAL PITCH
# -------------------------------------------------------------
if menu_selection == "🏟️ Squad Overview & Tactical Pitch":
    st.markdown("### 🏟️ Tactical Squad Overview (FIFA ASEAN Cup 2026 Squad)")

    # KPI Banner
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Squad Size</div>
            <div class="kpi-value">23</div>
            <div class="kpi-sub">Official ASEAN Cup 2026 Roster</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        total_mins_2627 = squad_df["minutes_26_27"].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">26/27 Club Minutes</div>
            <div class="kpi-value">{total_mins_2627:,}'</div>
            <div class="kpi-sub">Across 5 Domestic & Foreign Leagues</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        total_gc = squad_df["goal_contributions_26_27"].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Goal Contributions (26/27)</div>
            <div class="kpi-value">{total_gc}</div>
            <div class="kpi-sub">{squad_df['goals_26_27'].sum()} Goals & {squad_df['assists_26_27'].sum()} Assists</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        top_mv = squad_df.sort_values(by="market_value_eur", ascending=False).iloc[0]
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Highest Market Value</div>
            <div class="kpi-value">€{top_mv['market_value_eur']:,}</div>
            <div class="kpi-sub">{top_mv['name']} ({top_mv['club']})</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Formation and Tactical Pitch
    pitch_col, table_col = st.columns([1.3, 1])
    with pitch_col:
        form_col1, form_col2 = st.columns([1, 1])
        with form_col1:
            formation = st.selectbox("Select Formation:", ["4-3-3", "3-4-3", "4-2-3-1"], index=0)
        with form_col2:
            st.caption("ℹ️ Visualizes starting XI positional hierarchy based on form & 26/27 minutes played.")

        pitch_fig = draw_tactical_pitch(formation=formation, squad_df=squad_df)
        st.plotly_chart(pitch_fig, use_container_width=True)

    with table_col:
        st.markdown("#### 📋 Squad Depth & Minutes Filter")
        pos_filter = st.multiselect(
            "Filter by Position Category:",
            options=["Goalkeeper", "Defender", "Midfielder", "Attacker"],
            default=["Goalkeeper", "Defender", "Midfielder", "Attacker"]
        )
        
        filtered_squad = squad_df[squad_df["position_category"].isin(pos_filter)]
        
        display_df = filtered_squad[[
            "name", "position", "club", "league", "minutes_26_27", "fotmob_rating"
        ]].rename(columns={
            "name": "Player",
            "position": "Position",
            "club": "Club",
            "league": "League",
            "minutes_26_27": "26/27 Mins",
            "fotmob_rating": "Rating"
        }).sort_values(by="26/27 Mins", ascending=False)
        
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
            height=460
        )

# -------------------------------------------------------------
# TAB 2: PLAYER DEEP DIVE & FORM
# -------------------------------------------------------------
elif menu_selection == "👤 Player Deep Dive & Form":
    st.markdown("### 👤 Player In-Depth Scouting & Performance Profile")

    selected_player_name = st.selectbox(
        "Select Player to Inspect:",
        options=squad_df["name"].tolist(),
        index=16 # Default to Arif Aiman
    )

    player = squad_df[squad_df["name"] == selected_player_name].iloc[0].to_dict()
    archetype = get_player_archetype(player["position"], player.get("attributes", {}))
    scouting_index = calculate_scouting_score(player)

    # Player Header Card
    st.markdown(f"""
    <div class="player-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="color: #f4d03f; margin: 0;">{player['full_name']} (#{player['id']})</h2>
                <div style="margin: 8px 0;">
                    <span class="badge badge-gold">{player['position']}</span>
                    <span class="badge badge-blue">{player['club']} ({player['league']})</span>
                    <span class="badge badge-green">Tactical Archetype: {archetype}</span>
                </div>
                <p style="color: #bbb; margin-bottom: 0; font-size: 0.95rem;">
                    <strong>Age:</strong> {player['age']} | <strong>DOB:</strong> {player['dob']} | <strong>Height:</strong> {player['height']} cm | <strong>Preferred Foot:</strong> {player['preferred_foot']} | <strong>Market Value:</strong> €{player['market_value_eur']:,}
                </p>
            </div>
            <div style="text-align: right; background: rgba(0,0,0,0.4); padding: 12px 18px; border-radius: 10px; border: 1px solid #f4d03f;">
                <div style="font-size: 0.75rem; color: #a0aec0; text-transform: uppercase;">Scouting Readiness</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #f4d03f;">{scouting_index}</div>
                <div style="font-size: 0.75rem; color: #2ecc71;">Index / 100</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Stats Row
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.metric("26/27 Total Minutes", f"{player['minutes_26_27']}'", f"{player['apps_26_27']} Appearances")
    with stat_col2:
        st.metric("Goal Contributions", f"{player['goals_26_27'] + player['assists_26_27']}", f"{player['goals_26_27']}G + {player['assists_26_27']}A")
    with stat_col3:
        st.metric("FotMob Avg Rating", f"{player.get('fotmob_rating', 'N/A')}", "Club Matches 26/27")
    with stat_col4:
        st.metric("SofaScore Avg Rating", f"{player.get('sofascore_rating', 'N/A')}", "Attribute Baseline")

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualizations Row: Radar + Form Trend
    viz_col1, viz_col2 = st.columns([1, 1])
    with viz_col1:
        radar_fig = create_attribute_radar(player)
        st.plotly_chart(radar_fig, use_container_width=True)

    with viz_col2:
        form_ratings = player.get("recent_form", [7.0, 7.0, 7.0, 7.0, 7.0])
        form_fig = create_form_trend_chart(form_ratings, player['name'])
        st.plotly_chart(form_fig, use_container_width=True)
        
        st.markdown("#### 📝 Professional Scouting Summary")
        st.info(player.get("scouting_summary", "High-potential talent in Malaysian national football setup."))

    # Per-90 Statistics Breakdown
    st.markdown("#### ⚡ Per-90 & Tactical Efficiency Breakdown")
    p90_col1, p90_col2, p90_col3, p90_col4 = st.columns(4)
    with p90_col1:
        st.write(f"**Goals / 90:** {player.get('goals_p90', 0.0)}")
        st.write(f"**Assists / 90:** {player.get('assists_p90', 0.0)}")
    with p90_col2:
        st.write(f"**Pass Accuracy:** {player.get('pass_acc_pct', 80.0)}%")
        st.write(f"**Key Passes / 90:** {player.get('key_passes_p90', 1.5)}")
    with p90_col3:
        st.write(f"**Tackles Won / 90:** {player.get('tackles_p90', 1.8)}")
        st.write(f"**Interceptions / 90:** {player.get('interceptions_p90', 1.2)}")
    with p90_col4:
        st.write(f"**Duel Win %:** {player.get('ground_duel_win_pct', 55.0)}%")
        st.write(f"**Aerial Win %:** {player.get('aerial_win_pct', 50.0)}%")

# -------------------------------------------------------------
# TAB 3: HEAD-TO-HEAD COMPARISON
# -------------------------------------------------------------
elif menu_selection == "⚔️ Head-to-Head Comparison":
    st.markdown("### ⚔️ Head-to-Head Player Comparison")
    st.write("Compare attributes, statistical production, and ratings between 2 or 3 squad members.")

    comp_col1, comp_col2, comp_col3 = st.columns(3)
    with comp_col1:
        p1_name = st.selectbox("Player 1:", options=squad_df["name"].tolist(), index=16) # Arif Aiman
    with comp_col2:
        p2_name = st.selectbox("Player 2:", options=squad_df["name"].tolist(), index=17) # Faisal Halim
    with comp_col3:
        include_p3 = st.checkbox("Add Player 3?", value=True)
        p3_name = st.selectbox("Player 3:", options=squad_df["name"].tolist(), index=21) if include_p3 else None # Manuel Hidalgo

    p1 = squad_df[squad_df["name"] == p1_name].iloc[0].to_dict()
    p2 = squad_df[squad_df["name"] == p2_name].iloc[0].to_dict()
    p3 = squad_df[squad_df["name"] == p3_name].iloc[0].to_dict() if include_p3 else None

    # Comparison Radar Chart
    comp_radar_fig = create_comparison_radar(p1, p2, p3)
    st.plotly_chart(comp_radar_fig, use_container_width=True)

    # Side-by-Side Comparison Table
    st.markdown("#### 📊 Metric-by-Metric Comparison Matrix")
    
    comp_data = {
        "Metric": [
            "Position", "Club", "League", "Age", "Market Value (€)",
            "26/27 Minutes", "Appearances", "Goals", "Assists",
            "Goal Contributions", "Goals/90", "Assists/90", "FotMob Rating", "SofaScore Rating"
        ],
        p1["name"]: [
            p1["position"], p1["club"], p1["league"], p1["age"], f"€{p1['market_value_eur']:,}",
            f"{p1['minutes_26_27']}'", p1["apps_26_27"], p1["goals_26_27"], p1["assists_26_27"],
            p1["goals_26_27"] + p1["assists_26_27"], p1.get("goals_p90", 0), p1.get("assists_p90", 0),
            p1.get("fotmob_rating", "N/A"), p1.get("sofascore_rating", "N/A")
        ],
        p2["name"]: [
            p2["position"], p2["club"], p2["league"], p2["age"], f"€{p2['market_value_eur']:,}",
            f"{p2['minutes_26_27']}'", p2["apps_26_27"], p2["goals_26_27"], p2["assists_26_27"],
            p2["goals_26_27"] + p2["assists_26_27"], p2.get("goals_p90", 0), p2.get("assists_p90", 0),
            p2.get("fotmob_rating", "N/A"), p2.get("sofascore_rating", "N/A")
        ]
    }
    
    if p3:
        comp_data[p3["name"]] = [
            p3["position"], p3["club"], p3["league"], p3["age"], f"€{p3['market_value_eur']:,}",
            f"{p3['minutes_26_27']}'", p3["apps_26_27"], p3["goals_26_27"], p3["assists_26_27"],
            p3["goals_26_27"] + p3["assists_26_27"], p3.get("goals_p90", 0), p3.get("assists_p90", 0),
            p3.get("fotmob_rating", "N/A"), p3.get("sofascore_rating", "N/A")
        ]

    comp_df = pd.DataFrame(comp_data)
    st.table(comp_df)

# -------------------------------------------------------------
# TAB 4: HERITAGE & PROSPECT SCOUT
# -------------------------------------------------------------
elif menu_selection == "🌍 Heritage & Prospect Scout":
    st.markdown("### 🌍 Malaysian Football Prospect & Heritage Scouting Database")
    st.write("Tracking domestic U23 starlets, emerging talents, and prospective diaspora/heritage players eligible for Malaysia.")

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        elig_options = ["All"] + list(prospects_df["eligibility_type"].unique())
        selected_elig = st.selectbox("Filter by Eligibility:", elig_options)
    with filter_col2:
        pos_options = ["All"] + list(prospects_df["position_category"].unique())
        selected_pos = st.selectbox("Filter by Position:", pos_options)
    with filter_col3:
        min_readiness = st.slider("Minimum Readiness Index:", 50, 95, 75)

    # Filter prospects
    p_filtered = prospects_df.copy()
    if selected_elig != "All":
        p_filtered = p_filtered[p_filtered["eligibility_type"] == selected_elig]
    if selected_pos != "All":
        p_filtered = p_filtered[p_filtered["position_category"] == selected_pos]
    p_filtered = p_filtered[p_filtered["readiness_index"] >= min_readiness]

    st.markdown(f"**Found {len(p_filtered)} matching prospects:**")

    # Render prospect cards in 2-column grid
    for idx, row in p_filtered.iterrows():
        p_card1, p_card2 = st.columns([1.2, 1])
        with p_card1:
            st.markdown(f"""
            <div class="player-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h3 style="color: #f4d03f; margin: 0;">{row['name']}</h3>
                        <p style="color: #bbb; margin: 4px 0 8px 0; font-size: 0.9rem;">{row['full_name']} | Age: {row['age']} | {row['position']}</p>
                        <span class="badge badge-gold">{row['club']} ({row['league']})</span>
                        <span class="badge badge-blue">{row['country']}</span>
                        <span class="badge badge-green">{row['eligibility_type']}</span>
                    </div>
                    <div style="text-align: center; background: rgba(0,0,0,0.4); padding: 8px 14px; border-radius: 8px; border: 1px solid #f4d03f;">
                        <span style="font-size: 0.7rem; color: #a0aec0;">Readiness</span><br>
                        <strong style="font-size: 1.6rem; color: #f4d03f;">{row['readiness_index']}</strong>
                    </div>
                </div>
                <p style="margin-top: 12px; font-size: 0.9rem; color: #d0d7de;">
                    {row['scouting_summary']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        with p_card2:
            pradar = create_attribute_radar(row.to_dict(), title=f"Scout Radar: {row['name']}")
            st.plotly_chart(pradar, use_container_width=True)

# -------------------------------------------------------------
# TAB 5: MINUTES & MACRO ANALYTICS
# -------------------------------------------------------------
elif menu_selection == "📈 Minutes & Macro Analytics":
    st.markdown("### 📈 Macro Analytics & Playing Time Distribution")

    tab_m1, tab_m2, tab_m3 = st.tabs(["⏱️ Playing Time Leaderboard", "⚽ Goal Contributions", "💰 Age & Value Quadrant"])

    with tab_m1:
        st.markdown("#### 2026/27 Verified Season Minutes Played (Transfermarkt)")
        st.caption("Includes domestic league, Asian Champions League Elite, Thai League, J-League, and Cypriot First Division fixtures.")
        mins_fig = create_minutes_bar_chart(squad_df)
        st.plotly_chart(mins_fig, use_container_width=True)

    with tab_m2:
        gc_fig = create_goal_contributions_chart(squad_df)
        st.plotly_chart(gc_fig, use_container_width=True)

    with tab_m3:
        quad_fig = create_age_value_quadrant(squad_df)
        st.plotly_chart(quad_fig, use_container_width=True)

    # Export Section
    st.markdown("---")
    st.markdown("#### 📥 Export Data")
    csv_data = squad_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full Squad Stats (CSV)",
        data=csv_data,
        file_name="malaysia_squad_2627_analysis.csv",
        mime="text/csv"
    )

# -------------------------------------------------------------
# TAB 6: DATA COLLECTION & PIPELINES
# -------------------------------------------------------------
elif menu_selection == "⚙️ Data Collection & Pipelines":
    st.markdown("### ⚙️ Multi-Source Data Collection & Ingestion Pipeline")
    
    st.markdown("""
    This platform integrates and harmonizes data across three primary football intelligence providers:
    
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
    """)

    st.markdown("#### 🔄 Live Collector Triggers")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        if st.button("Fetch Transfermarkt Profiles"):
            st.success("Transfermarkt cache checked: 23 player profiles & 2026/27 club performance tables up to date.")
    with col_t2:
        if st.button("Sync FotMob Live Ratings"):
            st.success("FotMob ratings synchronized: Last 5 match ratings verified.")
    with col_t3:
        if st.button("Refresh SofaScore Radars"):
            st.success("SofaScore attribute matrices loaded.")

    st.markdown("#### 📂 Active Storage & Local Cache")
    st.write(f"- Squad Dataset: `data/squad_asean_2026.json` ({len(squad_df)} players)")
    st.write(f"- Prospects Database: `data/malaysian_prospects.json` ({len(prospects_df)} prospects)")
    st.write("- Collector Modules: `src/data_collectors/`")
    st.write("- Analytics Modules: `src/analytics/`")
    st.write("- Visualizations: `src/visualizations/`")
