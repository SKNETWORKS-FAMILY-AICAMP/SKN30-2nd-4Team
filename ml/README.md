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
├─ [셀 1~9]   v1 피처 생성       → feature_table_v1.csv
└─ [셀 10~11] v2 피처 추가 및 전처리 → feature_table_v2.csv, feature_table_v2_processed.csv
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

## 상영관·상영 수 시뮬레이터 모델

### 개요

본 프로젝트의 최종 산출물은 단순한 관객수 예측 모델이 아닌,  
**"개봉 첫날 스크린 확보 규모에 따른 최종 관객수 변화를 시뮬레이션하는 배급 전략 의사결정 도구"** 입니다.

배급사 마케팅 담당자가 영화의 기본 정보(배우, 감독, 장르, 사전 버즈 등)를 입력한 뒤  
**스크린 수 슬라이더를 조절하면 예상 최종 관객수가 실시간으로 변화하는 What-If 시뮬레이터**를 구현합니다.

---

### 왜 2-Stage 구조인가?

개봉 첫날 스크린 수(`scrnCnt_day1`)는 최종 관객수에 큰 영향을 미치지만,  
이 값을 다른 피처와 함께 단일 모델에 넣으면 **내생성(Endogeneity) 문제**가 발생합니다.

> 스크린 수는 배급사가 임의로 정하는 값이 아니라,  
> 영화의 스타파워·장르·버즈에 기반한 극장 체인의 수요 예측 결과물이다.  
> 즉, 우리 모델의 다른 피처들이 스크린 수를 이미 결정하고 있으므로  
> 단순 병합 시 스크린 수가 Feature Importance를 독점하고 다른 피처의 기여도가 묻힌다.

이를 해결하기 위해 모델을 **2개의 단계(Stage)**로 분리합니다.

```
Stage 1: 흥행 잠재력 모델 (순수 영화의 힘)
  Input  → 개봉 전 피처만 (배우, 감독, 버즈, 장르, 시즌 등)
  Output → pred_potential (스크린 요인을 제외한 순수 모객력 점수)

                    ↓ pred_potential 전달

Stage 2: 배급 스케일 보정 모델 (시뮬레이터)
  Input  → [pred_potential] + [scrnCnt_day1, showCnt_day1]
  Output → 최종 예상 관객수 (log_audience)
```

---

### 핵심 변수 명세

#### Stage 1 입력 피처 (개봉 전 피처 전체)
기존 피처 테이블(v2, v3 등)의 모든 개봉 전 피처를 사용합니다.  
**`scrnCnt_day1`, `showCnt_day1`은 절대 포함하지 않습니다.**

#### Stage 2 입력 피처 (3개만 사용)

| 피처명 | 설명 | 비고 |
|--------|------|------|
| `pred_potential` | Stage 1 모델의 예측 출력값 | 영화 콘텐츠 자체의 잠재력 점수 |
| `scrnCnt_day1` | 개봉 첫날 스크린 수 | 시뮬레이터의 제어 변수 (What-If 슬라이더) |
| `showCnt_day1` | 개봉 첫날 상영 횟수 | 스크린 수와 함께 배급 강도를 표현 |

#### 피처 산출 SQL
```sql
SELECT dbo.movie_id,
       dbo.scrnCnt AS scrnCnt_day1,
       dbo.showCnt AS showCnt_day1
FROM daily_box_office dbo
JOIN (
    SELECT movie_id, MIN(target_date) AS first_date
    FROM daily_box_office
    GROUP BY movie_id
) fd ON dbo.movie_id = fd.movie_id
    AND dbo.target_date = fd.first_date;
```

---

### 개발 순서

```
[1단계] Stage 1 앙상블 모델 완성 (현재 집중 단계)
  - 피처 테이블 고도화 (v2 → v3 → ...)
  - XGBoost, LightGBM, RF 학습 및 Optuna 튜닝
  - 최종 앙상블(Voting/Stacking) 구축 → stage1_ensemble.pkl 저장
  
[2단계] Stage 2 보정 모델 학습
  - Stage 1 OOF 예측값(pred_potential) 산출
  - scrnCnt_day1, showCnt_day1과 결합하여 Stage 2 XGBoost 학습
  - stage2_simulator.pkl 저장

[3단계] Streamlit 웹 데모 구현
  - 두 모델 파일을 로드하여 시뮬레이션 파이프라인 조립
  - UI: 영화 정보 입력 패널 + 스크린 수 슬라이더 + 반응 곡선 시각화
```

> ⚠️ **1단계가 완성되기 전까지 2~3단계 작업을 시작하지 않습니다.**  
> Stage 1의 성능이 시뮬레이터 전체의 정밀도를 결정하므로, 1단계 성능 극대화에 집중합니다.

---

### 참고사항

#### Stage 1 학습 시 주의점
- Stage 2에 전달할 Train 예측값은 반드시 **Out-of-Fold(OOF) 교차검증 예측**을 사용해야 합니다.
- `model.predict(X_train)`으로 구한 값은 이미 외운 데이터의 답안이므로,  
  Stage 2가 `pred_potential`만 베끼고 스크린 수를 무시하게 됩니다.
- `sklearn.model_selection.cross_val_predict`를 사용하면 간편하게 OOF 예측값을 산출할 수 있습니다.

#### Stage 2 학습 시 주의점
- Stage 2 모델은 반드시 **비선형 모델(XGBoost 등)**을 사용합니다.
- Ridge 같은 선형 모델은 스크린 수의 한계 효용 체감(Diminishing Returns) 효과를 학습하지 못합니다.
- `scrnCnt_day1`, `showCnt_day1`에 `np.log1p()` 변환을 적용하면 스케일 안정성이 향상됩니다.

#### 시뮬레이션 안전장치 (Guardrails)
- 시뮬레이션 시 사용자가 입력 가능한 스크린 수 범위를 **영화 체급별(장르·배급사 규모)로 제한**합니다.
- 과거 유사 영화의 스크린 분포에서 10th ~ 90th percentile 범위만 허용하여  
  학습 데이터에 없는 비현실적 조합(예: 독립영화 + 스크린 1,500개)에 대한 외삽 오류를 차단합니다.

#### 분류 모델과의 관계
- 본 프로젝트의 피처 검증 및 성능 튜닝은 **회귀 모델(`log_audience` 타겟) 기준**으로 수행합니다.
- 회귀 모델의 연속적인 $R^2$ 지표가 피처 추가/제거에 가장 민감하게 반응하므로  
  피처 엔지니어링 단계에서 효과를 판별하기에 최적입니다.
- 분류 모델(`hit_class`)은 회귀 모델 완성 후, 동일 피처로 학습하면 높은 성능을 자연스럽게 기대할 수 있습니다.
- 분류 시 클래스 불균형(0: 86.4%, 1~3: 13.6%)이 극심하므로  
  `class_weight='balanced'` 적용 및 **Macro F1-Score** 기준 평가가 필수입니다.