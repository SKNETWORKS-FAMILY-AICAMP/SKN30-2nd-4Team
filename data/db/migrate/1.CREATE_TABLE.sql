DROP TABLE IF EXISTS movie_casting;
DROP TABLE IF EXISTS company_part;
DROP TABLE IF EXISTS daily_box_office;
DROP TABLE IF EXISTS daily_market_stats;
DROP TABLE IF EXISTS holidays;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS companys;

-- 1. 영화 정보 테이블
CREATE TABLE movies (
    movie_id      VARCHAR(20)  NOT NULL, -- KOBIS 영화코드
    title         VARCHAR(255) NOT NULL, -- 영화명
    genre         VARCHAR(50)  NOT NULL, -- 장르
    rating        VARCHAR(30)  NOT NULL, -- 관람등급
    nation        VARCHAR(50)  NOT NULL, -- 제작국가
    open_date     DATE         NOT NULL, -- 개봉일
    runtime       SMALLINT UNSIGNED NOT NULL, -- 상영시간(분)
    audits        JSON         NOT NULL, -- 심의 목록
    people        JSON         NOT NULL, -- 영화인 목록 {"actors": ["배우1", "배우2"], "directors": ["감독1"]} 형태로 저장
    PRIMARY KEY (movie_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 영화인 정보 테이블
CREATE TABLE people (
    person_id  VARCHAR(20)  NOT NULL, -- 영화인 코드
    name       VARCHAR(100) NOT NULL, -- 이름
    PRIMARY KEY (person_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 3. 영화-영화인 매핑 (출연/캐스팅)
CREATE TABLE movie_casting (
    person_id     VARCHAR(20)  NOT NULL,
    movie_id      VARCHAR(20)  NOT NULL,
    cast_role     VARCHAR(50)  NOT NULL, -- 감독, 주연, 조연 등
    PRIMARY KEY (person_id, movie_id),
    FOREIGN KEY (person_id) REFERENCES people(person_id),
    FOREIGN KEY (movie_id)  REFERENCES movies(movie_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 4. 영화사 정보 테이블
CREATE TABLE companys (
    company_id    VARCHAR(20)  NOT NULL, -- 회사 코드
    company_name  VARCHAR(100) NOT NULL, -- 회사명
    PRIMARY KEY (company_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 5. 영화-영화사 매핑 (참여 역할)
CREATE TABLE company_part (
    company_id  VARCHAR(20)  NOT NULL,
    movie_id    VARCHAR(20)  NOT NULL,
    part_role   VARCHAR(50)  NOT NULL, -- 배급, 수입 등
    PRIMARY KEY (company_id, movie_id),
    FOREIGN KEY (company_id) REFERENCES companys(company_id),
    FOREIGN KEY (movie_id)  REFERENCES movies(movie_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 6. 일별 박스오피스 테이블
CREATE TABLE daily_box_office (
    target_date     DATE          NOT NULL, -- 집계일자
    movie_id        VARCHAR(20)   NOT NULL, -- KOBIS 영화코드
    boxofficeType   VARCHAR(50)   NOT NULL, -- 박스오피스 종류
    showRange       VARCHAR(20)   NOT NULL, -- 박스오피스 조회 일자
    `rank`            TINYINT UNSIGNED NOT NULL, -- 순위 (1~255)
    rankInten       SMALLINT      NOT NULL, -- 전일대비 순위 증감분
    rankOldAndNew   CHAR(3)       NOT NULL, -- 신규진입여부
    salesAmt        BIGINT        NOT NULL DEFAULT 0, -- 해당일 매출액
    salesShare      DECIMAL(5,2)  NOT NULL DEFAULT 0, -- 매출 점유율
    salesInten      BIGINT        NOT NULL DEFAULT 0, -- 전일대비 매출 증감분
    salesChange     DECIMAL(15,2)  NOT NULL DEFAULT 0, -- 전일대비 매출 증감비율
    salesAcc        BIGINT        NOT NULL DEFAULT 0, -- 누적 매출액
    audiCnt         INT UNSIGNED  NOT NULL DEFAULT 0, -- 해당일 관객수
    audiInten       INT           NOT NULL DEFAULT 0, -- 전일대비 관객 증감분
    audiChange      DECIMAL(15,2)  NOT NULL DEFAULT 0, -- 전일대비 관객 증감비율
    audiAcc         INT UNSIGNED  NOT NULL DEFAULT 0, -- 누적 관객수
    scrnCnt         SMALLINT UNSIGNED NOT NULL DEFAULT 0, -- 해당일 상영 스크린 수
    showCnt         SMALLINT UNSIGNED NOT NULL DEFAULT 0, -- 해당일 상영 횟수
    PRIMARY KEY (target_date, movie_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 7. 시장 전체 통계 테이블
CREATE TABLE daily_market_stats (
    target_date  DATE          NOT NULL, -- 집계 일자
    total_audi   INT UNSIGNED  NOT NULL DEFAULT 0, -- 영화 전체 총 관객수
    total_show   INT UNSIGNED  NOT NULL DEFAULT 0, -- 영화 전체 총 상영횟수
    top1_share   DECIMAL(5,2)  NOT NULL DEFAULT 0, -- 1위 영화 점유율
    total_sales  BIGINT        NOT NULL DEFAULT 0, -- 영화 전체 총 매출
    total_scrn   SMALLINT UNSIGNED NOT NULL DEFAULT 0, -- 영화 전체 총 상영 스크린 수
    PRIMARY KEY (target_date)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



-- 8. 공휴일 정보 테이블
CREATE TABLE holidays (
    holiday_date DATE PRIMARY KEY,     -- 공휴일 날짜 (예: '2024-12-25')
    holiday_name VARCHAR(50) NOT NULL, -- 공휴일 명칭 (예: '크리스마스')
    holiday_type VARCHAR(20) DEFAULT 'National', -- 구분 (National: 법정공휴일, Special: 임시공휴일/샌드위치데이 등)
    is_weekend_effect BOOLEAN DEFAULT FALSE    -- 주말과 이어진 황금연휴 여부 (피처 가중치용)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;