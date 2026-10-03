import requests
import json
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}

class FotmobCollector:
    """Collector for FotMob match ratings, xG/xA, and player performance metrics."""
    def __init__(self, cache_dir="data/cache/fotmob"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch_player_data(self, player_id: int):
        """Fetch FotMob player details from public API."""
        cache_path = os.path.join(self.cache_dir, f"player_{player_id}.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        url = f"https://www.fotmob.com/api/playerData?id={player_id}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                return data
        except Exception as e:
            print(f"[FotmobCollector] Error fetching FotMob player {player_id}: {e}")

        return None

    def extract_recent_ratings(self, player_data: dict) -> list:
        """Extract last 5 match ratings from FotMob match history."""
        if not player_data:
            return []
        
        ratings = []
        try:
            matches = player_data.get("recentMatches", [])
            for m in matches[:5]:
                rating = m.get("rating", {}).get("num")
                if rating:
                    ratings.append(float(rating))
        except Exception:
            pass
        return ratings
