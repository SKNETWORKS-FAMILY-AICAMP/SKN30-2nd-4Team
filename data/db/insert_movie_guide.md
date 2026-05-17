# 🎬 영화 상세 정보 수집 가이드 (최종 통합본)

이 문서는 영화 상세 정보를 수집하고 저장하기 위한 `insert_movie.ipynb` 구현 지침입니다.

---

## 1. 하이브리드 수집 전략
KOBIS API의 응답 특성에 따라 데이터별로 저장 방식을 다르게 가져갑니다.

### 👤 영화인 (People) - 지연 수집 전략
- **특징**: 영화 상세 API에서 고유 코드(`peopleCd`)를 주지 않음.
- **방식**: 수집 단계에서는 감독/배우 **이름만** 리스트로 묶어 `movies` 테이블의 `people` JSON 컬럼에 저장합니다.
- **구조**: `{"directors": ["봉준호"], "actors": ["송강호", "이선균"]}`

### 🏢 영화사 (Company) - 즉시 수집 전략
- **특징**: API에서 고유 코드(`companyCd`)를 제공함.
- **방식**: **제작사, 배급사, 제공** 파트에 해당하는 회사만 필터링하여 `companys` 및 `company_part` 테이블에 즉시 저장합니다.

---

## 2. 데이터 흐름 (Workflow)
1.  **대상 확인**: `daily_box_office`에는 존재하지만 `movies` 테이블에는 없는 `movie_id` 리스트를 추출합니다.
2.  **API 호출**: 각 `movie_id`에 대해 `searchMovieInfo.json`을 호출합니다.
3.  **데이터 가공**:
    - 기본 정보(장르, 런타임 등) 추출
    - 심의 목록(`audits`) 및 영화인 리스트(`people`)를 JSON 문자열로 변환
    - 특정 역할을 가진 영화사 데이터 필터링 및 리스트업
4.  **Bulk Insert**: 30~50일 단위로 모아서 테이블별 `Upsert` 쿼리 실행.

---

## 3. 구현 핵심 코드 가이드

### 🛠 파이썬 데이터 가공 예시
```python
import json

# 1. 영화인 정보 가공 (이름만 추출)
people_json = json.dumps({
    "directors": [d.peopleNm for d in movie_info.directors],
    "actors": [a.peopleNm for a in movie_info.actors]
})

# 2. 영화사 정보 필터링 및 가공
target_parts = ["제작사", "배급사", "제공"]
company_rows = []      # (company_id, company_name)
company_part_rows = [] # (company_id, movie_id, part_role)

for comp in movie_info.companys:
    if comp.companyPartNm in target_parts:
        company_rows.append((comp.companyCd, comp.companyNm))
        company_part_rows.append((comp.companyCd, movie_id, comp.companyPartNm))
```

### 💾 SQL 쿼리 가이드 (Upsert)
모든 저장은 `ON DUPLICATE KEY UPDATE`를 사용합니다.

```sql
-- 1. 영화 정보 저장
INSERT INTO movies (movie_id, title, genre, rating, nation, open_date, runtime, audits, people) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE genre=VALUES(genre), rating=VALUES(rating), runtime=VALUES(runtime), 
                        audits=VALUES(audits), people=VALUES(people);

-- 2. 영화사 기본 정보 저장
INSERT INTO companys (company_id, company_name) VALUES (%s, %s)
ON DUPLICATE KEY UPDATE company_name = VALUES(company_name);

-- 3. 영화-영화사 관계 저장
INSERT INTO company_part (company_id, movie_id, part_role) VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE part_role = VALUES(part_role);
```

---

## 4. 기대 효과 및 다음 단계
- **효율성**: 영화당 API를 단 1번만 호출하여 대부분의 핵심 데이터를 확보합니다.
- **확장성**: 이름 기반으로 저장된 영화인 정보는 추후 `insert_people.ipynb` 작업 시 영화인 검색 API를 통해 고유 ID로 정밀 매핑될 예정입니다.

**주의**: 대량 수집 시 반드시 **Checkpoint(중간 저장)** 로직을 구현하여 네트워크 오류 등에 대비하세요!
