import numpy as np
import pandas as pd

def compute_player_feature_vector(player: dict) -> np.ndarray:
    """
    Extracts a standardized 10-dimensional analytical feature vector for cosine similarity matching.
    Dimensions:
    1. Attacking output (Goals p90 + xG p90)
    2. Playmaking output (Assists p90 + xA p90)
    3. Passing accuracy & security (Pass Acc %)
    4. Progression capacity (Prog Passes p90 + Prog Carries p90)
    5. Chance creation (Key Passes p90)
    6. Defensive disruption (Tackles + Interceptions p90)
    7. Duel dominance (Duel Win %)
    8. Physicality / Work Rate attribute
    9. Technical composure / Dribbling attribute
    10. Overall Readiness Index
    """
    p90 = player.get("p90_metrics") or {}
    attrs = player.get("attributes") or {}

    g_p90 = float(p90.get("goals_p90", player.get("goals_26_27", 0) / max(1, player.get("minutes_26_27", 90) / 90)))
    xg_p90 = float(p90.get("xg_p90", g_p90 * 0.85))
    a_p90 = float(p90.get("assists_p90", player.get("assists_26_27", 0) / max(1, player.get("minutes_26_27", 90) / 90)))
    xa_p90 = float(p90.get("xa_p90", a_p90 * 0.9))

    pass_acc = float(p90.get("pass_acc_pct", player.get("pass_acc_pct", 80.0)))
    prog_pass = float(p90.get("prog_passes_p90", 4.0))
    prog_carry = float(p90.get("prog_carries_p90", 3.0))
    key_pass = float(p90.get("key_passes_p90", 1.5))
    def_act = float(p90.get("tackles_interceptions_p90", p90.get("tackles_p90", 2.0) + p90.get("interceptions_p90", 1.5)))
    duel_win = float(p90.get("duel_win_pct", 55.0))

    phys = float(attrs.get("Physical", attrs.get("Work Rate", 75.0)))
    tech = float(attrs.get("Dribbling", attrs.get("Passing", 75.0)))
    readiness = float(player.get("readiness_index", 75.0))

    # Standardized normalized components (0 - 100 scale baseline)
    vec = np.array([
        (g_p90 + xg_p90) * 35.0,
        (a_p90 + xa_p90) * 45.0,
        pass_acc,
        (prog_pass + prog_carry) * 8.0,
        key_pass * 28.0,
        def_act * 15.0,
        duel_win,
        phys,
        tech,
        readiness
    ], dtype=float)

    return vec

def find_similar_players(target_player: dict, player_pool: list, top_n: int = 3) -> list:
    """
    Data Science Cosine Similarity engine that identifies the closest tactical and statistical lookalikes.
    Filters within compatible positional families unless specified otherwise.
    """
    target_name = target_player.get("name", "")
    target_pos_cat = target_player.get("position_category", "Midfielder")
    target_age = target_player.get("age", 25)
    target_vec = compute_player_feature_vector(target_player)
    target_norm = np.linalg.norm(target_vec)

    if target_norm == 0:
        return []

    candidates = []
    for candidate in player_pool:
        c_name = candidate.get("name", "")
        if c_name == target_name:
            continue

        c_pos_cat = candidate.get("position_category", "")
        # Prioritize same or adjacent positional family
        if target_pos_cat != c_pos_cat:
            # allow attacker/midfielder crossover or defender/midfielder crossover with slight penalty
            if not ((target_pos_cat in ["Attacker", "Midfielder"] and c_pos_cat in ["Attacker", "Midfielder"]) or
                    (target_pos_cat in ["Defender", "Midfielder"] and c_pos_cat in ["Defender", "Midfielder"])):
                continue

        c_vec = compute_player_feature_vector(candidate)
        c_norm = np.linalg.norm(c_vec)
        if c_norm == 0:
            continue

        cosine_sim = float(np.dot(target_vec, c_vec) / (target_norm * c_norm))
        # Scale into intuitive 70% - 99% similarity score
        sim_pct = round(min(99.4, max(60.0, cosine_sim * 100.0)), 1)

        c_age = candidate.get("age", 25)
        if c_age < target_age and (target_age - c_age) >= 3:
            archetype_badge = "Young High-Ceiling Twin"
        elif abs(c_age - target_age) <= 3 and sim_pct >= 94.0:
            archetype_badge = "Direct Tactical Replacement"
        elif candidate.get("club") != target_player.get("club"):
            archetype_badge = "Cross-Club Scouting Match"
        else:
            archetype_badge = "Squad Rotation Lookalike"

        candidates.append({
            "player": candidate,
            "similarity_pct": sim_pct,
            "badge": archetype_badge,
            "age_diff": c_age - target_age,
            "market_value": candidate.get("market_value_eur", 0),
            "club": candidate.get("club", "Free Agent"),
            "position": candidate.get("position", "")
        })

    candidates.sort(key=lambda x: x["similarity_pct"], reverse=True)
    return candidates[:top_n]
