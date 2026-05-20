# 목차

1. [[API 명세서] 일일 박스오피스 서비스 (Daily BoxOffice)](#api-명세서-일일-박스오피스-서비스-daily-boxoffice)
2. [[API 명세서] 공통코드 조회 서비스](#api-명세서-공통코드-조회-서비스)
3. [[API 명세서] 영화목록 조회 서비스](#api-명세서-영화목록-조회-서비스)
4. [[API 명세서] 영화 상세정보 조회 서비스](#api-명세서-영화-상세정보-조회-서비스)
5. [[API 명세서] 영화사 목록 조회 서비스](#api-명세서-영화사-목록-조회-서비스)
6. [[API 명세서] 영화사 상세정보 조회 서비스](#api-명세서-영화사-상세정보-조회-서비스)
7. [[API 명세서] 영화인목록 조회 서비스](#api-명세서-영화인목록-조회-서비스)
8. [[API 명세서] 영화인 상세정보 조회 서비스](#api-명세서-영화인-상세정보-조회-서비스)

---

# [API 명세서] 일일 박스오피스 서비스 (Daily BoxOffice)

특정 일자의 박스오피스 정보를 조회하며, 영화 구분(다양성/상업), 한국/외국 영화 구분, 상영 지역 등의 조건으로 필터링이 가능합니다.

## 1. 기본 정보

* **요청 URL:** `http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json`
* **HTTP Method:** `GET`
* **응답 형식:** `JSON` (또는 XML)

---

## 2. 요청 인터페이스 (Request Parameters)

| 변수명 | 타입 | 필수여부 | 설명 |
| --- | --- | --- | --- |
| **key** | 문자열 | **필수** | 발급받은 API 키 값을 입력합니다. |
| **targetDt** | 문자열 | **필수** | 조회하고자 하는 날짜를 `yyyymmdd` 형식으로 입력합니다. |
| **itemPerPage** | 문자열 | 선택 | 결과 ROW 의 개수를 지정합니다. (기본값: "10", 최대: "10") |
| **multiMovieYn** | 문자열 | 선택 | "Y": 다양성 영화, "N": 상업영화 (기본값: 전체) |
| **repNationCd** | 문자열 | 선택 | "K": 한국영화, "F": 외국영화 (기본값: 전체) |
| **wideAreaCd** | 문자열 | 선택 | 상영지역별 코드 (공통코드 조회 서비스 "0105000000" 참조) |

---

## 3. 응답 구조 (Response Fields)

### 3.1. 박스오피스 기본 정보

| 필드명 | 설명 |
| --- | --- |
| **boxofficeType** | 박스오피스 종류를 출력합니다. |
| **showRange** | 박스오피스 조회 일자를 출력합니다. |

### 3.2. 일별 박스오피스 리스트 (`dailyBoxOfficeList`)

| 필드명 | 설명 |
| --- | --- |
| **rnum** | 순번을 출력합니다. |
| **rank** | 해당일자의 박스오피스 순위를 출력합니다. |
| **rankInten** | 전일대비 순위의 증감분을 출력합니다. |
| **rankOldAndNew** | 랭킹 신규진입 여부 ("OLD": 기존, "NEW": 신규) |
| **movieCd** | 영화의 대표코드를 출력합니다. |
| **movieNm** | 영화명(국문)을 출력합니다. |
| **openDt** | 영화의 개봉일을 출력합니다. |
| **salesAmt** | 해당일의 매출액을 출력합니다. |
| **salesShare** | 해당일자 매출총액 대비 해당 영화의 매출비율을 출력합니다. |
| **salesAcc** | 누적매출액을 출력합니다. |
| **audiCnt** | 해당일의 관객수를 출력합니다. |
| **audiAcc** | 누적관객수를 출력합니다. |
| **scrnCnt** | 해당일자에 상영한 스크린수를 출력합니다. |
| **showCnt** | 해당일자에 상영된 횟수를 출력합니다. |

---

## 4. 요청 예시 (Sample Request)

```http
GET http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=YOUR_API_KEY&targetDt=20260514

```

---

# [API 명세서] 공통코드 조회 서비스

특정 코드값을 조건으로 그에 해당하는 하위 코드 정보(지역 코드, 영화 형식 등)를 조회합니다.

## 1. 기본 정보

* **요청 URL:** `http://www.kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.json`
* **HTTP Method:** `GET`
* **응답 형식:** `JSON` (또는 XML)

---

## 2. 요청 인터페이스 (Request Parameters)

| 요청 변수 | 타입 | 필수여부 | 설명 |
| --- | --- | --- | --- |
| **key** | 문자열 | **필수** | 발급받은 API 키 값을 입력합니다. |
| **comCode** | 문자열 | **필수** | 조회하고자 하는 상위 코드를 입력합니다. (예: 지역코드 `0105000000`) |

---

## 3. 응답 구조 (Response Fields)

| 응답 필드 | 타입 | 설명 |
| --- | --- | --- |
| **fullCd** | 문자열 | 해당 코드의 전체 코드를 출력합니다. |
| **korNm** | 문자열 | 해당 코드의 국문명을 출력합니다. |
| **engNm** | 문자열 | 해당 코드의 영문명을 출력합니다. |

---

## 4. 활용 예시

### 4.1. 요청 예시 (REST/JSON)

```http
GET http://www.kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.json?key=YOUR_API_KEY&comCode=0105000000

```

### 4.2. 주요 상위 코드 (comCode)

* **0105000000:** 지역 코드 (서울, 부산, 경기 등 전국 지역 구분)
* **0104000000:** 영화 성격 코드 (다양성영화, 상업영화 등)
* **0102000000:** 영화 유형 코드 (장편, 단편, 옴니버스 등)

---


# [API 명세서] 영화목록 조회 서비스

영화명, 감독명, 제작연도, 개봉연도 등 다양한 조건을 통해 통합전산망에 등록된 영화 리스트를 조회합니다.

## 1. 기본 정보

* **요청 URL:** `http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json`
* **HTTP Method:** `GET`
* **응답 형식:** `JSON` (또는 XML)

---

## 2. 요청 인터페이스 (Request Parameters)

| 변수명 | 타입 | 필수여부 | 설명 |
| --- | --- | --- | --- |
| **key** | 문자열 | **필수** | 발급받은 API 키 값을 입력합니다. |
| **curPage** | 문자열 | 선택 | 현재 페이지를 지정합니다. (기본값: "1") |
| **itemPerPage** | 문자열 | 선택 | 결과 ROW 의 개수를 지정합니다. (기본값: "10") |
| **movieNm** | 문자열 | 선택 | 영화명으로 조회합니다. (UTF-8 인코딩) |
| **directorNm** | 문자열 | 선택 | 감독명으로 조회합니다. (UTF-8 인코딩) |
| **openStartDt** | 문자열 | 선택 | YYYY 형식의 조회 시작 개봉연도를 입력합니다. |
| **openEndDt** | 문자열 | 선택 | YYYY 형식의 조회 종료 개봉연도를 입력합니다. |
| **prdtStartYear** | 문자열 | 선택 | YYYY 형식의 조회 시작 제작연도를 입력합니다. |
| **prdtEndYear** | 문자열 | 선택 | YYYY 형식의 조회 종료 제작연도를 입력합니다. |
| **repNationCd** | 문자열 | 선택 | 국적코드로 조회합니다. (공통코드 "2204" 참조) |
| **movieTypeCd** | 문자열 | 선택 | 영화유형코드로 조회합니다. (공통코드 "2201" 참조) |

---

## 3. 응답 구조 (Response Fields)

| 필드명 | 설명 |
| --- | --- |
| **movieCd** | 영화코드를 출력합니다. |
| **movieNm** | 영화명(국문)을 출력합니다. |
| **movieNmEn** | 영화명(영문)을 출력합니다. |
| **prdtYear** | 제작연도를 출력합니다. |
| **openDt** | 개봉일을 출력합니다. |
| **typeNm** | 영화유형을 출력합니다. |
| **prdtStatNm** | 제작상태를 출력합니다. |
| **nationAlt** | 제작국가(전체)를 출력합니다. |
| **genreAlt** | 영화장르(전체)를 출력합니다. |
| **repNationNm** | 대표 제작국가명을 출력합니다. |
| **repGenreNm** | 대표 장르명을 출력합니다. |
| **directors** | 영화감독 정보 (배열) |
| **peopleNm** | 영화감독명을 출력합니다. |
| **companys** | 제작사 정보 (배열) |
| **companyCd** | 제작사 코드를 출력합니다. |
| **companyNm** | 제작사명을 출력합니다. |

---

## 4. 요청 예시 (Sample Request)

```http
GET http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=YOUR_API_KEY&movieNm=기생충

```

---

# [API 명세서] 영화 상세정보 조회 서비스

특정 영화의 고유 코드(`movieCd`)를 사용하여 해당 영화의 상세한 메타데이터(감독, 배우, 장르, 상영형태, 심의정보 등)를 조회합니다.

## 1. 기본 정보

* **요청 URL:** `http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json`
* **HTTP Method:** `GET`
* **응답 형식:** `JSON` (또는 XML)

---

## 2. 요청 인터페이스 (Request Parameters)

| 변수명 | 타입 | 필수여부 | 설명 |
| --- | --- | --- | --- |
| **key** | 문자열 | **필수** | 발급받은 API 키 값을 입력합니다. |
| **movieCd** | 문자열 | **필수** | 조회를 원하는 영화의 고유 코드를 입력합니다. |

---

## 3. 응답 구조 (주요 필드)

| 필드명 | 설명 | 비고 |
| --- | --- | --- |
| **movieCd** | 영화코드 |  |
| **movieNm** | 영화명(국문) |  |
| **movieNmEn** | 영화명(영문) |  |
| **showTm** | 상영시간 | 분 단위 |
| **openDt** | 개봉연도 | `YYYYMMDD` 형식 |
| **typeNm** | 영화유형명 | 장편, 단편 등 |
| **nations** | 제작국가 | 하위 `nationNm` 포함 |
| **genres** | 장르 | 하위 `genreNm` 포함 |
| **directors** | 감독 | 하위 `peopleNm`, `peopleNmEn` 포함 |
| **actors** | 배우 | 하위 `peopleNm`, `cast` (배역명) 포함 |
| **showTypes** | 상영형태 | 2D, 3D, IMAX 등 |
| **audits** | 심의정보 | `watchGradeNm` (관람등급) 포함 |
| **companys** | 참여 영화사 | 제작사, 배급사 등 구분 |

---

## 4. 요청 예시 (Sample Request)

```http
GET http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key=YOUR_API_KEY&movieCd=20124079

```

---

# [API 명세서] 영화사 목록 조회 서비스

영화진흥위원회 통합전산망에 등록된 영화사 정보를 영화사명, 대표자명 등의 조건으로 조회합니다.

## 1. 기본 정보

* **요청 URL:** `http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.json`
* **HTTP Method:** `GET`
* **응답 형식:** `JSON` (또는 XML)

---

## 2. 요청 인터페이스 (Request Parameters)

| 요청 변수 | 타입 | 필수여부 | 설명 |
| --- | --- | --- | --- |
| **key** | 문자열 | **필수** | 발급받은 API 키 값을 입력합니다. |
| **curPage** | 문자열 | 선택 | 현재 페이지를 지정합니다. (기본값: "1") |
| **itemPerPage** | 문자열 | 선택 | 결과 ROW의 개수를 지정합니다. (기본값: "10") |
| **companyNm** | 문자열 | 선택 | 영화사명으로 조회합니다. |
| **ceoNm** | 문자열 | 선택 | 대표자명으로 조회합니다. |
| **companyPartCd** | 문자열 | 선택 | 영화사 분류코드로 조회합니다. (공통코드 "2601" 참조) |

---

## 3. 응답 구조 (Response Fields)

| 응답 필드 | 설명 |
| --- | --- |
| **companyCd** | 영화사 코드를 출력합니다. |
| **companyNm** | 영화사명을 출력합니다. |
| **companyNmEn** | 영화사명(영문)을 출력합니다. |
| **companyPartNames** | 영화사 분류(제작사, 배급사 등)를 출력합니다. |
| **ceoNm** | 대표자명을 출력합니다. |
| **filmoNames** | 해당 영화사의 주요 필모그래피 리스트를 출력합니다. |

---

## 4. 요청 예시 (Sample Request)

```http
GET http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.json?key=YOUR_API_KEY&companyNm=CJ

```

---

# [API 명세서] 영화사 상세정보 조회 서비스

특정 영화사의 고유 코드(`companyCd`)를 사용하여 해당 영화사의 상세 정보(대표자명, 영화사 분류, 참여 영화 필모그래피 등)를 조회합니다.

## 1. 기본 정보

* **요청 URL:** `http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyInfo.json`
* **HTTP Method:** `GET`
* **응답 형식:** `JSON` (또는 XML)

---

## 2. 요청 인터페이스 (Request Parameters)

| 요청 변수 | 타입 | 필수여부 | 설명 |
| --- | --- | --- | --- |
| **key** | 문자열 | **필수** | 발급받은 API 키 값을 입력합니다. |
| **companyCd** | 문자열 | **필수** | 조회를 원하는 영화사의 고유 코드를 입력합니다. |

---

## 3. 응답 구조 (Response Fields)

| 응답 필드 | 설명 | 비고 |
| --- | --- | --- |
| **companyCd** | 영화사 코드 |  |
| **companyNm** | 영화사명(국문) |  |
| **companyNmEn** | 영화사명(영문) |  |
| **ceoNm** | 대표자명 |  |
| **parts** | 영화사 분류 정보 | 하위 `companyPartNm` 포함 |
| **filmos** | 참여 영화 필모그래피 | 하위 `movieCd`, `movieNm`, `companyPartNm` 포함 |

---

## 4. 요청 예시 (Sample Request)

```http
GET http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyInfo.json?key=YOUR_API_KEY&companyCd=20122497

```

---

# [API 명세서] 영화인목록 조회 서비스

영화진흥위원회 통합전산망에 등록된 영화인 정보를 영화인명, 필모그래피 등의 조건을 통해 조회합니다.

## 1. 기본 정보

* **요청 URL:** `http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json`
* **HTTP Method:** `GET`
* **응답 형식:** `JSON` (또는 XML)

---

## 2. 요청 인터페이스 (Request Parameters)

| 요청 변수 | 타입 | 필수여부 | 설명 |
| --- | --- | --- | --- |
| **key** | 문자열 | **필수** | 발급받은 API 키 값을 입력합니다. |
| **curPage** | 문자열 | 선택 | 현재 페이지를 지정합니다. (기본값: "1") |
| **itemPerPage** | 문자열 | 선택 | 결과 ROW의 개수를 지정합니다. (기본값: "10") |
| **peopleNm** | 문자열 | 선택 | 영화인명으로 조회합니다. |
| **filmoNames** | 문자열 | 선택 | 영화인의 필모리스트(작품명)로 조회합니다. |

---

## 3. 응답 구조 (Response Fields)

| 응답 필드 | 설명 |
| --- | --- |
| **peopleCd** | 영화인 코드를 출력합니다. |
| **peopleNm** | 영화인명을 출력합니다. |
| **peopleNmEn** | 영화인명(영문)을 출력합니다. |
| **repRoleNm** | 영화인의 주 활동 분야(감독, 배우 등)를 출력합니다. |
| **filmoNames** | 해당 영화인의 필모리스트를 출력합니다. |

---

## 4. 요청 예시 (Sample Request)

```http
GET http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=YOUR_API_KEY&peopleNm=봉준호

```

---

# [API 명세서] 영화인 상세정보 조회 서비스

영화진흥위원회 통합전산망에 등록된 특정 영화인의 상세 정보(성별, 활동 분야, 참여 작품 필모그래피 등)를 영화인 코드(`peopleCd`)를 통해 조회합니다.

## 1. 기본 정보

* **요청 URL:** `http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json`
* **HTTP Method:** `GET`
* **응답 형식:** `JSON` (또는 XML)

---

## 2. 요청 인터페이스 (Request Parameters)

| 요청 변수 | 타입 | 필수여부 | 설명 |
| --- | --- | --- | --- |
| **key** | 문자열 | **필수** | 발급받은 API 키 값을 입력합니다. |
| **peopleCd** | 문자열 | **필수** | 조회를 원하는 영화인의 고유 코드를 입력합니다. |

---

## 3. 응답 구조 (Response Fields)

| 응답 필드 | 설명 | 비고 |
| --- | --- | --- |
| **peopleCd** | 영화인 코드 |  |
| **peopleNm** | 영화인명(국문) |  |
| **peopleNmEn** | 영화인명(영문) |  |
| **sex** | 성별 |  |
| **repRoleNm** | 영화인 분류명 | 감독, 배우 등 대표 역할 |
| **filmos** | 참여 영화 필모그래피 | 하위 리스트 포함 |
| **movieCd** | 참여 영화 코드 |  |
| **movieNm** | 참여 영화명 |  |
| **moviePartNm** | 참여 분야 | 해당 영화에서의 역할 |
| **homepages** | 관련 URL | 공식 홈페이지 등 |

---

## 4. 요청 예시 (Sample Request)

```http
GET http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json?key=YOUR_API_KEY&peopleCd=20164556

```

---
