# AGENTS.md - Workspace Project Rules & Behavioral Constraints

## 🛡️ Anti-Overfitting & Realistic Backtesting Mandatory Guidelines (과적합 차단 필수 규정)

1. **승률 착시 경계 (Anti-Look-Ahead Bias & Zero Drawdown Block)**:
   - 승률이 **85%를 초과**하거나 Sharpe Ratio가 **3.5를 초과**하거나 Max Drawdown(MDD)이 **0.0% (Zero Drawdown)**인 시뮬레이션 결과는 **100% 미래 데이터 참조(Look-Ahead Bias) 또는 데이터 누수(Data Leakage) 착시**로 간주하고 즉시 하드 블록(Hard Block) 및 정밀 감사를 수행한다.
   - 주문 타점 스탬프 시 $T$ 시점에서 $T+1$ 미래 주가를 사전 참조하지 않도록 strict time-series lock을 항상 검증한다.

2. **현실적 거래 마찰 주입 (Mandatory Realistic Frictions)**:
   - 백테스팅 시 슬리피지(Slippage)는 최소 **10~15 bps (0.10% ~ 0.15%)** 이상, 거래 수수료는 **주당 $0.005** 이상을 반드시 주입하여 마찰 손실을 정밀 계산한다.

3. **Walk-Forward Out-of-Sample (OOS) 필수 검증**:
   - 학습 데이터(In-Sample) 성능만으로 최고 모델을 판정하지 않으며, 반드시 미공개 OOS 테스트 구간 및 Purged Group TimeSeries Cross-Validation을 거친 결과만 정식 베이스라인으로 승격(Version Up)시킨다.
