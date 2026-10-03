import json
import os
import pandas as pd

class DataAggregator:
    """Aggregates and normalizes player records from local verified datasets and master league databases."""
    
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
        self._add_derived_metrics(df)
        return df

    def load_prospects(self) -> pd.DataFrame:
        """Load the comprehensive Malaysian prospects and heritage database (in league and abroad)."""
        path = os.path.join(self.data_dir, "malaysian_prospects.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Prospects data not found at {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        df = pd.DataFrame(data)
        self._add_derived_metrics(df)
        return df

    def load_past_internationals(self) -> pd.DataFrame:
        """Load players who represented Malaysia in the last 3 years cycle (2023-2026)."""
        path = os.path.join(self.data_dir, "past_internationals_3yrs.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Past internationals data not found at {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        df = pd.DataFrame(data)
        self._add_derived_metrics(df)
        return df

    def load_master_database(self) -> pd.DataFrame:
        """Load the complete 109+ player database covering all 13 MSL clubs and overseas Malaysians."""
        path = os.path.join(self.data_dir, "malaysia_master_player_database.json")
        if not os.path.exists(path):
            # Fallback to combined if master file hasn't been generated yet
            return self.get_all_players_combined()

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        self._add_derived_metrics(df)
        return df

    def _add_derived_metrics(self, df: pd.DataFrame):
        """Adds p90 metrics and goal contributions safely."""
        if "minutes_26_27" in df.columns:
            if "goals_26_27" in df.columns:
                df["goals_p90"] = df.apply(
                    lambda r: round((r.get("goals_26_27", 0) / r["minutes_26_27"]) * 90, 2)
                    if pd.notna(r.get("minutes_26_27")) and r["minutes_26_27"] > 0 else 0.0, axis=1
                )
            if "assists_26_27" in df.columns:
                df["assists_p90"] = df.apply(
                    lambda r: round((r.get("assists_26_27", 0) / r["minutes_26_27"]) * 90, 2)
                    if pd.notna(r.get("minutes_26_27")) and r["minutes_26_27"] > 0 else 0.0, axis=1
                )
            if "goals_26_27" in df.columns and "assists_26_27" in df.columns:
                df["goal_contributions_26_27"] = df["goals_26_27"].fillna(0) + df["assists_26_27"].fillna(0)
                df["contrib_p90"] = df.apply(
                    lambda r: round((r["goal_contributions_26_27"] / r["minutes_26_27"]) * 90, 2)
                    if pd.notna(r.get("minutes_26_27")) and r["minutes_26_27"] > 0 else 0.0, axis=1
                )

    def get_all_players_combined(self) -> pd.DataFrame:
        """Combine national team squad with prospective pool and recent internationals for scouting comparisons."""
        master_path = os.path.join(self.data_dir, "malaysia_master_player_database.json")
        if os.path.exists(master_path):
            return self.load_master_database()

        squad = self.load_squad()
        prospects = self.load_prospects()
        past = self.load_past_internationals()
        
        squad["pool_status"] = "ASEAN Cup 2026 Squad"
        prospects["pool_status"] = "Prospect & Heritage Pool"
        past["pool_status"] = "Senior International (2023-2026)"
        
        combined = pd.concat([squad, prospects, past], ignore_index=True)
        return combined
