import os
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class DomainAgnosticLeakageDetector:
    """
    Domain-Agnostic Leakage & Overfitting Detector.
    Loads project-defined limits dynamically from config/project_rules.json.
    Strictly flags any signs of Data Leakage (unrealistically high metrics) or high Overfitting Probability (PBO).
    """

    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.rules_path = os.path.join(self.workspace_path, "config/project_rules.json")

    def load_project_rules(self):
        if os.path.exists(self.rules_path):
            try:
                with open(self.rules_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "max_metric_upper_cap": 0.95,
            "min_oos_decay_ratio": 0.70,
            "max_pbo_probability": 0.25
        }

    def evaluate_model_validity(self, metrics):
        rules = self.load_project_rules()
        hard_block_triggered = False
        reasons = []

        primary_val = metrics.get("primary_accuracy", metrics.get("r2_score", 0.0))
        metric_cap = rules.get("max_metric_upper_cap", 0.95)
        oos_decay = metrics.get("oos_decay", 0.75)
        min_decay = rules.get("min_oos_decay_ratio", 0.70)
        pbo = metrics.get("pbo", 0.10)
        max_pbo = rules.get("max_pbo_probability", 0.25)

        # 🚨 Detect Unrealistic Metric Cap -> 100% Data Leakage / Target Leakage / Look-Ahead Bias
        if primary_val > metric_cap:
            hard_block_triggered = True
            reasons.append(f"Primary Metric ({primary_val:.4f}) exceeds Project Upper Cap ({metric_cap:.4f}) -> Potential Data Leakage!")

        if oos_decay < min_decay:
            hard_block_triggered = True
            reasons.append(f"OOS Decay ({oos_decay:.3f}) below Project Minimum Target ({min_decay:.3f})")

        if pbo > max_pbo:
            hard_block_triggered = True
            reasons.append(f"PBO ({pbo*100:.1f}%) exceeds Project Maximum Target ({max_pbo*100:.1f}%)")

        return {
            "is_invalid": hard_block_triggered,
            "hard_block_reasons": reasons,
            "metrics": metrics
        }
