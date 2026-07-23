# 🤖 Reusable Autonomous AI R&D & 60-Second Loop Scheduler Suite

이 저장소는 자율 AI R&D 튜닝 루프, 5대 과적합 방화벽, 그리고 무인 상태에서 가설 검증과 시뮬레이션을 주기적으로 반복 실행하는 **60초 자율 루프 스케줄러**의 표준 템플릿 패키지 모음입니다.

용도와 프로젝트의 성격에 따라 아래의 두 가지 프레임워크 중 적절한 폴더를 복사하여 즉시 이식 구동할 수 있습니다.

---

## 📂 저장소 패키지 구성 (Framework Directory Layout)

### 1. 🌐 [universal_ai_framework/](./universal_ai_framework/)
- **특징**: 주식/금융에 종속되지 않은 **완전 도메인 독립형 범용 AI R&D 템플릿**.
- **적용 도메인**: 유통/물류 수요 예측, 제조업 센서/품질 예측, 기상 예측, 일반 정형 ML/DL 튜닝.
- **주요 구성**: 4단계 범용 파이프라인 인터페이스, project_rules.json 기반 동적 과적합 진단, 무인 R&D 루프 스케줄러.

### 2. 📈 [financial_quant_framework/](./financial_quant_framework/)
- **특징**: 주식/암호화폐/금융 시계열 R&D에 특화된 **금융 퀀트 전용 AI R&D 템플릿**.
- **적용 도메인**: 포트폴리오 자산 배분, 계량 투자, 시스템 트레이딩 알파 마이닝.
- **주요 구성**: Sharpe Cap, MDD Zero 방화벽, 20 bps 슬리피지/마찰 손실 시뮬레이션, GNN/TFT/HRP/DeepLOB 연동 뼈대, 무인 퀀트 백테스트 스케줄러.

---

## ⚡ 빠른 적용 가이드 (Quick Integration)

1. 이 저장소를 로컬로 복사하거나 필요한 프레임워크 폴더만 선택하여 새 프로젝트 루트 폴더에 복사합니다.
2. 복사한 폴더 내부의 `README.md`를 참고하여 필수 규칙(`.agents/AGENTS.md`) 및 기준 설정을 완료합니다.
3. 터미널에서 아래 명령을 구동하여 60초 주기 무인 자율 R&D 튜닝 스케줄러를 가동합니다:
   ```bash
   python auto_tuner_scheduler.py
   ```
