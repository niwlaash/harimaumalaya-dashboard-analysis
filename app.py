"""
Harimau Malaya // Performance Intelligence Hub
Opta Analyst / StatsBomb / Wyscout Editorial Standards
Author: Performance Analyst & Technical Scouting
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import urllib.parse
import os

from src.data_collectors.aggregator import DataAggregator
from src.visualizations.pitch import draw_tactical_pitch
from src.visualizations.heatmap import generate_player_action_heatmap, calculate_positional_coverage
from src.visualizations.radar import create_player_attribute_radar, create_comparison_radar
from src.visualizations.charts import create_minutes_bar_chart, create_goal_contributions_chart, create_age_value_quadrant
from src.analytics.tactical_engine import calculate_team_tactical_balance, analyze_player_swap
from src.analytics.scouting_model import calculate_scouting_score, get_player_archetype

from PIL import Image
import base64

# Load Official Harimau Malaya Crest
crest_path = "assets/harimau_malaya_crest.png"
if os.path.exists(crest_path):
    icon_image = Image.open(crest_path)
    with open(crest_path, "rb") as f:
        crest_b64 = base64.b64encode(f.read()).decode("utf-8")
    crest_uri = f"data:image/png;base64,{crest_b64}"
else:
    icon_image = "🐅"
    crest_uri = ""

# Streamlit Page Setup with Official Crest Favicon
st.set_page_config(
    page_title="Harimau Malaya // Performance Intelligence Hub",
    page_icon=icon_image,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Editorial Dark Theme (Opta Analyst / StatsBomb Standards)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #f1f5f9;
        background-color: #0b0f17;
    }
    
    .stApp {
        background-color: #0b0f17;
    }

    /* Masthead Header */
    .masthead {
        border-bottom: 2px solid #1e293b;
        padding-bottom: 1.2rem;
        margin-bottom: 1.5rem;
    }
    .harimau-badge {
        font-size: 2.2rem;
        background: radial-gradient(circle, #f59e0b 0%, #d97706 70%, #000000 100%);
        border: 2px solid #fbbf24;
        border-radius: 50%;
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.35);
        flex-shrink: 0;
    }
    .masthead-title {
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #f8fafc;
        line-height: 1.2;
    }
    .masthead-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 400;
        margin-top: 3px;
        letter-spacing: 0.01em;
    }

    /* KPI / Stat Cards */
    .stat-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 6px;
        padding: 12px 14px;
        position: relative;
    }
    .stat-card-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #9ca3af;
        font-weight: 600;
    }
    .stat-card-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f9fafb;
        font-family: 'JetBrains Mono', monospace;
        margin: 4px 0 2px 0;
    }
    .stat-card-sub {
        font-size: 0.72rem;
        color: #6b7280;
    }

    /* Tags & Badges */
    .tag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }
    .tag-gold {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .tag-blue {
        background: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.35);
    }
    .tag-green {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .tag-slate {
        background: rgba(148, 163, 184, 0.12);
        color: #cbd5e1;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }

    /* Profile Cards */
    .profile-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 16px;
        display: flex;
        gap: 16px;
        align-items: center;
        margin-bottom: 1rem;
    }
    .player-headshot {
        width: 82px;
        height: 82px;
        border-radius: 50%;
        border: 2px solid #374151;
        object-fit: cover;
        background-color: #1e293b;
        flex-shrink: 0;
    }
    .player-name-heading {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        line-height: 1.2;
    }
    .player-meta-line {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-top: 4px;
    }

    /* Metric cells */
    .metric-cell {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 10px;
        background: #151d2a;
        border-radius: 4px;
        margin-bottom: 5px;
        border-left: 3px solid #3b82f6;
        font-size: 0.83rem;
    }
    .metric-name {
        color: #cbd5e1;
        font-weight: 500;
    }
    .metric-score-high {
        color: #34d399;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-score-mid {
        color: #fbbf24;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-score-low {
        color: #f87171;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)


# Load Databases
@st.cache_data
def load_all_databases():
    aggregator = DataAggregator()
    squad_df = aggregator.load_squad()
    prospects_df = aggregator.load_prospects()
    past_df = aggregator.load_past_internationals()
    master_df = aggregator.load_master_database()
    return squad_df, prospects_df, past_df, master_df

try:
    squad_df, prospects_df, past_df, master_df = load_all_databases()
except Exception as e:
    st.error(f"Error initializing performance database: {e}")
    st.stop()


# Helper function to get resilient headshot URL with reliable SVG/Avatar fallback
def get_headshot(p) -> str:
    if isinstance(p, dict):
        url = p.get("photo_url")
        name = p.get("name", "Player")
    elif hasattr(p, "get"):
        url = p.get("photo_url")
        name = p.get("name", "Player")
    else:
        url = getattr(p, "photo_url", None)
        name = getattr(p, "name", "Player")

    safe_name = urllib.parse.quote(str(name) if name and not pd.isna(name) else "Harimau Malaya")
    default_avatar = f"https://ui-avatars.com/api/?name={safe_name}&background=1e293b&color=f59e0b&size=150&bold=true&font-size=0.38"

    if url is None or pd.isna(url) or not isinstance(url, str):
        return default_avatar

    url = url.strip()
    if not url or "default" in url or url.startswith("nan") or "fotmob.com" in url:
        return default_avatar

    return url


# Helper function for score formatting
def format_score(val: int) -> str:
    if val >= 82:
        return f'<span class="metric-score-high">{val}</span>'
    elif val >= 74:
        return f'<span class="metric-score-mid">{val}</span>'
    else:
        return f'<span class="metric-score-low">{val}</span>'


# Editorial Header with Official Harimau Malaya Crest
st.markdown(f"""
<div class="masthead">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 16px;">
            <img src="{crest_uri}" style="width: 64px; height: 64px; object-fit: contain; filter: drop-shadow(0 0 12px rgba(245, 158, 11, 0.5)); flex-shrink: 0;">
            <div>
                <div class="masthead-title">HARIMAU MALAYA // PERFORMANCE INTELLIGENCE HUB</div>
                <div class="masthead-subtitle">Persatuan Bolasepak Malaysia (FAM) • Technical Scouting & Tactical Studio</div>
            </div>
        </div>
        <div style="display: flex; gap: 8px;">
            <span class="tag tag-gold">26/27 VERIFIED MINUTES</span>
            <span class="tag tag-blue">OPTA / WYSCOUT METRICS</span>
            <span class="tag tag-green">100% ELIGIBLE MALAYSIAN POOL</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# STREAMLINED 3-HUB NAVIGATION
# ==============================================================================
st.sidebar.markdown(f"""
<div style="text-align: center; margin-bottom: 14px; padding: 6px 0;">
    <img src="{crest_uri}" style="width: 95px; height: 95px; object-fit: contain; filter: drop-shadow(0 0 14px rgba(245, 158, 11, 0.45)); margin: 0 auto; display: block;">
    <div style="color: #fbbf24; font-weight: 800; font-size: 0.88rem; margin-top: 8px; letter-spacing: 0.03em;">FA MALAYSIA</div>
    <div style="color: #94a3b8; font-size: 0.70rem; letter-spacing: 0.06em; text-transform: uppercase;">Technical Analysis Unit</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### OPERATIONAL WORKSPACES")
selected_workspace = st.sidebar.radio(
    "Select Workspace:",
    [
        "⚽ Tactical Studio & Lineup Customizer",
        "🔍 Player Intelligence & Scouting Radar",
        "📊 Squad Performance & Minutes Analytics"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### SQUAD POOL SUMMARY")
st.sidebar.write(f"• **Active ASEAN 2026 Squad:** {len(squad_df)} players")
st.sidebar.write(f"• **Recent Senior Internationals:** {len(past_df)} players")
st.sidebar.write(f"• **Scouted Prospects & Diaspora:** {len(prospects_df)} players")
st.sidebar.write(f"• **Total Eligible Player Pool:** {len(master_df)} Malaysian players")
st.sidebar.markdown("---")
st.sidebar.caption("Data Sources: Transfermarkt verified match time, FotMob event logs, SofaScore tactical coordinates, Wyscout benchmark percentiles.")


# ==============================================================================
# WORKSPACE 1: TACTICAL STUDIO & LINEUP CUSTOMIZER
# ==============================================================================
if selected_workspace == "⚽ Tactical Studio & Lineup Customizer":
    st.markdown("### ⚽ Tactical Studio & Lineup Customizer")
    st.caption("Interactively build the starting XI from all 103 eligible Malaysian players, monitor real-time balance metrics, and simulate tactical player substitutions.")

    tact_col1, tact_col2 = st.columns([1.35, 1])

    # Default starting XI (all verified eligible Malaysian internationals)
    default_names = [
        "Syihan Hazmi", "La'Vere Corbin-Ong", "Brad Tapp", "Ubaidullah Shamsul", "Dion Cools",
        "Hong Wan", "Nooa Laine", "Stuart Wilkin", "Faisal Halim", "Romel Morales", "Arif Aiman"
    ]
    all_players_pool = sorted(master_df["name"].dropna().unique().tolist())

    with tact_col2:
        st.markdown("#### Positional Lineup Configuration")
        formation = st.selectbox("Tactical Formation:", ["4-3-3", "3-4-3", "4-2-3-1"], index=0)

        slots_433 = [
            ("GK", "Goalkeeper", 0),
            ("LB", "Left-Back", 1),
            ("LCB", "Left Centre-Back", 2),
            ("RCB", "Right Centre-Back", 3),
            ("RB", "Right-Back", 4),
            ("DM", "Defensive Midfield", 5),
            ("LCM", "Left Central Midfield", 6),
            ("RCM", "Right Central Midfield", 7),
            ("LW", "Left Winger", 8),
            ("CF", "Centre-Forward", 9),
            ("RW", "Right Winger", 10),
        ]

        starting_xi_players = []
        slot_cols = st.columns(2)

        for idx, (role_code, role_desc, default_idx) in enumerate(slots_433):
            col_target = slot_cols[idx % 2]
            with col_target:
                def_name = default_names[default_idx] if default_idx < len(default_names) else all_players_pool[0]
                def_pos_idx = all_players_pool.index(def_name) if def_name in all_players_pool else 0

                chosen_name = st.selectbox(
                    f"[{role_code}] {role_desc}:",
                    options=all_players_pool,
                    index=def_pos_idx,
                    key=f"xi_slot_{idx}"
                )

                match = master_df[master_df["name"] == chosen_name]
                if not match.empty:
                    starting_xi_players.append(match.iloc[0].to_dict())

    with tact_col1:
        pitch_fig = draw_tactical_pitch(formation=formation, starting_xi_players=starting_xi_players)
        st.plotly_chart(pitch_fig, use_container_width=True)

    # Real-Time Team Tactical Balance Indices
    st.markdown("#### Team Tactical Balance Indices (Starting XI Balance)")
    balance = calculate_team_tactical_balance(starting_xi_players)

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Attacking Threat</div>
            <div class="stat-card-value">{balance['attacking_threat']}</div>
            <div class="stat-card-sub">Finishing & Shot Volume</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Defensive Solidity</div>
            <div class="stat-card-value">{balance['defensive_solidity']}</div>
            <div class="stat-card-sub">Duels & Rest-Defense</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Pressing Index</div>
            <div class="stat-card-value">{balance['pressing_intensity']}</div>
            <div class="stat-card-sub">Work Rate & Regains</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Build-Up Fluidity</div>
            <div class="stat-card-value">{balance['passing_fluidity']}</div>
            <div class="stat-card-sub">Progressive Passing</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi5:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Aerial Dominance</div>
            <div class="stat-card-value">{balance['aerial_dominance']}</div>
            <div class="stat-card-sub">Box Clearance Security</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi6:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Average XI Age</div>
            <div class="stat-card-value">{balance['average_age']}</div>
            <div class="stat-card-sub">Squad Age Profile</div>
        </div>
        """, unsafe_allow_html=True)

    # Integrated Substitution Delta Workbench
    st.markdown("---")
    st.markdown("#### 🔄 Substitution & Player Swap Delta (Performance Analyst Studio)")
    st.caption("Compare an incumbent starter with any rotation or prospective call-up to evaluate tactical variance and statistical tradeoffs.")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        idx_out = all_players_pool.index("Faisal Halim") if "Faisal Halim" in all_players_pool else 0
        p_out_name = st.selectbox("Starter OUT:", options=all_players_pool, index=idx_out)
    with col_s2:
        idx_in = all_players_pool.index("Safawi Rasid") if "Safawi Rasid" in all_players_pool else 1
        p_in_name = st.selectbox("Sub IN:", options=all_players_pool, index=idx_in)

    p_out = master_df[master_df["name"] == p_out_name].iloc[0].to_dict()
    p_in = master_df[master_df["name"] == p_in_name].iloc[0].to_dict()

    swap_data = analyze_player_swap(p_out, p_in)

    card1, card2 = st.columns(2)
    fallback_out = f"https://ui-avatars.com/api/?name={urllib.parse.quote(str(p_out['name']))}&background=1e293b&color=ef4444&size=150&bold=true"
    fallback_in = f"https://ui-avatars.com/api/?name={urllib.parse.quote(str(p_in['name']))}&background=1e293b&color=10b981&size=150&bold=true"

    with card1:
        st.markdown(f"""
        <div class="profile-card">
            <img src="{get_headshot(p_out)}" class="player-headshot" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src='{fallback_out}';">
            <div>
                <span class="tag tag-slate" style="color: #ef4444; border-color: #ef4444;">STARTER OUT</span>
                <h3 style="color: #ffffff; margin: 4px 0;">{p_out['name']}</h3>
                <div class="player-meta-line">{p_out.get('position', '')} | {p_out.get('club', '')} | 26/27 Mins: {p_out.get('minutes_26_27', 0)}'</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with card2:
        st.markdown(f"""
        <div class="profile-card">
            <img src="{get_headshot(p_in)}" class="player-headshot" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src='{fallback_in}';">
            <div>
                <span class="tag tag-slate" style="color: #10b981; border-color: #10b981;">SUB IN</span>
                <h3 style="color: #ffffff; margin: 4px 0;">{p_in['name']}</h3>
                <div class="player-meta-line">{p_in.get('position', '')} | {p_in.get('club', '')} | 26/27 Mins: {p_in.get('minutes_26_27', 0)}'</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    radar_col, delta_col = st.columns([1.1, 1])
    with radar_col:
        comp_radar = create_comparison_radar(p_out, p_in)
        st.plotly_chart(comp_radar, use_container_width=True)

    with delta_col:
        st.markdown("##### Attribute Delta Variance Matrix (Player IN − Player OUT)")
        for attr, diff in swap_data["deltas"].items():
            if diff > 0:
                diff_str = f'<strong style="color: #10b981;">+{diff}</strong>'
            elif diff < 0:
                diff_str = f'<strong style="color: #ef4444;">{diff}</strong>'
            else:
                diff_str = '<span style="color: #94a3b8;">0</span>'

            st.markdown(f"""
            <div class="metric-cell">
                <span class="metric-name">{attr}</span>
                <span>{diff_str}</span>
            </div>
            """, unsafe_allow_html=True)

    # Tactical Briefing
    st.markdown("##### Performance Analyst Briefing")
    adv_col, trade_col = st.columns(2)
    with adv_col:
        st.success("**Tactical Gains:**\n\n" + "\n\n".join([f"• {a}" for a in swap_data["advantages"]]))
    with trade_col:
        st.warning("**Tactical Trade-Offs:**\n\n" + "\n\n".join([f"• {t}" for t in swap_data["tradeoffs"]]))


# ==============================================================================
# WORKSPACE 2: PLAYER INTELLIGENCE & SCOUTING RADAR
# ==============================================================================
elif selected_workspace == "🔍 Player Intelligence & Scouting Radar":
    st.markdown("### 🔍 Player Intelligence & Wyscout Scouting Hub")
    st.caption("Comprehensive scouting database of all eligible Malaysian players across all 13 Malaysia Super League clubs and abroad.")

    # Multi-Dimensional Filters
    fc1, fc2, fc3, fc4, fc5 = st.columns(5)
    with fc1:
        pos_cats = ["All"] + sorted([c for c in master_df["position_category"].dropna().unique().tolist() if c])
        filter_pos_cat = st.selectbox("Position Group:", options=pos_cats)
    with fc2:
        roles = ["All"] + sorted([p for p in master_df["position"].dropna().unique().tolist() if p])
        filter_role = st.selectbox("Specific Role:", options=roles)
    with fc3:
        clubs = ["All"] + sorted([c for c in master_df["club"].dropna().unique().tolist() if c])
        filter_club = st.selectbox("Club:", options=clubs)
    with fc4:
        pools = ["All"] + sorted([p for p in master_df["pool_status"].dropna().unique().tolist() if p])
        filter_pool = st.selectbox("Squad Pool Category:", options=pools)
    with fc5:
        search_kw = st.text_input("Search by Name:", placeholder="e.g. Arif, Cools, Harith...")

    # Filter evaluation
    filtered_df = master_df.copy()
    if filter_pos_cat != "All":
        filtered_df = filtered_df[filtered_df["position_category"] == filter_pos_cat]
    if filter_role != "All":
        filtered_df = filtered_df[filtered_df["position"] == filter_role]
    if filter_club != "All":
        filtered_df = filtered_df[filtered_df["club"] == filter_club]
    if filter_pool != "All":
        filtered_df = filtered_df[filtered_df["pool_status"] == filter_pool]
    if search_kw:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search_kw, case=False, na=False) |
            filtered_df["full_name"].str.contains(search_kw, case=False, na=False)
        ]

    st.markdown(f"**Showing {len(filtered_df)} eligible Malaysian players matching active filters:**")

    # Master Table Display
    display_cols = [
        "name", "club", "position", "age", "pool_status", "minutes_26_27", 
        "apps_26_27", "caps", "goals", "readiness_index", "market_value_eur"
    ]
    valid_cols = [c for c in display_cols if c in filtered_df.columns]

    st.dataframe(
        filtered_df[valid_cols].rename(columns={
            "name": "Player",
            "club": "Club",
            "position": "Position",
            "age": "Age",
            "pool_status": "Squad Pool Category",
            "minutes_26_27": "26/27 Mins",
            "apps_26_27": "Apps",
            "caps": "Caps",
            "goals": "Goals",
            "readiness_index": "Readiness Index",
            "market_value_eur": "Market Value (€)"
        }),
        hide_index=True,
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("#### 🎯 Detailed Player Dossier & Visualizations (Available for All Players)")

    available_names = filtered_df["name"].tolist() if not filtered_df.empty else master_df["name"].tolist()
    default_target = "Arif Aiman" if "Arif Aiman" in available_names else available_names[0]
    p_inspect_name = st.selectbox("Select Player to Inspect Dossier & Heatmap:", options=available_names, index=available_names.index(default_target))

    p_inspect = master_df[master_df["name"] == p_inspect_name].iloc[0].to_dict()
    headshot = get_headshot(p_inspect)
    archetype = get_player_archetype(p_inspect.get("position", "Winger"), p_inspect.get("attributes", {}))
    scout_score = calculate_scouting_score(p_inspect)
    fallback_inspect = f"https://ui-avatars.com/api/?name={urllib.parse.quote(str(p_inspect['name']))}&background=1e293b&color=f59e0b&size=150&bold=true"

    # Profile Card
    st.markdown(f"""
    <div class="profile-card">
        <img src="{headshot}" class="player-headshot" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src='{fallback_inspect}';">
        <div style="flex-grow: 1;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h2 class="player-name-heading">{p_inspect.get('full_name', p_inspect['name'])}</h2>
                    <div style="margin: 6px 0;">
                        <span class="tag tag-gold">{p_inspect.get('position', 'Player')}</span>
                        <span class="tag tag-blue">{p_inspect.get('club', 'Club')} ({p_inspect.get('league', 'League')})</span>
                        <span class="tag tag-green">{p_inspect.get('pool_status', 'National Pool')}</span>
                        <span class="tag tag-slate">Role: {archetype}</span>
                    </div>
                    <div class="player-meta-line">
                        Age: <strong>{p_inspect.get('age', 25)}</strong> | Foot: <strong>{p_inspect.get('preferred_foot', 'Right')}</strong> | Height: <strong>{p_inspect.get('height', 178)} cm</strong> | 26/27 Mins: <strong>{p_inspect.get('minutes_26_27', 0)}'</strong> | Value: <strong>€{p_inspect.get('market_value_eur', 0):,}</strong>
                    </div>
                </div>
                <div style="text-align: right; background: rgba(0,0,0,0.3); padding: 8px 16px; border-radius: 6px; border: 1px solid #334155;">
                    <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Scouting Readiness</div>
                    <div style="font-size: 2rem; font-weight: 800; color: #facc15;">{p_inspect.get('readiness_index', scout_score)}</div>
                    <div style="font-size: 0.7rem; color: #10b981;">Index / 100</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_attrs, c_radar, c_heat = st.columns([1, 1.2, 1.4])

    with c_attrs:
        st.markdown("##### Key Attributes (1–99)")
        attrs = p_inspect.get("attributes", {})
        if attrs and isinstance(attrs, dict):
            for k, v in attrs.items():
                st.markdown(f"""
                <div class="metric-cell">
                    <span class="metric-name">{k}</span>
                    {format_score(v)}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("##### Wyscout Per-90 Metrics")
        if "p90_metrics" in p_inspect and isinstance(p_inspect["p90_metrics"], dict):
            for k, v in p_inspect["p90_metrics"].items():
                st.write(f"• **{k.replace('_', ' ').title()}:** {v}")
        else:
            st.write(f"• **Pass Accuracy:** {p_inspect.get('pass_acc_pct', 82.5)}%")
            st.write(f"• **Key Passes / 90:** {p_inspect.get('key_passes_p90', 1.8)}")

    with c_radar:
        st.markdown("##### Attribute Percentile Radar")
        radar_fig = create_player_attribute_radar(p_inspect)
        st.plotly_chart(radar_fig, use_container_width=True)

    with c_heat:
        st.markdown("##### 2D Touch & Action Density Heatmap")
        st.caption("Kernel density estimate of spatial match actions across tactical thirds and channel corridors.")
        heat_fig = generate_player_action_heatmap(p_inspect)
        st.plotly_chart(heat_fig, use_container_width=True)

        zones = calculate_positional_coverage(p_inspect.get("position", "Winger"))
        z1, z2, z3 = st.columns(3)
        with z1:
            st.write(f"🛡️ **Def 3rd:** {zones['def_third']}%")
            st.write(f"⬅️ **Left Flank:** {zones['left_flank']}%")
        with z2:
            st.write(f"⚙️ **Mid 3rd:** {zones['mid_third']}%")
            st.write(f"🎯 **Central:** {zones['central_chan']}%")
        with z3:
            st.write(f"⚡ **Final 3rd:** {zones['att_third']}%")
            st.write(f"➡️ **Right Flank:** {zones['right_flank']}%")


# ==============================================================================
# WORKSPACE 3: SQUAD PERFORMANCE & MINUTES ANALYTICS
# ==============================================================================
elif selected_workspace == "📊 Squad Performance & Minutes Analytics":
    st.markdown("### 📊 Squad Performance & Macro Minutes Analytics")
    st.caption("Comprehensive playing time distribution and performance quadrants across all eligible Malaysian players.")

    # High-level KPIs
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Eligible National Pool</div>
            <div class="stat-card-value">{len(master_df)}</div>
            <div class="stat-card-sub">Malaysian Citizens Across All Clubs</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        tot_val = master_df["market_value_eur"].fillna(0).sum()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Cumulative Market Value</div>
            <div class="stat-card-value">€{tot_val/1_000_000:.1f}M</div>
            <div class="stat-card-sub">Transfermarkt Valuation</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        tot_mins = master_df["minutes_26_27"].fillna(0).sum()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">26/27 Verified Minutes</div>
            <div class="stat-card-value">{int(tot_mins):,}</div>
            <div class="stat-card-sub">Competitive Season Time</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        avg_read = round(master_df["readiness_index"].fillna(75).mean(), 1)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Average Readiness Index</div>
            <div class="stat-card-value">{avg_read}</div>
            <div class="stat-card-sub">Opta National Benchmarks</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Scope Filter for Visualizations
    v_col1, v_col2 = st.columns([1, 1])
    with v_col1:
        pool_filter = st.selectbox(
            "Visualization Dataset Scope:",
            ["All Eligible Malaysian Players (103)", "Active ASEAN 2026 Squad (23)", "Recent Senior Internationals (12)", "Prospects & Overseas Pool (15)"]
        )
    with v_col2:
        pos_filter_vis = st.selectbox(
            "Filter Visualizations by Position:",
            ["All Positions", "Goalkeepers", "Defenders", "Midfielders", "Attackers"]
        )

    # Filter target dataset
    chart_df = master_df.copy()
    if "Active ASEAN" in pool_filter:
        chart_df = squad_df.copy()
    elif "Recent Senior" in pool_filter:
        chart_df = past_df.copy()
    elif "Prospects" in pool_filter:
        chart_df = prospects_df.copy()

    if pos_filter_vis != "All Positions":
        cat_map = {"Goalkeepers": "Goalkeeper", "Defenders": "Defender", "Midfielders": "Midfielder", "Attackers": "Attacker"}
        target_cat = cat_map.get(pos_filter_vis, "")
        chart_df = chart_df[chart_df["position_category"] == target_cat]

    chart_tab1, chart_tab2, chart_tab3 = st.tabs([
        "1. Verified Minutes Leaderboard",
        "2. Goal Contributions (Goals + Assists)",
        "3. Age vs. Market Value Distribution"
    ])

    with chart_tab1:
        st.markdown("#### Official 2026/27 Club Playing Minutes (Transfermarkt Verified)")
        top_mins = chart_df.sort_values(by="minutes_26_27", ascending=False).head(25)
        st.plotly_chart(create_minutes_bar_chart(top_mins), use_container_width=True)

    with chart_tab2:
        st.markdown("#### Direct Goal Contributions (2026/27 Season)")
        contrib_c = "goal_contributions_26_27" if "goal_contributions_26_27" in chart_df.columns else "goals_26_27"
        top_contrib = chart_df[chart_df[contrib_c] > 0].sort_values(by=contrib_c, ascending=False).head(20)
        if top_contrib.empty:
            top_contrib = chart_df.head(10)
        st.plotly_chart(create_goal_contributions_chart(top_contrib), use_container_width=True)

    with chart_tab3:
        st.markdown("#### Age Curve vs. Market Value (€) Matrix")
        st.plotly_chart(create_age_value_quadrant(chart_df), use_container_width=True)

    # Export
    st.markdown("---")
    csv_bytes = master_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full Eligible Malaysian Player Performance Database (CSV)",
        data=csv_bytes,
        file_name="harimau_malaya_eligible_master_database_2627.csv",
        mime="text/csv"
    )

    # Embedded Technical Methodology Guide
    st.markdown("---")
    with st.expander("ℹ️ Analytical Methodology, Data Provenance & Interactive Readiness Simulator", expanded=False):
        m_sub1, m_sub2, m_sub3 = st.tabs(["Formulas & Balance Equations", "Live Readiness Simulator", "Data Lineage & Glossary"])

        with m_sub1:
            st.markdown("""
            #### 1. Tactical Balance Indices (0–100 Scale)
            - **Attacking Threat:** $\\text{Mean}(\\text{Finishing} \\times 0.35 + \\text{Dribbling} \\times 0.25 + \\text{Passing} \\times 0.20 + \\text{Pace} \\times 0.20)$
            - **Defensive Solidity:** $\\text{Mean}(\\text{Defending} \\times 0.40 + \\text{Awareness} \\times 0.30 + \\text{Physicality} \\times 0.30)$
            - **Pressing Index:** $\\text{Mean}(\\text{Work Rate} \\times 0.45 + \\text{Pace} \\times 0.30 + \\text{Physical} \\times 0.25)$
            - **Build-Up Fluidity:** $\\text{Mean}(\\text{Passing} \\times 0.50 + \\text{Vision} \\times 0.30 + \\text{Dribbling} \\times 0.20)$
            - **Aerial Dominance:** $\\text{Mean}(\\text{Heading} \\times 0.60 + \\text{Physical} \\times 0.40)$

            #### 2. Attribute Delta Matrix
            $$\\Delta = \\text{Attribute}_{\\text{IN}} - \\text{Attribute}_{\\text{OUT}}$$
            $|\\Delta| \\ge 5$ indicates significant structural gains (green $\\mathbf{+}$) or concessions (red $\\mathbf{-}$).
            """)

        with m_sub2:
            st.markdown("""
            #### 🎛️ Live Scouting Readiness Simulator
            $$\\text{Readiness} = (\\text{Attributes}) \\times C_{\\text{League}} \\times M_{\\text{Sample}} \\times F_{\\text{Age}}$$
            """)
            sim_c1, sim_c2, sim_c3, sim_c4 = st.columns(4)
            with sim_c1:
                s_attr = st.slider("Base Attributes Avg:", 65, 95, 78, key="sim_attr_s")
            with sim_c2:
                s_tier = st.selectbox("League Tier:", ["Tier 1: European / MLS / J1 (1.18x)", "Tier 2: J3 / Thai League (1.08x)", "Tier 3: MSL Domestic (1.00x)"], key="sim_tier_s")
            with sim_c3:
                s_mins = st.slider("26/27 Mins:", 0, 900, 450, key="sim_mins_s")
            with sim_c4:
                s_age = st.slider("Age:", 18, 38, 25, key="sim_age_s")

            c_l = 1.18 if "Tier 1" in s_tier else (1.08 if "Tier 2" in s_tier else 1.00)
            m_s = min(1.03, 0.94 + (s_mins / 3000))
            f_a = 1.02 if 23 <= s_age <= 28 else (0.98 if s_age < 23 else 0.97)
            sim_read = round(min(99, max(50, s_attr * c_l * m_s * f_a)))

            st.markdown(f"""
            <div style="background: #111827; border: 1px solid #3b82f6; border-radius: 8px; padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                <div>
                    <span style="font-size: 0.82rem; color: #94a3b8; text-transform: uppercase;">Simulated Readiness Index</span>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #facc15;">{sim_read} <span style="font-size: 1rem; color: #94a3b8;">/ 100</span></div>
                </div>
                <div style="font-size: 0.85rem; color: #cbd5e1; text-align: right;">
                    <div>League: <strong>{c_l:.2f}x</strong> | Minutes: <strong>{m_s:.2f}x</strong> | Age Factor: <strong>{f_a:.2f}x</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m_sub3:
            st.markdown("""
            #### Data Provenance:
            - **Transfermarkt:** Official verified 2026/27 club minutes, FIFA-recognized international caps & goals, contract expiry timelines, and market valuations (€).
            - **FotMob:** Algorithmically generated match ratings (6.0–10.0 scale), direct goals, assists, and xG/xA.
            - **SofaScore:** Touch locations, KDE spatial action heatmaps, ground/aerial duel win rates.
            - **Wyscout:** Positional benchmark percentiles calibrated across Asian continental football.
            """)
