import os
import sys

# 실행 방식(streamlit run web/app.py 등)과 관계없이 루트 경로를 완벽 해석하도록 sys.path 보정
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# 패키지화된 절대 경로 유틸리티 임포트
from web.utils.loader import load_models, load_data
from web.utils.predictor import (
    compute_potential,
    make_prediction,
    calculate_importance,
    find_elbow_point
)
from web.utils.styles import apply_custom_css, FEATURE_NAME_MAP

# ── [1] Streamlit Page Configuration ──
st.set_page_config(
    page_title="2026 개봉작 흥행 예측 & 스크린 시뮬레이터",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS 스타일 및 토큰 적용
apply_custom_css()

# ── [2] Data & Model Resource Loaders ──
try:
    s1, s2 = load_models()
    df_2026, guardrails = load_data()
    df_2026 = df_2026.copy()  # Protect cached dataframe from mutation
except Exception as e:
    st.error(f"⚠️ 모델 또는 데이터를 불러오는 중에 오류가 발생했습니다: {e}")
    st.stop()

# Stacking weighted global feature importance 계산 (Top 10)
df_importance = calculate_importance(s1)
df_importance['feature_kr'] = df_importance['feature'].map(FEATURE_NAME_MAP).fillna(df_importance['feature'])
df_importance = df_importance.tail(10)  # Top 10

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
            display_features[FEATURE_NAME_MAP.get(col, col)] = movie_row[col]
    st.write(display_features)

# ── [4] Main Area Layout ──
st.title("🎬 2026 개봉작 흥행 예측 & 스크린 시뮬레이터")
st.write("학습되지 않은 2026년 개봉작 데이터를 로드하여 영화 고유의 콘텐츠 잠재력에 스크린 배급 조절을 시뮬레이션합니다.")

# ── [5] Stage 1 Inference ──
# 영화 자체 고유의 콘텐츠 잠재력 예측 점수 산출
pred_potential = compute_potential(s1, movie_row)

# ── [6] AREA A: 요약 관객수 카드 ──
st.subheader("📊 관객수 요약")

# Determine slider dynamic limits based on Genre Guardrails
genre = movie_row['genre']
genre_limit = guardrails.get(genre, guardrails['default'])

# Base prediction with actual screens
actual_scrn = float(movie_row['scrnCnt_day1'])
actual_show = float(movie_row['showCnt_day1'])
pred_actual_setup = make_prediction(s2, pred_potential, actual_scrn, actual_show)

raw_audi = movie_row.get('total_audience', 0)
actual_audience = int(raw_audi) if pd.notna(raw_audi) else 0

# Stage 1: 순수 콘텐츠 흥행 잠재력 (배급/스크린 효과가 완전히 배제된 순수 관객 동원력)
potential_audience = max(0, int(np.expm1(pred_potential)))

# ── [7] AREA B: What-If 시뮬레이터 ──
st.subheader("💡 What-If 배급 스케일 시뮬레이터")

# 실제 데이터 기반 개별 체급 동적 가드레일 설정 (실제값의 30% ~ 200%)
# 실제 데이터가 수집되지 않은 예외적 케이스(0 이하)일 경우 장르 가드레일로 폴백
if actual_scrn > 0:
    scrn_min_adj = max(5, int(actual_scrn * 0.3))
    scrn_max_adj = int(actual_scrn * 2.0)
    
    st.info(f"🛡️ **체급 기반 가드레일 활성화**: 해당 영화의 실제 개봉 첫날 스케일({int(actual_scrn):,}개 스크린) 대비 **30% ~ 200% 신뢰 구간** 내에서 슬라이더 범위가 엄격하게 제한됩니다. (외삽 오류 방지)")
else:
    scrn_min_adj = int(genre_limit['scrn_min'])
    scrn_max_adj = int(genre_limit['scrn_max'])
    
    st.info(f"🛡️ **장르 기반 가드레일 활성화**: {genre} 장르의 과거 실제 데이터 분포(과거 상위 95%)에 기반하여 안전 범위가 제어됩니다.")

if actual_show > 0:
    show_min_adj = max(10, int(actual_show * 0.3))
    show_max_adj = int(actual_show * 2.0)
else:
    show_min_adj = int(genre_limit['show_min'])
    show_max_adj = int(genre_limit['show_max'])

col_slider1, col_slider2 = st.columns(2)

with col_slider1:
    sim_scrn = st.slider(
        "🖥️ 시뮬레이션 스크린 수 (개봉 첫날)",
        min_value=scrn_min_adj,
        max_value=scrn_max_adj,
        value=int(actual_scrn) if actual_scrn > 0 else scrn_min_adj,
        step=5,
        help="극장에서 확보한 상영관(스크린)의 개수입니다. 실제 스펙 대비 30% ~ 200% 범위 내에서 조절 가능합니다."
    )

with col_slider2:
    sim_show = st.slider(
        "🎥 시뮬레이션 상영 횟수 (개봉 첫날)",
        min_value=show_min_adj,
        max_value=show_max_adj,
        value=int(actual_show) if actual_show > 0 else show_min_adj,
        step=10,
        help="확보한 스크린에서 하루 동안 상영하는 총 횟수입니다. 실제 스펙 대비 30% ~ 200% 범위 내에서 조절 가능합니다."
    )

# 유저가 설정한 시뮬레이션 배급 전략(비율) 산출
strategy_ratio = sim_show / sim_scrn if sim_scrn > 0 else 4.0

# 물리적 제약조건 (회차율) 검증 및 UI 표시
if strategy_ratio < 1.0:
    st.warning(f"⚠️ **물리적 배급 경고**: 스크린당 평균 상영 횟수가 **{strategy_ratio:.2f}회**로 지나치게 낮습니다. (통상 1회 이상 운영)")
elif strategy_ratio > 8.0:
    st.error(f"🚨 **물리적 배급 초과**: 스크린당 평균 상영 횟수가 **{strategy_ratio:.2f}회**입니다. 하루 상영 시간 한계를 초과했을 가능성이 큽니다. (상업영화 통상 3~6회)")
else:
    st.success(f"ℹ️ **배급 전략 비율**: 스크린 당 평균 **{strategy_ratio:.1f}회** 상영 (물리적으로 실현 가능한 적정 범위)")

# Current simulated prediction
sim_pred = make_prediction(s2, pred_potential, sim_scrn, sim_show)

# Display METRIC CARDS based on slider selection
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric(
        label="🎯 시뮬레이션 예상 최종 관객수",
        value=f"{sim_pred:,} 명",
        delta=f"{sim_pred - actual_audience:+,} 명 (실제 관객 대비)" if actual_audience > 0 else None
    )

with metric_col2:
    st.metric(
        label="✨ 순수 콘텐츠 잠재 흥행력",
        value=f"{potential_audience:,} 명",
        help="스크린 확보 규모 등 배급 스케일의 효과를 완전히 배제하고, 오직 감독/배우 스타파워, 장르, 개봉 시즌, 사전 검색 버즈 등의 콘텐츠 경쟁력만으로 예측한 순수 관객 동원력입니다."
    )

with metric_col3:
    st.metric(
        label="📈 실제 최종 관객수 (5.20 기준)",
        value=f"{actual_audience:,} 명" if actual_audience > 0 else "데이터 없음",
    )

with metric_col4:
    # Error rate between actual-setup prediction and actual audience
    if actual_audience > 0:
        err_pct = ((pred_actual_setup - actual_audience) / actual_audience) * 100
        
        if abs(err_pct) > 500:
            display_value = f"{err_pct:+.1f}%"
            help_text = f"실제 배급 오차율이 {err_pct:+.1f}%로 매우 높습니다. 개봉 전 인지도를 뛰어넘는 입소문(역주행 등)이나 비정형적 이상 흥행(Outlier)이 작용했을 가능성이 큽니다."
        else:
            display_value = f"{err_pct:+.1f}%"
            help_text = "실제 배급했던 스크린/상영 횟수 조건을 입력했을 때의 모델 예측 관객수와 실제 관객수의 차이 비율입니다."
            
        st.metric(
            label="🎯 실제 배급 조건 오차율",
            value=display_value,
            help=help_text
        )
    else:
        st.metric(label="🎯 실제 배급 조건 오차율", value="데이터 없음")

# Calculate Response Curve
scrn_range = np.linspace(scrn_min_adj, scrn_max_adj, 50)
curve_preds = []
for s_val in scrn_range:
    prop_show = s_val * strategy_ratio
    prop_show = np.clip(prop_show, show_min_adj, show_max_adj)
    curve_preds.append(make_prediction(s2, pred_potential, s_val, prop_show))

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

# ── [7-2] 시나리오 테이블 & 최적 효율 배급 추천 ──
st.write("---")
opt_col1, opt_col2 = st.columns([5, 3])

with opt_col1:
    st.write("#### 📊 스크린 규모별 배급 시나리오 테이블")
    
    # UI용 5개 대표 구간 시나리오 데이터프레임 산출
    step_count = 5
    scrn_steps = np.linspace(scrn_min_adj, scrn_max_adj, step_count).astype(int)
    scenario_data = []
    
    prev_aud = None
    prev_scrn = None
    for s_val in scrn_steps:
        prop_show = s_val * strategy_ratio
        prop_show = np.clip(prop_show, show_min_adj, show_max_adj)
        aud_pred = make_prediction(s2, pred_potential, s_val, prop_show)
        
        # 1개 스크린당 추가 관객 기여율 (한계 기여도)
        marginal_yield = 0
        if prev_aud is not None and prev_scrn is not None and (s_val - prev_scrn) > 0:
            marginal_yield = (aud_pred - prev_aud) / (s_val - prev_scrn)
            
        scenario_data.append({
            '스크린 수 (개)': int(s_val),
            '상영 횟수 (회)': int(prop_show),
            '예상 최종 관객수 (명)': f"{aud_pred:,} 명",
            '스크린당 관객수 (명)': f"{round(aud_pred / s_val, 1) if s_val > 0 else 0:,} 명",
            '한계 효율 (추가 관객/스크린)': marginal_yield,
            '_raw_scrn': s_val,
            '_raw_aud': aud_pred
        })
        prev_aud = aud_pred
        prev_scrn = s_val
        
    df_display = pd.DataFrame(scenario_data)
    
    # UI 노출용 포맷팅 (한계 효율 칼럼 문자열 변형 및 raw 칼럼 제거)
    df_display['한계 효율 (추가 관객/스크린)'] = df_display['한계 효율 (추가 관객/스크린)'].apply(lambda x: f"+{round(x, 1):,} 명" if x > 0 else "-")
    st.dataframe(
        df_display.drop(columns=['_raw_scrn', '_raw_aud']),
        use_container_width=True
    )

with opt_col2:
    st.write("#### 💡 최적 배급 효율 추천")
    
    # 예측기 모듈의 Elbow Point 고도화 알고리즘 호출
    rec_min, rec_max, opt_show_min, opt_show_max = find_elbow_point(
        s2, pred_potential, scrn_min_adj, scrn_max_adj, show_min_adj, show_max_adj, strategy_ratio
    )
    
    st.markdown(f"""
    * 🎯 **고효율 추천 구간**: 스크린 **`{rec_min:,}개 ~ {rec_max:,}개`**
    * 🎥 **적정 상영 횟수**: **`{opt_show_min:,}회 ~ {opt_show_max:,}회`**
    
    > **[비즈니스 의사결정 코멘트]**  
    > 해당 추천 영역은 트리 앙상블 반응 모델의 비선형 모객력을 분석하여 **최대 예상 관객수 잠재력의 90% 이상을 수확할 수 있는 최적의 효율 지점(Elbow Point)**을 기준으로 산출되었습니다.
    > 스크린 수를 `{rec_max:,}개` 이상 과잉 확보하더라도, P&A 비용 및 극장 부킹 영업 리소스 대비 **최종 관객수의 증가 속도가 급격히 정체**되는 구간에 진입하게 되므로, 투자 대비 최대 모객 효율을 일으키는 본 스윗스팟(Sweet Spot) 안에서의 집행을 강력히 권장합니다.
    """)

# ── [8] AREA C: 실제값 비교 & 피처 중요도 ──
st.subheader("📊 상세 성능 비교 및 분석")

analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:
    st.write("#### 📊 실제값 vs 예측값 비교")
    
    # 미개봉 신작(실제 관객수 0명)일 경우와 기개봉작일 경우를 동적으로 분기하여 시각적 조화 붕괴 방지
    if actual_audience > 0:
        compare_df = pd.DataFrame({
            '구분': ['순수 콘텐츠 잠재 흥행력', '실제 조건 예측', '시뮬레이터 예측', '실제 최종 관객수'],
            '관객수': [potential_audience, pred_actual_setup, sim_pred, actual_audience]
        })
        color_map = {
            '순수 콘텐츠 잠재 흥행력': '#a855f7',
            '실제 조건 예측': '#f43f5e',
            '시뮬레이터 예측': '#3b82f6',
            '실제 최종 관객수': '#10b981'
        }
    else:
        compare_df = pd.DataFrame({
            '구분': ['순수 콘텐츠 잠재 흥행력', '실제 조건 예측', '시뮬레이터 예측'],
            '관객수': [potential_audience, pred_actual_setup, sim_pred]
        })
        color_map = {
            '순수 콘텐츠 잠재 흥행력': '#a855f7',
            '실제 조건 예측': '#f43f5e',
            '시뮬레이터 예측': '#3b82f6'
        }
        st.info("ℹ️ 해당 영화는 아직 미개봉 상태이거나 실제 흥행 실적이 적재되지 않아, 예측 조건 모델값 비교로 자동 분기되었습니다.")
    
    fig_bar = px.bar(
        compare_df,
        x='구분',
        y='관객수',
        color='구분',
        color_discrete_map=color_map,
        text_auto=',',
        height=350
    )
    
    fig_bar.update_layout(
        xaxis_title="",
        yaxis_title="최종 관객수 (명)",
        showlegend=False,
        template="plotly_white",
        font=dict(family="Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"),
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
        font=dict(family="Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"),
        margin=dict(l=40, r=40, t=20, b=40)
    )
    st.plotly_chart(fig_imp, width='stretch')

# ── [9] Footer ──
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>SKN30-2nd-4Team | 개봉 예정작 흥행 예측 및 의사결정 시뮬레이터 데모</p>", unsafe_allow_html=True)
