import os
import sys
import json
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class DomainAgnosticChampionTracker:
    """
    Domain-Agnostic Champion Model Tracker.
    Calculates Composite Utility Score and promotes the best baseline model.
    """
    
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.workspace_path, "config/champion_model.json")

    def calculate_utility_score(self, metrics):
        accuracy = metrics.get("primary_accuracy", 0.0)
        r2 = metrics.get("r2_score", 0.0)
        score = (accuracy * 2.0) + (r2 * 1.5)
        return round(score, 4)

    def evaluate_and_promote(self, candidate_exp):
        current_champ = {"utility_score": 0.0}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    current_champ = json.load(f)
            except Exception:
                pass

        cand_utility = self.calculate_utility_score(candidate_exp)

        if cand_utility > current_champ.get("utility_score", 0.0):
            print(f" 👑 [ChampionTracker] PROMOTED NEW CHAMPION MODEL! (Utility: {cand_utility:.4f} > {current_champ.get('utility_score', 0.0):.4f})")
            candidate_exp["utility_score"] = cand_utility
            candidate_exp["promoted_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(candidate_exp, f, indent=2, ensure_ascii=False)
            return True
        return False
