import streamlit as st
import pandas as pd
import numpy as np
import json
import os

# Import modules
from src.data_collectors.aggregator import DataAggregator
from src.analytics.metrics import calculate_scouting_score, get_player_archetype
from src.analytics.tactical_engine import calculate_team_tactical_balance, analyze_player_swap
from src.visualizations.pitch import draw_tactical_pitch
from src.visualizations.radar import create_attribute_radar, create_comparison_radar
from src.visualizations.charts import (
    create_minutes_bar_chart,
    create_form_trend_chart,
    create_goal_contributions_chart,
    create_age_value_quadrant
)
from src.visualizations.heatmap import generate_player_heatmap

# Page Configuration
st.set_page_config(
    page_title="Harimau Malaya | FM Tactical Workbench",
    page_icon="🐅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Football Manager (FM) Sleek Dark UI Theme
st.markdown("""
<style>
    /* FM Background & Fonts */
    .stApp {
        background-color: #0b0f17;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Top Bar Header */
    .fm-navbar {
        background: linear-gradient(90deg, #161f30 0%, #1e293b 60%, #131b26 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 5px solid #00f2fe;
        border-radius: 8px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .fm-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: 1px;
        color: #ffffff;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .fm-subtitle {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-top: 4px;
    }
    
    /* Tactical KPI Tiles */
    .kpi-tile {
        background: #131b26;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .kpi-label {
        font-size: 0.72rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.8px;
    }
    .kpi-num {
        font-size: 1.6rem;
        font-weight: 800;
        color: #00f2fe;
        margin: 4px 0 2px 0;
    }
    .kpi-hint {
        font-size: 0.75rem;
        color: #94a3b8;
    }

    /* Player Profile Card */
    .fm-profile-card {
        background: #131b26;
        border: 1px solid #243247;
        border-radius: 10px;
        padding: 20px;
        display: flex;
        gap: 20px;
        align-items: center;
        margin-bottom: 20px;
    }
    .fm-avatar-img {
        width: 100px;
        height: 100px;
        border-radius: 10px;
        object-fit: cover;
        border: 2px solid #00f2fe;
        box-shadow: 0 4px 12px rgba(0, 242, 254, 0.2);
    }
    .fm-player-name {
        font-size: 1.6rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
    }
    .fm-player-meta {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-top: 4px;
    }

    /* FM Attribute Grid Badges */
    .attr-box {
        background: #0f1622;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 8px 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .attr-name {
        font-size: 0.82rem;
        color: #cbd5e1;
        font-weight: 600;
    }
    .attr-val-elite {
        color: #00ff87;
        font-weight: 800;
        font-size: 0.95rem;
    }
    .attr-val-good {
        color: #38bdf8;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .attr-val-avg {
        color: #fbbf24;
        font-weight: 700;
        font-size: 0.95rem;
    }

    /* FM Badges */
    .badge-pos {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 6px;
        background: #0284c7;
        color: #ffffff;
    }
    .badge-role {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        background: #334155;
        color: #f1f5f9;
    }

    /* Coach Swap Delta Box */
    .delta-card {
        background: #111a26;
        border: 1px solid #2a3c54;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 16px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Load Datasets
@st.cache_data
def load_all_databases():
    aggregator = DataAggregator()
    squad_df = aggregator.load_squad()
    prospects_df = aggregator.load_prospects()
    legends_df = aggregator.load_legends()
    return squad_df, prospects_df, legends_df

try:
    squad_df, prospects_df, legends_df = load_all_databases()
except Exception as e:
    st.error(f"Error loading football databases: {e}")
    st.stop()

# Header Navigation Bar
st.markdown("""
<div class="fm-navbar">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div class="fm-title">🐅 HARIMAU MALAYA // PRO TACTICAL WORKBENCH</div>
            <div class="fm-subtitle">National Squad Analytics • Tactical Performance Analyst Engine • Heritage & Historical Benchmark Scout</div>
        </div>
        <div style="display: flex; gap: 8px;">
            <span class="badge-pos">FM26 ENGINE</span>
            <span class="badge-role">PERFORMANCE ANALYST MODE</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### 📋 TACTICAL WORKBENCH")
mode_selection = st.sidebar.radio(
    "Navigation Menu:",
    [
        "🏟️ Tactical Board & Coach XI Builder",
        "👤 Player Profile & Heatmap",
        "🔄 Performance Analyst (PA) Swap Diff",
        "🏛️ Historical Legends & Benchmarks",
        "🌍 Global Prospects & Heritage Pool",
        "📊 26/27 Minutes & Macro Data"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### ⚡ SQUAD OVERVIEW")
st.sidebar.write(f"**ASEAN Cup Squad:** {len(squad_df)} players")
st.sidebar.write(f"**Prospects Database:** {len(prospects_df)} players")
st.sidebar.write(f"**Past Benchmark Legends:** {len(legends_df)} icons")
st.sidebar.markdown("---")
st.sidebar.caption("⚽ Developed with FotMob, SofaScore, and Transfermarkt verified data pipelines.")

# Helper function to get player photo
def get_photo_url(p: dict) -> str:
    url = p.get("photo_url", "")
    if url and "default" not in url:
        return url
    return "https://images.fotmob.com/image_resources/playerimages/1152012.png"

# Helper function to format attribute value with FM color class
def format_fm_val(val: int) -> str:
    if val >= 85:
        return f'<span class="attr-val-elite">{val}</span>'
    elif val >= 75:
        return f'<span class="attr-val-good">{val}</span>'
    else:
        return f'<span class="attr-val-avg">{val}</span>'


# ==============================================================================
# TAB 1: TACTICAL BOARD & COACH XI BUILDER
# ==============================================================================
if mode_selection == "🏟️ Tactical Board & Coach XI Builder":
    st.markdown("### 🏟️ Tactical Board & Dynamic Starting XI Customizer")
    st.write("Customize your starting XI, adjust positions in real-time, and monitor team tactical balance indices like a real Head Coach or Performance Analyst.")

    tact_col1, tact_col2 = st.columns([1.35, 1])

    # Default starting XI pool
    default_names = [
        "Syihan Hazmi", "La'Vere Corbin-Ong", "Brad Tapp", "Ubaidullah Shamsul", "Dion Cools",
        "Hong Wan", "Nooa Laine", "Stuart Wilkin", "Faisal Halim", "Bérgson", "Arif Aiman"
    ]
    all_player_names = squad_df["name"].tolist() + prospects_df["name"].tolist()

    with tact_col2:
        st.markdown("#### 🛠️ Team Sheet & Positional Adjustments")
        formation = st.selectbox("Select Tactical System:", ["4-3-3", "3-4-3", "4-2-3-1"], index=0)

        # Slot selectors
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
            ("ST", "Striker / Centre-Forward", 9),
            ("RW", "Right Winger", 10),
        ]

        starting_xi_players = []
        slot_cols = st.columns(2)
        
        for idx, (role_code, role_desc, default_idx) in enumerate(slots_433):
            col_target = slot_cols[idx % 2]
            with col_target:
                def_name = default_names[default_idx] if default_idx < len(default_names) else all_player_names[0]
                def_pos_idx = all_player_names.index(def_name) if def_name in all_player_names else 0
                
                chosen_name = st.selectbox(
                    f"[{role_code}] {role_desc}:",
                    options=all_player_names,
                    index=def_pos_idx,
                    key=f"slot_{idx}"
                )
                
                # Fetch player record
                match_squad = squad_df[squad_df["name"] == chosen_name]
                if not match_squad.empty:
                    starting_xi_players.append(match_squad.iloc[0].to_dict())
                else:
                    match_pros = prospects_df[prospects_df["name"] == chosen_name]
                    if not match_pros.empty:
                        starting_xi_players.append(match_pros.iloc[0].to_dict())

    with tact_col1:
        # Render Pitch Board
        pitch_fig = draw_tactical_pitch(formation=formation, starting_xi_players=starting_xi_players)
        st.plotly_chart(pitch_fig, use_container_width=True)

    # Real-Time Tactical Balance Metrics (PA Engine)
    st.markdown("#### 📊 Real-Time Team Tactical Balance Indices (Performance Analyst)")
    balance = calculate_team_tactical_balance(starting_xi_players)

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1:
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-label">Attacking Threat</div>
            <div class="kpi-num">{balance['attacking_threat']}</div>
            <div class="kpi-hint">Finishing & Vision</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-label">Defensive Solidity</div>
            <div class="kpi-num">{balance['defensive_solidity']}</div>
            <div class="kpi-hint">Duel & Shielding</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-label">Pressing Index</div>
            <div class="kpi-num">{balance['pressing_intensity']}</div>
            <div class="kpi-hint">Work Rate & Stamina</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-label">Passing Fluidity</div>
            <div class="kpi-num">{balance['passing_fluidity']}</div>
            <div class="kpi-hint">Progressive Build-up</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi5:
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-label">Aerial Dominance</div>
            <div class="kpi-num">{balance['aerial_dominance']}</div>
            <div class="kpi-hint">Box Heading Threat</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi6:
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-label">Starting XI Age</div>
            <div class="kpi-num">{balance['average_age']}</div>
            <div class="kpi-hint">Years Average</div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: PLAYER PROFILE & HEATMAP
# ==============================================================================
elif mode_selection == "👤 Player Profile & Heatmap":
    st.markdown("### 👤 Player Profile & Tactical Action Heatmap")

    # Combine squad and prospects for inspection
    combined_all = pd.concat([squad_df, prospects_df], ignore_index=True)
    p_name = st.selectbox("Select Player:", options=combined_all["name"].tolist(), index=16) # Arif Aiman

    p_data = combined_all[combined_all["name"] == p_name].iloc[0].to_dict()
    photo_url = get_photo_url(p_data)
    archetype = get_player_archetype(p_data["position"], p_data.get("attributes", {}))
    scout_score = calculate_scouting_score(p_data)

    # FM Profile Card with Photo
    st.markdown(f"""
    <div class="fm-profile-card">
        <img src="{photo_url}" class="fm-avatar-img" onerror="this.onerror=null; this.src='https://images.fotmob.com/image_resources/playerimages/1152012.png';">
        <div style="flex-grow: 1;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h2 class="fm-player-name">{p_data['full_name']}</h2>
                    <div style="margin: 6px 0;">
                        <span class="badge-pos">{p_data['position']}</span>
                        <span class="badge-role">{p_data['club']} ({p_data['league']})</span>
                        <span class="badge-role">Archetype: {archetype}</span>
                    </div>
                    <div class="fm-player-meta">
                        Age: <strong>{p_data['age']}</strong> | Foot: <strong>{p_data.get('preferred_foot', 'Right')}</strong> | Height: <strong>{p_data['height']} cm</strong> | Market Value: <strong>€{p_data.get('market_value_eur', 0):,}</strong>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.72rem; color: #64748b; text-transform: uppercase;">Scouting Readiness</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #00f2fe;">{scout_score}</div>
                    <div style="font-size: 0.72rem; color: #00ff87;">FM Index / 100</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3-Column FM Layout: Attributes Grid | Radar Profile | Heatmap
    col_attr, col_radar, col_heat = st.columns([1, 1.2, 1.4])

    with col_attr:
        st.markdown("#### ⚡ FM Attribute Matrix")
        attrs = p_data.get("attributes", {})
        if attrs:
            for k, v in attrs.items():
                st.markdown(f"""
                <div class="attr-box">
                    <span class="attr-name">{k}</span>
                    {format_fm_val(v)}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Attributes standard baseline loaded.")

        st.markdown("#### 🎯 Role Suitability")
        st.markdown(f"⭐ **{archetype}**: `94% Familiarity`")
        st.markdown(f"⭐ **Secondary Role**: `85% Familiarity`")

    with col_radar:
        st.markdown("#### 🕸️ Attribute Polygon")
        radar_fig = create_attribute_radar(p_data, title=f"Polygon: {p_data['name']}")
        st.plotly_chart(radar_fig, use_container_width=True)

        if "recent_form" in p_data:
            form_fig = create_form_trend_chart(p_data["recent_form"], p_data["name"])
            st.plotly_chart(form_fig, use_container_width=True)

    with col_heat:
        st.markdown("#### 🔥 Tactical Touch & Action Heatmap (SofaScore / WhoScored)")
        heat_fig, zones = generate_player_heatmap(
            p_data["name"],
            p_data["position"],
            p_data.get("heatmap_type")
        )
        st.plotly_chart(heat_fig, use_container_width=True)

        # Tactical Zone Breakdown
        st.markdown("##### 📍 Positional Thirds & Flank Density")
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
# TAB 3: PERFORMANCE ANALYST (PA) SWAP DIFF
# ==============================================================================
elif mode_selection == "🔄 Performance Analyst (PA) Swap Diff":
    st.markdown("### 🔄 Performance Analyst (PA) Swap & Substitution Delta")
    st.write("Analyze player swaps and tactical changes side-by-side. Measure exact attribute deltas and tactical consequences for the team.")

    all_names = squad_df["name"].tolist() + prospects_df["name"].tolist()

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        p_out_name = st.selectbox("Player OUT (Current Starter):", options=all_names, index=17) # Faisal Halim
    with col_s2:
        p_in_name = st.selectbox("Player IN (Replacement / Prospect):", options=all_names, index=20) # Fergus Tierney

    combined = pd.concat([squad_df, prospects_df], ignore_index=True)
    p_out = combined[combined["name"] == p_out_name].iloc[0].to_dict()
    p_in = combined[combined["name"] == p_in_name].iloc[0].to_dict()

    # Calculate Tactical Delta
    swap_analysis = analyze_player_swap(p_out, p_in)

    # Side-by-Side Visual Cards
    card1, card2 = st.columns(2)
    with card1:
        st.markdown(f"""
        <div class="fm-profile-card">
            <img src="{get_photo_url(p_out)}" class="fm-avatar-img">
            <div>
                <span class="badge-role" style="background: #e11d48;">SUB OUT</span>
                <h3 style="color: #ffffff; margin: 4px 0;">{p_out['name']}</h3>
                <div class="fm-player-meta">{p_out['position']} | {p_out['club']} | 26/27 Mins: {p_out.get('minutes_26_27', 0)}'</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with card2:
        st.markdown(f"""
        <div class="fm-profile-card">
            <img src="{get_photo_url(p_in)}" class="fm-avatar-img">
            <div>
                <span class="badge-role" style="background: #10b981;">SUB IN</span>
                <h3 style="color: #ffffff; margin: 4px 0;">{p_in['name']}</h3>
                <div class="fm-player-meta">{p_in['position']} | {p_in['club']} | 26/27 Mins: {p_in.get('minutes_26_27', 0)}'</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Overlaid Comparison Radar
    radar_col, delta_col = st.columns([1.1, 1])
    with radar_col:
        comp_radar = create_comparison_radar(p_out, p_in)
        st.plotly_chart(comp_radar, use_container_width=True)

    with delta_col:
        st.markdown("#### ⚡ Attribute Delta Matrix (Player IN vs Player OUT)")
        for attr, diff in swap_analysis["deltas"].items():
            if diff > 0:
                diff_str = f'<strong style="color: #10b981;">+{diff}</strong>'
            elif diff < 0:
                diff_str = f'<strong style="color: #ef4444;">{diff}</strong>'
            else:
                diff_str = '<span style="color: #94a3b8;">0</span>'

            st.markdown(f"""
            <div class="attr-box">
                <span class="attr-name">{attr}</span>
                <span>{diff_str}</span>
            </div>
            """, unsafe_allow_html=True)

    # Tactical Pros and Cons Report
    st.markdown("#### 📋 Performance Analyst Tactical Briefing")
    adv_col, trade_col = st.columns(2)
    with adv_col:
        st.success("**Tactical Advantages Gained:**\n\n" + "\n\n".join([f"• {a}" for a in swap_analysis["advantages"]]))
    with trade_col:
        st.warning("**Tactical Trade-Offs & Concessions:**\n\n" + "\n\n".join([f"• {t}" for t in swap_analysis["tradeoffs"]]))


# ==============================================================================
# TAB 4: HISTORICAL LEGENDS & BENCHMARKS
# ==============================================================================
elif mode_selection == "🏛️ Historical Legends & Benchmarks":
    st.markdown("### 🏛️ Historical Legends & Benchmark Icons")
    st.write("Compare contemporary Harimau Malaya stars against Malaysian football legends and all-time icons.")

    leg_col1, leg_col2 = st.columns([1, 1.2])

    with leg_col1:
        chosen_legend = st.selectbox(
            "Select Benchmark Legend:",
            options=legends_df["name"].tolist(),
            index=0 # Mokhtar Dahari
        )
        leg_data = legends_df[legends_df["name"] == chosen_legend].iloc[0].to_dict()

        st.markdown(f"""
        <div class="fm-profile-card">
            <div>
                <span class="badge-pos">{leg_data['era']}</span>
                <h2 style="color: #f59e0b; margin: 4px 0;">{leg_data['full_name']}</h2>
                <div class="fm-player-meta">
                    Position: <strong>{leg_data['position']}</strong> | Peak Club: <strong>{leg_data['club_peak']}</strong>
                </div>
                <div style="margin-top: 8px;">
                    Caps: <strong style="color: #00f2fe;">{leg_data['caps']}</strong> | International Goals: <strong style="color: #00ff87;">{leg_data['goals']}</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info(leg_data["scouting_summary"])

    with leg_col2:
        st.markdown("#### ⚔️ Compare with Active Harimau Malaya Star")
        active_comp = st.selectbox(
            "Select Current Player to Compare with Legend:",
            options=squad_df["name"].tolist(),
            index=19 # Bérgson or Arif Aiman
        )
        active_data = squad_df[squad_df["name"] == active_comp].iloc[0].to_dict()

        # Format attributes for comparison
        leg_radar = create_comparison_radar(leg_data, active_data)
        st.plotly_chart(leg_radar, use_container_width=True)

    # Full Legends Roster Table
    st.markdown("#### 📜 All-Time Legends Benchmark Directory")
    st.dataframe(
        legends_df[["name", "era", "caps", "goals", "position", "club_peak"]].rename(columns={
            "name": "Legend",
            "era": "Era",
            "caps": "Official Caps",
            "goals": "Goals",
            "position": "Position",
            "club_peak": "Peak Club"
        }),
        hide_index=True,
        use_container_width=True
    )


# ==============================================================================
# TAB 5: GLOBAL PROSPECTS & HERITAGE POOL
# ==============================================================================
elif mode_selection == "🌍 Global Prospects & Heritage Pool":
    st.markdown("### 🌍 Global Prospects & Heritage Scouting Database")
    st.write("Tracking domestic U23 starlets, emerging talents, and prospective Malaysian heritage/diaspora players across the globe.")

    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        elig_filter = st.selectbox("Eligibility Filter:", ["All"] + list(prospects_df["eligibility_type"].unique()))
    with f_col2:
        pos_filter = st.selectbox("Position Filter:", ["All"] + list(prospects_df["position_category"].unique()))
    with f_col3:
        min_idx = st.slider("Minimum Readiness Index:", 60, 95, 75)

    p_filtered = prospects_df.copy()
    if elig_filter != "All":
        p_filtered = p_filtered[p_filtered["eligibility_type"] == elig_filter]
    if pos_filter != "All":
        p_filtered = p_filtered[p_filtered["position_category"] == pos_filter]
    p_filtered = p_filtered[p_filtered["readiness_index"] >= min_idx]

    st.markdown(f"**Found {len(p_filtered)} matching prospects:**")

    for idx, p in p_filtered.iterrows():
        card_l, card_r = st.columns([1.3, 1])
        with card_l:
            st.markdown(f"""
            <div class="fm-profile-card">
                <div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <span class="badge-pos">{p['position']}</span>
                        <span class="badge-role">{p['eligibility_type']}</span>
                        <span class="badge-role">{p['club']} ({p['league']})</span>
                    </div>
                    <h3 style="color: #ffffff; margin: 8px 0 4px 0;">{p['name']} ({p['age']} y/o)</h3>
                    <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0;">{p['scouting_summary']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with card_r:
            st.markdown(f"**Scouting Readiness:** `{p['readiness_index']} / 100` | **Market Value:** `€{p.get('market_value_eur', 0):,}`")
            # Mini attributes progress
            p_attrs = p.get("attributes", {})
            for k in list(p_attrs.keys())[:3]:
                st.write(f"• **{k}**: {p_attrs[k]}")


# ==============================================================================
# TAB 6: 26/27 MINUTES & MACRO DATA
# ==============================================================================
elif mode_selection == "📊 26/27 Minutes & Macro Data":
    st.markdown("### 📊 Verified 2026/27 Season Playing Time & Squad Macro Analytics")

    m_tab1, m_tab2, m_tab3 = st.tabs(["⏱️ Minutes Leaderboard", "⚽ Goal Contributions", "💰 Age vs Market Value"])

    with m_tab1:
        st.markdown("#### Official 26/27 Club Minutes (Transfermarkt)")
        st.plotly_chart(create_minutes_bar_chart(squad_df), use_container_width=True)

    with m_tab2:
        st.plotly_chart(create_goal_contributions_chart(squad_df), use_container_width=True)

    with m_tab3:
        st.plotly_chart(create_age_value_quadrant(squad_df), use_container_width=True)

    # Export
    st.markdown("---")
    csv_bytes = squad_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Full Squad Dataset (CSV)",
        data=csv_bytes,
        file_name="harimau_malaya_squad_2627.csv",
        mime="text/csv"
    )
