import os
import sys
import time
import subprocess
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class UniversalRNDLoopScheduler:
    """
    Universal 60-Second Autonomous R&D Loop Scheduler.
    Runs any target pipeline / tuning script iteratively every N seconds.
    Monitors execution log, handles errors, and tracks continuous research progress.
    """

    def __init__(self, target_script="auto_rnd_loop.py", interval_seconds=60):
        self.target_script = target_script
        self.interval_seconds = interval_seconds
        self.workspace_path = os.path.dirname(os.path.abspath(__file__))
        self.target_path = os.path.join(self.workspace_path, self.target_script)

    def start_loop(self, max_iterations=5):
        """Starts the infinite/bounded execution loop."""
        print("=" * 80)
        print(f"⏰ [Universal R&D Loop Scheduler] Starting Autonomous Tuning Loop...")
        print(f" • Target Runner: {self.target_script}")
        print(f" • Dynamic Interval: {self.interval_seconds} seconds")
        print(f" • Workspace: {self.workspace_path}")
        print("=" * 80)

        iter_count = 0
        try:
            while iter_count < max_iterations:
                iter_count += 1
                print(f"\n🚀 [Scheduler Loop #{iter_count}] Triggering execution of {self.target_script}...")
                
                # Dynamic Subprocess Call with strict UTF-8 encoding
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
                    print(f" ❌ [Execution Error] Script failed with exit code {e.returncode}")
                    print(e.stderr)
                
                elapsed = time.time() - start_time
                print(f"⏱️ Loop #{iter_count} finished in {elapsed:.2f} seconds.")
                
                if iter_count >= max_iterations:
                    break
                    
                print(f"💤 Waiting {self.interval_seconds} seconds before next iteration...")
                time.sleep(self.interval_seconds)
                
        except KeyboardInterrupt:
            print("\n🛑 [Scheduler Loop] Interrupted and stopped by user command.")
        
        print("\n=" * 80)
        print("🏁 [Universal R&D Loop Scheduler] Finished execution sequence.")
        print("=" * 80)

if __name__ == "__main__":
    # Test Scheduler with a quick 5-second interval for 2 loops
    scheduler = UniversalRNDLoopScheduler(target_script="auto_rnd_loop.py", interval_seconds=5)
    scheduler.start_loop(max_iterations=2)
