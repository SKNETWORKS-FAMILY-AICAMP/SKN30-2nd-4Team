import os
import json
import joblib
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_resource
def load_models():
    """Load Stage 1 Stacking Ensemble and Stage 2 Simulator models."""
    s1_path = os.path.join(BASE_DIR, 'stage1_ensemble.pkl')
    s2_path = os.path.join(BASE_DIR, 'stage2_simulator.pkl')
    
    s1_model = joblib.load(s1_path)
    s2_model = joblib.load(s2_path)
    return s1_model, s2_model

@st.cache_data
def load_data():
    """Load pre-generated 2026 features and guardrails JSON."""
    csv_path = os.path.join(BASE_DIR, 'feature_table_2026.csv')
    json_path = os.path.join(BASE_DIR, 'genre_guardrails.json')
    
    df = pd.read_csv(csv_path)
    df['movie_id'] = df['movie_id'].astype(str)
    
    # 5월 20일 이전 개봉작만 필터링
    df = df[df['open_date'] < '2026-05-20']
    
    # Sort by open date descending (newest first)
    df = df.sort_values(by='open_date', ascending=False).reset_index(drop=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        guardrails = json.load(f)
        
    return df, guardrails
