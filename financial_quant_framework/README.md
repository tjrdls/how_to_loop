# 📈 Autonomous Financial Quant R&D & Scheduler Framework

본 프레임워크는 **주식, 암호화폐, 금융 시계열 R&D**에 특화된 자율 튜닝 루프 및 과적합 방화벽 패키지입니다.

주기(예: 60초)마다 자율적으로 백테스트 시뮬레이션(`auto_tuner_loop.py`)을 돌려 알파 예측 점수, 변동성 리스크, 포트폴리오 비중을 튜닝하는 **60초 무인 퀀트 스케줄러(auto_tuner_scheduler.py)**를 기본 탑재하고 있습니다.

---

## 🛡️ 금융 퀀트 특화 4대 과적합 차단 규정 (AGENTS.md)

이 프레임워크를 적용할 때, `.agents/AGENTS.md`에 아래 규정을 삽입하여 과적합과 데이터 누수를 강제로 감시합니다:

1. **승률 착시 경계 (Win Rate Cap)**: Win Rate > 85.0% 또는 Sharpe Ratio > 3.50 발생 시 미래 참조(Look-Ahead Bias)로 간주하고 즉시 하드 블록(Hard Block) 처리.
2. **MDD Zero 방화벽 (Zero Drawdown Block)**: Max Drawdown(MDD)이 0.0%인 경우 100% 미래 주가 선행 참조 착시로 간주하여 하드 블록.
3. **현실적 거래 마찰 주입 (Realistic Frictions)**: 슬리피지(Slippage) 최소 10~20 bps 및 거래 수수료를 차감하여 성과 계산.
4. **Walk-Forward OOS 검증**: In-Sample 대비 Out-of-Sample 성과 보존율 70% 이상 필수 검증.

---

## 📁 퀀트 프레임워크 패키지 구조

```text
financial_quant_framework/
├── .agents/
│   └── AGENTS.md                  <-- [규정 주입] AGENTS_RULE_TEMPLATE.md 바탕으로 작성
├── config/
│   └── champion_version.json       <-- [자동 생성] 최고 퀀트 챔피언 메타데이터
├── core/
│   ├── base_interface.py           <-- 4단계 파이프라인 인터페이스 (Alpha, Risk, Controller, Execution)
│   └── data_selector.py            <-- US/KR/Crypto 및 1D/1H/5M 해상도 멀티 데이터 셀렉터
├── modules/
│   ├── overfitting_detector.py     <-- PBO, OOS Decay, MDD Zero 5대 과적합 진단기
│   └── version_manager.py          <-- Utility Score 기반 챔피언 승격기
├── auto_tuner_scheduler.py         <-- ⏰ 60초 주기 무인 자율 백테스트/ R&D 스케줄러
├── auto_tuner_loop.py              <-- 단일 가설 백테스트 및 튜닝 실행 스크립트
└── main_pipeline.py                <-- 마스터 파이프라인 구동기
```

---

## ⚡ 빠른 구동 3단계 (Quick Start)

### Step 1.
`financial_quant_framework/` 폴더를 새 퀀트 프로젝트로 복사합니다.

### Step 2.
`.agents/AGENTS.md`에 필수 규정을 배치합니다.

### Step 3.
터미널에서 아래 명령어를 구동하여 무인 R&D 루프를 시작합니다:
```bash
python auto_tuner_scheduler.py
```
*(기본 주기는 60초로 설정되어 있으며, 코드 내 `interval_seconds` 파라미터로 자유롭게 조정할 수 있습니다.)*
