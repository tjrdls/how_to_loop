import os
import sys
import json
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class ChampionVersionManager:
    """Champion Version & Leaderboard Manager Template."""
    
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.getcwd()
        self.config_path = os.path.join(self.workspace_path, "config/champion_version.json")
        self.leaderboard_path = os.path.join(self.workspace_path, "Notes/Experiment_Leaderboard.md")

    def calculate_composite_utility(self, sharpe, ann_return, mdd, win_rate):
        score = (sharpe * 0.40) + (ann_return * 2.0) - (abs(mdd) * 1.5) + (win_rate * 0.5)
        return round(score, 4)

    def evaluate_and_promote(self, candidate_exp):
        current_champ = {"utility_score": 0.0}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    current_champ = json.load(f)
            except Exception:
                pass

        cand_utility = self.calculate_composite_utility(
            candidate_exp["sharpe"], candidate_exp["ann_return"], candidate_exp["mdd"], candidate_exp["win_rate"]
        )

        if cand_utility > current_champ.get("utility_score", 0.0):
            print(f" 👑 [VersionManager] PROMOTED NEW CHAMPION! (Utility: {cand_utility:.4f} > {current_champ.get('utility_score', 0.0):.4f})")
            candidate_exp["utility_score"] = cand_utility
            candidate_exp["promoted_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(candidate_exp, f, indent=2, ensure_ascii=False)
            return True
        return False
