import numpy as np
import pandas as pd
import hashlib

def generate_player_shots(player: dict) -> pd.DataFrame:
    """
    Generates realistic, statistically calibrated 2D shot event coordinates (StatsBomb / Wyscout standard)
    anchored on the player's verified 2026/27 competitive season statistics.
    Pitch dimensions: 105m length x 68m width.
    Target goal is located at x=105, y=34 (between y=30.68 and y=37.32).
    """
    player_name = player.get("name", "Player")
    goals_actual = int(player.get("goals_26_27", 0))
    pos_cat = player.get("position_category", "Midfielder")
    pos_name = player.get("position", "")

    # Seed random generator with player name for deterministic reproducibility
    seed_val = int(hashlib.md5(player_name.encode('utf-8')).hexdigest()[:7], 16)
    rng = np.random.RandomState(seed_val)

    # Determine total shots taken
    p90 = player.get("p90_metrics") or {}
    mins = player.get("minutes_26_27", 300)
    shots_p90 = float(p90.get("shots_p90", 2.5 if pos_cat == "Attacker" else 1.2 if pos_cat == "Midfielder" else 0.4))
    total_shots = max(goals_actual, int(round((mins / 90.0) * shots_p90)))

    if total_shots <= 0:
        if goals_actual > 0:
            total_shots = goals_actual
        else:
            return pd.DataFrame(columns=["shot_id", "x", "y", "distance_m", "xg", "outcome", "body_part", "period"])

    shots = []
    # Distribute outcomes: Goals, Saved, Blocked, Missed
    saved_count = max(0, int(total_shots * 0.35))
    blocked_count = max(0, int(total_shots * 0.20))
    missed_count = max(0, total_shots - goals_actual - saved_count - blocked_count)

    outcomes_pool = (
        ["Goal"] * goals_actual +
        ["Saved"] * saved_count +
        ["Blocked"] * blocked_count +
        ["Missed"] * missed_count
    )
    rng.shuffle(outcomes_pool)

    preferred_foot = player.get("preferred_foot", "Right")

    for idx, outcome in enumerate(outcomes_pool):
        is_goal = (outcome == "Goal")

        if is_goal:
            # Goals are predominantly inside 18-yard box (x between 89 and 102, y between 24 and 44)
            if "Forward" in pos_name or "Striker" in pos_name or "Bérgson" in player_name:
                # 6-yard box and central box poach
                x = rng.normal(loc=98.5, scale=3.5)
                y = rng.normal(loc=34.0, scale=4.5)
            else:
                # Wingers / Midfielders cutting in
                x = rng.normal(loc=93.0, scale=5.0)
                y = rng.normal(loc=34.0, scale=8.0)
        elif outcome == "Saved":
            x = rng.normal(loc=92.0, scale=5.5)
            y = rng.normal(loc=34.0, scale=9.0)
        elif outcome == "Blocked":
            x = rng.normal(loc=86.0, scale=6.0)
            y = rng.normal(loc=34.0, scale=11.0)
        else: # Missed
            x = rng.normal(loc=84.0, scale=8.0)
            y = rng.normal(loc=34.0, scale=14.0)

        # Clip within half-pitch boundaries (x between 70 and 104, y between 4 and 64)
        x = float(np.clip(x, 70.0, 104.2))
        y = float(np.clip(y, 6.0, 62.0))

        # Calculate geometric distance to goal centre (105, 34)
        dx = 105.0 - x
        dy = 34.0 - y
        dist_m = float(np.sqrt(dx**2 + dy**2))

        # Calculate calibrated xG value based on distance and angle
        angle_rad = np.arctan2(7.32 * dx, dx**2 + dy**2 - (7.32/2)**2)
        angle_rad = abs(angle_rad) if not np.isnan(angle_rad) else 0.3

        base_xg = float(np.exp(-0.11 * dist_m) * (angle_rad / 1.1))
        if is_goal:
            base_xg = max(0.18, min(0.78, base_xg * 1.35 + 0.12))
        else:
            base_xg = max(0.02, min(0.45, base_xg))

        xg_val = round(float(base_xg), 2)

        # Body part
        if dist_m < 9.0 and rng.rand() < 0.35:
            body_part = "Header"
        elif rng.rand() < 0.75:
            body_part = preferred_foot + " Foot"
        else:
            other_foot = "Left" if preferred_foot == "Right" else "Right"
            body_part = other_foot + " Foot"

        period = rng.choice(["1st Half", "2nd Half"], p=[0.45, 0.55])

        shots.append({
            "shot_id": idx + 1,
            "x": round(x, 1),
            "y": round(y, 1),
            "distance_m": round(dist_m, 1),
            "xg": xg_val,
            "outcome": outcome,
            "body_part": body_part,
            "period": period
        })

    return pd.DataFrame(shots)
