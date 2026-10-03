import json

with open("data/malaysia_master_player_database.json", "r", encoding="utf-8") as f:
    players = json.load(f)

for idx, p in enumerate(players):
    name = p["name"]
    club = p.get("club", "")
    pool = p.get("pool_status", "")
    elig = p.get("eligibility_type", "")
    # Check for keywords that might indicate ineligibility
    print(f"{idx+1:3d}. {name:25} | {club:30} | {pool}")
