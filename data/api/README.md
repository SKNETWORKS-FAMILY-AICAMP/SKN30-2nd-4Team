# 🎬 data/api 패키지 — KOBIS API 클라이언트

이 패키지는 영화진흥위원회(KOBIS)가 제공하는 Open API를 쉽게 호출할 수 있도록 만들어진 모듈입니다.
인터넷으로 KOBIS 서버에 요청을 보내고, 받아온 데이터를 파이썬 객체로 변환해줍니다.

---

## 📂 파일 구성

| 파일 | 역할 |
|------|------|
| `kobis_client.py` | KOBIS API를 실제로 호출하는 함수들이 모여 있습니다 |
| `kobis_dto.py` | API 응답 데이터를 파이썬 객체로 정의합니다 (Pydantic 사용) |
| `API_SPEC.md` | KOBIS API의 상세 명세서 (요청/응답 필드 설명) |
| `__init__.py` | 패키지 외부에서 함수를 쉽게 불러올 수 있도록 정리합니다 |

---

## 🚀 사용법

```python
from data.api import get_daily_box_office, get_movie_info, get_people_list
from datetime import date

# 1. 일별 박스오피스 조회 (날짜를 date 객체로 전달)
response = get_daily_box_office(date(2023, 12, 25))
for movie in response.boxOfficeResult.dailyBoxOfficeList:
    print(movie.rank, movie.movieNm, movie.audiCnt)

# 2. 영화 상세 정보 조회
response = get_movie_info(movie_cd="20124079")
movie = response.movieInfoResult.movieInfo
print(movie.movieNm, movie.genres)

# 3. 영화인 목록 검색 (동명이인 구분을 위해 filmoNames도 함께 사용)
response = get_people_list(people_nm="하정우", filmo_names="황해")
for person in response.peopleListResult.peopleList:
    print(person.peopleCd, person.peopleNm)
```

---

## 📋 제공하는 함수 목록

| 함수명 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `get_daily_box_office` | 특정 날짜의 박스오피스 Top 10 조회 | `target_dt: date` |
| `get_movie_list` | 영화 목록 검색 | `movie_nm`, `open_start_dt`, `open_end_dt` |
| `get_movie_info` | 영화 상세 정보 조회 | `movie_cd: str` |
| `get_company_list` | 영화사 목록 검색 | `company_nm` |
| `get_company_info` | 영화사 상세 정보 조회 | `company_cd: str` |
| `get_people_list` | 영화인 목록 검색 | `people_nm`, `filmo_names` |
| `get_people_info` | 영화인 상세 정보 조회 | `people_cd: str` |
| `get_common_codes` | 공통 코드 조회 (지역코드 등) | `com_code: str` |

---

## 💡 동작 원리 (입문자용 설명)

1. 함수를 호출하면 내부에서 KOBIS 서버로 HTTP 요청을 보냅니다.
2. 서버가 JSON 형식으로 데이터를 보내주면, `kobis_dto.py`에 정의된 Pydantic 모델이 그 데이터를 파이썬 객체로 자동 변환합니다.
3. 덕분에 `response.boxOfficeResult.dailyBoxOfficeList[0].rank` 처럼 **점(`.`)으로 이어지는 방식**으로 데이터에 접근할 수 있습니다.

> 📖 각 API의 요청/응답 필드 상세 설명은 `API_SPEC.md`를 참고하세요.
