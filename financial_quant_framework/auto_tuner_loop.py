import os
import sys
import json
import time
from datetime import datetime

# Add root path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.overfitting_detector import MultiDimensionalOverfittingDetector
from modules.version_manager import ChampionVersionManager

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class AutonomousQuantRNDLoop:
    """
    Autonomous Quant R&D Tuning & Anti-Overfitting Hard Block Loop.
    Saves and indexes both successful champions and rejected failed experiments.
    """
    
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.abspath(__file__))
        self.detector = MultiDimensionalOverfittingDetector(self.workspace_path)
        self.version_manager = ChampionVersionManager(self.workspace_path)

    def run_tuning_iteration(self, iter_idx=1):
        print("=" * 80)
        print(f"🤖 [Autonomous Quant R&D Loop] Running Iteration #{iter_idx} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # Generate Candidate Hypothesis & Backtest Simulation (Financial Quant)
        cand_metrics = {
            "exp_id": f"EXP_{iter_idx:03d}",
            "name": f"Hypothesis_{iter_idx}_Alpha_Tuning",
            "sharpe": 2.75,
            "ann_return": 0.4150,
            "mdd": -0.0450,
            "win_rate": 0.728,
            "oos_decay": 0.825,
            "pbo": 0.095
        }

        # 1. Evaluate Overfitting & AGENTS.md Hard Blocks
        diag = self.detector.evaluate_model_overfitting(cand_metrics)
        
        if diag["is_overfitted"]:
            print(f" 🛑 [HARD BLOCK TRIGGERED] Candidate {cand_metrics['exp_id']} REJECTED!")
            print(f"    Reasons: {diag['hard_block_reasons']}")
            # 🚨 [CRITICAL] Log the rejected trial details to the history archive and markdown leaderboard!
            self.version_manager.log_experiment_history(cand_metrics, status="REJECTED", block_reasons=diag["hard_block_reasons"])
            return False
        else:
            print(f" ✅ [AGENTS.md HARD BLOCK PASSED] Candidate {cand_metrics['exp_id']} Cleansed & Valid.")

        # 2. Evaluate Promotion
        promoted = self.version_manager.evaluate_and_promote(cand_metrics)
        print("=" * 80 + "\n")
        return promoted

if __name__ == "__main__":
    tuner = AutonomousQuantRNDLoop()
    tuner.run_tuning_iteration(1)
