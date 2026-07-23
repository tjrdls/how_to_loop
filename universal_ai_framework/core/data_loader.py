import os
import sys
from enum import Enum

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class DomainType(Enum):
    DEMAND_FORECASTING = "DEMAND_FORECASTING"       # 수요 예측
    MANUFACTURING_QUALITY = "MANUFACTURING_QUALITY" # 제조업 불량률 예측
    GENERAL_TABULAR = "GENERAL_TABULAR"             # 일반 정형 머신러닝/딥러닝

class UniversalDataLoader:
    """Domain-Agnostic Data Loader & Ingestion Engine."""
    
    def __init__(self, domain=DomainType.GENERAL_TABULAR):
        if isinstance(domain, DomainType):
            self.domain = domain
        else:
            self.domain = DomainType[str(domain).upper()]

    def load_domain_data(self, dataset_name="default_dataset"):
        return {
            "domain": self.domain.value,
            "dataset_name": dataset_name,
            "sample_count": 10000,
            "feature_count": 64,
            "status": "READY"
        }
