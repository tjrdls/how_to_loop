# AGENTS.md - Universal Workspace Project Rules & Behavioral Constraints Template

## 🛡️ Anti-Overfitting & Data Leakage Prevention Principles (범용 과적합 & 데이터 누수 차단 프로젝트 원칙)

1. **미래 데이터 참조(Look-Ahead Bias) 차단**:
   - 시계열 또는 순차 데이터 모델링 시, 시점 $T$ 이후의 미래 타깃 지표($T+\Delta$)를 사전에 참조하지 않도록 strict time-series / group locking을 적용한다.

2. **프로젝트 정의 하드 블록 임계치 준수 (Project-Defined Hard Block Limits)**:
   - 본 프로젝트의 `config/project_rules.json`에 정의된 **데이터 누수(Data Leakage) 및 비현실적 과적합 착시 상한선**을 초과하는 모델은 즉시 하드 블록(Hard Block) 및 탈락 처리한다.

3. **현실적 환경 마찰 반영 (Mandatory Environment Frictions)**:
   - 모든 시뮬레이션 평가 시 실제 운용/배포 환경에서 발생하는 측정 오차, 대기 시간(Latency), 데이터 누락 등 프로젝트에 정의된 마찰 손실을 정밀 반영한다.

4. **Walk-Forward Out-of-Sample (OOS) 필수 검증**:
   - 학습 데이터(In-Sample) 성능만으로 최고 모델을 판정하지 않으며, 반드시 미공개 OOS 테스트 구간 성과 보존율(OOS Decay Ratio)을 만족하는 가설만 정식 베이스라인(Champion Model)으로 승격시킨다.
