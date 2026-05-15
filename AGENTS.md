# 🤖 AGENT.md — 개봉 예정작 흥행 예측 프로젝트

이 문서는 AI 에이전트가 본 프로젝트를 빠르게 이해하고 효과적으로 기여하기 위한 지침서입니다.

---

## 1. 프로젝트 목표

**과거 상영작 데이터를 학습하여, 개봉 예정작의 흥행 여부를 예측하는 ML/DL 모델을 구축한다.**

- 타겟 변수: 누적 관객수(`audiAcc`), 누적 매출액(`salesAcc`) 등
- 예측 시점: 개봉 전 메타데이터만으로 예측하는 것이 핵심 목표

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
│   │   ├── __init__.py           # API 함수 export (get_daily_box_office 등 8개)
│   │   ├── kobis_client.py       # KOBIS REST API 호출 함수 구현체
│   │   ├── kobis_dto.py          # Pydantic DTO (자동 형변환 적용)
│   │   └── API_SPEC.md           # KOBIS API 명세서
│   │
│   └── db/
│       ├── __init__.py           # db(DBManager 인스턴스) export
│       ├── db_manager.py         # MySQL CRUD 클래스 (execute_many, fetch_all 등)
│       ├── migrate/
│       │   └── 1.CREATE_TABLE.sql  # 전체 테이블 DDL
│       │
│       ├── insert_box_office.ipynb  # ✅ 완료 — 박스오피스 데이터 수집
│       ├── insert_movie.ipynb       # 🔧 진행중 — 영화 상세 + 영화사 수집
│       └── insert_people.ipynb      # 📋 예정 — 영화인 ID 매핑 및 캐스팅 구축
│
└── ml/                           # (비어있음) ML 모델 코드가 들어갈 디렉토리
```

---

## 4. 핵심 모듈 사용법

### 4.1 설정 (Settings)
```python
from util import settings

settings.KOBIS_KEY   # API 키
settings.KOBIS_URL   # API Base URL
settings.DB_CONFIG   # MySQL 접속 딕셔너리
```

### 4.2 API 호출
```python
from data.api import get_daily_box_office, get_movie_info, get_people_list
from datetime import date

# 박스오피스 조회 (date 객체 전달 → 내부에서 YYYYMMDD 변환)
response = get_daily_box_office(date(2023, 12, 25))
result = response.boxOfficeResult

# 영화 상세 조회
response = get_movie_info(movie_cd="20124079")
movie = response.movieInfoResult.movieInfo
```

### 4.3 DB 작업
```python
from data.db import db

# 단일 쿼리
db.execute_query("INSERT INTO ...", params)

# 대량 삽입 (chunk_size=1000 기본, 내부 트랜잭션)
db.execute_many("INSERT INTO ...", rows_list)

# 조회
rows = db.fetch_all("SELECT * FROM movies WHERE genre = %s", ("액션",))
row  = db.fetch_one("SELECT * FROM movies WHERE movie_id = %s", ("20124079",))
```

> **중요**: 모든 DB 메서드는 오류 발생 시 에러를 출력한 뒤 **예외를 재발생(raise)**시킵니다.

---

## 5. 데이터베이스 스키마

| 테이블 | 역할 | PK | ML 활용 |
|--------|------|-----|---------|
| `movies` | 영화 메타데이터 (장르, 등급, 런타임, 국가, 개봉일) | `movie_id` | 기본 피처 |
| `daily_box_office` | 일별 순위, 관객수, 매출, 점유율 | `(target_date, movie_id)` | 타겟 변수 + 시계열 피처 |
| `daily_market_stats` | 일별 시장 전체 규모 (총 관객수, 총 매출, 1위 점유율) | `target_date` | 시장 상황 피처 |
| `companys` / `company_part` | 제작사·배급사 정보 및 영화 관계 | `company_id` / `(company_id, movie_id)` | 브랜드 파워 피처 |
| `people` / `movie_casting` | 감독·배우 정보 및 출연 관계 | `person_id` / `(person_id, movie_id)` | Star Power 피처 |
| `holidays` | 공휴일, 연휴 정보 | `holiday_date` | 시즌 피처 |

> `movies.people` 컬럼에는 `{"directors": [...], "actors": [...]}`형태의 JSON이 저장되어 있습니다.  
> `rank`는 MySQL 예약어이므로 SQL에서 반드시 **백틱**으로 감싸야 합니다: `` `rank` ``

---

## 6. 데이터 수집 현황

### ✅ 완료: 박스오피스 (`insert_box_office.ipynb`)
- `daily_box_office` + `daily_market_stats` 동시 수집
- 30일 단위 Checkpoint 방식의 Bulk Insert
- Upsert(`ON DUPLICATE KEY UPDATE`)로 멱등성 보장

### 🔧 진행중: 영화 상세 (`insert_movie.ipynb`)
- `movies` 테이블: 기본 정보 + 영화인 이름 JSON 저장
- `companys` + `company_part` 테이블: 제작사/배급사/제공만 필터링하여 동시 저장

### 📋 예정: 영화인 매핑 (`insert_people.ipynb`)
- `movies.people` JSON에서 이름 추출 → 중복 제거
- `searchPeopleList` API에 `peopleNm` + `filmoNames`로 조회하여 `peopleCd` 확보
- `people` + `movie_casting` 테이블 구축

---

## 7. 개발 컨벤션

1. **DB 작업**: 반드시 `from data.db import db`를 통해 싱글톤 `DBManager`를 사용한다.
2. **API 호출**: `from data.api import ...`로 호출하며, 날짜는 `date` 객체로 전달한다.
3. **대량 처리**: 30일 또는 적절한 단위로 중간 저장(Checkpoint)하여 데이터 손실을 방지한다.
4. **Upsert 전략**: 모든 INSERT는 `ON DUPLICATE KEY UPDATE`를 사용하여 재실행 안전성을 확보한다.
5. **예외 처리**: DB/API 오류는 `print` 후 `raise`하여 호출자에게 전파한다.
6. **환경 관리**: 패키지 설치는 `uv`를 사용한다. (`uv add`, `uv pip install -e .`)
7. **노트북 규칙**: 수집/분석 작업은 `data/db/` 하위 `.ipynb` 파일에서 수행한다.

---

## 8. 다음 단계 (로드맵)

| 단계 | 내용 | 상태 |
|------|------|------|
| 데이터 수집 | 박스오피스, 영화, 영화사, 영화인 데이터 적재 | 🔧 진행중 |
| 데이터 전처리 | 결측치 처리, 타입 정규화, 이상치 제거 | 📋 예정 |
| 피처 엔지니어링 | Star Power 지수, 배급사 평균 성적, 계절성 피처 설계 | 📋 예정 |
| EDA | 장르·요일·시즌별 흥행 상관관계 시각화 | 📋 예정 |
| 모델링 | 사용자와 협의하여 적절한 ML/DL 모델 선택 및 학습 | 📋 예정 |
| 평가·개선 | 교차검증, 하이퍼파라미터 튜닝, 앙상블 | 📋 예정 |
