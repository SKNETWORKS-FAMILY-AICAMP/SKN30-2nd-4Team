# ml — 모델링 작업 가이드

## 피처

- 피처 설계 상세: [baseline_feature_table.md](./data/baseline_feature_table.md)

---

## 작업 목록

| # | 작업 | 파일명 | 내용 |
|---|------|--------|------|
| 1 | EDA + Baseline ML | `01_eda_baseline.ipynb` | 데이터 분석·시각화 + Linear, Ridge, Lasso, RandomForest |
| 2 | Boosting ML | `02_boosting.ipynb` | XGBoost, LightGBM + 하이퍼파라미터 튜닝 |
| 3 | 딥러닝 | `03_deep_learning.ipynb` | MLP 회귀 + MLP 분류 |
| 4 | 모델 비교 및 최종 선정 | `04_model_comparison.ipynb` | 전체 모델 성능 비교 + 최적 모델 선정 |

> 각 모델 노트북에서 **피처 버전별(v1, v2, …) 성능 비교표**를 함께 작성합니다.

---

## 피처 테이블 버전업 규칙

### 작업 방식
`00_feature_table.ipynb`에서 **공동 작업**으로 셀을 추가하여 새 버전의 CSV를 생성합니다.

```
00_feature_table.ipynb (공동 작업)
├─ [셀 1~8]  v1 피처 생성       → feature_table_v1.csv
├─ [셀 9~?]  v2 피처 추가       → feature_table_v2.csv
└─ [셀 ?~?]  v3 피처 추가       → feature_table_v3.csv
```

### 규칙

1. **v1은 수정 금지** — 모든 모델의 성능 기준점(베이스라인)
2. **버전 번호는 순차적으로** — v2, v3, v4 순서대로 올림
3. **기존 컬럼 이름은 바꾸지 않음** — 새 피처 추가만 허용
4. **타겟 3개 구조 유지** — `total_audience`, `log_audience`, `hit_class`
5. **노트북 동시 편집 금지** — 한 명이 작업 → 커밋/푸시 → 다음 사람 pull 후 작업

### 변경 기록
피처를 추가할 때 [`data/CHANGELOG.md`](./data/CHANGELOG.md)에 한 줄 기록:

---

## 공통 코드

### 데이터 로드
```python
import pandas as pd

df = pd.read_csv(f'../data/feature_table_[사용할 버전].csv')

# 피처와 타겟 분리
target_col = 'log_audience'           # 회귀: log_audience / 분류: hit_class
drop_cols = ['movie_id', 'total_audience', 'log_audience', 'hit_class']

X = df.drop(columns=drop_cols)
y = df[target_col]
```

### Train/Test 분리
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

> ⚠️ `random_state=42` 고정 필수 — 모든 노트북에서 동일한 분할 보장

### 평가 지표

| 문제 유형 | 타겟 컬럼 | 평가 지표 |
|----------|----------|----------|
| 회귀 | `log_audience` | RMSE, MAE, R² |
| 분류 | `hit_class` (0~3) | Accuracy, F1-score (macro) |

---

## 주의사항

1. `movie_id`는 식별용 — **학습에 사용하지 않음** (반드시 drop)
2. 타겟 컬럼 3개 중 **사용하지 않는 나머지 2개도 drop**
3. 모델 파일은 `models/` 폴더에 저장 (예: `models/xgboost_v1.pkl`)

---

## 필수 산출물 작성 규칙

문서는 **외부 제출용**이므로, 결과·시각화·분석 내용을 문서 안에 직접 포함해야 합니다.

### 📄 인공지능 데이터 전처리 결과서

| 섹션 | 내용 | 작성자 |
|------|------|--------|
| 1. 데이터 수집 개요 | API 구조, DB 스키마, 수집 기간·규모 | 데이터 수집 수행자 |
| 2. EDA 시각화 및 분석 | 피처 분포, 상관관계, 이상치 분석 | EDA 수행자 |
| 3. 피처 엔지니어링 설계 | 피처 설계 근거, 버전별 변경 이력 | 피처 엔지니어링 수행자 |
| 4. 데이터 정제 처리 | 결측치·센티널 값 처리 방식 및 결과 | 전처리 수행자 |

### 📄 인공지능 학습 결과서

| 섹션 | 내용 | 작성자 |
|------|------|--------|
| 1. Baseline ML 결과 | Ridge, Lasso, RF 성능 + 피처 중요도 분석 | Baseline ML 수행자 |
| 2. Boosting ML 결과 | XGBoost, LightGBM 성능 + 튜닝 과정 | Boosting ML 수행자 |
| 3. DL 결과 | MLP 회귀/분류 성능 + 학습곡선 | DL 수행자 |
| 4. 모델 비교 및 최종 선정 | 전체 비교표 + 최적 모델 선정 근거 | 모델 비교 수행자 |

### 작업 흐름

```
1. 각자 노트북 작업 시, 주요 차트와 성능 지표를 이미지로 저장 (images/ 폴더)
2. 노트북 마지막 셀에 "결과서용 요약" 마크다운 작성 (아래 양식)
3. 총괄자가 각 요약 + 이미지를 모아서 최종 문서 편집
```

### 결과서용 요약 양식 (각 노트북 마지막 셀에 작성)

```markdown
## 📝 결과서용 요약
- **피처 버전**: v1
- **모델**: XGBoost (max_depth=6, n_estimators=300)
- **회귀 성능**: RMSE 1.23, R² 0.68
- **분류 성능**: Accuracy 0.71, F1 0.65
- **핵심 발견**: (한 줄 요약)
```