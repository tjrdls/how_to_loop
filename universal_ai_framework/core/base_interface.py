import os
import sys
from abc import ABC, abstractmethod

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class BaseFeaturePredictor(ABC):
    """Tier 1: Domain-Agnostic Feature Extractor & Predictive Scoring Engine Interface."""
    @abstractmethod
    def extract_features(self, raw_data):
        pass

    @abstractmethod
    def predict_target_scores(self, features):
        pass

class BaseDataQualitySafeguard(ABC):
    """Tier 2: Domain-Agnostic Data Quality, Leakage & Risk Safeguard Interface."""
    @abstractmethod
    def validate_quality(self, predictions, raw_data):
        pass

    @abstractmethod
    def calculate_confidence_scores(self, candidate_list, raw_data):
        pass

class BaseResourceAllocationEngine(ABC):
    """Tier 3: Domain-Agnostic Resource, Weight & Threshold Allocator Interface."""
    @abstractmethod
    def allocate_resources(self, validated_candidates, confidence_scores):
        pass

class BaseEvaluationSimulator(ABC):
    """Tier 4: Domain-Agnostic Validation & Friction Loss Evaluation Engine Interface."""
    @abstractmethod
    def simulate_environment(self, allocation_signals):
        pass

    @abstractmethod
    def evaluate_performance(self, simulation_logs):
        pass
