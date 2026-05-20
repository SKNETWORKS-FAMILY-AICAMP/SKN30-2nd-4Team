# 네이버 통합 검색어 트렌드 API 명세서

주제어로 묶은 검색어들에 대한 네이버 통합검색에서의 검색 추이 데이터를 JSON 형식으로 반환하는 RESTful API입니다. 비로그인 방식 오픈 API로, HTTP 요청 헤더에 클라이언트 아이디와 클라이언트 시크릿 값을 전송하여 사용합니다.

## 1. 기본 정보

| 항목 | 내용 |
| --- | --- |
| **요청 URL** | `https://openapi.naver.com/v1/datalab/search` |
| **프로토콜** | HTTPS |
| **HTTP 메서드** | **POST** |
| **하루 호출 한도** | 1,000회 |

---

## 2. 요청 헤더 (Request Headers)

API를 호출할 때 아래의 인증 정보를 헤더에 반드시 포함해야 합니다.

| 헤더명 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `X-Naver-Client-Id` | string | Y | 애플리케이션 등록 시 발급받은 클라이언트 아이디 값 |
| `X-Naver-Client-Secret` | string | Y | 애플리케이션 등록 시 발급받은 클라이언트 시크릿 값 |
| `Content-Type` | string | Y | `application/json` |

---

## 3. 요청 파라미터 (Request Body)

데이터는 **JSON 형식**으로 전달해야 합니다.

### 주요 파라미터

| 파라미터 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `startDate` | string | Y | 조회 기간 시작 날짜 (`yyyy-mm-dd` 형식, 2016년 1월 1일부터 조회 가능) |
| `endDate` | string | Y | 조회 기간 종료 날짜 (`yyyy-mm-dd` 형식) |
| `timeUnit` | string | Y | 구간 단위 (`date`: 일간, `week`: 주간, `month`: 월간) |
| `keywordGroups` | array(JSON) | Y | 주제어와 검색어 묶음 쌍의 배열 (최대 5개까지 설정 가능) |
| `device` | string | N | 검색 환경 조건 (설정 안 함: 모든 환경, `pc`: PC, `mo`: 모바일) |
| `gender` | string | N | 검색 사용자 성별 조건 (설정 안 함: 모든 성별, `m`: 남성, `f`: 여성) |
| `ages` | array(string) | N | 검색 사용자 연령 조건 (설정 안 함: 모든 연령, 하단 연령 코드 참조) |

### keywordGroups 내부 속성

| 속성명 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `groupName` | string | Y | 주제어 (검색어 묶음을 대표하는 이름) |
| `keywords` | array(string) | Y | 주제어에 해당하는 검색어 (최대 20개까지 설정 가능) |

> **연령 코드 (ages) 안내**
> * `1`: 0∼12세 | `2`: 13∼18세 | `3`: 19∼24세 | `4`: 25∼29세 | `5`: 30∼34세 | `6`: 35∼39세
> * `7`: 40∼44세 | `8`: 45∼49세 | `9`: 50∼54세 | `10`: 55∼59세 | `11`: 60세 이상
> 
> 

### 요청 바디 예시 (Request Body Example)

```json
{
  "startDate": "2017-01-01",
  "endDate": "2017-04-30",
  "timeUnit": "month",
  "keywordGroups": [
    {
      "groupName": "한글",
      "keywords": ["한글", "korean"]
    },
    {
      "groupName": "영어",
      "keywords": ["영어", "english"]
    }
  ],
  "device": "pc",
  "ages": ["1", "2"],
  "gender": "f"
}

```

---

## 4. 응답 데이터 (Response Body)

요청에 성공하면 결괏값을 **JSON 형식**으로 반환합니다.

### 응답 필드 설명

| 속성명 | 타입 | 설명 |
| --- | --- | --- |
| `startDate` | string | 조회 기간 시작 날짜 (`yyyy-mm-dd`) |
| `endDate` | string | 조회 기간 종료 날짜 (`yyyy-mm-dd`) |
| `timeUnit` | string | 구간 단위 (`date`, `week`, `month`) |
| `results` | array | 주제어별 검색 추이 결과 배열 |
| `results.title` | string | 주제어 |
| `results.keywords` | array | 주제어에 해당하는 검색어 목록 |
| `results.data` | array | 구간별 데이터 배열 |
| `results.data.period` | string | 구간별 시작 날짜 (`yyyy-mm-dd`) |
| `results.data.ratio` | number | 구간별 검색량의 상대적 비율 (조회 기간 내 가장 큰 값을 100으로 설정한 상댓값) |

### 응답 예시 (Response Example)

```json
{
  "startDate": "2017-01-01",
  "endDate": "2017-04-30",
  "timeUnit": "month",
  "results": [
    {
      "title": "한글",
      "keywords": ["한글", "korean"],
      "data": [
        { "period": "2017-01-01", "ratio": 47.0 },
        { "period": "2017-02-01", "ratio": 53.23 },
        { "period": "2017-03-01", "ratio": 100.0 },
        { "period": "2017-04-01", "ratio": 85.32 }
      ]
    },
    {
      "title": "영어",
      "keywords": ["영어", "english"],
      "data": [
        { "period": "2017-01-01", "ratio": 40.08 },
        { "period": "2017-02-01", "ratio": 36.69 },
        { "period": "2017-03-01", "ratio": 52.11 },
        { "period": "2017-04-01", "ratio": 44.45 }
      ]
    }
  ]
}

```

---

## 5. 오류 코드 (Error Codes)

| 오류 코드 | HTTP 상태 코드 | 오류 메시지 | 설명 및 해결 방법 |
| --- | --- | --- | --- |
| **400** | 400 | 잘못된 요청 | API 요청 URL의 프로토콜, 필수 파라미터 누락, 날짜 형식 오류 등이 있는지 확인합니다. |
| **403** | 403 | API 권한 없음 | 네이버 개발자 센터의 **[Application > 내 애플리케이션]** 메뉴에서 해당 애플리케이션의 API 설정 탭에 **[데이터랩 (검색어트렌드)]**가 체크되어 있는지 확인합니다. |
| **500** | 500 | 서버 내부 오류 | 네이버 내부 서버 오류입니다. 지속될 경우 개발자 포럼에 신고가 필요합니다. |