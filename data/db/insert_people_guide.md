# 👥 영화인 정보 및 캐스팅 관계 구축 가이드

이 가이드는 데이터 수집의 마지막 단계인 `insert_people.ipynb`를 구현하기 위한 지침입니다. `movies.people` JSON 컬럼에 임시 저장된 이름들을 실제 고유 코드(`peopleCd`)로 변환하고 관계를 연결합니다.

---

## 1. 개요
영화 상세 정보 수집 단계에서 이름만 저장해두었던 감독과 배우들을 대상으로:
1.  **고유 코드 확보**: 영화인 목록 API를 통해 `peopleCd`를 찾습니다.
2.  **마스터 구축**: `people` 테이블에 영화인 정보를 저장합니다.
3.  **관계 연결**: `movie_casting` 테이블에 영화-영화인 관계를 저장합니다.

## 2. 데이터 흐름 (Workflow)
1.  **데이터 추출**: `movies` 테이블에서 `people` JSON 데이터를 가져옵니다.
2.  **중복 제거**: 여러 영화에 출연한 배우들의 중복을 제거하여 **(이름, 출연작)** 쌍의 고유 리스트를 만듭니다.
3.  **API 호출 (매핑)**: `searchPeopleList.json` API에 `peopleNm`과 `filmoNames`를 넣어 정확한 `peopleCd`를 확보합니다.
4.  **최종 저장**: 확보된 데이터를 `people` 및 `movie_casting` 테이블에 Bulk Insert 합니다.

---

## 3. 구현 핵심 포인트

### 🛠 고유 영화인 리스트 생성 예시
```python
# DB에서 JSON 데이터 가져오기
rows = db.fetch_all("SELECT movie_id, title, people FROM movies")

unique_people = {} # {(이름, 영화제목): movie_id}

for row in rows:
    staff = json.loads(row['people'])
    movie_title = row['title']
    
    for name in staff['directors'] + staff['actors']:
        unique_people[(name, movie_title)] = row['movie_id']
```

### 🔍 동명이인 방지 검색 로직
단순히 이름만으로 검색하면 동명이인 리스트가 반환됩니다. `filmoNames`를 함께 사용해야 정확한 사람을 찾을 수 있습니다.
```python
# API 호출 예시
# searchPeopleList.json?peopleNm=하정우&filmoNames=황해
```

### 💾 관계 테이블 저장 전략
하나의 영화인 코드를 찾을 때마다 두 개의 리스트에 데이터를 추가합니다.
```python
people_master = []    # (people_id, name)
casting_relation = [] # (people_id, movie_id, cast_role)

# ... API 응답 파싱 후 ...
people_master.append((people_cd, name))
casting_relation.append((people_cd, movie_id, role)) # role은 감독/배우 등
```

---

## 4. SQL 쿼리 가이드 (Upsert)

```sql
-- 1. 영화인 마스터 저장
INSERT INTO people (person_id, name) VALUES (%s, %s)
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- 2. 캐스팅 관계 저장
INSERT INTO movie_casting (person_id, movie_id, cast_role) VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE cast_role = VALUES(cast_role);
```

---

## 5. 구현 팁 (Optimization)
- **점진적 수집**: 이미 `people` 테이블에 존재하는 영화인은 API 호출을 건너뛰도록 `NOT IN` 또는 `LEFT JOIN` 쿼리를 활용하세요.
- **배치 처리**: 영화인 정보도 양이 많으므로 반드시 **30~50명 단위의 중간 저장(Checkpoint)** 로직을 구현해야 합니다.
- **API 효율성**: 한 번의 API 호출 결과로 여러 영화의 출연진 정보를 한꺼번에 매핑할 수 있다면 더욱 좋습니다. (예: `filmoNames` 검색 결과에 나온 다른 영화들도 체크)

## 6. 마무리
이 과정이 끝나면 모든 영화와 영화인, 영화사가 고유 ID 기반으로 촘촘하게 연결된 **고품질의 영화 분석 데이터베이스**가 완성됩니다!
