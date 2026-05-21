## 1차 - 상관관계 및 중요도 기반 피처 제거 실험

[데이터 개요]
  - 사용 버전  : feature_table_v2.csv
  - 전체 샘플  : 2454편
  - 피처 수    : 19개 (수치형 18 + 범주형 1)
  - train/test : 1963 / 491

[회귀 결과 — 타겟: log_audience]
  - Linear Regression      R²=0.5739 / MAE(실제)=233.8만명
  - Ridge (alpha=1.0)      R²=0.5747 / MAE(실제)=230.5만명
  - Lasso (alpha=0.1)      R²=0.5169 / MAE(실제)=60.7만명
  - RandomForest           R²=0.7026 / MAE(실제)=41.2만명

[분류 결과 — 타겟: hit_class]
  - Logistic Regression    macro F1=0.4331
  - RandomForest           macro F1=0.3175

[주요 EDA 인사이트]
  - 평균 관객수 1위 장르: 사극
  - 한국 영화 평균 관객수: 85.4만명
  - 외국 영화 평균 관객수: 41.2만명
  - log_audience와 가장 상관 높은 피처: distributor_avg_audi
=======================================================

## 2차 - 클래스 재구성을 통한 분류 성능 개선 실험

============================================================
결과 요약: 01_eda_baseline_v2.ipynb
============================================================

[데이터 개요]
  - 사용 버전  : feature_table_v2.csv
  - 전체 샘플  : 2454편
  - 피처 수    : 19개 (수치형 18 + 범주형 1)
  - 회귀 train/test : 1963 / 491
  - 분류 train/test : 1963 / 491

[회귀 결과 — 타겟: log_audience]
  - Linear Regression      R²=0.5145 / MAE(실제)=50.0만명
  - Ridge (alpha=1.0)      R²=0.5150 / MAE(실제)=49.9만명
  - Lasso (alpha=0.1)      R²=0.4788 / MAE(실제)=47.2만명
  - RandomForest           R²=0.6628 / MAE(실제)=38.0만명

[분류 결과 — 타겟: hit_class]
  - Logistic Regression    macro F1=0.7707
  - RandomForest           macro F1=0.7568

[주요 EDA 인사이트]
  - 평균 관객수 1위 장르: 사극
  - 한국 영화 평균 관객수: 85.4만명
  - 외국 영화 평균 관객수: 41.2만명
  - log_audience와 가장 상관 높은 피처: distributor_avg_audi
============================================================

## 요약

1차 실험에서는 상관관계와 feature importance를 기반으로 주요 피처를 선별하고, 회귀 및 분류 성능을 비교했다.

회귀에서는 RandomForest가 가장 높은 성능(R² 0.70)을 기록했으며, `distributor_avg_audi`가 가장 영향력 있는 피처로 나타났다. 반면 분류에서는 클래스 불균형 영향으로 macro F1이 낮게 측정되었다.

이후 2차 실험에서는 `hit_class` 기준을 재구성하여 클래스 분포를 단순화했고, 그 결과 Logistic Regression과 RandomForest 모두 macro F1이 크게 향상되었다.

추가로 `total_sales`, `trend_pre30_avg`, `lead_actor_movie_count` 등 다중공선성 및 leakage 가능성이 있는 피처를 제거하고, 상관관계 상위 피처 중심으로 재구성한 15개 피처 조합을 기반으로 회귀 실험을 진행했다.

핵심적으로 의미 있게 확인된 피처는 다음과 같다.

- `distributor_avg_audi`
- `director_avg_audi`
- `genre_avg_audi`
- `trend_pre7_avg`
- `market_avg_audi_7d`

현재는 상관관계 기반 EDA와 feature selection을 마친 상태이며, 이후에는 VIF 분석, feature importance 비교, 하이퍼파라미터 튜닝 및 앙상블 모델 확장을 진행할 예정이다.