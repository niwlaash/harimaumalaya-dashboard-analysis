import requests
from bs4 import BeautifulSoup
import time
import json
import os
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

class TransfermarktCollector:
    """Collector for Transfermarkt player and squad data."""
    def __init__(self, cache_dir="data/cache/transfermarkt"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch_player_profile(self, player_id: int, player_slug: str = "player"):
        """Fetch player profile html and parse core biographical & market data."""
        cache_path = os.path.join(self.cache_dir, f"profile_{player_id}.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        url = f"https://www.transfermarkt.com/{player_slug}/profil/spieler/{player_id}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                data = self._parse_profile_soup(soup, player_id)
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                return data
        except Exception as e:
            print(f"[TransfermarktCollector] Error fetching player {player_id}: {e}")

        return None

    def _parse_profile_soup(self, soup: BeautifulSoup, player_id: int):
        """Parse core attributes from Transfermarkt profile page."""
        data = {"player_id": player_id}
        
        # Name
        h1 = soup.find("h1", class_="data-header__headline-wrapper")
        if h1:
            data["name"] = h1.get_text(strip=True).replace("\n", " ")

        # Market Value
        mv_box = soup.find("a", class_="data-header__market-value-wrapper")
        if mv_box:
            data["market_value_str"] = mv_box.get_text(strip=True)

        # Club
        club_span = soup.find("span", class_="data-header__club")
        if club_span:
            data["club"] = club_span.get_text(strip=True)

        # Labels (DOB, height, citizenship, etc.)
        info_items = soup.find_all("li", class_="data-header__label")
        for item in info_items:
            text = item.get_text(strip=True)
            content = item.find_next_sibling("span", class_="data-header__content")
            if content:
                c_text = content.get_text(strip=True)
                if "Date of birth" in text:
                    data["dob"] = c_text
                elif "Citizenship" in text:
                    data["citizenship"] = c_text
                elif "Height" in text:
                    data["height"] = c_text
                elif "Position" in text:
                    data["position"] = c_text

        return data

    def fetch_club_season_stats(self, club_id: int, season: str = "2026"):
        """Fetch detailed club performance data table (appearances, goals, assists, minutes)."""
        url = f"https://www.transfermarkt.com/club/leistungsdaten/verein/{club_id}/reldata/%26{season}/plus/1"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                table = soup.find("table", class_="items")
                if not table:
                    return []
                
                rows = []
                for tr in table.find_all("tr"):
                    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                    if len(cols) >= 10:
                        rows.append(cols)
                return rows
        except Exception as e:
            print(f"[TransfermarktCollector] Error fetching club {club_id}: {e}")
        return []
