import json
import os
import pandas as pd

class DataAggregator:
    """Aggregates and normalizes player records from local verified datasets and live collectors."""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def load_squad(self) -> pd.DataFrame:
        """Load the verified 23-player Malaysia squad from FIFA ASEAN Cup 2026."""
        path = os.path.join(self.data_dir, "squad_asean_2026.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Squad data not found at {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        
        # Calculate derived metrics
        df["goals_p90"] = df.apply(
            lambda r: round((r["goals_26_27"] / r["minutes_26_27"]) * 90, 2) if r["minutes_26_27"] > 0 else 0.0, axis=1
        )
        df["assists_p90"] = df.apply(
            lambda r: round((r["assists_26_27"] / r["minutes_26_27"]) * 90, 2) if r["minutes_26_27"] > 0 else 0.0, axis=1
        )
        df["goal_contributions_26_27"] = df["goals_26_27"] + df["assists_26_27"]
        df["contrib_p90"] = df.apply(
            lambda r: round((r["goal_contributions_26_27"] / r["minutes_26_27"]) * 90, 2) if r["minutes_26_27"] > 0 else 0.0, axis=1
        )
        return df

    def load_prospects(self) -> pd.DataFrame:
        """Load the comprehensive Malaysian prospects and heritage database."""
        path = os.path.join(self.data_dir, "malaysian_prospects.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Prospects data not found at {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return pd.DataFrame(data)

    def get_all_players_combined(self) -> pd.DataFrame:
        """Combine national team squad with prospective pool for scouting comparisons."""
        squad = self.load_squad()
        prospects = self.load_prospects()
        
        squad["squad_category"] = "Senior National Team (ASEAN Cup 2026)"
        prospects["squad_category"] = "Prospect / Heritage Pool"
        
        combined = pd.concat([squad, prospects], ignore_index=True)
        return combined
