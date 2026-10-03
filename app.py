"""
Harimau Malaya Performance Intelligence Hub
Opta Analyst / StatsBomb / Wyscout Editorial Standards
Author: Performance Analyst & Data Engineering
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

# Streamlit Page Setup
st.set_page_config(
    page_title="Harimau Malaya // Performance Intelligence Hub",
    page_icon="🐅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Opta Analyst / StatsBomb Editorial Dark Theme
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

    /* Editorial Masthead */
    .masthead {
        border-bottom: 2px solid #1e293b;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
    .masthead-title {
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .masthead-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 400;
        margin-top: 4px;
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
        font-size: 1.65rem;
        font-weight: 700;
        color: #f9fafb;
        font-family: 'JetBrains Mono', monospace;
        margin: 4px 0 2px 0;
    }
    .stat-card-sub {
        font-size: 0.72rem;
        color: #6b7280;
    }

    /* Editorial Badges & Tags */
    .tag {
        display: inline-block;
        padding: 2px 7px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }
    .tag-gold {
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .tag-blue {
        background: rgba(59, 130, 246, 0.12);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .tag-green {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
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

    /* Metric cell */
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

    /* Methodology Banner */
    .methodology-box {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 12px 0;
        font-size: 0.84rem;
        color: #94a3b8;
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


# Editorial Header
st.markdown("""
<div class="masthead">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div class="masthead-title">HARIMAU MALAYA // PERFORMANCE INTELLIGENCE HUB</div>
            <div class="masthead-subtitle">National Squad Analytics • Tactical Selection Workbench • Scouting Radar (2023–2026 Cycle)</div>
        </div>
        <div style="display: flex; gap: 8px;">
            <span class="tag tag-gold">26/27 VERIFIED MINUTES</span>
            <span class="tag tag-blue">OPTA / WYSCOUT METRICS</span>
            <span class="tag tag-green">ALL 13 MSL CLUBS</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("### PERFORMANCE SUITE")
selected_view = st.sidebar.radio(
    "Navigation Modules:",
    [
        "Tactical Board & Starting XI Customizer",
        "Player Profile & Action Heatmap",
        "Squad Depth & Substitution Delta (PA)",
        "Master Malaysian Player Register (Wyscout Database)",
        "Recent Internationals (2023–2026 Cycle)",
        "National Prospect & Heritage Scouting",
        "Performance Data & Minutes Tracker"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### SQUAD METRICS SUMMARY")
st.sidebar.write(f"• **Active 2026 ASEAN Squad:** {len(squad_df)} players")
st.sidebar.write(f"• **Recent Internationals (3Y):** {len(past_df)} players")
st.sidebar.write(f"• **Scouted Prospects Pool:** {len(prospects_df)} players")
st.sidebar.write(f"• **Total Master Player Pool:** {len(master_df)} Malaysian players")
st.sidebar.markdown("---")
st.sidebar.caption("Data sources: Transfermarkt verified playing minutes, FotMob match logs, SofaScore tactical radars, Wyscout benchmark percentiles.")


# ==============================================================================
# VIEW 1: TACTICAL BOARD & STARTING XI CUSTOMIZER
# ==============================================================================
if selected_view == "Tactical Board & Starting XI Customizer":
    st.markdown("### Tactical Board & Starting XI Customizer")
    st.caption("Interactively build the starting XI from the full Malaysian player pool, test tactical positioning, and monitor real-time team balance metrics.")

    tact_col1, tact_col2 = st.columns([1.35, 1])

    # Default XI
    default_names = [
        "Syihan Hazmi", "La'Vere Corbin-Ong", "Brad Tapp", "Ubaidullah Shamsul", "Dion Cools",
        "Hong Wan", "Nooa Laine", "Stuart Wilkin", "Faisal Halim", "Romel Morales", "Arif Aiman"
    ]
    # Build complete selection pool across all 109 players
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

                # Fetch player record from master database
                match = master_df[master_df["name"] == chosen_name]
                if not match.empty:
                    starting_xi_players.append(match.iloc[0].to_dict())

    with tact_col1:
        pitch_fig = draw_tactical_pitch(formation=formation, starting_xi_players=starting_xi_players)
        st.plotly_chart(pitch_fig, use_container_width=True)

    # Real-Time Team Tactical Balance Indices
    st.markdown("#### Team Tactical Balance Indices (Performance Analyst Engine)")
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
            <div class="stat-card-sub">Box Clearance Success</div>
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


# ==============================================================================
# VIEW 2: PLAYER PROFILE & ACTION HEATMAP
# ==============================================================================
elif selected_view == "Player Profile & Action Heatmap":
    st.markdown("### Player Performance Intelligence & Action Heatmap")

    all_player_names = sorted(master_df["name"].dropna().unique().tolist())
    def_idx = all_player_names.index("Arif Aiman") if "Arif Aiman" in all_player_names else 0
    p_name = st.selectbox("Select Player from Entire Database:", options=all_player_names, index=def_idx)

    p_data = master_df[master_df["name"] == p_name].iloc[0].to_dict()
    headshot = get_headshot(p_data)
    archetype = get_player_archetype(p_data.get("position", "Winger"), p_data.get("attributes", {}))
    scout_score = calculate_scouting_score(p_data)

    fallback_img = f"https://ui-avatars.com/api/?name={urllib.parse.quote(str(p_data['name']))}&background=1e293b&color=f59e0b&size=150&bold=true"

    # Editorial Profile Card
    st.markdown(f"""
    <div class="profile-card">
        <img src="{headshot}" class="player-headshot" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src='{fallback_img}';">
        <div style="flex-grow: 1;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h2 class="player-name-heading">{p_data['full_name']}</h2>
                    <div style="margin: 6px 0;">
                        <span class="tag tag-gold">{p_data.get('position', 'Forward')}</span>
                        <span class="tag tag-blue">{p_data.get('club', 'Club')} ({p_data.get('league', 'League')})</span>
                        <span class="tag tag-green">{p_data.get('pool_status', 'National Pool')}</span>
                        <span class="tag tag-slate">Archetype: {archetype}</span>
                    </div>
                    <div class="player-meta-line">
                        Age: <strong>{p_data.get('age', 25)}</strong> | Foot: <strong>{p_data.get('preferred_foot', 'Right')}</strong> | Height: <strong>{p_data.get('height', 178)} cm</strong> | 26/27 Mins: <strong>{p_data.get('minutes_26_27', 0)}'</strong> | Value: <strong>€{p_data.get('market_value_eur', 0):,}</strong>
                    </div>
                </div>
                <div style="text-align: right; background: rgba(0,0,0,0.3); padding: 8px 16px; border-radius: 6px; border: 1px solid #334155;">
                    <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Performance Rating</div>
                    <div style="font-size: 2rem; font-weight: 800; color: #facc15;">{scout_score}</div>
                    <div style="font-size: 0.7rem; color: #10b981;">Index / 100</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_metrics, col_radar, col_heatmap = st.columns([1, 1.2, 1.4])

    with col_metrics:
        st.markdown("#### Performance Metrics")
        attrs = p_data.get("attributes", {})
        if attrs:
            for k, v in attrs.items():
                st.markdown(f"""
                <div class="metric-cell">
                    <span class="metric-name">{k}</span>
                    {format_score(v)}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("#### Key Per-90 Data")
        if "p90_metrics" in p_data and isinstance(p_data["p90_metrics"], dict):
            for k, v in p_data["p90_metrics"].items():
                st.write(f"• **{k.replace('_', ' ').title()}:** {v}")
        else:
            st.write(f"• **Pass Accuracy:** {p_data.get('pass_acc_pct', 82.5)}%")
            st.write(f"• **Key Passes / 90:** {p_data.get('key_passes_p90', 1.8)}")

    with col_radar:
        st.markdown("#### Attribute Percentile Radar")
        radar_fig = create_player_attribute_radar(p_data)
        st.plotly_chart(radar_fig, use_container_width=True)

    with col_heatmap:
        st.markdown("#### 2D Touch & Action Density Heatmap")
        st.caption("Kernel density estimate of pitch involvement across tactical thirds and channel corridors.")
        heatmap_fig = generate_player_action_heatmap(p_data)
        st.plotly_chart(heatmap_fig, use_container_width=True)

        zones = calculate_positional_coverage(p_data.get("position", "Winger"))
        st.markdown("##### Positional Field Distribution")
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
# VIEW 3: SQUAD DEPTH & SUBSTITUTION DELTA (PA WORKBENCH)
# ==============================================================================
elif selected_view == "Squad Depth & Substitution Delta (PA)":
    st.markdown("### Performance Analyst (PA) Substitution & Call-Up Delta")
    st.caption("Evaluate player swaps and squad rotation options side-by-side to understand statistical gains vs structural trade-offs.")

    all_names = sorted(master_df["name"].dropna().unique().tolist())

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        idx_out = all_names.index("Faisal Halim") if "Faisal Halim" in all_names else 0
        p_out_name = st.selectbox("Player OUT (Incumbent Starter):", options=all_names, index=idx_out)
    with col_s2:
        idx_in = all_names.index("Safawi Rasid") if "Safawi Rasid" in all_names else 1
        p_in_name = st.selectbox("Player IN (Call-Up / Rotation Option):", options=all_names, index=idx_in)

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
        st.markdown("#### Attribute Delta Variance Matrix (Player IN - Player OUT)")
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
    st.markdown("#### Performance Analyst Briefing")
    adv_col, trade_col = st.columns(2)
    with adv_col:
        st.success("**Tactical Advantages Gained:**\n\n" + "\n\n".join([f"• {a}" for a in swap_data["advantages"]]))
    with trade_col:
        st.warning("**Tactical Trade-Offs & Concessions:**\n\n" + "\n\n".join([f"• {t}" for t in swap_data["tradeoffs"]]))

    # Analytical Methodology Explainer
    with st.expander("ℹ️ Analytical Methodology: Attribute Delta Variance Matrix & Team Balance Indices", expanded=False):
        st.markdown("""
        #### Analytical Framework: Attribute Delta & Tactical Balance
        
        1. **Data Sources & Metric Ingestion:**
           - **Match Event Logs:** Official match logs and tracking statistics from **Transfermarkt**, **FotMob**, and **SofaScore**.
           - **Verified Minutes:** Official 2026/27 domestic and continental match time logs.
        
        2. **Positional Percentile Normalization (1–99 Scale):**
           - Raw per-90 metrics (e.g., *key passes/90*, *progressive carries/90*, *tackles + interceptions/90*, *aerial duel success %*) are normalized against Wyscout/Opta benchmark distributions for Asian & Southeast Asian continental football.
           - A rating of **85+** represents the top 10th percentile across regional professional competitions.
        
        3. **Attribute Delta ($\Delta$) Calculation:**
           $$\\Delta = \\text{Attribute}_{\\text{IN}} - \\text{Attribute}_{\\text{OUT}}$$
           - **Green positive (+)**: The incoming player enhances that specific tactical facet (e.g., higher recovery pace or aerial win rate).
           - **Red negative (-)**: The tactical trade-off or concession the coaching staff accepts when executing the substitution.
        
        4. **Team Tactical Balance Indices (0–100 Formulation):**
           - **Attacking Threat:** Weighted composite of starting front-line and attacking midfielders: $\\text{Finishing} \\times 0.35 + \\text{Dribbling} \\times 0.25 + \\text{Passing} \\times 0.20 + \\text{Pace} \\times 0.20$.
           - **Defensive Solidity:** Weighted composite of back-four and defensive midfielders: $\\text{Defending} \\times 0.40 + \\text{Positioning/IQ} \\times 0.30 + \\text{Physicality} \\times 0.30$.
           - **Pressing Index:** Outfield pressing capacity: $\\text{Work Rate} \\times 0.45 + \\text{Pace} \\times 0.30 + \\text{Physical} \\times 0.25$.
           - **Build-Up Fluidity:** Passing progression: $\\text{Passing} \\times 0.50 + \\text{Vision} \\times 0.30 + \\text{Dribbling} \\times 0.20$.
           - **Aerial Dominance:** Box aerial security: $\\text{Aerial/Heading} \\times 0.60 + \\text{Physical} \\times 0.40$.
        """)


# ==============================================================================
# VIEW 4: MASTER MALAYSIAN PLAYER REGISTER (WYSCOUT DATABASE)
# ==============================================================================
elif selected_view == "Master Malaysian Player Register (Wyscout Database)":
    st.markdown("### Master Malaysian Player Register & Wyscout Intelligence Database")
    st.caption("Comprehensive registry of Malaysian players across all 13 Malaysia Super League clubs, semi-pro divisions, and overseas leagues.")

    # High-level KPIs
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Total Registered Players</div>
            <div class="stat-card-value">{len(master_df)}</div>
            <div class="stat-card-sub">Malaysian Pool Across All Clubs</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        total_val = master_df["market_value_eur"].fillna(0).sum()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Cumulative Market Value</div>
            <div class="stat-card-value">€{total_val/1_000_000:.1f}M</div>
            <div class="stat-card-sub">Transfermarkt Valuation</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        tot_mins = master_df["minutes_26_27"].fillna(0).sum()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">26/27 Verified Minutes</div>
            <div class="stat-card-value">{int(tot_mins):,}</div>
            <div class="stat-card-sub">Active Season Competitive Time</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        avg_readiness = round(master_df["readiness_index"].fillna(75).mean(), 1)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">Average Readiness Index</div>
            <div class="stat-card-value">{avg_readiness}</div>
            <div class="stat-card-sub">Opta National Benchmarks</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Filter Controls
    f_c1, f_c2, f_c3, f_c4 = st.columns(4)
    with f_c1:
        all_clubs = ["All"] + sorted([c for c in master_df["club"].dropna().unique().tolist() if c])
        sel_club = st.selectbox("Filter by Club:", options=all_clubs)
    with f_c2:
        all_pools = ["All"] + sorted([p for p in master_df["pool_status"].dropna().unique().tolist() if p])
        sel_pool = st.selectbox("Filter by Pool Status:", options=all_pools)
    with f_c3:
        all_pos = ["All"] + sorted([p for p in master_df["position_category"].dropna().unique().tolist() if p])
        sel_pos = st.selectbox("Filter by Position:", options=all_pos)
    with f_c4:
        search_query = st.text_input("Search Player by Name:", placeholder="e.g. Arif, Cools, Syihan...")

    # Filter Application
    filtered_master = master_df.copy()
    if sel_club != "All":
        filtered_master = filtered_master[filtered_master["club"] == sel_club]
    if sel_pool != "All":
        filtered_master = filtered_master[filtered_master["pool_status"] == sel_pool]
    if sel_pos != "All":
        filtered_master = filtered_master[filtered_master["position_category"] == sel_pos]
    if search_query:
        filtered_master = filtered_master[
            filtered_master["name"].str.contains(search_query, case=False, na=False) |
            filtered_master["full_name"].str.contains(search_query, case=False, na=False)
        ]

    st.markdown(f"**Showing {len(filtered_master)} players matching search parameters:**")

    # Display Table with Wyscout Data
    display_cols = [
        "name", "club", "position", "age", "pool_status", "minutes_26_27", 
        "apps_26_27", "caps", "goals", "readiness_index", "market_value_eur"
    ]
    # Filter to existing columns
    valid_cols = [c for c in display_cols if c in filtered_master.columns]

    st.dataframe(
        filtered_master[valid_cols].rename(columns={
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


# ==============================================================================
# VIEW 5: RECENT INTERNATIONALS (2023–2026 CYCLE)
# ==============================================================================
elif selected_view == "Recent Internationals (2023–2026 Cycle)":
    st.markdown("### Recent Internationals (2023–2026 Cycle)")
    st.write("Tracking senior players who represented Malaysia over the last 3 years (AFC Asian Cup Qatar, World Cup Qualifiers, Merdeka Cup) who remain eligible for national team selection.")

    filter_pos = st.selectbox(
        "Filter by Position Category:",
        ["All"] + list(past_df["position_category"].unique())
    )

    p_list = past_df.copy()
    if filter_pos != "All":
        p_list = p_list[p_list["position_category"] == filter_pos]

    st.markdown(f"**Found {len(p_list)} senior internationals in active pool:**")

    for idx, p in p_list.iterrows():
        c_left, c_right = st.columns([1.3, 1])
        fallback_url = f"https://ui-avatars.com/api/?name={urllib.parse.quote(str(p['name']))}&background=1e293b&color=f59e0b&size=150&bold=true"
        with c_left:
            st.markdown(f"""
            <div class="profile-card">
                <img src="{get_headshot(p)}" class="player-headshot" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src='{fallback_url}';">
                <div>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span class="tag tag-gold">{p.get('position', 'Player')}</span>
                        <span class="tag tag-blue">{p.get('club', 'Club')}</span>
                        <span class="tag tag-slate">{p.get('caps', 0)} Caps ({p.get('goals', 0)} Goals)</span>
                    </div>
                    <h3 style="color: #ffffff; margin: 6px 0 2px 0;">{p.get('full_name', p.get('name'))}</h3>
                    <p style="color: #64748b; font-size: 0.8rem; margin-bottom: 6px;">Last Represented: {p.get('last_represented', '2024')}</p>
                    <p style="color: #cbd5e1; font-size: 0.86rem; margin: 0;">{p.get('scouting_summary', '')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c_right:
            st.markdown(f"**Market Value:** `€{p.get('market_value_eur', 0):,}` | **26/27 Mins:** `{p.get('minutes_26_27', 0)}'`")
            if "p90_metrics" in p and isinstance(p["p90_metrics"], dict):
                for k, v in p["p90_metrics"].items():
                    st.write(f"• **{k.replace('_', ' ').title()}:** {v}")

    # Roster Table
    st.markdown("#### Complete 3-Year Internationals Register")
    st.dataframe(
        past_df[["name", "position", "club", "caps", "goals", "last_represented", "minutes_26_27", "market_value_eur"]].rename(columns={
            "name": "Player",
            "position": "Position",
            "club": "Club",
            "caps": "Caps",
            "goals": "Goals",
            "last_represented": "Last Campaign",
            "minutes_26_27": "26/27 Mins",
            "market_value_eur": "Market Value (€)"
        }),
        hide_index=True,
        use_container_width=True
    )


# ==============================================================================
# VIEW 6: NATIONAL PROSPECT & HERITAGE SCOUTING
# ==============================================================================
elif selected_view == "National Prospect & Heritage Scouting":
    st.markdown("### National Prospect & Heritage Scouting Database")
    st.write("Tracking emerging U23 domestic talents in the Malaysia Super League as well as prospective diaspora/heritage players abroad.")

    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        elig_filter = st.selectbox("Eligibility Classification:", ["All"] + list(prospects_df["eligibility_type"].dropna().unique()))
    with f_col2:
        pos_filter = st.selectbox("Position:", ["All"] + list(prospects_df["position_category"].dropna().unique()))
    with f_col3:
        min_idx = st.slider("Minimum Scouting Readiness Index:", 60, 95, 75)

    p_filtered = prospects_df.copy()
    if elig_filter != "All":
        p_filtered = p_filtered[p_filtered["eligibility_type"] == elig_filter]
    if pos_filter != "All":
        p_filtered = p_filtered[p_filtered["position_category"] == pos_filter]
    p_filtered = p_filtered[p_filtered["readiness_index"] >= min_idx]

    st.markdown(f"**Found {len(p_filtered)} matching prospects:**")

    for idx, p in p_filtered.iterrows():
        card_l, card_r = st.columns([1.3, 1])
        fallback_url = f"https://ui-avatars.com/api/?name={urllib.parse.quote(str(p['name']))}&background=1e293b&color=f59e0b&size=150&bold=true"
        with card_l:
            st.markdown(f"""
            <div class="profile-card">
                <img src="{get_headshot(p)}" class="player-headshot" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src='{fallback_url}';">
                <div>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span class="tag tag-gold">{p['position']}</span>
                        <span class="tag tag-blue">{p['eligibility_type']}</span>
                        <span class="tag tag-slate">{p['club']} ({p['league']})</span>
                    </div>
                    <h3 style="color: #ffffff; margin: 8px 0 4px 0;">{p['name']} ({p['age']} y/o)</h3>
                    <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0;">{p['scouting_summary']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with card_r:
            st.markdown(f"**Readiness Index:** `{p['readiness_index']} / 100` | **Market Value:** `€{p.get('market_value_eur', 0):,}`")
            p_attrs = p.get("attributes", {})
            if isinstance(p_attrs, dict):
                for k in list(p_attrs.keys())[:3]:
                    st.write(f"• **{k}**: {p_attrs[k]}")

    # Analytical Methodology Explainer
    with st.expander("ℹ️ Analytical Methodology: Scouting Readiness Index Formula & League Tier Weighting", expanded=False):
        st.markdown("""
        #### Scouting Readiness Index Mathematical Model
        
        The **Readiness Index (60–100)** assesses whether a domestic prospect or overseas heritage player is primed for immediate Harimau Malaya senior international competition:
        
        $$\\text{Readiness Index} = \\left( \\sum_{i} w_i \\cdot A_i \\right) \\times C_{\\text{League}} \\times M_{\\text{Sample}} \\times F_{\\text{Age}}$$
        
        1. **Core Positional Attributes ($A_i$):**
           - Evaluated across Technical, Tactical, Physical, and Mental dimensions calibrated from Wyscout / FotMob event logs.
        
        2. **Competition Tier Multiplier ($C_{\\text{League}}$):**
           - **Tier 1 ($1.18\\times$):** Eredivisie (Netherlands), MLS (USA), J1 League (Japan), Premier League / Championship.
           - **Tier 2 ($1.08\\times$):** J3 League, Thai League 1, 3. Liga (Germany), Belgian Challenger Pro League.
           - **Tier 3 ($1.00\\times$):** Malaysia Super League (MSL) domestic competition baseline.
        
        3. **Playing Time Reliability Factor ($M_{\\text{Sample}}$):**
           - Calibrated on verified **2026/27 and 2025/26 club match minutes** from Transfermarkt:
           $$M_{\\text{Sample}} = \\min\\left(1.03, 0.94 + \\frac{\\text{Minutes}_{26/27}}{3000}\\right)$$
           - A player playing regular 90-minute matches against elite opposition carries higher confidence and match sharpness than an unproven reserve.
        
        4. **Age Development Trajectory ($F_{\\text{Age}}$):**
           - Peak physical and tactical window (23–28 y/o): $1.02\\times$.
           - Emerging U23 prospect: $0.98\\times$ baseline with higher ceiling potential rating.
           - Senior veteran (>29 y/o): $0.97\\times$ durability factor.
        """)


# ==============================================================================
# VIEW 7: PERFORMANCE DATA & MINUTES TRACKER
# ==============================================================================
elif selected_view == "Performance Data & Minutes Tracker":
    st.markdown("### Verified 2026/27 Playing Time & Macro Performance Analytics")

    m_tab1, m_tab2, m_tab3 = st.tabs(["Playing Time Leaderboard", "Goal Contributions", "Age vs Market Value"])

    with m_tab1:
        st.markdown("#### Official 2026/27 Club Minutes (Transfermarkt Verified)")
        st.caption("Cumulative minutes across Malaysia Super League, J1 League, Thai League 1, and European Leagues.")
        st.plotly_chart(create_minutes_bar_chart(squad_df), use_container_width=True)

    with m_tab2:
        st.plotly_chart(create_goal_contributions_chart(squad_df), use_container_width=True)

    with m_tab3:
        st.plotly_chart(create_age_value_quadrant(squad_df), use_container_width=True)

    # Export
    st.markdown("---")
    csv_bytes = master_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full Malaysian Player Performance Database (109 Players - CSV)",
        data=csv_bytes,
        file_name="malaysia_master_player_database_2627.csv",
        mime="text/csv"
    )
