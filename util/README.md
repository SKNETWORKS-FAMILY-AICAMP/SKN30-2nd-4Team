# ⚙️ util 패키지 — 프로젝트 환경 설정

이 패키지는 프로젝트 전체에서 사용하는 **API 키, DB 접속 정보** 등 민감한 설정값을 안전하게 관리합니다.

---

## 📂 파일 구성

| 파일 | 역할 |
|------|------|
| `config.py` | `.env` 파일을 읽어 설정값을 파이썬 객체로 만들어 줍니다 |
| `__init__.py` | `settings` 객체를 외부에서 쉽게 가져올 수 있도록 내보냅니다 |

---

## 🚀 사용법

```python
from util import settings

print(settings.KOBIS_KEY)   # KOBIS API 키
print(settings.KOBIS_URL)   # KOBIS API 주소
print(settings.DB_CONFIG)   # MySQL 접속 정보 (딕셔너리)
```

---

## 🔑 환경변수 설정 (`.env` 파일)

프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 채워주세요.  
이 파일은 Git에 올라가지 않으므로 **팀원 각자가 직접 만들어야 합니다.**

```dotenv
# KOBIS API
KOBIS_URL=http://www.kobis.or.kr/kobisopenapi/webservice/rest
KOBIS_KEY=발급받은_API_키를_여기에_입력

# MySQL DB
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=비밀번호
DB_NAME=데이터베이스명
```

> ⚠️ `.env` 파일에 실제 비밀번호나 API 키를 넣은 채로 GitHub에 Push하면 안 됩니다!

---

## 💡 동작 원리 (입문자용 설명)

`.env` 파일에 설정값을 적어두면, `config.py`가 프로그램 실행 시 자동으로 그 값을 읽어서 `settings` 객체에 담아줍니다.
그래서 코드 어디서든 `from util import settings`만 입력하면 설정값에 접근할 수 있습니다.
