import os
import sys
import json
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class ChampionVersionManager:
    """
    Champion Version & Markdown Experiment History Manager.
    Logs successful champions, validated candidates, and rejected overfitted trials
    exclusively in markdown format to prevent duplicate failures in Obsidian.
    """
    
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.workspace_path, "config/champion_version.json")
        self.leaderboard_path = os.path.join(self.workspace_path, "Notes/Experiment_Leaderboard.md")

    def calculate_composite_utility(self, sharpe, ann_return, mdd, win_rate):
        score = (sharpe * 0.40) + (ann_return * 2.0) - (abs(mdd) * 1.5) + (win_rate * 0.5)
        return round(score, 4)

    def log_experiment_history(self, candidate_exp, status="SUCCESS", block_reasons=None):
        """Saves backtest trials directly to the Markdown leaderboard and individual notes."""
        utility = self.calculate_composite_utility(
            candidate_exp.get("sharpe", 0.0),
            candidate_exp.get("ann_return", 0.0),
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

        # 1. Update Master Markdown Leaderboard
        self._update_markdown_leaderboard(trial_data)
        
        # 2. Write Individual Experiment Note
        self._write_individual_experiment_note(trial_data)

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

        row = f"| {trial['timestamp']} | **{trial['exp_id']}** | {trial['name']} | {status_str} | {trial['utility_score']} | {m.get('sharpe', 0.0):.2f} | {m.get('ann_return', 0.0)*100:.1f}% | {m.get('mdd', 0.0)*100:.2f}% | {m.get('win_rate', 0.0)*100:.1f}% | {reasons_str} |\n"
        
        with open(self.leaderboard_path, "a", encoding="utf-8") as f:
            f.write(row)

    def _write_individual_experiment_note(self, trial):
        """Generates an individual markdown file inside Notes/ directory for Obsidian lookup."""
        notes_dir = os.path.join(self.workspace_path, "Notes")
        os.makedirs(notes_dir, exist_ok=True)
        note_path = os.path.join(notes_dir, f"{trial['exp_id']}.md")

        status_str = "🏆 CHAMPION" if trial["status"] == "CHAMPION" else ("✅ VALIDATED" if trial["status"] == "SUCCESS" else "❌ REJECTED")
        reasons_str = "\n".join([f"- {r}" for r in trial["reasons"]]) if trial["reasons"] else "None"
        m = trial["metrics"]

        note_content = f"""---
aliases: [{trial['exp_id']}, {trial['name']}]
tags:
  - quant/experiment
  - status/{trial['status'].lower()}
---

# 📝 Quant Experiment Record: {trial['exp_id']}

- **Hypothesis Name**: {trial['name']}
- **Run Timestamp**: {trial['timestamp']}
- **Execution Status**: **{status_str}**
- **Calculated Utility Score**: {trial['utility_score']}

## 📊 Backtest Performance Metrics
- **Sharpe Ratio**: {m.get('sharpe', 0.0):.2f}
- **Annualized Return (CAGR)**: {m.get('ann_return', 0.0)*100:.2f}%
- **Max Drawdown (MDD)**: {m.get('mdd', 0.0)*100:.2f}%
- **Win Rate**: {m.get('win_rate', 0.0)*100:.1f}%
- **OOS Performance Decay**: {m.get('oos_decay', 0.0)}
- **Probability of Overfitting (PBO)**: {m.get('pbo', 0.0)}

## 🛡️ Anti-Overfitting Hard Block Reasons
{reasons_str}
"""
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(note_content)

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
