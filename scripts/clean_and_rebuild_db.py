import json
import os
import urllib.parse

def clean_database():
    print("--- 1. Cleaning squad_asean_2026.json ---")
    with open("data/squad_asean_2026.json", "r", encoding="utf-8") as f:
        squad = json.load(f)

    # Filter out Bergson and Manuel Hidalgo (ineligible foreign players)
    eligible_squad = []
    for p in squad:
        name = p["name"]
        if "Bérgson" in name or "Bergson" in name or "Hidalgo" in name:
            print(f"REMOVING INELIGIBLE SQUAD PLAYER: {name}")
            continue
        eligible_squad.append(p)

    # Add Romel Morales and Safawi Rasid if not already present
    squad_names = [p["name"] for p in eligible_squad]
    if "Romel Morales" not in squad_names:
        romel = {
            "id": 20,
            "name": "Romel Morales",
            "full_name": "Romel Oswaldo Morales Ramírez",
            "age": 28,
            "dob": "1997-08-23",
            "height": 187,
            "position": "Centre-Forward",
            "position_category": "Attacker",
            "preferred_foot": "Right",
            "club": "Johor Darul Ta'zim",
            "league": "Malaysia Super League",
            "country": "Malaysia",
            "market_value_eur": 350000,
            "contract_expires": "2027-12-31",
            "transfermarkt_id": 486821,
            "fotmob_id": 894318,
            "sofascore_id": 850234,
            "minutes_25_26": 1720,
            "minutes_26_27": 480,
            "apps_26_27": 6,
            "goals_26_27": 3,
            "assists_26_27": 1,
            "fotmob_rating": 7.38,
            "sofascore_rating": 7.40,
            "attributes": {"Pace": 78, "Shooting": 85, "Passing": 76, "Dribbling": 79, "Heading": 86, "Physical": 84, "Work Rate": 83},
            "p90_metrics": {"goals_p90": 0.56, "shots_p90": 2.8, "duel_win_pct": 64.5, "pass_acc_pct": 79.2},
            "scouting_summary": "Naturalized Malaysian forward. Hero of Malaysia's 3-3 draw vs South Korea at AFC Asian Cup 2023 with 90+15' equalizer. Towering target man with physical hold-up and clinical box finishing.",
            "photo_url": "https://ui-avatars.com/api/?name=Romel+Morales&background=1e293b&color=f59e0b&size=150&bold=true&font-size=0.38"
        }
        eligible_squad.append(romel)
        print("ADDED ELIGIBLE STRIKER: Romel Morales")

    if "Safawi Rasid" not in squad_names:
        safawi = {
            "id": 22,
            "name": "Safawi Rasid",
            "full_name": "Muhammad Safawi bin Rasid",
            "age": 28,
            "dob": "1997-03-05",
            "height": 173,
            "position": "Right Winger",
            "secondary_positions": ["Left Winger", "Centre-Forward"],
            "position_category": "Attacker",
            "preferred_foot": "Left",
            "club": "Terengganu FC",
            "league": "Malaysia Super League",
            "country": "Malaysia",
            "market_value_eur": 275000,
            "contract_expires": "2026-11-30",
            "transfermarkt_id": 483677,
            "fotmob_id": 873953,
            "sofascore_id": 850239,
            "minutes_25_26": 1820,
            "minutes_26_27": 540,
            "apps_26_27": 6,
            "goals_26_27": 3,
            "assists_26_27": 2,
            "fotmob_rating": 7.34,
            "sofascore_rating": 7.36,
            "attributes": {"Pace": 83, "Shooting": 84, "Passing": 79, "Dribbling": 82, "Physical": 77, "Work Rate": 84},
            "p90_metrics": {"goals_p90": 0.50, "shots_p90": 3.2, "key_passes_p90": 2.1, "pass_acc_pct": 81.0},
            "scouting_summary": "Long-standing talismanic Malaysian winger and dead-ball specialist with over 60 caps and 20 international goals.",
            "photo_url": "https://ui-avatars.com/api/?name=Safawi+Rasid&background=1e293b&color=f59e0b&size=150&bold=true&font-size=0.38"
        }
        eligible_squad.append(safawi)
        print("ADDED ELIGIBLE WINGER: Safawi Rasid")

    with open("data/squad_asean_2026.json", "w", encoding="utf-8") as f:
        json.dump(eligible_squad, f, indent=2)
    print(f"Squad cleaned: {len(eligible_squad)} eligible players.")

    print("\n--- 2. Cleaning malaysian_prospects.json ---")
    with open("data/malaysian_prospects.json", "r", encoding="utf-8") as f:
        prospects = json.load(f)

    eligible_prospects = []
    for p in prospects:
        name = p["name"]
        if name in ["Mats Deijl", "Ferdy Druijf", "Sem Scheperman", "Julian Bechler"]:
            print(f"REMOVING INELIGIBLE PROSPECT: {name} (FIFA Article 8 ineligibility / unverified)")
            continue
        # Ensure photo_url is clean
        name_enc = urllib.parse.quote(name)
        if not p.get("photo_url") or "default" in p.get("photo_url", "") or "dicebear" in p.get("photo_url", ""):
            p["photo_url"] = f"https://ui-avatars.com/api/?name={name_enc}&background=1e293b&color=f59e0b&size=150&bold=true&font-size=0.38"
        eligible_prospects.append(p)

    with open("data/malaysian_prospects.json", "w", encoding="utf-8") as f:
        json.dump(eligible_prospects, f, indent=2)
    print(f"Prospects cleaned: {len(eligible_prospects)} eligible prospects.")

    print("\n--- 3. Rebuilding master player database ---")
    # Load all and assemble into master database
    with open("data/past_internationals_3yrs.json", "r", encoding="utf-8") as f:
        past = json.load(f)

    # Import build_master_db and re-run
    import scripts.build_master_db as b_db
    b_db.main()

if __name__ == "__main__":
    clean_database()
