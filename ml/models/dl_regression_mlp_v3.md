

# 모델: MLP Regression

epochs: 100
optimizer: Adam
loss_fn: MSELoss
layer 구조 (input, 128) -> (128, 64) -> (64, 32) -> (32, 1)
normalization: LayerNorm(128), LayerNorm(64)
dropout: 0.15 -> 0.10 -> 0.05
learning_rate: 0.001
활성화 함수: ReLU
Early Stopping = yes

성능 점수
MSE : 1.647805094718933
RMSE: 1.2836686078263864
MAE : 0.9863911271095276
R2  : 0.657833456993103

## detail params
params = {
    "target_col": "log_audience",
    "test_size": 0.2,
    "random_state": 42,
    "batch_size": 32,
    "epochs": 300,
    "epochs_run": 97,
    "early_stopping": True,
    "early_stopping_patience": 15,
    "early_stopping_min_delta": 0.0001,
    "best_val_loss": 1.647805094718933,
    "learning_rate": 0.001,
    "optimizer": "Adam",
    "loss_fn": "MSELoss",
    "model": "RegressionMLP",
    "layer_structure": "(input_dim, 128) -> (128, 64) -> (64, 32) -> (32, 1)",
    "hidden_layers": [128, 64, 32],
    "activation": "ReLU",
    "normalization": ["LayerNorm(128)", "LayerNorm(64)"],
    "dropout": [0.15, 0.10, 0.05],
    "standard_train": standard_train,
    "one_hot_train": one_hot_train,
    "no_encode_scale_train": no_encode_scale_train,
    "drop_when_train": drop_when_train,
}
