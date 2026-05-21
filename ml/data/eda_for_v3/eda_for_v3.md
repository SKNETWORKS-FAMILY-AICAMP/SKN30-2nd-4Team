# v3 15개 피처 회귀 실험 결과 정리

## 목적

`feature_table_v3.csv`를 기준으로 다중공선성 및 누수 가능성이 있는 피처를 제외하고, 상관관계와 도메인 판단을 반영한 15개 피처만 사용해 회귀 모델 성능을 확인했다.

이번 실험의 핵심 확인 항목은 다음과 같다.

- `log_audience` 예측을 위한 15개 고정 피처 구성
- 15개 피처와 `log_audience` 간 상관관계 확인
- Linear Regression, Ridge, Lasso, RandomForest 회귀 성능 비교
- RandomForest 최적 파라미터 적용 후 성능 확인

## 실험 설정

[데이터 개요]

- 사용 버전: `feature_table_v3.csv`
- 전체 샘플: 2,489편
- 전체 컬럼 수: 44개
- 결측치: 없음
- 피처 수: 15개
- 수치형 피처: 15개
- 범주형 피처: 0개
- 회귀 train/test: 1,991 / 498
- 분할 방식: `open_year` 컬럼이 없어 random split 사용

## 사용 피처

이번 회귀 실험에서 사용한 15개 피처는 다음과 같다.

| No. | Feature |
|---:|---|
| 1 | `relative_search_share` |
| 2 | `distributor_avg_audi` |
| 3 | `trend_pre7_avg` |
| 4 | `trend_pre7_max` |
| 5 | `is_new_director` |
| 6 | `genre_avg_audi` |
| 7 | `is_new_lead` |
| 8 | `is_new_producer` |
| 9 | `runtime` |
| 10 | `market_avg_audi_7d` |
| 11 | `is_covid_period` |
| 12 | `director_avg_audi` |
| 13 | `producer_avg_audi` |
| 14 | `holiday_nearby_count` |
| 15 | `same_week_releases` |

## 생성 이미지

| 구분 | Image |
|---|---|
| 타겟 분포 | `ml/images/eda_v3/13회차/01_target_distribution_v3.png` |
| Star/Brand Power 분포 | `ml/images/eda_v3/13회차/05_star_brand_power_dist_v3.png` |
| 상관관계 히트맵 | `ml/images/eda_v3/13회차/06_correlation_heatmap_v3.png` |
| 회귀 실제 vs 예측 | `ml/images/eda_v3/13회차/07_regression_scatter_v3.png` |
| RandomForest 피처 중요도 | `ml/images/eda_v3/13회차/08_rf_feature_importance_reg_v3.png` |
| 회귀 모델 비교 | `ml/images/eda_v3/13회차/10_regression_model_comparison_v3.png` |

### Target Distribution

![target distribution](../../images/eda_v3/13회차/01_target_distribution_v3.png)

### Feature Correlation Heatmap

![correlation heatmap](../../images/eda_v3/13회차/06_correlation_heatmap_v3.png)

### Regression Scatter

![regression scatter](../../images/eda_v3/13회차/07_regression_scatter_v3.png)

### RandomForest Feature Importance

![rf feature importance](../../images/eda_v3/13회차/08_rf_feature_importance_reg_v3.png)

### Model Comparison

![model comparison](../../images/eda_v3/13회차/10_regression_model_comparison_v3.png)

## 상관관계 TOP 5

상관계수는 `log_audience`와 각 피처 간 Pearson correlation의 절대값 기준으로 확인했다.

| Rank | Feature | Abs. Correlation |
|---:|---|---:|
| 1 | `relative_search_share` | 0.5378 |
| 2 | `distributor_avg_audi` | 0.4789 |
| 3 | `trend_pre7_avg` | 0.4689 |
| 4 | `trend_pre7_max` | 0.3496 |
| 5 | `is_new_director` | 0.3139 |

## 회귀 결과

[회귀 결과 - 타겟: `log_audience`]

| Model | R² | RMSE(log) | MAE(실제 관객수, 만명) |
|---|---:|---:|---:|
| RandomForest | 0.6645 | 1.2710 | 37.6 |
| Linear Regression | 0.5876 | 1.4092 | 44.7 |
| Lasso | 0.5874 | 1.4095 | 44.7 |
| Ridge | 0.5873 | 1.4098 | 44.8 |

RandomForest가 가장 높은 R²와 가장 낮은 RMSE(log), MAE를 기록했다.

## 최적 모델과 파라미터

***최적의 모델과 파라미터 산출***

모델명: `RandomForest`

파라미터:

```python
{
    "model__n_estimators": 500,
    "model__max_depth": 16,
    "model__min_samples_split": 5,
    "model__min_samples_leaf": 2,
    "model__max_features": 0.8,
    "model__bootstrap": True,
}
```

## 주요 EDA 인사이트

- 평균 관객수 1위 장르: 사극
- 한국 영화 평균 관객수: 84.2만명
- 외국 영화 평균 관객수: 41.7만명
- `log_audience`와 가장 상관 높은 피처: `relative_search_share`
- 검색 점유율, 배급사 과거 평균 관객수, 개봉 전 7일 트렌드 지표가 관객수 예측에 강하게 작용했다.
- `is_new_director`, `is_new_lead`, `is_new_producer`는 음의 상관관계를 보이며, 신인 여부가 흥행 안정성과 관련될 수 있음을 시사한다.

## 요약

v3 15개 피처 실험에서는 `total_sales`, `trend_pre30_avg`, `lead_actor_movie_count` 등 누수 또는 다중공선성 우려가 있는 피처를 제외하고 회귀 성능을 확인했다.

15개 피처만 사용했음에도 RandomForest는 R² 0.6645, 실제 관객수 기준 MAE 37.6만명을 기록했다. 선형 계열 모델은 R² 약 0.59 수준으로 비슷하게 나타났고, 비선형 관계를 포착하는 RandomForest가 가장 안정적인 성능을 보였다.

핵심 피처는 다음과 같이 정리된다.

- `relative_search_share`
- `distributor_avg_audi`
- `trend_pre7_avg`
- `trend_pre7_max`
- `genre_avg_audi`
- `director_avg_audi`

현재 v3 15개 피처 구성은 과도한 타겟 누수를 줄이면서도 기본 회귀 성능을 확보한 기준선으로 볼 수 있다. 이후에는 시간 기준 분할(`open_date` 기반 연도 분할), 교차검증 확대, Boosting 계열 모델 비교를 통해 일반화 성능을 추가 검증할 필요가 있다.
