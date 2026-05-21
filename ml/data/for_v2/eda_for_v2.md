# 01_eda_baseline.ipynb 실행 결과 정리
## 목적
feature_table_v1 ~ v4 에 동일한 EDA를 적용해
버전별 피처 구성 차이가 log_audience 와 어떤 상관관계를 가지는지 확인했습니다.

## 확인 항목

숫자형 피처 상관관계
log_audience 기준 상관계수 TOP 5
데이터 크기 및 hit_class 분포

---

## [데이터 개요]
v1

Rows: 3,869
Columns: 27
Numeric: 23
hit_class: 0(3239) / 1(406) / 2(115) / 3(109)

v2

Rows: 3,869
Columns: 33
Numeric: 29
hit_class 동일

v3

Rows: 3,869
Columns: 38
Numeric: 34
hit_class 동일

v4

Rows: 3,869
Columns: 32
Numeric: 28
hit_class: 0(3645) / 1(224)

---

## [log_audience 상관계수 TOP 5]
모든 버전(v1~v4) 동일

lead_actor_avg_audi : 0.3747
cast_max_star_power : 0.3494
runtime : 0.3050
director_avg_audi : 0.2950
producer_avg_audi : 0.2865

※ total_audience, hit_class 제외 후 계산

---

## [핵심 Feature]
distributor_avg_audi

CatBoost 기준 높은 중요도
배급사 흥행력이 강한 영향

lead_actor_avg_audi

모든 버전에서 상위권 유지
배우 흥행력이 안정적으로 기여

runtime

상관관계 및 중요도 모두 높게 확인
기본 메타 피처 역할

---

[요약]
배우, 배급사, 러닝타임 관련 피처가 반복적으로 유의미하게 나타났으며,
특히 distributor_avg_audi, lead_actor_avg_audi, runtime 이 핵심 피처로 확인되었습니다.