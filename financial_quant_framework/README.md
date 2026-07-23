# 📈 Autonomous Financial Quant Agent-Led R&D Loop Guide

본 프레임워크는 사용자가 파이썬 코드를 로컬에서 계속 켜두는 것이 아니라, **AI 에이전트(Antigravity)가 `schedule` 도구를 사용해 스스로 60초마다 깨어나 자율 퀀트 백테스트 시뮬레이션 및 알파 튜닝을 수행하는 에이전트 주도형 템플릿**입니다.

---

## 🛡️ 금융 퀀트 특화 4대 과적합 차단 규정 (AGENTS.md)

이 프레임워크 적용 시, `.agents/AGENTS.md`에 아래 규정을 삽입하여 에이전트의 데이터 누수와 승률 착시를 차단해야 합니다:

1. **승률 착시 경계 (Win Rate Cap)**: Win Rate > 85.0% 또는 Sharpe Ratio > 3.50 발생 시 미래 참조로 간주하고 즉시 하드 블록.
2. **MDD Zero 방화벽 (Zero Drawdown Block)**: Max Drawdown(MDD)이 0.0%인 경우 100% 미래 주가 선행 참조 착시로 간주하여 하드 블록.
3. **현실적 거래 마찰 주입 (Realistic Frictions)**: 슬리피지 최소 10~20 bps 및 거래 수수료를 차감하여 성과 계산.
4. **Walk-Forward OOS 검증**: In-Sample 대비 Out-of-Sample 성과 보존율 70% 이상 필수 검증.

---

## 🤖 AI 에이전트에게 60초 자율 퀀트 R&D 구동 지시하는 방법 (Prompting Guide)

이 폴더를 새 프로젝트에 복사한 뒤, AI 에이전트에게 다음과 같이 채팅창에 입력하십시오:

> **"이 폴더에 있는 템플릿을 기반으로 60초 자율 퀀트 R&D 스케줄러 루프를 돌려줘. 매 60초마다 `schedule` 도구를 사용해 대기하고, 깨어나면 `python auto_tuner_loop.py`를 직접 1회씩 실행하며 최적의 알파 및 가중치 조합을 지속적으로 탐색해줘."**

---

## 🔁 에이전트 자율 60초 루프 작동 매커니즘 (Agent Self-Loop Mechanism)

1. **가설 적용**: 에이전트가 알파 가설 코드 및 파라미터를 수정합니다.
2. **코드 직접 실행**: 에이전트가 `run_command` 도구로 `python auto_tuner_loop.py`를 1회 실행하여 백테스트를 수행합니다.
3. **과적합 검증 및 챔피언 승격**: 실행 결과를 분석하여 5대 과적합 방화벽(`overfitting_detector.py`)을 통과하고 성능이 향상되면 챔피언 버전으로 승격시킵니다.
4. **60초 자율 대기**: 에이전트가 스스로 `schedule(DurationSeconds=60)` 도구를 호출하여 타이머를 세팅하고 잠에 듭니다.
5. **무한 순환**: 60초 후 시스템에 의해 에이전트가 깨어나면 다시 **1단계**부터 루프를 반복 구동합니다.
