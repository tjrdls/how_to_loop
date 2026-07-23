import os
import sys
import json
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class DomainAgnosticChampionTracker:
    """
    Domain-Agnostic Champion Model & History Tracker.
    Calculates Composite Utility Score, promotes champions, and saves ALL (success/rejected) history.
    """
    
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.workspace_path, "config/champion_model.json")
        self.history_path = os.path.join(self.workspace_path, "config/experiment_history.json")
        self.leaderboard_path = os.path.join(self.workspace_path, "Notes/Model_Leaderboard.md")

    def calculate_utility_score(self, metrics):
        accuracy = metrics.get("primary_accuracy", 0.0)
        r2 = metrics.get("r2_score", 0.0)
        score = (accuracy * 2.0) + (r2 * 1.5)
        return round(score, 4)

    def log_experiment_history(self, candidate_exp, status="SUCCESS", block_reasons=None):
        """Saves ALL trial results (including failures and hard blocks) to prevent duplicated mistakes."""
        history = []
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                pass

        trial_data = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "model_id": candidate_exp.get("model_id", "MODEL_UNKNOWN"),
            "name": candidate_exp.get("name", "Hypothesis_Unnamed"),
            "status": status,
            "reasons": block_reasons or [],
            "metrics": candidate_exp,
            "utility_score": self.calculate_utility_score(candidate_exp)
        }
        history.append(trial_data)

        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        self._update_markdown_leaderboard(trial_data)

    def _update_markdown_leaderboard(self, trial):
        """Appends the success/failure status dynamically to the Obsidian markdown leaderboard."""
        os.makedirs(os.path.dirname(self.leaderboard_path), exist_ok=True)
        
        # Create file with table header if not exists
        if not os.path.exists(self.leaderboard_path):
            header = """# 📊 Model Exploration History & Leaderboard

This file tracks ALL historical runs (including successful promotions and rejected overfitted trials) to prevent duplicate exploration.

| Timestamp | Model ID | Hypothesis Name | Status | Utility Score | Primary Metric | R2 Score | Hard Block Reasons |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
            with open(self.leaderboard_path, "w", encoding="utf-8") as f:
                f.write(header)

        status_str = "🏆 CHAMPION" if trial["status"] == "CHAMPION" else ("✅ VALIDATED" if trial["status"] == "SUCCESS" else "❌ REJECTED")
        reasons_str = ", ".join(trial["reasons"]) if trial["reasons"] else "-"
        
        row = f"| {trial['timestamp']} | **{trial['model_id']}** | {trial['name']} | {status_str} | {trial['utility_score']} | {trial['metrics'].get('primary_accuracy', 0.0)} | {trial['metrics'].get('r2_score', 0.0)} | {reasons_str} |\n"
        
        with open(self.leaderboard_path, "a", encoding="utf-8") as f:
            f.write(row)

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
            
            self.log_experiment_history(candidate_exp, status="CHAMPION")
            return True
        
        self.log_experiment_history(candidate_exp, status="SUCCESS")
        return False
