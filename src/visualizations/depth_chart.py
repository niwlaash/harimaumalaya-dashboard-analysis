import pandas as pd
import streamlit as st

def render_national_depth_chart(master_df: pd.DataFrame):
    """
    Renders an elite professional coaching Depth Chart & Squad Drop-Off Matrix
    covering the 11 positions for Harimau Malaya.
    Displays 1st Choice (Starter), 2nd Choice (Primary Rotation), and 3rd Choice (Emerging/Reserve).
    """
    # Define the 11 tactical positions and candidate selection criteria
    positions_config = [
        {"code": "GK", "role": "Goalkeeper", "target_pos": "Goalkeeper", "slots": ["Syihan Hazmi", "Haziq Nadzli", "Sikh Izhan"]},
        {"code": "RB", "role": "Right-Back", "target_pos": "Defender", "slots": ["Matthew Davies", "Azam Azmi", "Richard Chin"]},
        {"code": "RCB", "role": "Right Centre-Back", "target_pos": "Defender", "slots": ["Dion Cools", "Shahrul Saad", "Junior Eldstål"]},
        {"code": "LCB", "role": "Left Centre-Back", "target_pos": "Defender", "slots": ["Feroz Baharudin", "Dominic Tan", "Harith Haiqal"]},
        {"code": "LB", "role": "Left-Back", "target_pos": "Defender", "slots": ["La'Vere Corbin-Ong", "Daniel Ting", "Declan Lambert"]},
        {"code": "DM", "role": "Defensive Midfield (Anchor)", "target_pos": "Midfielder", "slots": ["Nacho Méndez", "Hong Wan", "Syamer Kutty Abba"]},
        {"code": "RCM", "role": "Right Central Midfield (Engine)", "target_pos": "Midfielder", "slots": ["Stuart Wilkin", "Brendan Gan", "Endrick dos Santos"]},
        {"code": "LCM", "role": "Left Central Midfield (Playmaker)", "target_pos": "Midfielder", "slots": ["Nooa Laine", "Wan Kuzain", "Mukhairi Ajmal"]},
        {"code": "RW", "role": "Right Winger", "target_pos": "Attacker", "slots": ["Arif Aiman", "Manuel Hidalgo", "Safawi Rasid"]},
        {"code": "CF", "role": "Centre-Forward (Striker)", "target_pos": "Attacker", "slots": ["Bérgson", "Romel Morales", "Paulo Josué"]},
        {"code": "LW", "role": "Left Winger", "target_pos": "Attacker", "slots": ["Faisal Halim", "Akhyar Rashid", "T. Saravanan"]}
    ]

    # Create mapping of player records from master_df
    player_lookup = {row["name"]: row for _, row in master_df.iterrows()}

    st.markdown("##### 📋 Positional Squad Depth Chart & Readiness Drop-Off")
    st.caption("Visual hierarchy showing 1st Choice (Starter), 2nd Choice (Backup), and 3rd Choice (Depth) with readiness scores and tactical degradation index.")

    rows = []
    for pos in positions_config:
        p1_name = pos["slots"][0]
        p2_name = pos["slots"][1]
        p3_name = pos["slots"][2]

        p1 = player_lookup.get(p1_name, {})
        p2 = player_lookup.get(p2_name, {})
        p3 = player_lookup.get(p3_name, {})

        r1 = p1.get("readiness_index", 85)
        r2 = p2.get("readiness_index", 80)
        r3 = p3.get("readiness_index", 75)

        # Tactical drop-off from Starter to 2nd choice
        drop_off = round(((r1 - r2) / r1) * 100, 1) if r1 > 0 else 0.0

        rows.append({
            "Pos": pos["code"],
            "Role Definition": pos["role"],
            "1st Choice (Starter)": f"★ {p1_name} ({p1.get('club', '')}) — R:{r1}",
            "2nd Choice (Backup)": f"{p2_name} ({p2.get('club', '')}) — R:{r2}",
            "3rd Choice (Depth)": f"{p3_name} ({p3.get('club', '')}) — R:{r3}",
            "Backup Drop-Off": f"-{drop_off}%" if drop_off > 0 else "0.0%"
        })

    depth_df = pd.DataFrame(rows)
    st.dataframe(
        depth_df,
        use_container_width=True,
        hide_index=True
    )

    # Coaching Insights Panel
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style="background:#1e293b; border-radius:8px; padding:12px; border-left:4px solid #10b981;">
            <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Deepest Positions</div>
            <div style="font-size:1.05rem; font-weight:700; color:#10b981; margin:4px 0;">Centre-Forward & Right Wing</div>
            <div style="font-size:0.8rem; color:#cbd5e1;">Bérgson, Romel Morales, Paulo Josué & Arif Aiman, Manuel Hidalgo, Safawi give elite redundancy (< 4% drop-off).</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#1e293b; border-radius:8px; padding:12px; border-left:4px solid #f59e0b;">
            <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Key Tactical Pivot</div>
            <div style="font-size:1.05rem; font-weight:700; color:#f59e0b; margin:4px 0;">Central Midfield (DM / CM)</div>
            <div style="font-size:0.8rem; color:#cbd5e1;">Nacho Méndez, Nooa Laine & Stuart Wilkin provide European tempo control; Wan Kuzain provides direct MLS technical backup.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="background:#1e293b; border-radius:8px; padding:12px; border-left:4px solid #ef4444;">
            <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Vulnerability Warning</div>
            <div style="font-size:1.05rem; font-weight:700; color:#ef4444; margin:4px 0;">Left-Back (LB) Depth</div>
            <div style="font-size:0.8rem; color:#cbd5e1;">Corbin-Ong (34) possesses highest physical ceiling; Richard Chin and Daniel Ting must be integrated for long-term succession.</div>
        </div>
        """, unsafe_allow_html=True)
