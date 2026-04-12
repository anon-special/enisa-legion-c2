import streamlit as st
import cv2
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime
import random

# ==========================================
# ENISA | v5.2 ELITE OVERWATCH
# ==========================================

st.set_page_config(layout="wide", page_title="ENISA | LEGION", page_icon="👤")

# --- 1. THE ULTIMATE SHADOW CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&display=swap');
    
    /* FORCE GLOBAL DARK MODE */
    .main, .stApp { background-color: #000000 !important; color: #00FF41 !important; font-family: 'JetBrains Mono', monospace; }
    
    /* THE SUIT ICON STYLING */
    .anon-logo { font-size: 150px; text-align: center; color: #FFF; text-shadow: 0 0 20px #00FF41; margin-top: 50px; }
    
    /* NEWS TICKER ANIMATION */
    .ticker-wrap { width: 100%; overflow: hidden; background: #050505; border: 1px solid #333; padding: 10px; margin-bottom: 20px; }
    .ticker { white-space: nowrap; animation: ticker 30s linear infinite; font-weight: bold; color: #00FF41; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #000; border-bottom: 1px solid #00FF41; }
    .stTabs [data-baseweb="tab"] { color: #888; }
    .stTabs [data-baseweb="tab"]:hover { color: #00FF41; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="anon-logo">👤</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>ANONYMOUS</h1>", unsafe_allow_html=True)
    
    _, col_b, _ = st.columns([1, 2, 1])
    with col_b:
        with st.form("auth"):
            pwd = st.text_input("DIRECTOR KEYCODE", type="password")
            if st.form_submit_button("AUTHORIZE"):
                if pwd == "ENISA-ZERO":
                    st.session_state.auth = True
                    st.rerun()
    st.stop()

# --- 3. LIVE INTEL TICKER (NEW) ---
news_items = [
    "--- [INTEL] Rerouting traffic through Node-77 ---",
    "--- [ALERT] Cyber-threat detected in Eastern Europe sector ---",
    "--- [SIGINT] Encrypted comms intercepted from Target-Delta ---",
    "--- [SYSTEM] All Blue-Force nodes secured ---",
    "--- [WARGAME] Simulation 14-B active ---"
]
st.markdown(f'<div class="ticker-wrap"><div class="ticker">{" ".join(news_items)}</div></div>', unsafe_allow_html=True)

# --- 4. THEATER INTERFACE ---
st.title("ENISA COMMAND | OVERWATCH")

tab1, tab2 = st.tabs(["GLOBAL INTEL", "SENTINEL EYE"])

with tab1:
    # DYNAMIC THREAT MAP
    st.markdown("### 🌍 GLOBAL THREAT VECTORS")
    # Generating 5 random threat locations
    lats = [9.03, 55.75, 35.67, 39.9, -23.55]
    lons = [38.74, 37.61, 139.65, 116.4, -46.63]
    colors = ['#00FF41', '#FF003C', '#FF003C', '#FF003C', '#00FF41']
    
    fig = go.Figure(go.Scattergeo(lat=lats, lon=lons, mode='markers', 
                                  marker=dict(size=12, color=colors, symbol='x')))
    fig.update_layout(geo=dict(projection_type="orthographic", bgcolor="#000", showland=True, landcolor="#050505"),
                      margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="#000")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### 👁️ SENTINEL EYE")
    cam_url = st.text_input("RTSP LINK", value="0", type="password")
    run_cam = st.checkbox("UPLINK ACTIVE")
    frame_window = st.empty()
    
    if run_cam:
        cap = cv2.VideoCapture(int(cam_url) if cam_url == "0" else cam_url)
        while run_cam:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_window.image(frame, use_container_width=True)
            time.sleep(0.01)
        cap.release()
