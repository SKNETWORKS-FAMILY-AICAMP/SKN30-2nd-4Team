import numpy as np
import pandas as pd

def compute_potential(s1, movie_row):
    """
    Stage 1 Inference: 예측 변수 meta 데이터셋을 가공하여 콘텐츠 흥행 잠재력 점수를 산출
    """
    X_s1 = pd.DataFrame(0.0, index=[0], columns=s1['feature_columns'])
    for col in s1['feature_columns']:
        if col in movie_row:
            X_s1.at[0, col] = float(movie_row[col])
            
    # Scale MLP
    scaler = s1['mlp_scaler']
    X_s1_scaled = pd.DataFrame(scaler.transform(X_s1), columns=X_s1.columns)
    
    # Base model predictions for Stacking input
    preds = {}
    for name in s1['model_names']:
        model = s1['base_models'][name]
        if name == 'mlp':
            preds[name] = model.predict(X_s1_scaled)[0]
        else:
            preds[name] = model.predict(X_s1)[0]
            
    # Calculate Meta Model Stacking Potential Score
    X_meta = pd.DataFrame([preds], columns=s1['model_names'])
    pred_potential = s1['meta_model'].predict(X_meta)[0]
    return pred_potential

def make_prediction(s2, pred_potential, scrn, show):
    """
    Stage 2 Simulator Inference: 잠재력과 배급 스케일을 변환/조합하여 최종 관객수를 계산
    """
    X_s2 = pd.DataFrame([{
        'pred_potential': pred_potential,
        'log_scrnCnt_day1': np.log1p(scrn),
        'log_showCnt_day1': np.log1p(show)
    }], columns=['pred_potential', 'log_scrnCnt_day1', 'log_showCnt_day1'])
    pred_log = s2.predict(X_s2)[0]
    return max(0, int(np.expm1(pred_log)))

def calculate_importance(s1):
    """
    CatBoost 80% + XGBoost 20% Stacking 기여 가중 피처 중요도 계산
    """
    cat_imp = np.array(s1['base_models']['cat'].feature_importances_)
    cat_imp = cat_imp / cat_imp.sum()

    xgb_imp = np.array(s1['base_models']['xgb'].feature_importances_)
    xgb_imp = xgb_imp / xgb_imp.sum()

    weighted_imp = 0.8 * cat_imp + 0.2 * xgb_imp
    df_importance = pd.DataFrame({
        'feature': s1['feature_columns'],
        'importance': weighted_imp
    }).sort_values(by='importance', ascending=True)
    
    return df_importance

def find_elbow_point(s2, pred_potential, scrn_min, scrn_max, show_min, show_max, strategy_ratio):
    """
    30단계 고해상도 내부 스윕 및 최대 예상 관객 수의 90% 달성 Elbow Point 임계 영역 산출
    """
    fine_steps = 30
    fine_scrn_range = np.linspace(scrn_min, scrn_max, fine_steps)
    fine_preds = []
    
    for s_val in fine_scrn_range:
        prop_show = s_val * strategy_ratio
        prop_show = np.clip(prop_show, show_min, show_max)
        fine_preds.append(make_prediction(s2, pred_potential, s_val, prop_show))
        
    min_pred_val = min(fine_preds) if fine_preds else 0
    max_pred_val = max(fine_preds) if fine_preds else 1
    dynamic_range = max_pred_val - min_pred_val
    
    opt_scrn = int(scrn_max)
    if dynamic_range > 0:
        target_threshold = min_pred_val + (dynamic_range * 0.90)  # 최대 잠재력의 90% 임계점
        for s_val, p_val in zip(fine_scrn_range, fine_preds):
            if p_val >= target_threshold:
                opt_scrn = int(s_val)
                break
                
    # 피크 임계점 기준 ±10% 보정
    rec_min = max(int(scrn_min), int(opt_scrn * 0.9))
    rec_max = min(int(scrn_max), int(opt_scrn * 1.1))
    
    # 겹침 현상 방어 최소 마진 제공
    if rec_min == rec_max:
        rec_min = max(int(scrn_min), rec_min - 10)
        rec_max = min(int(scrn_max), rec_max + 10)
        
    opt_show_min = int(np.clip(rec_min * strategy_ratio, show_min, show_max))
    opt_show_max = int(np.clip(rec_max * strategy_ratio, show_min, show_max))
    
    return rec_min, rec_max, opt_show_min, opt_show_max
