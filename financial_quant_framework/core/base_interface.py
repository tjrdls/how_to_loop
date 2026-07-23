import os
import sys
from abc import ABC, abstractmethod

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class BaseAlphaModel(ABC):
    """Tier 1: Standard Alpha Mining & Scoring Engine Interface."""
    @abstractmethod
    def extract_features(self, market_data):
        pass

    @abstractmethod
    def predict_alpha_scores(self, features):
        pass

class BaseRiskFilter(ABC):
    """Tier 2: Standard Multi-Layered Risk Safeguard & Veto Interface."""
    @abstractmethod
    def filter_candidates(self, alpha_predictions, market_data):
        pass

    @abstractmethod
    def calculate_risk_scores(self, candidate_list, market_data):
        pass

class BasePortfolioController(ABC):
    """Tier 3: Standard Position & Capital Allocation Controller Interface."""
    @abstractmethod
    def optimize_portfolio(self, filtered_candidates, risk_scores):
        pass

    @abstractmethod
    def calculate_rebalance_signals(self, target_weights, current_portfolio):
        pass

class BaseExecutionEngine(ABC):
    """Tier 4: Standard Backtest & Live Execution Simulation Interface."""
    @abstractmethod
    def execute_orders(self, rebalance_signals):
        pass

    @abstractmethod
    def simulate_slippage_and_fees(self, order):
        pass

    @abstractmethod
    def run_backtest_simulation(self, portfolio_history, execution_logs):
        pass
