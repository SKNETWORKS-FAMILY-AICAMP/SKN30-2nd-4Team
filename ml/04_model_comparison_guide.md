# 04_model_comparison 구현 가이드

`04_model_comparison.ipynb`에서 수행할 **Stage 1 OOF 기반 Stacking 앙상블** 구현 흐름입니다.
팀원별 개별 모델 학습(01~03 노트북)이 완료된 상태를 전제로 작성되었습니다.

---

## 1. 아키텍처 개요

```
[피처 테이블 v3]
       │
       ▼
 train_test_split (80:20, random_state=42)
       │
  ┌────┴────┐
  │         │
X_train   X_test
  │         │
  ▼         │
5-Fold OOF  │    ← 개별 모델 4종 (RF, XGB, LGBM, MLP)
  │         │
  ▼         ▼
X_train_meta  X_test_meta   ← OOF 예측 / Fold 평균 예측
  │              │
  ▼              ▼
Meta-Learner (Ridge) 학습 → 평가 (R², RMSE)
  │
  ▼
pred_potential (OOF)  ← Stage 2 학습용 피처
  │
  ▼
Stage 2 XGBoost 학습  ← [pred_potential, log_scrnCnt_day1, log_showCnt_day1]
  │
  ▼
추론 파이프라인 번들 저장  ← stage1_ensemble.pkl + stage2_simulator.pkl
```

**핵심 원칙**:
- Train 예측값은 반드시 **OOF(Out-of-Fold)** — `model.predict(X_train)` 사용 금지
- Test 예측값은 **K-Fold 평균** — 각 Fold 모델이 Test를 예측한 결과의 평균
- Meta-Learner는 **규제 선형 모델(Ridge)** — 비선형 패턴은 이미 Base 모델이 학습했으므로 과적합 방지
- 추론용 모델은 **전체 Train으로 Refit** — OOF 모델은 메타 학습 전용, 배포용은 별도 재학습

---

## 2. 전제 조건 — 팀원별 산출물

각 노트북에서 Optuna 튜닝이 완료되어, 아래와 같이 최적 하이퍼파라미터가 확보된 상태여야 합니다.

| 출처 노트북 | 모델 | 수집할 산출물 |
|---|---|---|
| `01_eda_baseline.ipynb` | `RandomForestRegressor` | `best_params_rf` (dict) |
| `02_boosting.ipynb` | `XGBRegressor` | `best_params_xgb` (dict) |
| `02_boosting.ipynb` | `LGBMRegressor` | `best_params_lgbm` (dict) |
| `03_deep_learning.ipynb` | `MLPRegressor` | `best_params_mlp` (dict) |

> 각 dict에 `random_state=42`를 반드시 포함합니다.

---

## 3. 구현 코드

### 3-1. 데이터 로드 및 Hold-out 분할

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.base import clone
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import joblib

# ── 데이터 로드 (Project Convention 준수) ──
df = pd.read_csv('data/processed/feature_table_v2.csv')  # v3 확정 시 교체
target_col = 'log_audience'
drop_cols = ['movie_id', 'total_audience', 'log_audience', 'hit_class']

X = df.drop(columns=drop_cols)
y = df[target_col]

# ── Hold-out Test 분리 (random_state=42 고정) ──
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
X_train = X_train.reset_index(drop=True)
y_train = y_train.reset_index(drop=True)
X_test = X_test.reset_index(drop=True)
y_test = y_test.reset_index(drop=True)

print(f"Train: {len(X_train)}, Test: {len(X_test)}")
```

### 3-2. 개별 모델 선언 (팀원 튜닝 결과 주입)

```python
# ── 팀원별 Optuna 최적 파라미터를 여기에 반영 ──
# TODO: 각 노트북에서 확정된 best_params로 교체할 것

models = {
    'rf': RandomForestRegressor(
        n_estimators=200, max_depth=10, random_state=42
        # **best_params_rf  ← Optuna 결과로 교체
    ),
    'xgb': XGBRegressor(
        n_estimators=300, max_depth=6, learning_rate=0.05,
        random_state=42, verbosity=0
        # **best_params_xgb
    ),
    'lgbm': LGBMRegressor(
        n_estimators=300, max_depth=6, learning_rate=0.05,
        random_state=42, verbose=-1
        # **best_params_lgbm
    ),
    'mlp': MLPRegressor(
        hidden_layer_sizes=(128, 64), max_iter=500,
        early_stopping=True, random_state=42
        # **best_params_mlp
    ),
}
```

### 3-3. K-Fold OOF 예측 + Test 예측 생성

```python
N_SPLITS = 5
kf = KFold(n_splits=N_SPLITS, shuffle=True, random_state=42)

# OOF 예측 (Train용) 및 Test 예측 (Fold별 수집 → 평균)
oof_preds = {name: np.zeros(len(X_train)) for name in models}
test_preds_folds = {name: [] for name in models}

print("=" * 60)
print("Stage 1: K-Fold OOF 학습 시작")
print("=" * 60)

for fold, (train_idx, val_idx) in enumerate(kf.split(X_train, y_train)):
    print(f"\n--- Fold {fold + 1}/{N_SPLITS} ---")
    X_tr, y_tr = X_train.iloc[train_idx], y_train.iloc[train_idx]
    X_val, y_val = X_train.iloc[val_idx], y_train.iloc[val_idx]

    for name, model in models.items():
        m = clone(model)
        m.fit(X_tr, y_tr)

        # (1) Validation 예측 → OOF 벡터에 적재
        oof_preds[name][val_idx] = m.predict(X_val)

        # (2) Test 예측 → Fold별 수집 (나중에 평균)
        test_preds_folds[name].append(m.predict(X_test))

    # Fold별 간이 성능 출력
    for name in models:
        fold_rmse = np.sqrt(mean_squared_error(
            y_train.iloc[val_idx], oof_preds[name][val_idx]
        ))
        print(f"  {name:>5s}  RMSE: {fold_rmse:.4f}")

# Test 예측: K-Fold 평균
test_preds = {
    name: np.mean(preds, axis=0)
    for name, preds in test_preds_folds.items()
}
```

### 3-4. 개별 모델 OOF 성능 확인

```python
print("\n" + "=" * 60)
print("개별 모델 OOF 성능 (Train 전체 기준)")
print("=" * 60)

oof_results = []
for name in models:
    rmse = np.sqrt(mean_squared_error(y_train, oof_preds[name]))
    mae = mean_absolute_error(y_train, oof_preds[name])
    r2 = r2_score(y_train, oof_preds[name])
    oof_results.append({'model': name, 'RMSE': rmse, 'MAE': mae, 'R²': r2})
    print(f"  {name:>5s}  RMSE={rmse:.4f}  MAE={mae:.4f}  R²={r2:.4f}")

df_oof_results = pd.DataFrame(oof_results)
```

### 3-5. Meta Feature 구축 및 Meta-Learner 학습

```python
# ── Meta Feature 데이터셋 구축 ──
X_train_meta = pd.DataFrame(oof_preds)       # Train: OOF 예측값들
X_test_meta = pd.DataFrame(test_preds)       # Test: K-Fold 평균 예측값들

print(f"\nMeta Feature 차원: Train {X_train_meta.shape}, Test {X_test_meta.shape}")
print(X_train_meta.head())

# ── Meta-Learner (Ridge) 학습 ──
meta_model = Ridge(alpha=1.0)
meta_model.fit(X_train_meta, y_train)

# ── 모델별 가중치 확인 ──
print("\n" + "=" * 60)
print("Meta-Learner 가중치 (각 Base 모델의 기여도)")
print("=" * 60)
for name, coef in zip(models.keys(), meta_model.coef_):
    print(f"  {name:>5s}: {coef:+.4f}")
print(f"  {'bias':>5s}: {meta_model.intercept_:+.4f}")
```

### 3-6. 최종 성능 평가 (Hold-out Test)

```python
# ── Test 셋 최종 평가 ──
pred_test_meta = meta_model.predict(X_test_meta)

test_rmse = np.sqrt(mean_squared_error(y_test, pred_test_meta))
test_mae = mean_absolute_error(y_test, pred_test_meta)
test_r2 = r2_score(y_test, pred_test_meta)

print("\n" + "=" * 60)
print("Stage 1 Stacking 앙상블 — Hold-out Test 최종 성능")
print("=" * 60)
print(f"  RMSE : {test_rmse:.4f}")
print(f"  MAE  : {test_mae:.4f}")
print(f"  R²   : {test_r2:.4f}")

# ── 개별 모델 Test 성능과 비교 ──
print("\n--- 개별 모델 Test 성능 vs Stacking ---")
comparison = []
for name in models:
    r = {
        'model': name,
        'Test_RMSE': np.sqrt(mean_squared_error(y_test, test_preds[name])),
        'Test_R²': r2_score(y_test, test_preds[name]),
    }
    comparison.append(r)
    print(f"  {name:>5s}  RMSE={r['Test_RMSE']:.4f}  R²={r['Test_R²']:.4f}")

comparison.append({
    'model': 'stacking',
    'Test_RMSE': test_rmse,
    'Test_R²': test_r2,
})
df_comparison = pd.DataFrame(comparison)
print(f"\n  {'stack':>5s}  RMSE={test_rmse:.4f}  R²={test_r2:.4f}  ← Stacking")
```

### 3-7. Stage 2 연계용 pred_potential 산출

```python
# ── Stage 2 학습을 위한 Train/Test pred_potential 산출 ──
# Train: Meta-Learner가 OOF 메타 피처로 예측한 값 (누수 없음)
pred_potential_train = meta_model.predict(X_train_meta)

# Test: Meta-Learner가 K-Fold 평균 메타 피처로 예측한 값
pred_potential_test = pred_test_meta

print(f"\npred_potential 산출 완료")
print(f"  Train: {len(pred_potential_train)}, Test: {len(pred_potential_test)}")
```

### 3-8. 추론 파이프라인용 전체 Refit 및 번들 저장

OOF는 **메타 모델 학습 및 Stage 2 학습 전용**입니다.
실제 배포(추론) 시에는 전체 Train 데이터로 재학습한 모델을 사용해야 합니다.

```python
# ── 추론용 Base 모델 전체 재학습 (Refit) ──
print("\n" + "=" * 60)
print("추론 파이프라인용 전체 Refit")
print("=" * 60)

final_base_models = {}
for name, model in models.items():
    refit = clone(model)
    refit.fit(X_train, y_train)
    final_base_models[name] = refit
    print(f"  {name:>5s} Refit 완료")

# ── Stage 1 앙상블 번들 저장 ──
# 추론 시 필요한 모든 구성요소를 하나의 dict로 묶어 저장
stage1_bundle = {
    'base_models': final_base_models,       # Refit된 개별 모델들
    'meta_model': meta_model,               # 학습된 Meta-Learner
    'feature_columns': list(X_train.columns), # 피처 컬럼 순서
    'model_names': list(models.keys()),      # Base 모델 이름 순서
}

joblib.dump(stage1_bundle, 'models/stage1_ensemble.pkl')
print("\n✅ models/stage1_ensemble.pkl 저장 완료")

# ── OOF 결과 CSV 저장 (재현성 보관) ──
X_train_meta.to_csv('data/stage1_oof_predictions.csv', index=False)
print("✅ data/stage1_oof_predictions.csv 저장 완료")
```

---

## 4. Stage 2 시뮬레이터 모델 학습

Stage 1이 완성된 후, `scrnCnt_day1` / `showCnt_day1`을 결합하여 최종 관객수를 예측하는 보정 모델을 학습합니다.

### 4-1. Stage 2 데이터셋 구축

```python
# ── 개봉 첫날 스크린/상영 데이터 로드 ──
# feature_table에 포함되어 있다면 df에서 직접 추출
# 미포함 시 아래 SQL로 DB 조회 후 movie_id JOIN

"""
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
"""

# ── Train/Test 동일 인덱스로 Stage 2 데이터셋 구축 ──
# (train_test_split 시 사용한 동일 인덱스 기준)
df_stage2_train = pd.DataFrame({
    'pred_potential': pred_potential_train,
    'scrnCnt_day1': df.iloc[X_train.index]['scrnCnt_day1'].values,
    'showCnt_day1': df.iloc[X_train.index]['showCnt_day1'].values,
})

df_stage2_test = pd.DataFrame({
    'pred_potential': pred_potential_test,
    'scrnCnt_day1': df.iloc[X_test.index]['scrnCnt_day1'].values,
    'showCnt_day1': df.iloc[X_test.index]['showCnt_day1'].values,
})

# 로그 변환 (한계 효용 체감 반영)
for d in [df_stage2_train, df_stage2_test]:
    d['log_scrnCnt_day1'] = np.log1p(d['scrnCnt_day1'])
    d['log_showCnt_day1'] = np.log1p(d['showCnt_day1'])

s2_features = ['pred_potential', 'log_scrnCnt_day1', 'log_showCnt_day1']
X_s2_train = df_stage2_train[s2_features]
X_s2_test = df_stage2_test[s2_features]
y_s2_train = y_train
y_s2_test = y_test
```

### 4-2. Stage 2 모델 학습 및 평가

```python
# ── Stage 2: 비선형 모델 (XGBoost) ──
# 선형 모델은 스크린 수의 한계 효용 체감을 학습하지 못하므로 반드시 비선형 사용
stage2_model = XGBRegressor(
    n_estimators=150, max_depth=4, learning_rate=0.05,
    random_state=42, verbosity=0
)
stage2_model.fit(X_s2_train, y_s2_train)

# ── 평가 ──
s2_pred_test = stage2_model.predict(X_s2_test)
s2_rmse = np.sqrt(mean_squared_error(y_s2_test, s2_pred_test))
s2_r2 = r2_score(y_s2_test, s2_pred_test)

print("\n" + "=" * 60)
print("Stage 2 시뮬레이터 — Hold-out Test 성능")
print("=" * 60)
print(f"  RMSE : {s2_rmse:.4f}")
print(f"  R²   : {s2_r2:.4f}")

# ── Feature Importance 확인 ──
# pred_potential이 지배적이되, scrnCnt가 유의미한 기여를 해야 정상
s2_importance = pd.DataFrame({
    'feature': s2_features,
    'importance': stage2_model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nStage 2 Feature Importance:")
print(s2_importance.to_string(index=False))

# ── 저장 ──
joblib.dump(stage2_model, 'models/stage2_simulator.pkl')
print("\n✅ models/stage2_simulator.pkl 저장 완료")
```

---

## 5. 추론 파이프라인 (Streamlit 연동용)

저장된 `stage1_ensemble.pkl` + `stage2_simulator.pkl`을 로드하여
새 영화의 피처 입력 → 스크린 수 슬라이더 → 예상 관객수를 출력하는 흐름입니다.

```python
def predict_audience(new_movie_features: pd.DataFrame,
                     scrn_cnt: int,
                     show_cnt: int) -> float:
    """
    새 영화에 대한 최종 관객수 예측.

    Parameters
    ----------
    new_movie_features : 1행 DataFrame (Stage 1 피처 컬럼 순서 준수)
    scrn_cnt : 개봉 첫날 스크린 수 (What-If 슬라이더 값)
    show_cnt : 개봉 첫날 상영 횟수

    Returns
    -------
    predicted_audience : 예상 최종 관객수 (원본 스케일)
    """
    # Stage 1: 개별 모델 예측 → Meta-Learner 결합
    bundle = joblib.load('models/stage1_ensemble.pkl')
    base_preds = {}
    for name in bundle['model_names']:
        base_preds[name] = bundle['base_models'][name].predict(new_movie_features)
    meta_input = pd.DataFrame(base_preds)
    pred_potential = bundle['meta_model'].predict(meta_input)

    # Stage 2: 배급 스케일 보정
    s2_model = joblib.load('models/stage2_simulator.pkl')
    s2_input = pd.DataFrame({
        'pred_potential': pred_potential,
        'log_scrnCnt_day1': np.log1p([scrn_cnt]),
        'log_showCnt_day1': np.log1p([show_cnt]),
    })
    log_audience = s2_model.predict(s2_input)

    # 원본 스케일 복원
    predicted_audience = np.expm1(log_audience[0])
    return predicted_audience
```

---

## 6. 결과서용 요약 양식

노트북 마지막 셀에 아래 양식을 작성합니다.

```markdown
## 📝 결과서용 요약
- **피처 버전**: v3
- **앙상블 구성**: Stacking (RF + XGBoost + LightGBM + MLP → Ridge Meta-Learner)
- **Stage 1 회귀 성능 (Test)**: RMSE __.__, R² __.__
- **Stage 2 시뮬레이터 성능 (Test)**: RMSE __.__, R² __.__
- **Meta-Learner 가중치**: RF=__.__, XGB=__.__, LGBM=__.__, MLP=__.__
- **핵심 발견**: (한 줄 요약)
```

---

## 7. 체크리스트

- [ ] 팀원별 최적 하이퍼파라미터(best_params) 수집 완료
- [ ] Hold-out Test 분리 (random_state=42, test_size=0.2)
- [ ] 5-Fold OOF 예측 + Test Fold 평균 예측 생성
- [ ] 개별 모델 OOF 성능 비교표 작성
- [ ] Meta-Learner (Ridge) 학습 및 가중치 분석
- [ ] Stacking vs 개별 모델 Test 성능 비교
- [ ] Stage 2 데이터셋 구축 (pred_potential + scrnCnt_day1 + showCnt_day1)
- [ ] Stage 2 XGBoost 학습 및 Feature Importance 확인
- [ ] 추론용 Refit + 번들 저장 (stage1_ensemble.pkl, stage2_simulator.pkl)
- [ ] 결과서용 요약 작성
