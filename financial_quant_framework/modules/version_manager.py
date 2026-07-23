import os
import sys
import json
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class ChampionVersionManager:
    """
    Champion Version & Experiment History Manager.
    Logs both successful promotions and rejected overfitted trials to ensure full traceback.
    """
    
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.workspace_path, "config/champion_version.json")
        self.history_path = os.path.join(self.workspace_path, "config/quant_history.json")
        self.leaderboard_path = os.path.join(self.workspace_path, "Notes/Experiment_Leaderboard.md")

    def calculate_composite_utility(self, sharpe, ann_return, mdd, win_rate):
        score = (sharpe * 0.40) + (ann_return * 2.0) - (abs(mdd) * 1.5) + (win_rate * 0.5)
        return round(score, 4)

    def log_experiment_history(self, candidate_exp, status="SUCCESS", block_reasons=None):
        """Saves both successful promotions and rejected/failed runs to preserve historical intelligence."""
        history = []
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                pass

        utility = self.calculate_composite_utility(
            candidate_exp.get("sharpe", 0.0),
            candidate_exp.get("ann_return", candidate_exp.get("ann_return", 0.0)),
            candidate_exp.get("mdd", 0.0),
            candidate_exp.get("win_rate", 0.0)
        )

        trial_data = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "exp_id": candidate_exp.get("exp_id", "EXP_UNKNOWN"),
            "name": candidate_exp.get("name", "Hypothesis_Unnamed"),
            "status": status,
            "reasons": block_reasons or [],
            "metrics": candidate_exp,
            "utility_score": utility
        }
        history.append(trial_data)

        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        self._update_markdown_leaderboard(trial_data)

    def _update_markdown_leaderboard(self, trial):
        """Appends the run dynamically to the Experiment Leaderboard markdown table."""
        os.makedirs(os.path.dirname(self.leaderboard_path), exist_ok=True)

        if not os.path.exists(self.leaderboard_path):
            header = """# 📊 Quant Experiment Exploration History & Leaderboard

Tracks all historical backtests including champions and rejected look-ahead/overfitted ideas to prevent duplicate failures.

| Timestamp | Exp ID | Hypothesis Name | Status | Utility Score | Sharpe | CAGR | MDD | Win Rate | Block Reasons |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
            with open(self.leaderboard_path, "w", encoding="utf-8") as f:
                f.write(header)

        status_str = "🏆 CHAMPION" if trial["status"] == "CHAMPION" else ("✅ VALIDATED" if trial["status"] == "SUCCESS" else "❌ REJECTED")
        reasons_str = ", ".join(trial["reasons"]) if trial["reasons"] else "-"
        m = trial["metrics"]

        row = f"| {trial['timestamp']} | **{trial['exp_id']}** | {trial['name']} | {status_str} | {trial['utility_score']} | {m.get('sharpe', 0.0):.2f} | {m.get('ann_return', m.get('ann_return', 0.0))*100:.1f}% | {m.get('mdd', 0.0)*100:.2f}% | {m.get('win_rate', 0.0)*100:.1f}% | {reasons_str} |\n"
        
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
            
            self.log_experiment_history(candidate_exp, status="CHAMPION")
            return True
        
        self.log_experiment_history(candidate_exp, status="SUCCESS")
        return False
