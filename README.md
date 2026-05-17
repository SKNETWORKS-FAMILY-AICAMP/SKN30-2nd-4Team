# SKN30-2nd-4Team

**모든 내용을 필독해주세요**

# 프로젝트 구조

```
SKN30-2nd-4Team/
├── .env                          # 환경변수 (DB 접속정보, API 키)
├── pyproject.toml                # 프로젝트 설정 및 의존성 (uv 관리)
├── AGENTS.md                     # AI 참고용 문서
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
│       ├── migrate/              # DB 마이그레이션 sql 파일
│
└── ml/                           # (비어있음) ML 모델 코드가 들어갈 디렉토리
```

---

# 초기 세팅

## 1. 가상환경 및 의존성 설치
본 프로젝트는 `uv`를 사용하여 패키지를 관리합니다. 프로젝트 루트에서 아래 명령어를 실행하여 가상환경을 생성하고 필요한 패키지를 설치합니다.

```bash
# 의존성 설치 및 가상환경 생성 (.venv 폴더 생성됨)
uv sync
```

## 2. 환경 변수 설정 (`.env`)
프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 입력합니다. 발급받은 KOBIS API 키와 본인의 MySQL 접속 정보를 입력해야 합니다.

```dotenv
# KOBIS API
KOBIS_URL=http://www.kobis.or.kr/kobisopenapi/webservice/rest
KOBIS_KEY=발급받은_API_키를_여기에_입력

# MySQL DB
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=비밀번호
DB_NAME=film
```

> [!IMPORTANT]
> MySQL에서 미리 `DB_NAME`에 지정한 이름(예: `film`)으로 데이터베이스를 생성해두어야 합니다. 한글 깨짐 방지를 위해 아래와 같이 유니코드 옵션을 붙여서 생성하는 것을 강력히 권장합니다.
> ```sql
> CREATE DATABASE film CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> ```
> 
## 3. 데이터베이스 마이그레이션
테이블 구조를 생성하고 초기 데이터를 적재합니다. 윈도우 사용자는 **Git Bash** 환경에서 실행하는 것을 권장합니다. (보통은 vscode에서 그냥 실행하시면 됩니다.)

```bash
# 1. 실행 권한 부여 (필요 시)
chmod +x migrate.sh

# 2. 전체 마이그레이션 실행 (테이블 생성 + 데이터 적재)
./migrate.sh
```

**특정 단계만 실행하고 싶은 경우:**
- `./migrate.sh --step=1`: 테이블 생성만 수행 (`1.CREATE_TABLE.sql`)
- `./migrate.sh --step=2`: 박스오피스 데이터 적재 (`2.INSERT_BOX_OFFICE_...sql`)

---

## 폴더 별 상세 설명 (필독)
각 폴더의 역할과 상세 사용법은 아래 문서를 참고하세요.

- [📂 data/api](data/api/README.md): KOBIS API 호출 모듈 및 DTO 정의
- [📂 data/db](data/db/README.md): **(중요)** DB 접속 관리 및 마이그레이션 가이드
- [📂 util](util/README.md): 환경 설정 및 `settings` 객체 관리

# AI와 협업하기

본 프로젝트는 AI 에이전트 및 LLM과의 협업을 고려하여 설계되었습니다. AI에게 아래 문서들을 컨텍스트로 제공하면 더 정확한 코드 작성과 문제 해결이 가능합니다.

### 1. AI 에이전트 사용자 (Cursor, Claude code, Codex, Antigravity 등)
*   프로젝트 루트의 `AGENTS.md`를 인식시키세요.

### 2. 웹 채팅 사용자 (ChatGPT, Claude, Gemini 등)
웹 환경에서 AI와 대화할 때, 대화 시작 시 아래 파일들의 내용을 복사해서 붙여넣어 주세요. AI가 프로젝트의 구조와 규칙을 완벽히 이해한 상태로 답변해 줍니다.

*   **[AGENTS.md](AGENTS.md)**: 프로젝트의 전체 목표, 역할분담, 현재 진행 상황 및 컨벤션 정보
*   **[data/api/README.md](data/api/README.md)**: 사용 가능한 API 함수 목록과 데이터 모델(DTO) 정보
*   **[data/db/README.md](data/db/README.md)**: 데이터베이스 스키마 및 DB 접근 방식
*   **[util/README.md](util/README.md)**: 환경 설정 및 설정값 접근 방법

> 💡 **Tip**: "이 파일들은 내 프로젝트의 가이드라인이야. 내용을 읽고 내가 요청하는 기능을 구현해줘."라고 먼저 말한 뒤 코드를 요청해 보세요!
