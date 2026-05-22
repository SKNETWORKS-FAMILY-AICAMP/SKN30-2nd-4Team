# 🤖 AGENT.md — 개봉 예정작 흥행 예측 & 스크린 시뮬레이터 프로젝트

이 문서는 차후 본 프로젝트를 리딩하거나 기여하게 될 AI 에이전트가 데이터 수집부터 피처 엔지니어링, 2-Stage 머신러닝/딥러닝 모델링, 그리고 Streamlit 시뮬레이터 대시보드 웹 서비스까지의 **전체 구현 완료 스펙을 명확하게 파악하고 안정적으로 유지보수하기 위한 기술 지침서**입니다.

---

## 1. 프로젝트 완료 목표와 산출물

**과거 8년간의 KOBIS 상영작 및 Naver 트렌드 버즈 데이터를 기반으로 개봉 예정작의 콘텐츠 고유 흥행력(Stage 1)을 진단하고, 첫날 배급 전략에 따른 예상 누적 관객수(Stage 2)를 시뮬레이션하는 비선형 의사결정 시뮬레이터를 완벽하게 구현 완료했습니다.**

### 🎯 프로젝트 달성 목표
1. **비즈니스 이해**: 스크린 독점 및 배급 내생성(Endogeneity) 문제를 해소하는 2-Stage 예측 체계 정립
2. **데이터셋 준비 및 전처리**: 데이터 누수(Data Leakage)가 완벽히 소거된 v3 피처 테이블 구축
3. **학습 및 평가**: ML(CatBoost, XGBoost) 및 DL(PyTorch MLP) 앙상블 흥행 예측 모델 완료
4. **최적화 및 배포**: 의사결정권자를 위한 이중 가드레일 및 스윗스팟(Elbow Point) 추천 Streamlit 대시보드 배포

### 📦 최종 산출물
1. **[인공지능 데이터 전처리 결과서](docs/인공지능%20데이터%20전처리%20결과서.md)**
2. **[인공지능 학습 결과서](docs/인공지능%20학습%20결과서.md)**
3. **학습 완료된 2-Stage 인공지능 모델** (`stage1_ensemble.pkl`, `stage2_simulator.pkl`)
4. **원클릭 배포 가능한 Streamlit What-If 대시보드 패키지** (`web/`, `main.py`)

---

## 2. 에이전트 역할과 행동 강령

- **페르소나**: Python 기반 데이터 사이언티스트, 고급 ML/DL 엔지니어, Streamlit 풀스택 개발자
- **전문 분야**: 피처 엔지니어링, 다중 앙상블 모델링, 시계열 및 비선형 시뮬레이션, 반응 곡선 최적화 알고리즘
- **핵심 원칙**:
  - 사용자의 피드백과 설계를 최우선으로 존중한다.
  - 임의의 자동화 브라우저 검증(`browser_subagent`)은 사용자가 직접 요청할 때만 수행한다.
  - 패키지화 규칙(PEP 8 절대 경로 임포트)을 준수하며 모듈의 디커플링을 유지한다.

---

## 3. 완료된 프로젝트 아키텍처 (구조)

```
SKN30-2nd-4Team/
├── .env                          # MySQL DB 접속 및 외부 API 연동 환경변수
├── pyproject.toml                # 프로젝트 의존성 관리 및 uv 설정 파일
├── AGENTS.md                     # 에이전트 가이드 (이 문서)
├── main.py                       # [Streamlit Launch Router] 클라우드 원클릭 배포 런처
│
├── util/                         # 공통 환경설정 모듈
│   ├── __init__.py               
│   └── config.py                 # Pydantic 기반 AppSettings (.env 파일 파싱)
│
├── data/                         # 데이터 파이프라인 레이어
│   ├── api/                      # KOBIS 및 NAVER API 수집 클라이언트 모듈
│   │   ├── __init__.py           
│   │   ├── kobis_client.py       # 박스오피스 & 영화 정보 REST API
│   │   ├── naver_client.py       # 네이버 통합 검색량 데이터 크롤러
│   │   └── README.md             # API 가이드 명세
│   └── db/                       # MySQL 적재 마이그레이션 및 삽입 노트북
│       ├── __init__.py           
│       ├── db_manager.py         # Bulk Upsert 및 CRUD 매니저 클래스
│       └── README.md             
│
├── ml/                           # 머신러닝/딥러닝 모델링 레이어
│   ├── README.md                 # 모델링 설계서 및 시뮬레이터 변수 명세
│   ├── 00_feature_table_v3.ipynb # 누수 소거 및 신규 피처 3종 추가 공통 피처 테이블 v3 생성
│   ├── 01_eda_baseline.ipynb     # Baseline 회귀 모델 평가
│   ├── 02_boosting.ipynb         # Optuna 하이퍼파라미터 튜닝 완료 XGB, LGBM, CatBoost
│   ├── 03_deep_learning.ipynb    # MLP deep learning 학습 모델
│   ├── 04_model_comparison.ipynb # 최종 CatBoost 8 : XGBoost 2 Stacking 메타 앙상블 확정
│   └── data/
│       ├── baseline_feature_table.md  # 피처 명세서
│       └── CHANGELOG.md          # 피처 버전 변경 기록
│
└── web/                          # Streamlit 시뮬레이터 패키지 레이어 (3단 디커플링 구현 완료)
    ├── __init__.py              # web 패키지화 선언
    ├── app.py                   # [Orchestrator] UI 렌더링 전담 컴팩트 레이아웃 (Thin Controller)
    ├── README.md                # 대시보드 화면 구성 및 구현 흐름 기술 명세서
    ├── genre_guardrails.json    # 외삽 오류 방지용 과거 장르별 스크린/상영수 분포 가드레일
    ├── stage1_ensemble.pkl      # 학습 완료된 Stage 1 고유 잠재력 예측 Stacking 피처 파일
    ├── stage2_simulator.pkl      # 학습 완료된 Stage 2 배급 보정용 단조 제약 XGBoost 파일
    └── utils/                   # 화면과 로직을 분리한 기능별 모듈 폴더
        ├── __init__.py          # utils 패키지화 선언
        ├── loader.py            # [Data Loader] Streamlit 리소스 및 CSV 데이터 캐싱 전담
        ├── predictor.py         # [Model Engine] 2-Stage 추론 연산 및 Elbow Point 스윗스팟 계산
        └── styles.py            # [Visual Token] Premium UI CSS 테마 주입 및 한글 변환 사전
```

---

## 4. 2-Stage 시뮬레이터 모델 아키텍처 개요

본 프로젝트는 첫날 배급사의 영업력(스크린 독점)에 의해 최종 성적이 왜곡되는 내생성(Endogeneity) 문제를 해소하기 위해 **2단계 독립 추론 아키텍처**를 설계하여 반영했습니다.

### 🔄 추론 흐름 및 데이터 플로우

```
Stage 1 (콘텐츠 잠재력 모델)
  Input  ──> 개봉 전 순수 콘텐츠 메타 (배우/감독 스타파워, 시즌, 사전 트렌드 버즈, 장르 등)
  Output ──> pred_potential (스크린 배급 요인이 완전히 배제된 순수 흥행 잠재 점수)
                    │
                    ▼ [pred_potential 점수 전달]
Stage 2 (배급 스케일 보정 모델 = 시뮬레이터)
  Input  ──> [pred_potential] + [scrnCnt_day1, showCnt_day1 (제어/시뮬레이션 변수)]
  Output ──> 최종 예상 누적 관객수 (XGBoost Monotonic Constraints)
```

- **Stage 1 (Pure Power)**: 개봉 전 요인들만으로 콘텐츠 고유의 체급을 객관적으로 진단합니다.
- **Stage 2 (Distribution Power)**: Stage 1 예측 점수에 배급사가 통제할 수 있는 개봉 첫날 스크린 수와 상영 횟수(Log 스케일 변환)를 합성하여, 단조 증가 제약(Monotonic Constraints) 조건 하에서 최종 예상 관객수를 정밀하게 보정합니다.
- **의사결정 혜택**: 스크린 확보를 무리하게 수십 배 늘리더라도 관객수 증가 효율이 꺾이는 한계 기여 곡선을 가시화하여 배급 최적점인 **Elbow Point**를 분석할 수 있습니다.

---

## 5. 💡 에이전트를 위한 핵심 개발 가이드 및 패키지별 유의사항

후속 에이전트가 본 프로젝트의 각 레이어(데이터, 모델, 웹 서비스)를 유지보수하거나 기여할 때는 아래 패키지별 개발 가이드와 상세 `README.md` 문서를 반드시 참조 및 준수해야 합니다.

### ① 데이터 수집 및 API 레이어 (`data/api/`)
*   **상세 기술 명세서**: ➡️ [data/api/README.md](file:///home/hong/project/ai-camp-project-note/projects/SKN30-2nd-4Team/data/api/README.md)
*   **개발 핵심 규칙**:
    *   KOBIS와 NAVER API 연동 시 Pydantic DTO(`kobis_dto.py`, `naver_dto.py`)를 통해 데이터 형변환 및 검증을 완벽히 수행하여 DB 입력 정합성을 유지합니다.
    *   API 실패 대처와 Rate Limit 방지를 위해 Batch 단위 호출 및 딜레이 예외 처리가 필수 적용되어야 합니다.

### ② 데이터베이스 및 마이그레이션 레이어 (`data/db/`)
*   **상세 기술 명세서**: ➡️ [data/db/README.md](file:///home/hong/project/ai-camp-project-note/projects/SKN30-2nd-4Team/data/db/README.md)
*   **개발 핵심 규칙**:
    *   모든 MySQL 테이블 형상 관리는 `migrate/1.CREATE_TABLE.sql` 통합 SQL 마이그레이션 버전을 경유합니다.
    *   Upsert 대용량 적재 시 `db_manager.py` 내의 `execute_many` 벌크 인서트 메소드를 반드시 타야 하며, DB Connection Leak 예방을 위한 리소스 close 처리를 보존합니다.

### ③ 머신러닝 & 딥러닝 모델링 레이어 (`ml/`)
*   **상세 기술 명세서**: ➡️ [ml/README.md](file:///home/hong/project/ai-camp-project-note/projects/SKN30-2nd-4Team/ml/README.md)
*   **개발 핵심 규칙**:
    *   피처 엔지니어링 수행 시 데이터 누수(Data Leakage)가 절대 발생하지 않도록 개봉일 기준 피처 스위핑을 지킵니다. (v3 피처 스펙 유지)
    *   하이퍼파라미터 최적화는 Optuna 튜닝 프로세스를 활용하고, 피처 변동 사항은 `ml/data/CHANGELOG.md`에 기록 관리합니다.
    *   Stage 1 메타 앙상블 가중 피처 중요도는 CatBoost 8 : XGBoost 2 메타 메커니즘을 따릅니다.

### ④ Streamlit 대시보드 웹 서비스 레이어 (`web/`)
*   **상세 기술 명세서**: ➡️ [web/README.md](file:///home/hong/project/ai-camp-project-note/projects/SKN30-2nd-4Team/web/README.md)
*   **개발 핵심 규칙**:
    *   **데이터 로딩 및 캐싱 (`web/utils/loader.py`)**: 모든 ML 모델과 CSV 데이터는 `@st.cache_resource`와 `@st.cache_data`를 경유해야 리액티브 엔진의 낭비가 방지됩니다.
    *   **추론/연산 비즈니스 로직 (`web/utils/predictor.py`)**: 화면 렌더링에 노출되는 모든 수식, 2-Stage 추론 연산, 30단계 초정밀 스 Sweep 기반의 최적 효율 스윗스팟(Elbow Point) 계산 로직은 본 파일 안의 순수 함수(Pure Function)로 완전히 격리하고 유지합니다.
    *   **디자인 테마 및 한글화 사전 (`web/utils/styles.py`)**: Premium Visual CSS 테마 주입 및 28개 피처 한글 매핑 사전을 단독 분리 관리합니다.

### ⑤ 플랫폼 원클릭 배포 설정 (`main.py`)
*   **개발 핵심 규칙**:
    *   배포 플랫폼(Streamlit Cloud)에서 루트의 `main.py`가 런칭 엔트리포인트로 기동되도록 설계되어 있습니다. 절대 경로 해석 정합성을 훼손하는 임의의 파일 이동이나 파일명 변경은 엄격히 금지됩니다.
