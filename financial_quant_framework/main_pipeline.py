import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from core.base_interface import BaseAlphaModel, BaseRiskFilter, BasePortfolioController, BaseExecutionEngine
from core.data_selector import UniversalDataSelector

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class SampleAlphaModel(BaseAlphaModel):
    def extract_features(self, market_data):
        return {"universe": market_data.get("universe", ["NVDA", "AAPL"])}
    def predict_alpha_scores(self, features):
        return {"top_k_stocks": features["universe"][:3]}

class SampleRiskFilter(BaseRiskFilter):
    def filter_candidates(self, alpha_predictions, market_data):
        return {"safe_stocks": alpha_predictions["top_k_stocks"]}
    def calculate_risk_scores(self, candidate_list, market_data):
        return {c: 0.01 for c in candidate_list}

class SamplePortfolioController(BasePortfolioController):
    def optimize_portfolio(self, filtered_candidates, risk_scores):
        stocks = filtered_candidates["safe_stocks"]
        return {s: round(1.0 / len(stocks), 4) for s in stocks}
    def calculate_rebalance_signals(self, target_weights, current_portfolio):
        return target_weights

class SampleExecutionEngine(BaseExecutionEngine):
    def execute_orders(self, rebalance_signals):
        return {"status": "SUCCESS"}
    def simulate_slippage_and_fees(self, order):
        return {"slippage_bps": 20.0}
    def run_backtest_simulation(self, portfolio_history, execution_logs):
        return {"sharpe": 2.70, "ann_return": 0.4000, "mdd": -0.0450, "win_rate": 0.720}

class MasterQuantPipeline:
    def __init__(self, market="US_EQUITY", timeframe="1D"):
        self.selector = UniversalDataSelector(market=market, timeframe=timeframe)
        self.alpha = SampleAlphaModel()
        self.risk = SampleRiskFilter()
        self.controller = SamplePortfolioController()
        self.execution = SampleExecutionEngine()

    def run(self):
        data = self.selector.fetch_market_data()
        feats = self.alpha.extract_features(data)
        preds = self.alpha.predict_alpha_scores(feats)
        safe = self.risk.filter_candidates(preds, data)
        weights = self.controller.optimize_portfolio(safe, None)
        signals = self.controller.calculate_rebalance_signals(weights, None)
        exec_res = self.execution.execute_orders(signals)
        sim_res = self.execution.run_backtest_simulation(None, None)
        print(f" [MasterQuantPipeline] Pipeline Executed Successfully. Sharpe: {sim_res['sharpe']}")
        return sim_res

if __name__ == "__main__":
    pipeline = MasterQuantPipeline()
    pipeline.run()
