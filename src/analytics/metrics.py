import pandas as pd
import numpy as np

def calculate_scouting_score(player: dict) -> float:
    """
    Calculate overall scouting readiness index (0-100) combining:
    - League coefficient (J1 / Eredivisie = 1.3, MSL / Thai 1 = 1.0, lower tiers = 0.8)
    - Match minutes regular status
    - Average ratings (FotMob / SofaScore)
    - Age factor (peak curve 23-28)
    """
    league = player.get("league", "")
    age = player.get("age", 25)
    rating = player.get("fotmob_rating", player.get("sofascore_rating", 7.0))
    minutes = player.get("minutes_26_27", 300)

    # League multiplier
    if any(k in league for k in ["J1", "Eredivisie", "Bundesliga", "MLS"]):
        league_mult = 1.3
    elif any(k in league for k in ["Thai League", "Cyprus", "Super League"]):
        league_mult = 1.05
    else:
        league_mult = 0.9

    # Rating contribution (scale from 6.0-9.0 to 0-40)
    rating_score = max(0, min(40, (rating - 6.0) * (40 / 2.5)))

    # Minutes contribution (up to 30)
    minutes_score = min(30, (minutes / 600.0) * 30)

    # Age optimization curve (peak at 24-28)
    if 23 <= age <= 28:
        age_score = 30
    elif 19 <= age < 23:
        age_score = 28  # High future potential bonus
    elif 29 <= age <= 33:
        age_score = 25
    else:
        age_score = 20

    raw_score = (rating_score + minutes_score + age_score) * (league_mult / 1.1)
    return round(min(99.0, max(45.0, raw_score)), 1)

def get_player_archetype(position: str, attributes: dict) -> str:
    """Classify player into tactical tactical archetype based on primary traits."""
    if not attributes:
        return "All-Rounder"

    if "Goalkeeper" in position:
        if attributes.get("Distribution", 0) > 75:
            return "Modern Sweeper Keeper"
        return "Traditional Shot Stopper"

    if any(p in position for p in ["Centre-Back", "Defender"]):
        if attributes.get("Passing", 0) > 75 or attributes.get("Tactical Awareness", 0) > 82:
            return "Ball-Playing Defender"
        if attributes.get("Aerial", 0) > 80:
            return "No-Nonsense Stopper"
        return "Complete Central Defender"

    if any(p in position for p in ["Right-Back", "Left-Back"]):
        if attributes.get("Pace", 0) > 78 and attributes.get("Passing", 0) > 74:
            return "Attacking Wingback"
        return "Inverted Fullback"

    if "Defensive Midfield" in position:
        if attributes.get("Passing", 0) > 80:
            return "Deep-Lying Playmaker (Regista)"
        return "Defensive Ball-Winner (Anchor)"

    if "Central Midfield" in position:
        if attributes.get("Work Rate", 0) > 82 or attributes.get("Physical", 0) > 78:
            return "Box-to-Box Engine"
        return "Creative Midfield Controller"

    if any(p in position for p in ["Winger", "Right Winger", "Left Winger"]):
        if attributes.get("Passing", 0) > 84 or attributes.get("Vision", 0) > 85:
            return "Inverted Playmaker"
        return "Explosive Classic Winger"

    if any(p in position for p in ["Centre-Forward", "Striker"]):
        if attributes.get("Aerial", 0) > 84 or attributes.get("Heading", 0) > 82:
            return "Target Man & Box Dominator"
        if attributes.get("Pace", 0) > 82:
            return "Advanced Poacher"
        return "Complete Forward"

    return "Tactical Specialist"
