# 🤖 AGENT.md — 개봉 예정작 흥행 예측 프로젝트

이 문서는 AI 에이전트가 본 프로젝트를 빠르게 이해하고 효과적으로 기여하기 위한 지침서입니다.

---

## 1. 프로젝트 목표와 산출물

**과거 상영작 데이터를 학습하여, 개봉 예정작의 흥행 여부를 예측하는 ML/DL 모델을 구축한다.**

### 🎯 프로젝트 목표
1. **비즈니스 이해**: 비즈니스 이해를 통한 머신러닝 모델 활용 계획 수립
2. **데이터 셋 준비 및 전처리**: 머신러닝 모델 구축을 위한 데이터 셋 준비 및 전처리
3. **학습 및 평가**: 머신러닝 모델과 딥러닝 모델 학습 및 평가
4. **최적화 및 배포**: 평가를 통한 성능이 좋은 최적의 모델 설정 및 배포

### 📝 프로젝트 내용
* 프로젝트와 관련된 비즈니스 목표 이해
* 데이터 탐색적 분석 및 데이터 전처리
* 학습용 데이터셋과 테스트 데이터셋 분리
* 활용할 머신러닝/딥러닝 모델들 후보 선정하고 모델링 진행
* 다양한 모델링 결과 측정 지표로 측정하고 최적의 모델 선정
* 최적의 모델 배포 및 테스트
* *타겟 변수*: 누적 관객수(`audiAcc`), 누적 매출액(`salesAcc`) 등 (개봉 전 메타데이터만으로 예측)

### 📦 필수 산출물
1. **인공지능 데이터 전처리 결과서**
2. **인공지능 학습 결과서**
3. **학습된 인공지능 모델**

---

## 2. 에이전트 역할

- **페르소나**: Python 기반 데이터 사이언티스트 및 ML/DL 전문가
- **전문 분야**: 피처 엔지니어링, 탐색적 데이터 분석(EDA), 회귀/분류 모델링, 딥러닝
- **원칙**:
  - 사용자의 의견을 최우선으로 존중한다.
  - 전문가로서 최선의 방안을 제시하되, 최종 결정은 사용자가 한다.
  - 코드는 항상 기존 프로젝트 컨벤션을 따른다.

---

## 3. 프로젝트 구조

```
SKN30-2nd-4Team/
├── .env                          # 환경변수 (DB 접속정보, API 키)
├── pyproject.toml                # 프로젝트 설정 및 의존성 (uv 관리)
├── AGENTS.md                     # 이 문서
│
├── util/
│   ├── __init__.py               # settings 객체 export
│   └── config.py                 # AppSettings (Pydantic 기반, .env 로드)
│
├── data/
│   ├── api/
│   │   ├── __init__.py           # API 함수 export (KOBIS 8개 + NAVER 1개)
│   │   ├── kobis_client.py       # KOBIS REST API 호출 함수 구현체
│   │   ├── kobis_dto.py          # Pydantic DTO (자동 형변환 적용)
│   │   ├── KOBIS_API_SPEC.md     # KOBIS API 명세서
│   │   ├── naver_client.py       # NAVER REST API 호출 함수 구현체
│   │   ├── naver_dto.py          # Pydantic DTO (네이버 검색어 트렌드)
│   │   └── NAVER_API_SPEC.md     # NAVER API 명세서
│   │
│   └── db/
│       ├── __init__.py           # db(DBManager 인스턴스) export
│       ├── db_manager.py         # MySQL CRUD 클래스 (execute_many, fetch_all 등)
│       ├── migrate/
│       │   └── 1.CREATE_TABLE.sql  # 전체 테이블 DDL
│       │
│       ├── insert_box_office.ipynb  # 박스오피스 데이터 수집
│       ├── insert_movie.ipynb       # 영화 상세 + 영화사 수집
│       ├── insert_people.ipynb      # 영화인 ID 매핑 및 캐스팅 구축
│       └── insert_naver_trend.ipynb # 네이버 검색 트렌드 수집 및 적재
│
└── ml/                           # ML/DL 모델링 (상세: ml/README.md 참조)
    ├── README.md                 # 모델링 작업 가이드 및 협업 규칙
    ├── 00_feature_table.ipynb    # 공통 피처 테이블 생성 (공동 작업용)
    ├── 01_eda_baseline.ipynb     # EDA + Baseline ML
    ├── 02_boosting.ipynb         # XGBoost, LightGBM + 튜닝
    ├── 03_deep_learning.ipynb    # MLP 회귀 + 분류
    ├── 04_model_comparison.ipynb # 전체 모델 비교 및 최종 선정
    └── data/
        ├── baseline_feature_table.md      # 피처 설계 명세서
        └── CHANGELOG.md          # 피처 버전 변경 기록
```
----

## 4. 핵심 모듈 가이드 (상세 README 참조)

프로젝트 코드 작성 규칙 및 상세 사용법은 각 폴더에 위치한 개별 문서를 참조하세요:

- **데이터 수집 (`data/api/`)**: API 호출 및 DTO 처리 방식 ➡️ [`data/api/README.md`](data/api/README.md)
- **데이터베이스 (`data/db/`)**: DB 쿼리(CRUD), 대량 삽입(Upsert), 초기화(migrate) 규칙 ➡️ [`data/db/README.md`](data/db/README.md)
- **공통 설정 (`util/`)**: 환경 변수 및 설정 객체 관리 ➡️ [`util/README.md`](util/README.md)
- **ML 모델링 (`ml/`)**: 작업 분담, 공통 코드, 피처 버전업 규칙 ➡️ [`ml/README.md`](ml/README.md)

## 5. 데이터베이스 스키마

| 테이블 | 역할 | PK | ML 활용 |
|--------|------|-----|---------|
| `movies` | 영화 메타데이터 (장르, 등급, 런타임, 국가, 개봉일) | `movie_id` | 기본 피처 |
| `daily_box_office` | 일별 순위, 관객수, 매출, 점유율 | `(target_date, movie_id)` | 타겟 변수 + 시계열 피처 |
| `daily_market_stats` | 일별 시장 전체 규모 (총 관객수, 총 매출, 1위 점유율) | `target_date` | 시장 상황 피처 |
| `companys` / `company_part` | 제작사·배급사 정보 및 영화 관계 | `company_id` / `(company_id, movie_id)` | 브랜드 파워 피처 |
| `people` / `movie_casting` | 감독·배우 정보 및 출연 관계 | `person_id` / `(person_id, movie_id)` | Star Power 피처 |
| `holidays` | 공휴일, 연휴 정보 | `holiday_date` | 시즌 피처 |
| `naver_search_trend` | 네이버 검색 트렌드 (기간별 검색량 점수) | `(movie_id, trend_date)` | 관심도/화제성 피처 |

> `movies.people` 컬럼에는 `{"directors": [...], "actors": [...]}`형태의 JSON이 저장되어 있습니다.  
> `rank`는 MySQL 예약어이므로 SQL에서 반드시 **백틱**으로 감싸야 합니다: `` `rank` ``

---

## 6. 다음 단계 (로드맵)

| 단계 | 내용 | 상태 |
|------|------|------|
| 데이터 수집 | 박스오피스, 영화, 영화사 데이터, 영화인 ID 매핑 및 캐스팅 적재 | ✅ 완료 |
| 피처 엔지니어링 | 공통 피처 테이블 v1 생성 (46개 컬럼) | 완료 |
| 피처 엔지니어링 | 피처 버전업 (v2, v3, …) | 🔧 진행중 |
| EDA + Baseline ML | 탐색적 분석 + Linear, Ridge, Lasso, RF | 🔧 진행중 |
| Boosting ML | XGBoost, LightGBM + Optuna 튜닝 | 🔧 진행중 |
| 딥러닝 | MLP 회귀 + MLP 분류 | 🔧 진행중 |
| 모델 비교 | 전체 모델 성능 비교 + 최적 모델 선정 | 📋 예정 |

> ML/DL 모델링의 작업 목록, 피처 버전업 규칙, 공통 코드, 산출물 작성 규칙은 `ml/README.md` 참조
