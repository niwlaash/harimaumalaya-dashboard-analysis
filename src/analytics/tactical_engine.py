import pandas as pd
import numpy as np

def calculate_team_tactical_balance(starting_xi_players: list) -> dict:
    """
    Computes professional team tactical balance indices (0-100)
    for a chosen starting XI (Football Manager style).
    """
    if not starting_xi_players:
        return {
            "attacking_threat": 75.0,
            "defensive_solidity": 75.0,
            "pressing_intensity": 75.0,
            "passing_fluidity": 75.0,
            "aerial_dominance": 75.0,
            "average_age": 26.5
        }

    # Extract player attribute dictionaries
    outfield = [p for p in starting_xi_players if "Goalkeeper" not in p.get("position", "")]
    all_players = starting_xi_players

    # 1. Attacking Threat
    attackers_and_mid = [p for p in outfield if any(c in p.get("position_category", "") for c in ["Attacker", "Midfielder"])]
    if not attackers_and_mid:
        attackers_and_mid = outfield
    att_scores = []
    for p in attackers_and_mid:
        attr = p.get("attributes", {})
        score = (
            attr.get("Shooting", attr.get("Finishing", 75)) * 0.35 +
            attr.get("Dribbling", 75) * 0.25 +
            attr.get("Passing", 75) * 0.20 +
            attr.get("Pace", 75) * 0.20
        )
        att_scores.append(score)
    attacking_threat = round(float(np.mean(att_scores)), 1) if att_scores else 75.0

    # 2. Defensive Solidity
    defenders_and_dm = [p for p in all_players if any(c in p.get("position_category", "") for c in ["Defender", "Goalkeeper"]) or "Defensive Midfield" in p.get("position", "")]
    if not defenders_and_dm:
        defenders_and_dm = all_players
    def_scores = []
    for p in defenders_and_dm:
        attr = p.get("attributes", {})
        score = (
            attr.get("Defending", attr.get("Shot Stopping", 78)) * 0.40 +
            attr.get("Tactical Awareness", attr.get("Positioning", 76)) * 0.30 +
            attr.get("Physical", 76) * 0.30
        )
        def_scores.append(score)
    defensive_solidity = round(float(np.mean(def_scores)), 1) if def_scores else 75.0

    # 3. Pressing & Work Rate
    press_scores = []
    for p in outfield:
        attr = p.get("attributes", {})
        score = (
            attr.get("Work Rate", 80) * 0.45 +
            attr.get("Pace", 75) * 0.30 +
            attr.get("Physical", 75) * 0.25
        )
        press_scores.append(score)
    pressing_intensity = round(float(np.mean(press_scores)), 1) if press_scores else 78.0

    # 4. Passing Fluidity
    pass_scores = []
    for p in outfield:
        attr = p.get("attributes", {})
        score = (
            attr.get("Passing", 76) * 0.50 +
            attr.get("Tactical Awareness", attr.get("Vision", 76)) * 0.30 +
            attr.get("Dribbling", 74) * 0.20
        )
        pass_scores.append(score)
    passing_fluidity = round(float(np.mean(pass_scores)), 1) if pass_scores else 76.0

    # 5. Aerial Dominance
    aerial_scores = []
    for p in all_players:
        attr = p.get("attributes", {})
        score = (
            attr.get("Aerial", attr.get("Heading", 72)) * 0.60 +
            attr.get("Physical", 75) * 0.40
        )
        aerial_scores.append(score)
    aerial_dominance = round(float(np.mean(aerial_scores)), 1) if aerial_scores else 74.0

    avg_age = round(float(np.mean([p.get("age", 26) for p in all_players])), 1)

    return {
        "attacking_threat": attacking_threat,
        "defensive_solidity": defensive_solidity,
        "pressing_intensity": pressing_intensity,
        "passing_fluidity": passing_fluidity,
        "aerial_dominance": aerial_dominance,
        "average_age": avg_age
    }

def analyze_player_swap(player_out: dict, player_in: dict) -> dict:
    """
    Generates a coach / Performance Analyst swap delta comparison between two players.
    """
    attr_out = player_out.get("attributes", {})
    attr_in = player_in.get("attributes", {})

    deltas = {}
    for metric in ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical", "Work Rate"]:
        v_out = attr_out.get(metric, 75)
        v_in = attr_in.get(metric, 75)
        deltas[metric] = v_in - v_out

    # Minutes & Ratings deltas
    min_delta = player_in.get("minutes_26_27", 0) - player_out.get("minutes_26_27", 0)
    rating_out = player_out.get("fotmob_rating", 7.0)
    rating_in = player_in.get("fotmob_rating", 7.0)
    rating_delta = round(rating_in - rating_out, 2)

    # Tactical Pros and Trade-offs
    advantages = []
    tradeoffs = []

    if deltas["Pace"] >= 5:
        advantages.append(f"+{deltas['Pace']} Pace: Superior counter-attack speed and recovery sprints.")
    elif deltas["Pace"] <= -5:
        tradeoffs.append(f"{deltas['Pace']} Pace: Reduced burst against high-defensive lines.")

    if deltas["Defending"] >= 5:
        advantages.append(f"+{deltas['Defending']} Defending: Stronger transition shielding and tackle success.")
    elif deltas["Defending"] <= -5:
        tradeoffs.append(f"{deltas['Defending']} Defending: Lower defensive work when defending transitions.")

    if deltas["Passing"] >= 5:
        advantages.append(f"+{deltas['Passing']} Passing: Higher build-up composure and through-ball frequency.")
    elif deltas["Passing"] <= -5:
        tradeoffs.append(f"{deltas['Passing']} Passing: Decreased progressive pass completion in tight channels.")

    if deltas["Work Rate"] >= 5:
        advantages.append(f"+{deltas['Work Rate']} Work Rate: Relentless pressing engine and defensive tracking.")
    elif deltas["Work Rate"] <= -5:
        tradeoffs.append(f"{deltas['Work Rate']} Work Rate: May require deeper defensive support.")

    if not advantages:
        advantages.append("Balanced profile: Similar stylistic output with fresh legs and match sharpness.")
    if not tradeoffs:
        tradeoffs.append("Minimal trade-offs: Lateral stylistic transition without defensive compromise.")

    return {
        "deltas": deltas,
        "min_delta": min_delta,
        "rating_delta": rating_delta,
        "advantages": advantages,
        "tradeoffs": tradeoffs
    }
