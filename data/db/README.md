# 🗄️ data/db 패키지 — 데이터베이스 관리

이 패키지는 MySQL 데이터베이스에 데이터를 저장하고 조회하는 기능을 담당합니다.
API로 수집한 영화 데이터를 실제 DB에 넣거나 꺼내는 모든 작업이 이곳을 통해 이루어집니다.

---

## 📂 파일 구성

| 파일/폴더 | 역할 |
|-----------|------|
| `db_manager.py` | DB에 연결하고 쿼리를 실행하는 핵심 클래스(`DBManager`) |
| `migrate/` | 테이블을 생성하는 SQL 파일 모음 |
| `migrate/1.CREATE_TABLE.sql` | 전체 테이블 생성 DDL (최초 1회 실행 필요) |
| `insert_box_office.ipynb` | ✅ 박스오피스 데이터 수집 노트북 |
| `insert_movie.ipynb` | 🔧 영화 상세 + 영화사 수집 노트북 |
| `insert_people.ipynb` | 📋 영화인 ID 매핑 노트북 |

---

## 🚀 사용법

```python
from data.db import db  # 싱글톤 DB 객체

# 1. 데이터 삽입/수정/삭제 (단건)
db.execute_query(
    "INSERT INTO movies (movie_id, title) VALUES (%s, %s)",
    ("20124079", "명량")
)

# 2. 데이터 대량 삽입 (리스트)
rows = [("20124079", "명량"), ("20136803", "국제시장")]
db.execute_many("INSERT INTO movies (movie_id, title) VALUES (%s, %s)", rows)

# 3. 여러 행 조회
movies = db.fetch_all("SELECT * FROM movies WHERE genre = %s", ("액션",))
for movie in movies:
    print(movie["title"])  # 딕셔너리 형태로 반환

# 4. 단일 행 조회
movie = db.fetch_one("SELECT * FROM movies WHERE movie_id = %s", ("20124079",))
print(movie["title"])
```

---

## 🗃️ 데이터베이스 테이블 구조

```
daily_box_office   : 일별 박스오피스 (순위, 관객수, 매출액 등)
daily_market_stats : 일별 전체 시장 통계 (총 관객수, 총 매출 등)
movies             : 영화 정보 (장르, 등급, 런타임, 개봉일 등)
people             : 영화인 정보 (감독, 배우)
movie_casting      : 영화-영화인 출연 관계
companys           : 영화사 정보 (제작사, 배급사 등)
company_part       : 영화-영화사 참여 관계
holidays           : 공휴일 정보
```

> 📖 테이블 컬럼 상세 내용은 `migrate/1.CREATE_TABLE.sql` 파일을 참고하세요.

---

## 🛠️ 마이그레이션 (자동 환경 구축)

프로젝트 루트의 `migrate.sh`를 사용하면 `migrate/` 폴더 내의 모든 SQL 파일을 순서대로 실행하여 테이블 구조 생성 및 초기 데이터 적재를 자동으로 수행합니다.

### 로컬 MySQL 사용 시
터미널에 mysql 커맨드가 사용 가능한 상태여야합니다.
```bash
./migrate.sh
```

### 특정 단계(파일)만 실행 시
전체 데이터 적재가 부담스럽거나 특정 테이블만 수정했을 때 사용합니다.
```bash
./migrate.sh --step=1  # 테이블 생성만 수행
./migrate.sh --step=2  # 박스오피스 데이터 적재만 수행
```

---

## 📤 데이터 추출 (mysqldump)

특정 데이터를 SQL 파일로 저장하여 공유해야 할 때 사용합니다. 네이밍 맞춰주세요. ex: 순서.실행쿼리_테이블_범위.sql

```bash
# 특정 테이블만 추출
mysqldump -u [사용자] -p[비밀번호] [DB이름] [테이블1] [테이블2] > [파일명].sql
```

**예시:**
```bash
mysqldump -u root -p password123 film movies daily_box_office > historical_data.sql
```

추출 후 insert문만 남겨주세요.

---

## ✅ 최초 환경 세팅 순서

1.  MySQL에 데이터베이스(`film`)를 생성합니다.
2.  프로젝트 루트의 `.env` 파일에 DB 접속 정보를 입력합니다.
3.  `./migrate.sh`를 실행하여 테이블과 초기 데이터를 구축합니다.
4.  `insert_movie.ipynb` 등 노트북을 실행하여 추가 데이터를 수집합니다.

---

## 💡 주의사항

- **모든 오류는 예외(Exception)로 전파됩니다.** 에러 발생 시 즉시 실행이 중단되므로, 노트북에서 오류 메시지를 꼭 확인하세요.
- **대량 데이터 삽입 시** `execute_many`를 사용하면 내부적으로 1,000건씩 나누어 처리하므로 안전합니다.
- **같은 데이터를 두 번 넣어도** `ON DUPLICATE KEY UPDATE` 전략 덕분에 중복 오류 없이 최신 데이터로 업데이트됩니다.
