import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import pandas as pd
from src.analytics.metrics import get_player_archetype

def enrich_master_database():
    path = "data/malaysia_master_player_database.json"
    with open(path, "r", encoding="utf-8") as f:
        players = json.load(f)

    print(f"Enriching {len(players)} players with Data Science & Performance Analytics data...")

    # Phase 1: Ensure all numerical base metrics and p90 values
    for p in players:
        mins = int(p.get("minutes_26_27") or 300)
        p["minutes_26_27"] = mins
        mins_p90 = max(1.0, mins / 90.0)

        goals = int(p.get("goals_26_27") or 0)
        assists = int(p.get("assists_26_27") or 0)
        p["goals_26_27"] = goals
        p["assists_26_27"] = assists
        p["goal_contributions_26_27"] = goals + assists

        pos_cat = p.get("position_category", "Midfielder")
        pos_name = p.get("position", "")
        attrs = p.get("attributes") or {}

        # Tactical archetype
        p["tactical_archetype"] = get_player_archetype(pos_name, attrs)

        p90 = p.get("p90_metrics") or {}

        g_p90 = round(goals / mins_p90, 2)
        a_p90 = round(assists / mins_p90, 2)
        p90["goals_p90"] = g_p90
        p90["assists_p90"] = a_p90

        if pos_cat == "Attacker":
            shots_p90 = float(p90.get("shots_p90") or round(max(1.8, min(4.8, g_p90 * 3.4 + 1.2)), 2))
            xg_p90 = float(p90.get("xg_p90") or round(max(0.14, min(0.96, g_p90 * 0.84 + (shots_p90 * 0.08))), 2))
            xa_p90 = float(p90.get("xa_p90") or round(max(0.08, min(0.48, a_p90 * 0.88 + 0.08)), 2))
            key_p90 = float(p90.get("key_passes_p90") or round(max(1.1, min(2.9, a_p90 * 2.1 + 1.1)), 2))
            prog_c = float(p90.get("prog_carries_p90") or round(max(2.4, min(6.4, (attrs.get("Dribbling", 75) - 60) * 0.17)), 2))
            prog_p = float(p90.get("prog_passes_p90") or round(max(1.8, min(4.6, (attrs.get("Passing", 75) - 60) * 0.12)), 2))
            def_act = float(p90.get("tackles_interceptions_p90") or round(max(0.8, min(2.2, (attrs.get("Work Rate", 75) - 60) * 0.06)), 2))
            duel_w = float(p90.get("duel_win_pct") or round(max(44.0, min(62.0, (attrs.get("Physical", 75) * 0.72))), 1))
            pass_acc = float(p90.get("pass_acc_pct") or round(max(75.0, min(86.5, (attrs.get("Passing", 75) * 0.95) + 6.0)), 1))
            conv_pct = float(p90.get("conversion_rate_pct") or round(max(12.0, min(30.0, (attrs.get("Finishing", 76) * 0.28) + (g_p90 * 6.0))), 1))
            press_p90 = float(p90.get("pressures_p90") or round(max(12.0, min(26.0, (attrs.get("Work Rate", 75) * 0.24)), 1)))

            p90["shots_p90"] = shots_p90
            p90["xg_p90"] = xg_p90
            p90["xa_p90"] = xa_p90
            p90["key_passes_p90"] = key_p90
            p90["prog_carries_p90"] = prog_c
            p90["prog_passes_p90"] = prog_p
            p90["tackles_interceptions_p90"] = def_act
            p90["duel_win_pct"] = duel_w
            p90["pass_acc_pct"] = pass_acc
            p90["conversion_rate_pct"] = conv_pct
            p90["pressures_p90"] = press_p90

        elif pos_cat == "Midfielder":
            pass_acc = float(p90.get("pass_acc_pct") or round(max(82.0, min(92.5, (attrs.get("Passing", 75) * 0.90) + 16.0)), 1))
            prog_p = float(p90.get("prog_passes_p90") or round(max(4.0, min(8.6, (attrs.get("Passing", 75) - 65) * 0.22 + 4.2)), 2))
            prog_c = float(p90.get("prog_carries_p90") or round(max(1.8, min(4.9, (attrs.get("Dribbling", 75) - 65) * 0.14 + 2.1)), 2))
            key_p90 = float(p90.get("key_passes_p90") or round(max(1.1, min(2.8, a_p90 * 2.2 + 1.2)), 2))
            def_act = float(p90.get("tackles_interceptions_p90") or round(max(2.6, min(5.8, (attrs.get("Defending", 75) - 60) * 0.12 + 2.5)), 2))
            recov = float(p90.get("recoveries_p90") or round(max(4.8, min(9.2, (attrs.get("Work Rate", 75) - 65) * 0.18 + 5.2)), 2))
            duel_w = float(p90.get("duel_win_pct") or round(max(52.0, min(68.0, (attrs.get("Physical", 75) * 0.76))), 1))
            xg_p90 = float(p90.get("xg_p90") or round(max(0.06, min(0.35, g_p90 * 0.85 + 0.06)), 2))
            xa_p90 = float(p90.get("xa_p90") or round(max(0.11, min(0.42, a_p90 * 0.90 + 0.11)), 2))

            p90["pass_acc_pct"] = pass_acc
            p90["prog_passes_p90"] = prog_p
            p90["prog_carries_p90"] = prog_c
            p90["key_passes_p90"] = key_p90
            p90["tackles_interceptions_p90"] = def_act
            p90["recoveries_p90"] = recov
            p90["duel_win_pct"] = duel_w
            p90["xg_p90"] = xg_p90
            p90["xa_p90"] = xa_p90

        elif pos_cat == "Defender":
            pass_acc = float(p90.get("pass_acc_pct") or round(max(79.0, min(90.5, (attrs.get("Passing", 75) * 0.86) + 19.5)), 1))
            def_act = float(p90.get("tackles_interceptions_p90") or round(max(3.4, min(6.6, (attrs.get("Defending", 75) - 65) * 0.15 + 3.6)), 2))
            duel_w = float(p90.get("duel_win_pct") or round(max(58.0, min(75.0, (attrs.get("Defending", 75) * 0.82))), 1))
            aerial_w = float(p90.get("aerial_win_pct") or round(max(56.0, min(78.5, (attrs.get("Aerial", attrs.get("Heading", 75)) * 0.86))), 1))
            prog_p = float(p90.get("prog_passes_p90") or round(max(2.6, min(6.8, (attrs.get("Passing", 75) - 65) * 0.18 + 2.9)), 2))
            recov = float(p90.get("recoveries_p90") or round(max(4.6, min(9.5, (attrs.get("Work Rate", 75) - 65) * 0.18 + 5.1)), 2))
            xg_p90 = float(p90.get("xg_p90") or round(max(0.02, min(0.12, g_p90 * 0.80 + 0.02)), 2))
            xa_p90 = float(p90.get("xa_p90") or round(max(0.03, min(0.24, a_p90 * 0.85 + 0.03)), 2))

            p90["pass_acc_pct"] = pass_acc
            p90["tackles_interceptions_p90"] = def_act
            p90["duel_win_pct"] = duel_w
            p90["aerial_win_pct"] = aerial_w
            p90["prog_passes_p90"] = prog_p
            p90["recoveries_p90"] = recov
            p90["xg_p90"] = xg_p90
            p90["xa_p90"] = xa_p90

        else: # Goalkeeper
            save_pct = float(p.get("save_percentage") or 79.5)
            saves = float(p.get("saves_p90") or 3.2)
            cs = int(p.get("clean_sheets_26_27") or int(round(p.get("apps_26_27", 5) * 0.4)))
            psxg = float(p90.get("psxg_diff_p90") or round(max(0.08, min(0.42, (attrs.get("Reflexes", 78) - 70) * 0.025 + 0.15)), 2))
            pass_acc = float(p.get("pass_acc_pct") or round(max(68.0, min(82.0, (attrs.get("Distribution", 75) * 0.95)), 1)))

            p["save_percentage"] = save_pct
            p["saves_p90"] = saves
            p["clean_sheets_26_27"] = cs
            p["pass_acc_pct"] = pass_acc
            p90["psxg_diff_p90"] = psxg
            p90["pass_acc_pct"] = pass_acc

        # Store calculated seasonal cumulative xG and xA
        p["xg_26_27"] = round(p90.get("xg_p90", 0.1) * mins_p90, 2)
        p["xa_26_27"] = round(p90.get("xa_p90", 0.1) * mins_p90, 2)
        p["xg_diff"] = round(p["goals_26_27"] - p["xg_26_27"], 2)

        p["p90_metrics"] = p90

    # Phase 2: Compute Empirical Percentile Ranks within each position group
    df_all = pd.DataFrame(players)

    for cat in ["Attacker", "Midfielder", "Defender", "Goalkeeper"]:
        cat_indices = df_all[df_all["position_category"] == cat].index.tolist()
        if not cat_indices:
            continue

        if cat == "Attacker":
            metric_cols = [
                ("xg_p90", "pct_xg"),
                ("xa_p90", "pct_xa"),
                ("key_passes_p90", "pct_key_passes"),
                ("prog_carries_p90", "pct_prog_carries"),
                ("conversion_rate_pct", "pct_conversion"),
                ("pressures_p90", "pct_press")
            ]
        elif cat == "Midfielder":
            metric_cols = [
                ("pass_acc_pct", "pct_pass_acc"),
                ("prog_passes_p90", "pct_prog_pass"),
                ("key_passes_p90", "pct_key_pass"),
                ("tackles_interceptions_p90", "pct_def_act"),
                ("recoveries_p90", "pct_recov"),
                ("duel_win_pct", "pct_duel")
            ]
        elif cat == "Defender":
            metric_cols = [
                ("tackles_interceptions_p90", "pct_def_act"),
                ("aerial_win_pct", "pct_aerial"),
                ("duel_win_pct", "pct_duel"),
                ("prog_passes_p90", "pct_prog_pass"),
                ("pass_acc_pct", "pct_pass_acc"),
                ("recoveries_p90", "pct_recov")
            ]
        else: # Goalkeeper
            metric_cols = [
                ("save_percentage", "pct_save_pct"),
                ("saves_p90", "pct_saves"),
                ("psxg_diff_p90", "pct_psxg"),
                ("pass_acc_pct", "pct_pass_acc"),
                ("clean_sheets_26_27", "pct_cs"),
                ("Command of Area", "pct_command")
            ]

        for metric_key, pct_key in metric_cols:
            vals = []
            for idx in cat_indices:
                p = players[idx]
                p90 = p.get("p90_metrics") or {}
                attrs = p.get("attributes") or {}
                # check where key resides
                if metric_key in p90:
                    v = float(p90[metric_key])
                elif metric_key in p:
                    v = float(p[metric_key])
                elif metric_key in attrs:
                    v = float(attrs[metric_key])
                else:
                    v = 50.0
                vals.append((idx, v))

            s = pd.Series([x[1] for x in vals])
            ranks = (s.rank(pct=True) * 100).round().astype(int)
            # Clip between 15 and 99 for realistic scouting curves
            ranks = ranks.clip(lower=15, upper=99)

            for (idx, _), rank_val in zip(vals, ranks):
                players[idx]["p90_metrics"][pct_key] = int(rank_val)

    # Save enriched database
    with open(path, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=2)

    print(f"Successfully enriched all {len(players)} players with advanced analytical metrics and percentiles!")

if __name__ == "__main__":
    enrich_master_database()
