import os
import sys
import json
from enum import Enum

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class MarketType(Enum):
    US_EQUITY = "US_EQUITY"
    KR_EQUITY = "KR_EQUITY"
    CRYPTO = "CRYPTO"

class TimeframeType(Enum):
    DAILY = "1D"
    HOURLY = "1H"
    MINUTE_5 = "5M"
    MINUTE_1 = "1M"

class UniversalDataSelector:
    """Universal Data Selector & Ingestion Engine Template."""
    
    def __init__(self, market=MarketType.US_EQUITY, timeframe=TimeframeType.DAILY):
        if isinstance(market, MarketType):
            self.market = market
        else:
            self.market = MarketType[str(market).upper()]

        if isinstance(timeframe, TimeframeType):
            self.timeframe = timeframe
        else:
            tf_map = {
                "1D": TimeframeType.DAILY, "DAILY": TimeframeType.DAILY,
                "1H": TimeframeType.HOURLY, "HOURLY": TimeframeType.HOURLY,
                "5M": TimeframeType.MINUTE_5, "MINUTE_5": TimeframeType.MINUTE_5,
                "1M": TimeframeType.MINUTE_1, "MINUTE_1": TimeframeType.MINUTE_1
            }
            self.timeframe = tf_map.get(str(timeframe).upper(), TimeframeType.DAILY)

        self.universes = {
            MarketType.US_EQUITY: ["NVDA", "AAPL", "MSFT", "AMZN", "META"],
            MarketType.KR_EQUITY: ["005930.KS", "000660.KS", "035420.KS", "005380.KS", "035720.KS"],
            MarketType.CRYPTO: ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "BNB/USDT"]
        }

    def fetch_market_data(self, start_date="2023-01-01", end_date="2025-12-31"):
        universe = self.universes.get(self.market, ["NVDA", "AAPL"])
        return {
            "market": self.market.value,
            "timeframe": self.timeframe.value,
            "universe": universe,
            "start_date": start_date,
            "end_date": end_date,
            "status": "READY"
        }
