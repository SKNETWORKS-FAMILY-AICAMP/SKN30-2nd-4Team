# SKN30-2nd-4Team

[참고 AGENT.md](AGENTS.md)


## 1.프로젝트 구조

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
│       ├── insert_box_office.ipynb  # ✅ 완료 — 박스오피스 데이터 수집
│       ├── insert_movie.ipynb       # 🔧 진행중 — 영화 상세 + 영화사 수집
│       └── insert_people.ipynb      # 📋 예정 — 영화인 ID 매핑 및 캐스팅 구축
│
└── ml/                           # (비어있음) ML 모델 코드가 들어갈 디렉토리
```

---

## 2. 폴더 별 설명 (필독)
[data/api](data/api/README.md)

[data/db](data/db/README.md) **특히 중요** 마이그래이션 부분은 필필독입니다.

[util](util/README.md)

