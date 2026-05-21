# v2피처 테이블 설계서

이 문서는 `v1` 베이스라인 피처의 상관관계 분석을 통해 **불필요한 피처를 제거**하고, **기존 피처를 보강(로그 변환, 결측 보정)**하며, **네이버 검색 트렌드 피처를 추가**하여 개봉 예정작 흥행 예측력을 높이기 위한 설계서입니다.

---

## 📅 v2 피처 테이블 구조 요약

> ⚠️ **데이터 누수 방지 원칙**:
>  **개봉 이후** 수집 데이터는 완전히 제외합니다.

```
feature_table_v2.csv
─────────────────────────────────────────────────────────────────────────────
[식별]   movie_id, title
[타겟]   total_audience, log_audience, hit_class

[메타]   genre, rating_encoded, is_korean, runtime
[시간]   open_month, open_day_of_week, is_summer, is_winter,
         is_holiday_release, holiday_nearby_count
[스타]   director_avg_audi, director_movie_count,
         lead_actor_avg_audi, lead_actor_movie_count, cast_max_star_power
[브랜드] distributor_avg_audi, distributor_movie_count,
         producer_avg_audi, producer_movie_count
[경쟁]   same_week_releases, market_avg_audi_7d
[트렌드] trend_pre7_avg, trend_pre7_max, trend_growth_rate,
         relative_search_share
─────────────────────────────────────────────────────────────────────────────
총 31개 컬럼 (식별자 2개, 타겟 3개, 원본 피처 26개)
→ 전처리 후: 삭제 7개 + 신규 4개(is_new_*) = 최종 피처 23개
```

---

## 1. v1 대비 변경 요약

### 삭제 피처 (7개)

| 삭제 피처 | 삭제 근거 |
|:---|:---|
| `open_month` | 상관계수 $+0.007$. 1~12 숫자에 크기 의미 없음. `is_summer`/`is_winter`로 충분히 대체됨 |
| `cast_max_star_power` | `lead_actor_avg_audi`와 상관계수 $0.85$ 이상. 다중공선성 원흉 |
| `director_movie_count` | 상관계수 $+0.098$. 단순 다작 여부로, `director_avg_audi`에 이미 흥행력 반영됨 |
| `lead_actor_movie_count` | 상관계수 $+0.087$. 위와 동일 사유 |
| `distributor_movie_count` | 상관계수 $+0.079$. `distributor_avg_audi`로 충분 |
| `producer_movie_count` | 상관계수 $+0.068$. `producer_avg_audi`로 충분 |
| `rating_encoded` (순서형) | 상관계수 $+0.007$. 순서형 인코딩은 의미 없음. **원-핫 인코딩으로 변환** |

### 신규 피처 (4개) — 기존 피처 보강

| 신규 피처 | 산출 방법 | 의미 |
|:---|:---|:---|
| `is_new_director` | `director_avg_audi == 0` → 1 | 신인 감독 여부 |
| `is_new_lead` | `lead_actor_avg_audi == 0` → 1 | 신인 주연배우 여부 |
| `is_new_distributor` | `distributor_avg_audi == 0` → 1 | 신생 배급사 여부 |
| `is_new_producer` | `producer_avg_audi == 0` → 1 | 신생 제작사 여부 |

---

## 2. 기존 피처 보강: 로그 변환 & 결측 보정

### 2-1. 신인/영세 결측 보정 (Imputation)

과거 실적이 없는 신인의 `avg_audi`가 `0`이면, 모델이 "흥행 실패"와 "데이터 없음"을 구분하지 못합니다.

**보정 방법**: 해당 컬럼에서 0이 아닌 값들의 **중위값(Non-zero Median)**으로 대체합니다.

| 대상 컬럼 | 보정 전 | 보정 후 |
|:---|:---|:---|
| `director_avg_audi` | 0 (신인) | Non-zero Median |
| `lead_actor_avg_audi` | 0 (신인) | Non-zero Median |
| `distributor_avg_audi` | 0 (영세) | Non-zero Median |
| `producer_avg_audi` | 0 (영세) | Non-zero Median |

### 2-2. 로그(`log1p`) 변환

타겟 변수처럼 극단적인 롱테일 분포를 갖는 수치형 피처에 `np.log1p`를 적용하여, 트리 모델의 분기 안정성을 확보합니다.

| 변환 피처 | 변환 사유 |
|:---|:---|
| `director_avg_audi` | 0명 ~ 1,000만 명까지 극단적 스케일 |
| `lead_actor_avg_audi` | 배우별 관객수 분포 우측 치우침 |
| `distributor_avg_audi` | 대형 배급사 vs 인디 배급사 격차 |
| `producer_avg_audi` | 제작사 규모 격차 |
| `market_avg_audi_7d` | 성수기/비수기 시장 규모 격차 |

### 2-3. 장르 흥행력 기반 그룹화 (Genre Box-Office Power Binning)

단순한 빈도 기준(`value_counts < 1%`) 병합은 작품 수가 적지만 개봉 시 파괴력이 큰 장르(예: SF, 어드벤처)와 저예산 위주의 마니아 장르(예: 다큐멘터리, 공연)를 구별하지 못하는 정보 손실이 발생합니다.

**보정 방법**: 각 영화 개봉 시점 기준으로 **"개봉 전 해당 장르의 과거 평균 관객수"**를 계산하여 장르의 체급을 등급화(Tier)하거나, 아예 수치형 피처로 **타겟 인코딩(Target Encoding)**을 적용합니다.

*   **고흥행 등급 (High-tier)**: 과거 평균 100만 명 이상 (예: SF, 액션, 범죄)
*   **중흥행 등급 (Mid-tier)**: 과거 평균 20만 ~ 100만 명 (예: 드라마, 코미디, 스릴러)
*   **저흥행 등급 (Low-tier)**: 과거 평균 20만 명 미만 및 미개척 장르 (예: 공연, 다큐멘터리, 서부극, 기타)

이렇게 분류한 뒤 원-핫 인코딩을 적용하면 차원의 저주를 방지하면서도 장르 고유의 흥행 포텐셜 정보를 완벽하게 보존할 수 있습니다.

### 2-4. 범주형 인코딩 교정

| 피처 | 기존 (v1) | 변경 (v2) |
|:---|:---|:---|
| `genre` | `LabelEncoder` (인위적 크기 부여) | **`genre_avg_audi` 수치형 타겟 인코딩 적용** (원-핫 불필요) |
| `rating_encoded` | 순서형 정수 (전체=0, 12세=1, …) | `pd.get_dummies` (원-핫) |

---

## 3. 신규 피처: 네이버 검색 트렌드 (4개)

### 3-1. 피처 명세

개봉 **전**에 수집 가능한 네이버 검색 트렌드 데이터를 활용하여, 대중의 실시간 관심도를 정량화합니다.

| 피처 | 산출 방법 | 의미 |
|:---|:---|:---|
| `trend_pre7_avg` | 개봉일 D-7 ~ D-1의 `search_index` 평균 | 개봉 직전 1주간 대중 관심도 |
| `trend_pre7_max` | 개봉일 D-7 ~ D-1의 `search_index` 최댓값 | 직전 1주 피크 화제성 |
| `trend_growth_rate` | `pre7_avg / pre30_avg` | 관심도 상승 추세 (1 초과 = 상승, 1 미만 = 하락) |
| `relative_search_share` | `pre30_avg / (경쟁 Top5 pre30_avg 합)` | 동시기 경쟁작 대비 검색 우위 |

### 3-2. 산출 로직 (의사 코드)

```python
# 1. 개봉일 이전 데이터만 필터
pre_data = trend[trend['trend_date'] < open_date]

# 2. D-7 ~ D-1 구간 통계
pre7  = pre_data[trend_date >= open_date - 7일]
pre7_avg = pre7['search_index'].mean()
pre7_max = pre7['search_index'].max()

# 3. D-30 ~ D-1 구간 통계
pre30 = pre_data[trend_date >= open_date - 30일]
pre30_avg = pre30['search_index'].mean()

# 4. 성장률
trend_growth_rate = pre7_avg / pre30_avg  (pre30_avg > 0일 때)

# 5. 경쟁 대비 상대적 검색 점유율
경쟁작 = 개봉일 D-30 ~ D-1 사이에 개봉한 다른 영화들
각 경쟁작의 pre30_avg 중 Top 5의 합 = top5_sum
relative_search_share = pre30_avg / top5_sum
```

### 3-3. 학습 데이터 범위 결정

네이버 검색 트렌드 수집 범위(2016년~)와 학습 데이터 범위를 일치시켜, 트렌드 피처의 효용을 극대화합니다.

| 구간 | 영화 수 | 트렌드 보유율 | 역할 |
|:---|---:|---:|:---|
| **2010~2015** | 약 1,305편 | 0% | **히스토리 전용** — Star/Brand Power 산출의 과거 실적 기반으로만 활용 |
| **2016~2025** | **2,454편** | **98.6%** (2,420/2,454) | **학습 대상** — 모든 피처가 유효한 학습·평가 데이터셋 |

> 💡 2010~2015 영화는 학습 샘플에서 제외하되, 감독/배우/배급사의 **과거 흥행 실적 계산에는 그대로 반영**됩니다.
> 예: 2016년 개봉작의 `director_avg_audi`를 산출할 때 해당 감독의 2010~2015 작품 관객수가 포함됩니다.

### 3-4. 검증 결과 (2016년 이후 기준)

2016년 이후 개봉작 **2,454편**에 대한 트렌드 피처 통계 및 `log_audience`와의 상관계수입니다.

**`log_audience`와의 상관계수**:

| 피처 | 상관계수 (2016~) | 전체(3,869편) 대비 변화 | 해석 |
|:---|---:|:---|:---|
| `trend_pre7_max` | **+0.4157** | $+0.22 → +0.42$ | ✅ 직전 1주 피크 화제성. 가장 강력한 트렌드 피처 |
| `trend_pre7_avg` | **+0.4126** | $+0.23 → +0.41$ | ✅ 직전 1주 평균 관심도. 거의 동급의 예측력 |
| `relative_search_share` | **+0.3435** | $+0.19 → +0.34$ | ✅ 경쟁작 대비 검색 우위. 대폭 상승 |
| `trend_growth_rate` | **+0.0467** | $-0.17 → +0.05$ | ⚠️ 음의 상관 해소됨. 약한 양의 상관으로 전환 |

> **핵심 발견**: 2010~2015 데이터를 학습에서 제외하자, 트렌드 피처 3개(`pre7_avg`, `pre7_max`, `search_share`)의 상관계수가 **$+0.20$ → $+0.34 \sim +0.42$로 2배 가까이 급등**했습니다. 이는 트렌드 미보유 영화(2015 이전 대작)가 상관관계를 심하게 희석시키고 있었음을 증명합니다.

### 3-5. 트렌드 피처 주의사항

1. **`trend_growth_rate`의 약한 상관 ($+0.05$)**:
   2016+ 기준으로 음의 상관은 해소되었으나, 여전히 상관계수가 $+0.05$로 매우 낮습니다. `trend_growth_rate = pre7_avg / pre30_avg`이므로, 개봉 30일 전부터 검색량이 높았던 대작은 직전 7일에 성장 여지가 적어 성장률이 낮고, 소규모 영화는 직전에만 살짝 검색되어 성장률이 높게 나오는 구조적 특성 때문입니다. 모델 학습에는 포함하되, 단독 예측 변수로서의 기대치는 낮게 설정합니다.

---

## 4. 전처리 파이프라인 구현 코드

```python
# ── [0] 학습 범위 필터: 2016년 이후만 학습 대상 ──
df['open_date'] = pd.to_datetime(df['open_date'], errors='coerce')
df['open_year'] = df['open_date'].dt.year
df_train = df[df['open_year'] >= 2016].reset_index(drop=True)

# ── 피처/타겟 분리 ──
target_col = "log_audience" if TARGET_TYPE == "regression" else "hit_class"
y = df_train[target_col].copy()
exclude_cols = ["movie_id", "title", "total_audience", "log_audience",
                "hit_class", "open_date", "open_year"]
feature_cols = [c for c in df_train.columns if c not in exclude_cols]
X = df_train[feature_cols].copy()

# ── [1] 불필요 피처 삭제 ──
drop_cols = ['open_month', 'cast_max_star_power',
             'director_movie_count', 'lead_actor_movie_count',
             'distributor_movie_count', 'producer_movie_count']
X = X.drop(columns=[c for c in drop_cols if c in X.columns])

# ── [2] 장르 흥행력 기반 타겟 인코딩 (누수 없는 개봉 전 과거 기준) ──
# 각 영화 개봉일 이전의 동일 장르 과거 평균 관객수 산출
genre_past_means = []
# 전체 셋에서 순회하며 개봉 전 데이터로만 산출하여 타겟 누수 방지
for idx, row in df_train.iterrows():
    past_same_genre = df_train[
        (df_train['genre'] == row['genre']) & 
        (df_train['open_date'] < row['open_date'])
    ]
    if not past_same_genre.empty:
        # 과거 평균 관객수를 로그 스케일로 기록
        genre_past_means.append(np.log1p(past_same_genre['total_audience'].mean()))
    else:
        # 과거 기록이 없는 신생/미개척 장르는 전체 Non-zero 중위값 부여
        genre_past_means.append(np.log1p(df_train.loc[df_train['total_audience'] > 0, 'total_audience'].median()))

X['genre_avg_audi'] = genre_past_means
X = X.drop(columns=['genre']) # 기존 카테고리형 genre 컬럼 제거 (원핫 인코딩 불필요)

# ── [3] 신인 지시자 생성 및 Non-zero 중위값 대체 ──
impute_cols = ['director_avg_audi', 'lead_actor_avg_audi',
               'producer_avg_audi', 'distributor_avg_audi']
for col in impute_cols:
    non_zero_median = X.loc[X[col] > 0, col].median()
    if pd.isna(non_zero_median):
        non_zero_median = 10000.0
    prefix = col.split('_')[0]
    X[f'is_new_{prefix}'] = (X[col] == 0).astype(int)
    X.loc[X[col] == 0, col] = non_zero_median

# ── [4] 수치 피처 로그 변환 ──
log_cols = ['director_avg_audi', 'lead_actor_avg_audi',
            'distributor_avg_audi', 'producer_avg_audi',
            'market_avg_audi_7d']
for col in log_cols:
    if col in X.columns:
        X[col] = np.log1p(X[col])

# ── [5] 범주형 원-핫 인코딩 (genre는 이미 수치형 제거되어 rating만 원핫) ──
X = pd.get_dummies(X, columns=['rating_encoded'],
                   drop_first=True, dtype=int)
```
