import streamlit as st

def apply_custom_css():
    """Apply global customized styling tokens to the Streamlit app for premium Aesthetics."""
    st.markdown("""
        <style>
            /* 1. Global typography and sans-serif integration */
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;700&display=swap');
            
            html, body, [class*="css"], .stMarkdown {
                font-family: 'Outfit', 'Inter', 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }
            
            /* 2. Sleek Custom Metric Cards styling */
            div[data-testid="stMetric"] {
                background: linear-gradient(135deg, rgba(255,255,255,0.85) 0%, rgba(240,245,255,0.7) 100%);
                border: 1px solid rgba(220, 230, 255, 0.6);
                border-radius: 12px;
                padding: 18px 24px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
                transition: all 0.3s ease;
            }
            div[data-testid="stMetric"]:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(59, 130, 246, 0.08);
                border-color: rgba(59, 130, 246, 0.3);
            }
            
            /* 3. Slider visual polishing */
            div[data-baseweb="slider"] {
                padding: 8px 0;
            }
            
            /* 4. Beautiful Custom alert borders */
            div[data-testid="stAlert"] {
                border-radius: 10px;
                border: none;
                box-shadow: 0 2px 10px rgba(0,0,0,0.02);
            }
            
            /* 5. Custom header style */
            .main-header {
                font-size: 2.2rem;
                font-weight: 800;
                color: #1e293b;
                margin-bottom: 0.5rem;
                background: linear-gradient(to right, #1e3a8a, #3b82f6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
        </style>
    """, unsafe_allow_html=True)

# 28개 입력 피처 정제 매핑 사전
FEATURE_NAME_MAP = {
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
