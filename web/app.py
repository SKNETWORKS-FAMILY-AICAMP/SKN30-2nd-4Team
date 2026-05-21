import os
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ── [1] Streamlit Page Configuration ──
st.set_page_config(
    page_title="2026 개봉작 흥행 예측 & 스크린 시뮬레이터",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── [2] Data & Model Cache Loaders ──
@st.cache_resource
def load_models():
    """Load Stage 1 Stacking Ensemble and Stage 2 Simulator models."""
    s1_path = '/home/hong/project/SKN30-2nd-4Team/ml/models/stage1_ensemble.pkl'
    s2_path = '/home/hong/project/SKN30-2nd-4Team/ml/models/stage2_simulator.pkl'
    
    s1_model = joblib.load(s1_path)
    s2_model = joblib.load(s2_path)
    return s1_model, s2_model

@st.cache_data
def load_data():
    """Load pre-generated 2026 features and guardrails JSON."""
    csv_path = '/home/hong/project/SKN30-2nd-4Team/web/feature_table_2026.csv'
    json_path = '/home/hong/project/SKN30-2nd-4Team/web/genre_guardrails.json'
    
    df = pd.read_csv(csv_path)
    df['movie_id'] = df['movie_id'].astype(str)
    # Sort by open date descending (newest first)
    df = df.sort_values(by='open_date', ascending=False).reset_index(drop=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        guardrails = json.load(f)
        
    return df, guardrails

# Load resources
try:
    s1, s2 = load_models()
    df_2026, guardrails = load_data()
except Exception as e:
    st.error(f"⚠️ 모델 또는 데이터를 불러오는 중에 오류가 발생했습니다: {e}")
    st.stop()

# Calculate Stacking Weighted Global Feature Importance
cat_imp = np.array(s1['base_models']['cat'].feature_importances_)
cat_imp = cat_imp / cat_imp.sum()

xgb_imp = np.array(s1['base_models']['xgb'].feature_importances_)
xgb_imp = xgb_imp / xgb_imp.sum()

# Weighted combination (8:2 Stacking weight)
weighted_imp = 0.8 * cat_imp + 0.2 * xgb_imp
df_importance = pd.DataFrame({
    'feature': s1['feature_columns'],
    'importance': weighted_imp
}).sort_values(by='importance', ascending=True).tail(10)  # Top 10 for display

# Rename features to clean Korean names for visual presentation
feature_name_map = {
    'runtime': '상영시간 (분)',
    'director_avg_audi': '감독 과거 평균 관객수 (Log)',
    'lead_actor_avg_audi': '주연배우 과거 평균 관객수 (Log)',
    'distributor_avg_audi': '배급사 과거 평균 관객수 (Log)',
    'producer_avg_audi': '제작사 과거 평균 관객수 (Log)',
    'trend_pre7_avg': '개봉 전 7일 평균 검색량',
    'trend_pre7_max': '개봉 전 7일 최대 검색량',
    'trend_growth_rate': '검색량 증가 추세',
    'trend_pre30_avg': '개봉 전 30일 평균 검색량',
    'relative_search_share': '경쟁작 대비 검색 점유율',
    'market_avg_audi_7d': '개봉 직전 7일 시장 관객수 (Log)',
    'ticket_price_pre30': '개봉 시점 티켓 단가 수준',
    'open_day_of_week': '개봉 요일',
    'is_peak_season': '극성수기 개봉 여부',
    'is_covid_period': '코로나19 침체기 여부',
    'is_korean': '한국 영화 여부',
    'holiday_nearby_count': '개봉 전후 공휴일 수',
    'is_holiday_release': '공휴일 개봉 여부',
    'same_week_releases': '동시기 경쟁 신작 수',
    'is_new_director': '신인 감독 여부',
    'is_new_lead': '신인 배우 여부',
    'is_new_producer': '신생 제작사 여부',
    'is_new_distributor': '신생 배급사 여부',
    'genre_avg_audi': '장르 과거 흥행력 (Log)',
    'rating_15세관람가': '관람등급_15세',
    'rating_15세이상관람가': '관람등급_15세이상',
    'rating_전체관람가': '관람등급_전체',
    'rating_청소년관람불가': '관람등급_청소년관람불가'
}
df_importance['feature_kr'] = df_importance['feature'].map(feature_name_map).fillna(df_importance['feature'])

# ── [3] Streamlit Sidebar: Movie Selection & Meta Info ──
st.sidebar.title("🎬 KO-BOX PREDICT 2026")
st.sidebar.write("2-Stage 흥행 잠재력 & 배급 시뮬레이터")

# Movie selector
movie_options = [f"[{row['open_date']}] {row['title']}" for _, row in df_2026.iterrows()]
selected_option = st.sidebar.selectbox("🎯 2026년 개봉작 선택", movie_options)
selected_idx = movie_options.index(selected_option)
movie_row = df_2026.iloc[selected_idx]

# Movie meta display card in sidebar
st.sidebar.subheader("🎬 영화 기본 정보")
meta_markdown = f"""
* 🏷️ **제목**: {movie_row['title']}
* 🎭 **장르**: {movie_row['genre']}
* 🌍 **국가**: {'한국' if movie_row['is_korean'] == 1 else '외국'}
* 📅 **개봉일**: {movie_row['open_date']}
* ⏱️ **상영시간**: {movie_row['runtime']}분
"""
st.sidebar.markdown(meta_markdown)

# Actual screen counts in sidebar for reference
st.sidebar.subheader("📈 실제 배급 수치")
st.sidebar.markdown(f"""
* 🖥️ **스크린 수 (첫날)**: `{int(movie_row['scrnCnt_day1']):,} 개`
* 🎥 **상영 횟수 (첫날)**: `{int(movie_row['showCnt_day1']):,} 회`
""")

# Expander for feature details
with st.sidebar.expander("🔍 28개 입력 피처 데이터 상세"):
    display_features = {}
    for col in s1['feature_columns']:
        if col in movie_row:
            display_features[feature_name_map.get(col, col)] = movie_row[col]
    st.write(display_features)

# ── [4] Main Area Layout ──
st.title("🎬 2026 개봉작 흥행 예측 & 스크린 시뮬레이터")
st.write("학습되지 않은 2026년 개봉작 데이터를 로드하여 영화 고유의 콘텐츠 잠재력에 스크린 배급 조절을 시뮬레이션합니다.")

# ── [5] Stage 1 Inference ──
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

# Calculate Stacking Potential Score
X_meta = pd.DataFrame([preds], columns=s1['model_names'])
pred_potential = s1['meta_model'].predict(X_meta)[0]

# ── [6] AREA A: 요약 관객수 카드 ──
st.subheader("📊 관객수 요약")

# Determine slider dynamic limits based on Genre Guardrails
genre = movie_row['genre']
genre_limit = guardrails.get(genre, guardrails['default'])

# Helper function for predictions
def make_prediction(scrn, show):
    X_s2 = pd.DataFrame([{
        'pred_potential': pred_potential,
        'log_scrnCnt_day1': np.log1p(scrn),
        'log_showCnt_day1': np.log1p(show)
    }], columns=['pred_potential', 'log_scrnCnt_day1', 'log_showCnt_day1'])
    pred_log = s2.predict(X_s2)[0]
    return int(np.expm1(pred_log))

# Base prediction with actual screens
actual_scrn = float(movie_row['scrnCnt_day1'])
actual_show = float(movie_row['showCnt_day1'])
pred_actual_setup = make_prediction(actual_scrn, actual_show)
actual_audience = int(movie_row['total_audience'])

# ── [7] AREA B: What-If 시뮬레이터 ──
st.subheader("💡 What-If 배급 스케일 시뮬레이터")
st.write(f"**{genre}** 장르의 과거 실제 데이터 분포에 맞추어 슬라이더의 범위가 동적으로 조정되었습니다 (Guardrails 적용).")

col_slider1, col_slider2 = st.columns(2)

with col_slider1:
    sim_scrn = st.slider(
        "🖥️ 시뮬레이션 스크린 수 (개봉 첫날)",
        min_value=int(genre_limit['scrn_min']),
        max_value=int(genre_limit['scrn_max']),
        value=int(np.clip(actual_scrn, genre_limit['scrn_min'], genre_limit['scrn_max'])),
        step=5
    )

with col_slider2:
    # We clip the actual shows to fit within the show limits
    sim_show = st.slider(
        "🎥 시뮬레이션 상영 횟수 (개봉 첫날)",
        min_value=int(genre_limit['show_min']),
        max_value=int(genre_limit['show_max']),
        value=int(np.clip(actual_show, genre_limit['show_min'], genre_limit['show_max'])),
        step=10
    )

# Current simulated prediction
sim_pred = make_prediction(sim_scrn, sim_show)

# Display METRIC CARDS based on slider selection
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        label="🎯 시뮬레이션 예상 관객수",
        value=f"{sim_pred:,} 명",
        delta=f"{sim_pred - actual_audience:+,} 명 (실제 관객 대비)" if actual_audience > 0 else None
    )

with metric_col2:
    st.metric(
        label="📈 실제 최종 관객수",
        value=f"{actual_audience:,} 명" if actual_audience > 0 else "데이터 없음",
    )

with metric_col3:
    # Error rate between actual-setup prediction and actual audience
    if actual_audience > 0:
        err_pct = ((pred_actual_setup - actual_audience) / actual_audience) * 100
        st.metric(
            label="🎯 실제 배급 조건 오차율",
            value=f"{err_pct:+.1f}%",
            help="실제 배급했던 스크린/상영 횟수 조건을 입력했을 때의 모델 예측 관객수와 실제 관객수의 차이 비율입니다."
        )
    else:
        st.metric(label="🎯 실제 배급 조건 오차율", value="데이터 없음")

# Calculate Response Curve
scrn_range = np.linspace(genre_limit['scrn_min'], genre_limit['scrn_max'], 50)
curve_preds = []
for s_val in scrn_range:
    # Maintain proportional show count for realistic sweep
    prop_show = (sim_show / sim_scrn) * s_val if sim_scrn > 0 else s_val * 4
    prop_show = np.clip(prop_show, genre_limit['show_min'], genre_limit['show_max'])
    curve_preds.append(make_prediction(s_val, prop_show))

# Plotly Response Curve Chart
fig_curve = go.Figure()

# Add Area fill for premium feel
fig_curve.add_trace(go.Scatter(
    x=scrn_range,
    y=curve_preds,
    mode='lines',
    name='예상 관객수 곡선',
    line=dict(color='#3b82f6', width=3),
    fill='tozeroy',
    fillcolor='rgba(59, 130, 246, 0.1)'
))

# Highlight current selection
fig_curve.add_trace(go.Scatter(
    x=[sim_scrn],
    y=[sim_pred],
    mode='markers+text',
    name='현재 시뮬레이션 설정',
    marker=dict(color='#8b5cf6', size=12, symbol='circle'),
    text=[f"현재: {sim_pred:,}명"],
    textposition="top left"
))

# Highlight actual setup
fig_curve.add_trace(go.Scatter(
    x=[actual_scrn],
    y=[pred_actual_setup],
    mode='markers',
    name='실제 배급 설정 (예측)',
    marker=dict(color='#e11d48', size=10, symbol='x')
))

fig_curve.update_layout(
    title="📈 스크린 규모 확보에 따른 예상 최종 관객수 반응 곡선",
    xaxis_title="첫날 스크린 수 (개)",
    yaxis_title="최종 관객수 (명)",
    template="plotly_white",
    hovermode="x unified",
    height=400,
    margin=dict(l=40, r=40, t=50, b=40)
)

st.plotly_chart(fig_curve, width='stretch')

# ── [8] AREA C: 실제값 비교 & 피처 중요도 ──
st.subheader("📊 상세 성능 비교 및 분석")

analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:
    st.write("#### 📊 실제값 vs 예측값 비교")
    
    # Render Bar chart of actual vs prediction
    compare_df = pd.DataFrame({
        '구분': ['실제 최종 관객수', '실제 조건 예측', '시뮬레이터 예측'],
        '관객수': [actual_audience, pred_actual_setup, sim_pred],
        '컬러': ['#10b981', '#ef4444', '#3b82f6']
    })
    
    fig_bar = px.bar(
        compare_df,
        x='구분',
        y='관객수',
        color='구분',
        color_discrete_map={
            '실제 최종 관객수': '#10b981',
            '실제 조건 예측': '#f43f5e',
            '시뮬레이터 예측': '#3b82f6'
        },
        text_auto=',',
        height=350
    )
    
    fig_bar.update_layout(
        xaxis_title="",
        yaxis_title="최종 관객수 (명)",
        showlegend=False,
        template="plotly_white",
        margin=dict(l=40, r=40, t=20, b=40)
    )
    st.plotly_chart(fig_bar, width='stretch')

with analysis_col2:
    st.write("#### 📊 2-Stage Stacking 모델 변수 중요도 (Top 10)")
    
    fig_imp = px.bar(
        df_importance,
        x='importance',
        y='feature_kr',
        orientation='h',
        color='importance',
        color_continuous_scale='Blues',
        labels={'importance': '가중 기여도', 'feature_kr': '피처명'},
        height=350
    )
    
    fig_imp.update_layout(
        xaxis_title="가중 기여도 (CatBoost 80% + XGBoost 20% Stacking 가중치)",
        yaxis_title="",
        coloraxis_showscale=False,
        template="plotly_white",
        margin=dict(l=40, r=40, t=20, b=40)
    )
    st.plotly_chart(fig_imp, width='stretch')

# ── [9] Footer ──
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>SKN30-2nd-4Team | 개봉 예정작 흥행 예측 및 의사결정 시뮬레이터 데모</p>", unsafe_allow_html=True)
