import os
import sys
import time
import subprocess
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class FinancialQuantLoopScheduler:
    """
    60-Second Autonomous Financial Quant R&D Loop Scheduler.
    Runs auto_tuner_loop.py at N-second intervals to tune alpha, risk, and portfolio weights.
    """

    def __init__(self, target_script="auto_tuner_loop.py", interval_seconds=60):
        self.target_script = target_script
        self.interval_seconds = interval_seconds
        self.workspace_path = os.path.dirname(os.path.abspath(__file__))
        self.target_path = os.path.join(self.workspace_path, self.target_script)

    def start_loop(self, max_iterations=5):
        """Starts the execution loop for financial backtesting and tuning."""
        print("=" * 80)
        print(f"⏰ [Financial Quant R&D Scheduler] Starting Autonomous Tuning Loop...")
        print(f" • Target Runner: {self.target_script}")
        print(f" • Dynamic Interval: {self.interval_seconds} seconds")
        print(f" • Workspace: {self.workspace_path}")
        print("=" * 80)

        iter_count = 0
        try:
            while iter_count < max_iterations:
                iter_count += 1
                print(f"\n🚀 [Quant Scheduler Loop #{iter_count}] Triggering {self.target_script}...")
                
                start_time = time.time()
                try:
                    res = subprocess.run(
                        [sys.executable, self.target_path],
                        capture_output=True,
                        encoding="utf-8",
                        cwd=self.workspace_path,
                        check=True
                    )
                    print(res.stdout)
                except subprocess.CalledProcessError as e:
                    print(f" ❌ [Execution Error] Quant script failed with exit code {e.returncode}")
                    print(e.stderr)
                
                elapsed = time.time() - start_time
                print(f"⏱️ Loop #{iter_count} finished in {elapsed:.2f} seconds.")
                
                if iter_count >= max_iterations:
                    break
                    
                print(f"💤 Waiting {self.interval_seconds} seconds before next quant simulation...")
                time.sleep(self.interval_seconds)
                
        except KeyboardInterrupt:
            print("\n🛑 [Quant Scheduler Loop] Interrupted and stopped by user.")
        
        print("\n=" * 80)
        print("🏁 [Financial Quant R&D Scheduler] Finished execution sequence.")
        print("=" * 80)

if __name__ == "__main__":
    # Test Scheduler with a quick 5-second interval for 2 loops
    scheduler = FinancialQuantLoopScheduler(target_script="auto_tuner_loop.py", interval_seconds=5)
    scheduler.start_loop(max_iterations=2)
