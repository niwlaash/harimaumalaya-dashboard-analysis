import requests
import json
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.sofascore.com/"
}

class SofascoreCollector:
    """Collector for SofaScore player attributes, ratings, and heatmaps."""
    def __init__(self, cache_dir="data/cache/sofascore"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch_player_details(self, player_id: int):
        """Fetch SofaScore player details and current ratings."""
        cache_path = os.path.join(self.cache_dir, f"player_{player_id}.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        url = f"https://api.sofascore.com/api/v1/player/{player_id}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                return data
        except Exception as e:
            print(f"[SofascoreCollector] Error fetching SofaScore player {player_id}: {e}")

        return None

    def fetch_player_attribute_radar(self, player_id: int):
        """Fetch player attribute ratings (attacking, defending, tactical, technical, creativity)."""
        url = f"https://api.sofascore.com/api/v1/player/{player_id}/attribute-overviews"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return None
