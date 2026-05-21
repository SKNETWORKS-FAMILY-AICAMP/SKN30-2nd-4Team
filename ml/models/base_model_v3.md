최적의 모델과 파라미터 산출

모델명: RandomForest

파라미터:

{
    'model__n_estimators': 500,
    'model__min_samples_split': 5,
    'model__min_samples_leaf': 2,
    'model__max_features': 0.8,
    'model__max_depth': 16,
    'model__bootstrap': True
}
참고 성능: R²=0.6645, RMSE(log)=1.2710, MAE=37.6만명

# 추신 (홍철민)
```
if not TIME_SPLIT:
    X_train_reg, X_test_reg, yr_train, yr_test = train_test_split(
        X,
        yr,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )
    print(f"regression random split: train={len(X_train_reg)} / test={len(X_test_reg)}")
```
노트북에서 시계열을 쪼개기 위한 기준 컬럼인 open_year가 없거나 활성화되지 않아, 코드 내부적으로 예외 처리가 작동하면서 결국 **train_test_split(..., shuffle=True) 기반의 무작위 랜덤 분할(Random Split)**을 적용해 버린 것입니다.

이로 인해 2016~2024년 영화 데이터가 무작위로 섞였고, **미래의 시장 트렌드와 관람 효과를 미리 학습한 상태에서 과거 영화를 예측하는 "시간적 데이터 누수(Data Leakage / Look-ahead Bias)"**가 발생했습니다.