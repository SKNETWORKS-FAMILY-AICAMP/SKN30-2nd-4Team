## 프로젝트의 핵심 제약조건

 **"개봉 전 메타데이터만으로 예측"** → 해당 영화의 박스오피스 실적(audiCnt, salesAmt 등)은 피처로 사용 불가. 개봉일 이전에 알 수 있는 정보만 피처가 될 수 있음.

---

## v1 피처 테이블 구조 요약

```
feature_table_v1.csv 
─────────────────────────────────────
[식별]  movie_id, title
[타겟]  total_audience, log_audience, hit_class
[메타]  genre, rating_encoded, is_korean, runtime
[시간]  open_month, open_day_of_week, is_holiday_release, holiday_nearby_count, is_summer, is_winter
[스타]  director_avg_audi, director_movie_count, lead_actor_avg_audi, lead_actor_movie_count, cast_max_star_power
[브랜드] distributor_avg_audi, distributor_movie_count, producer_avg_audi, producer_movie_count
[경쟁]  same_week_releases, market_avg_audi_7d
─────────────────────────────────────
총 26개 컬럼 (식별자 2개, 타겟 3개, 피처 21개)
```


---

## 공통 피처 테이블 설계

**최종 형태**: 영화 1편 = 1행, 모든 피처가 컬럼으로 펼쳐진 flat table

```
movie_id | target | genre_액션 | genre_드라마 | ... | director_avg_audi |distributor_power | ...
20124079 | 10042  |    1      |     0       | ... |      856423       |      1234567      | ...
```

---

### 1. 타겟 변수 (from `daily_box_office`)

```sql
SELECT movie_id, MAX(audiAcc) AS total_audience
FROM daily_box_office
GROUP BY movie_id
```

| 컬럼 | 설명 | 용도 |
|------|------|------|
| `total_audience` | 최종 누적 관객수 | 회귀 타겟 원본 |
| `log_audience` | `log1p(total_audience)` | 회귀 타겟 (실제 학습용) |
| `hit_class` | 관객수 구간 (0~3) | 분류 타겟 |

<details>
  <summary>로그(log) 변환을 적용한 핵심 이유</summary>

### 1. 극단적인 비대칭 분포(Right-Skewed) 완화 <br>
영화 산업의 관객수 데이터는 소수의 '천만 영화'가 전체 파이를 독식하고 대다수의 영화는 관객수가 적은 전형적인 멱법칙(Power Law, 꼬리가 긴 비대칭) 분포를 따릅니다.
타겟 변수가 한쪽으로 심하게 치우쳐 있으면, 특히 선형 회귀(Linear, Ridge, Lasso) 기반 모델들은 가중치 업데이트가 매우 불안정해져 학습 성능이 크게 떨어집니다. 로그를 취하면 이 분포가 **정규 분포(종 모양)에 가깝게 변형**되어 모델의 예측 성능이 대폭 향상됩니다.

### 2. 이상치(Outlier)에 의한 모델 편향(Bias) 방지 <br>
머신러닝 회귀 모델은 예측 오차(예: MSE)를 줄이는 방향으로 학습합니다.
만약 로그를 씌우지 않으면, 관객수가 1,000만 명인 영화 1건을 맞추기 위해 발생하는 오차가 관객수 1만 명인 영화 100건을 맞출 때의 오차보다 훨씬 커지게 됩니다. 이로 인해 모델이 **오직 몇 개의 대작 영화 특성에만 과도하게 맞춰져(과적합) 평범한 영화들의 예측 정확도를 희생**하는 현상이 발생합니다. 로그 변환은 수치의 스케일을 압축하여 이런 스케일 왜곡을 방지합니다.

### 3. `np.log` 대신 `np.log1p`를 사용한 이유
어떤 이유로 관객수가 `0`명인 데이터가 존재할 경우, 일반적인 `np.log(0)`을 씌우면 값이 마이너스 무한대(`-inf`)가 되어 학습 코드가 중단(Error)됩니다.
`np.log1p(x)`는 `np.log(x + 1)`과 동일한 수식으로, 관객수가 0일 때 깔끔하게 `0`을 반환하도록 하여 계산 오버플로우를 방지하는 수학적 안전장치입니다.

---
> 💡 **모델 평가 시 팁**: 회귀 모델이 `log_audience`를 타겟으로 예측(예: `14.5`)한 결과를 최종 사용자나 보고서에 보여줄 때는, `np.expm1(예측값)`을 사용하여 원래 관객수 수치(예: 약 `1,980,000`명)로 복원(역변환)해서 보여주면 됩니다.
</details>

---

### 2. 영화 메타 피처 (from `movies`)

개봉 전에 확정되는 정보이므로 **모두 사용 가능**합니다.

| 피처 | 원본 컬럼 | 변환 방법 |
|------|----------|----------|
| `genre` | `genre` | 원본 문자열 사용 |
| `rating_encoded` | `rating` | 순서형 인코딩 (전체 < 12세 < 15세 < 청불) |
| `is_korean` | `nation` | 이진 (한국=1, 외국=0) |
| `runtime` | `runtime` | 그대로 사용 (분) |

---

### 3. 시간/계절 피처 (from `movies.open_date` + `holidays`)

| 피처 | 산출 방법 | 의미 |
|------|----------|------|
| `open_month` | 개봉일에서 추출 | 여름(7~8)·겨울(12~1) 성수기 효과 |
| `open_day_of_week` | 개봉일 요일 | 수요일 개봉 vs 목요일 개봉 |
| `is_holiday_release` | holidays 테이블 JOIN | 공휴일/연휴 개봉 여부 |
| `holiday_nearby_count` | 개봉일 ±7일 내 공휴일 수 | 개봉 첫 주 관객 동원 잠재력 |
| `is_summer` / `is_winter` | 월 기반 | 성수기 이진 변수 |

---

### 4. Star Power 피처 (from `people` + `movie_casting` + `daily_box_office`)

**핵심 원칙: 해당 영화 개봉일 이전의 과거 실적만 참조**

```python
# 의사코드: 감독 A의 star power (영화 X 기준)
감독A의_과거영화 = 감독A가_참여한_영화 WHERE 개봉일 < 영화X의_개봉일
감독A의_avg_audience = MEAN(과거영화들의 total_audience)
```

| 피처 | 산출 방법 | 의미 |
|------|----------|------|
| `director_avg_audi` | 감독의 과거 영화 평균 관객수 | 감독 흥행력 |
| `director_movie_count` | 감독의 과거 영화 편수 | 감독 경력 |
| `lead_actor_avg_audi` | 주연 배우의 과거 평균 관객수 | 배우 흥행력 |
| `lead_actor_movie_count` | 주연 배우의 과거 영화 편수 | 배우 경력 |
| `cast_max_star_power` | 출연진 중 최고 평균 관객수 | 캐스팅 파워 상한 |

> ⚠️ 신인 감독/배우(과거 데이터 없음)의 경우 → 0 또는 전체 중앙값으로 대체

---

### 5. Brand Power 피처 (from `companys` + `company_part` + `daily_box_office`)

| 피처 | 산출 방법 | 의미 |
|------|----------|------|
| `distributor_avg_audi` | 배급사의 과거 영화 평균 관객수 | 배급 역량 |
| `distributor_movie_count` | 배급사의 과거 영화 편수 | 배급 규모 |
| `producer_avg_audi` | 제작사의 과거 영화 평균 관객수 | 제작 역량 |
| `producer_movie_count` | 제작사의 과거 영화 편수 | 제작 규모 |

---

### 6. 경쟁 환경 피처 (from `daily_box_office` + `daily_market_stats`)

| 피처 | 산출 방법 | 의미 |
|------|----------|------|
| `same_week_releases` | 개봉일 ±3일 내 다른 신작 수 | 경쟁 강도 |
| `market_avg_audi_7d` | 개봉 직전 7일 시장 평균 관객수 | 시장 활성도 |

---
