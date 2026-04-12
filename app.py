import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import sqlite3
import time
import os
from datetime import datetime

# ==========================================
# ENISA | v5.1 THE LEGION BUILD (PATCHED)
# ==========================================

st.set_page_config(layout="wide", page_title="ENISA | LEGION", page_icon="👤")

# --- 1. THE ANONYMOUS CSS OVERRIDE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500;700&display=swap');
    html, body, [class*="css"] { 
        background-color: #000000; 
        color: #00FF41; 
        font-family: 'Fira Code', monospace;
    }
    .stMetric { border: 1px solid #00FF41; background: rgba(0, 255, 65, 0.05); padding: 15px; border-radius: 5px; }
    .stButton>button { 
        background-color: #000; border: 1px solid #00FF41; color: #00FF41;
        font-weight: bold; width: 100%; transition: 0.5s; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 25px #00FF41; }
    h1, h2, h3 { color: #FFF; text-shadow: 0 0 10px #00FF41; text-transform: uppercase; letter-spacing: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZATION ---
if "auth" not in st.session_state: st.session_state.auth = False

# --- 3. THE LOCK SCREEN ---
if not st.session_state.auth:
    _, col_b, _ = st.columns([1, 2, 1])
    with col_b:
        st.markdown("<br><br><h1 style='text-align: center; font-size: 10em; margin-bottom:0;'>👤</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>ANONYMOUS</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>WE ARE LEGION. EXPECT US.</p>", unsafe_allow_html=True)
        
        with st.form("auth_gate"):
            pwd = st.text_input("ENTER SYSTEM KEY", type="password")
            if st.form_submit_button("INITIALIZE UPLINK"):
                if pwd == "ENISA-ZERO":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("ACCESS DENIED.")
    st.stop()

# --- 4. MAIN INTERFACE ---
st.title("ENISA COMMAND | LEGION v5.1")
st.markdown("<hr style='border: 0.5px solid #00FF41;'>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["[ THEATER OVERWATCH ]", "[ KNOWLEDGE GRAPH ]", "[ SENTINEL SHIELD ]"])

with tab1:
    col_map, col_eye = st.columns([1, 1])
    with col_map:
        st.markdown("### 🌍 GLOBAL THREAT THEATER")
        fig = go.Figure(go.Scattergeo(lat=[9.03], lon=[38.7], mode='markers', marker=dict(size=15, color='#00FF41')))
        fig.update_layout(geo=dict(projection_type="orthographic", bgcolor="#000", showland=True, landcolor="#111"),
                          margin=dict(l=0,r=0,t=0,b=0), height=400, paper_bgcolor="#000")
        st.plotly_chart(fig, use_container_width=True)

    with col_eye:
        st.markdown("### 👁️ SENTINEL EYE (CCTV)")
        cam_url = st.text_input("RTSP URL (Enter 0 for Webcam)", value="0", type="password")
        run_cam = st.checkbox("ACTIVATE UPLINK")
        frame_window = st.empty()
        
        if run_cam:
            target = int(cam_url) if cam_url == "0" else cam_url
            cap = cv2.VideoCapture(target)
            while run_cam:
                ret, frame = cap.read()
                if not ret: break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_window.image(frame, use_container_width=True)
                time.sleep(0.1)
            cap.release()

with tab2:
    st.markdown("### 🕸️ KNOWLEDGE GRAPH")
    st.info("System is mapping entity relationships...")

with tab3:
    st.markdown("### 🛡️ SENTINEL SHIELD")
    st.metric("VULNERABILITY SCORE", "9.2", "CRITICAL", delta_color="inverse")
