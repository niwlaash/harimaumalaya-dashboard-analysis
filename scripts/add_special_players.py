import json
import os

def add_players():
    path = "data/malaysian_prospects.json"
    with open(path, "r", encoding="utf-8") as f:
        prospects = json.load(f)

    existing_names = {p["name"].lower() for p in prospects}

    new_players = [
        {
            "id": 118,
            "name": "Bérgson",
            "full_name": "Bérgson Gustavo Silveira da Silva",
            "age": 35,
            "dob": "1991-02-09",
            "height": 181,
            "position": "Centre-Forward",
            "secondary_positions": ["Second Striker", "Attacking Midfield"],
            "position_category": "Attacker",
            "preferred_foot": "Right",
            "club": "Johor Darul Ta'zim",
            "league": "Malaysia Super League",
            "country": "Malaysia",
            "citizenship": "Malaysia / Brazil",
            "eligibility_type": "5-Year Residency Naturalization (2021-2026)",
            "pool_status": "Heritage & Scouting Prospect",
            "tier": "Naturalization / Star Prospect",
            "readiness_index": 93,
            "market_value_eur": 450000,
            "contract_expires": "2027-12-31",
            "transfermarkt_id": 103585,
            "fotmob_id": 212458,
            "sofascore_id": 142981,
            "minutes_25_26": 2420,
            "minutes_26_27": 580,
            "apps_26_27": 7,
            "goals_26_27": 8,
            "assists_26_27": 3,
            "goal_contributions_26_27": 11,
            "fotmob_rating": 8.18,
            "sofascore_rating": 8.12,
            "recent_form": [8.4, 7.9, 8.5, 8.0, 8.1],
            "attributes": {
                "Pace": 78,
                "Shooting": 91,
                "Finishing": 92,
                "Physical": 84,
                "Heading": 86,
                "Composure": 88,
                "Work Rate": 82
            },
            "p90_metrics": {
                "goals_p90": 1.24,
                "shots_p90": 4.8,
                "conversion_rate_pct": 28.5,
                "xG_p90": 0.88,
                "duel_win_pct": 58.5
            },
            "heatmap_type": "advanced_forward",
            "scouting_summary": "All-time record goalscorer for Johor Darul Ta'zim with over 130 competitive goals. Lethal penalty box instincts, elite aerial timing, and devastating finishing across domestic and AFC Champions League Elite competitions. Naturalization candidate via 5-year continuous Malaysian residency.",
            "photo_url": "https://img.a.transfermarkt.technology/portrait/header/103585-1673783389.jpg?lm=4711"
        },
        {
            "id": 119,
            "name": "Manuel Hidalgo",
            "full_name": "Manuel Federico Hidalgo",
            "age": 27,
            "dob": "1999-05-03",
            "height": 169,
            "position": "Right Winger",
            "secondary_positions": ["Attacking Midfield", "Left Winger"],
            "position_category": "Attacker",
            "preferred_foot": "Left",
            "club": "Johor Darul Ta'zim",
            "league": "Malaysia Super League",
            "country": "Malaysia",
            "citizenship": "Malaysia / Argentina",
            "eligibility_type": "5-Year Residency Naturalization (2021-2026)",
            "pool_status": "Heritage & Scouting Prospect",
            "tier": "Naturalization / Star Prospect",
            "readiness_index": 86,
            "market_value_eur": 400000,
            "contract_expires": "2028-05-31",
            "transfermarkt_id": 568391,
            "fotmob_id": 1102914,
            "sofascore_id": 991823,
            "minutes_25_26": 2100,
            "minutes_26_27": 510,
            "apps_26_27": 6,
            "goals_26_27": 3,
            "assists_26_27": 5,
            "goal_contributions_26_27": 8,
            "fotmob_rating": 7.64,
            "sofascore_rating": 7.60,
            "recent_form": [7.5, 7.8, 7.4, 7.9, 7.6],
            "attributes": {
                "Pace": 82,
                "Dribbling": 88,
                "Passing": 84,
                "Shooting": 80,
                "Agility": 90,
                "Vision": 83,
                "Work Rate": 80
            },
            "p90_metrics": {
                "dribbles_succ_p90": 4.1,
                "key_passes_p90": 2.8,
                "crosses_acc_pct": 38.0,
                "pass_acc_pct": 82.5,
                "goals_p90": 0.53
            },
            "heatmap_type": "inverted_winger_right",
            "scouting_summary": "Argentine-born technical virtuoso who has starred across the Malaysia Super League since 2021 (Sri Pahang, Kedah, JDT). Exceptional low center of gravity, creative vision in central half-spaces, and dangerous curling deliveries from set pieces.",
            "photo_url": "https://img.a.transfermarkt.technology/portrait/header/534358-1569492781.jpg?lm=4711"
        },
        {
            "id": 120,
            "name": "Nacho Méndez",
            "full_name": "Ignacio Méndez-Navia Fernández",
            "age": 28,
            "dob": "1998-03-30",
            "height": 180,
            "position": "Central Midfield",
            "secondary_positions": ["Defensive Midfield", "Attacking Midfield"],
            "position_category": "Midfielder",
            "preferred_foot": "Right",
            "club": "Johor Darul Ta'zim",
            "league": "Malaysia Super League",
            "country": "Malaysia",
            "citizenship": "Malaysia / Spain",
            "eligibility_type": "Heritage (Penang Grandfather Lineage) / Malaysian Citizen",
            "pool_status": "Heritage & Scouting Prospect",
            "tier": "Heritage / National Pool Candidate",
            "readiness_index": 92,
            "market_value_eur": 1200000,
            "contract_expires": "2028-12-31",
            "transfermarkt_id": 494576,
            "fotmob_id": 894512,
            "sofascore_id": 878345,
            "minutes_25_26": 2250,
            "minutes_26_27": 540,
            "apps_26_27": 6,
            "goals_26_27": 2,
            "assists_26_27": 3,
            "goal_contributions_26_27": 5,
            "fotmob_rating": 7.62,
            "sofascore_rating": 7.58,
            "recent_form": [7.7, 7.5, 7.8, 7.4, 7.7],
            "attributes": {
                "Pace": 74,
                "Passing": 88,
                "Vision": 87,
                "Composure": 86,
                "Tactical IQ": 88,
                "Work Rate": 84,
                "Defending": 78,
                "Physical": 77
            },
            "p90_metrics": {
                "pass_acc_pct": 88.5,
                "progressive_passes_p90": 7.2,
                "tackles_p90": 2.4,
                "interceptions_p90": 1.8,
                "key_passes_p90": 2.2
            },
            "heatmap_type": "midfield_pivot",
            "scouting_summary": "High-pedigree Spanish-born midfielder with over 200 appearances for Sporting de Gijón in Spanish Segunda División. Registered with Malaysian citizenship in July 2025 via Penang grandfather heritage. Dictates play with elite passing accuracy, press resistance, and metronomic tempo control.",
            "photo_url": "https://img.a.transfermarkt.technology/portrait/header/494576-1701336495.jpg?lm=4711"
        }
    ]

    for np in new_players:
        if np["name"].lower() not in existing_names:
            prospects.append(np)
            print(f"Added player: {np['name']}")
        else:
            print(f"Player already in database: {np['name']}")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(prospects, f, indent=2)

    print(f"Total prospects now: {len(prospects)}")

if __name__ == "__main__":
    add_players()
