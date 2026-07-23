import os
import sys
import json
from datetime import datetime

# Add root path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.leakage_detector import DomainAgnosticLeakageDetector
from modules.champion_tracker import DomainAgnosticChampionTracker

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class UniversalAutonomousRNDLoop:
    """Domain-Agnostic Autonomous AI R&D Loop with Failure Logging."""
    
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.abspath(__file__))
        self.detector = DomainAgnosticLeakageDetector(self.workspace_path)
        self.tracker = DomainAgnosticChampionTracker(self.workspace_path)

    def run_iteration(self, iter_idx=1):
        print("=" * 80)
        print(f"🤖 [Universal AI R&D Loop] Running Iteration #{iter_idx} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # Generate Candidate model metrics (Domain-Agnostic)
        cand_metrics = {
            "model_id": f"MODEL_{iter_idx:03d}",
            "name": f"Hypothesis_{iter_idx}_Architecture_Tuning",
            "primary_accuracy": 0.885,
            "r2_score": 0.892,
            "oos_decay": 0.815,
            "pbo": 0.095
        }

        # 1. Evaluate Leakage & Overfitting Safeguards
        diag = self.detector.evaluate_model_validity(cand_metrics)
        if diag["is_invalid"]:
            print(f" 🛑 [HARD BLOCK TRIGGERED] Candidate {cand_metrics['model_id']} REJECTED!")
            print(f"    Reasons: {diag['hard_block_reasons']}")
            # 🚨 [CRITICAL] Log the failed run to ensure history preservation and prevent duplicate mistakes!
            self.tracker.log_experiment_history(cand_metrics, status="REJECTED", block_reasons=diag["hard_block_reasons"])
            return False
        else:
            print(f" ✅ [AGENTS.md UNIVERSAL RULE PASSED] Candidate {cand_metrics['model_id']} Validated.")

        # 2. Evaluate Promotion
        promoted = self.tracker.evaluate_and_promote(cand_metrics)
        print("=" * 80 + "\n")
        return promoted

if __name__ == "__main__":
    loop = UniversalAutonomousRNDLoop()
    loop.run_iteration(1)
