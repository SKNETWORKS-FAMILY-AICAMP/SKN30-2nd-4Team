# 모델별 최적 파라미터 정리

## V2 최적 파라미터

### XGBoost (XGB)

* **최적 R² Score**: `0.5732971311968086`

| 파라미터             | 값                      |
| ---------------- | ---------------------- |
| n_estimators     | 788                    |
| max_depth        | 3                      |
| learning_rate    | 0.006797783576203758   |
| subsample        | 0.7200183490338203     |
| colsample_bytree | 0.6741093743775898     |
| min_child_weight | 10                     |
| reg_alpha        | 2.9292578715664305e-08 |
| reg_lambda       | 1.159894031209044e-07  |

---

### LightGBM (LGB)

* **최적 R² Score**: `0.5637165650320419`

| 파라미터              | 값                    |
| ----------------- | -------------------- |
| n_estimators      | 546                  |
| max_depth         | 3                    |
| learning_rate     | 0.018582530814233854 |
| subsample         | 0.8644541212903576   |
| colsample_bytree  | 0.9451038106232729   |
| min_child_samples | 57                   |
| reg_alpha         | 0.022757519343496128 |
| reg_lambda        | 4.334788671830664    |
| num_leaves        | 153                  |

---

### CatBoost (CAT)

* **최적 R² Score**: `0.5967524479875749`

| 파라미터              | 값                    |
| ----------------- | -------------------- |
| iterations        | 1801                 |
| depth             | 5                    |
| learning_rate     | 0.054560006980028566 |
| l2_leaf_reg       | 5.634311594468995    |
| subsample         | 0.664149715143098    |
| colsample_bylevel | 0.8615687507581833   |
| min_data_in_leaf  | 28                   |

---

# V3 최적 파라미터

## XGBoost (XGB)

* **최적 R² Score**: `0.5396805413649011`

| 파라미터             | 값                      |
| ---------------- | ---------------------- |
| n_estimators     | 863                    |
| max_depth        | 3                      |
| learning_rate    | 0.005934921506705023   |
| subsample        | 0.6839996494742674     |
| colsample_bytree | 0.5002998622747432     |
| min_child_weight | 1                      |
| reg_alpha        | 0.37388378953696294    |
| reg_lambda       | 2.3814074258429286e-06 |

---

## LightGBM (LGB)

* **최적 R² Score**: `0.5524012818970885`

| 파라미터              | 값                   |
| ----------------- | ------------------- |
| n_estimators      | 797                 |
| max_depth         | 3                   |
| learning_rate     | 0.07547574825052426 |
| subsample         | 0.6275910164022495  |
| colsample_bytree  | 0.575048451387538   |
| min_child_samples | 83                  |
| reg_alpha         | 0.03538800255930426 |
| reg_lambda        | 3.276394057169492   |
| num_leaves        | 255                 |

---

## CatBoost (CAT)

* **최적 R² Score**: `0.5699019904219325`

| 파라미터              | 값                    |
| ----------------- | -------------------- |
| iterations        | 365                  |
| depth             | 4                    |
| learning_rate     | 0.05468505449600897  |
| l2_leaf_reg       | 3.21561835915569e-08 |
| subsample         | 0.7318363784167181   |
| colsample_bylevel | 0.5148731778974988   |
| min_data_in_leaf  | 50                   |

---

# 성능 비교 요약

| Version | 모델  | 최고 R²      |
| ------- | --- | ---------- |
| V2      | XGB | 0.5733     |
| V2      | LGB | 0.5637     |
| V2      | CAT | **0.5968** |
| V3      | XGB | 0.5397     |
| V3      | LGB | 0.5524     |
| V3      | CAT | 0.5699     |

## 최종 정리

* 전체 성능 기준 최고 모델은 **V2 CatBoost**
* 최고 R² Score:
  `0.5967524479875749`
* V3는 전반적으로 성능이 소폭 감소했지만, 일부 모델(LGB)은 비교적 안정적인 성능 유지
