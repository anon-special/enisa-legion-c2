import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import sqlite3
import time
import os
import json
from datetime import datetime

# ==========================================
# ENISA | v5.0 THE LEGION BUILD
# THEME: ANONYMOUS SHADOW OPERATIVE
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
    .report-card { border: 1px solid #333; background: #050505; padding: 15px; margin-bottom: 10px; border-left: 5px solid #00FF41; }
    h1, h2, h3 { color: #FFF; text-shadow: 0 0 10px #00FF41; text-transform: uppercase; letter-spacing: 5px; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #333; }
    </style>
""", unsafe_content_safe=True)

# --- 2. INITIALIZATION & DATABASE ---
def init_db():
    conn = sqlite3.connect('enisa_legion.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS notebook (id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, content TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS assets (name TEXT PRIMARY KEY, type TEXT, status TEXT, patch REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS captures (id INTEGER PRIMARY KEY, path TEXT, time TEXT)')
    conn.commit()
    return conn

conn = init_db()
if "auth" not in st.session_state: st.session_state.auth = False

# --- 3. THE LOCK SCREEN (ANONYMOUS LOGO) ---
if not st.session_state.auth:
    _, col_b, _ = st.columns([1, 2, 1])
    with col_b:
        st.markdown("<br><br><h1 style='text-align: center; font-size: 10em; margin-bottom:0;'>👤</h1>", unsafe_content_safe=True)
        st.markdown("<h2 style='text-align: center;'>ANONYMOUS</h2>", unsafe_content_safe=True)
        st.markdown("<p style='text-align: center; color: #888;'>WE ARE LEGION. EXPECT US.</p>", unsafe_content_safe=True)
        
        # Use st.form to prevent accidental refreshes
        with st.form("auth_gate"):
            pwd = st.text_input("ENTER SYSTEM KEY", type="password")
            if st.form_submit_button("INITIALIZE UPLINK"):
                if pwd == "ENISA-ZERO":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("ACCESS DENIED.")
    st.stop()

# --- 4. SIDEBAR: INTEL NOTEBOOK & ASSET TRACKER ---
with st.sidebar:
    st.markdown("### 📝 SIGINT LOGS")
    note_input = st.text_area("Record Intercept...", placeholder="Enter raw data here...")
    if st.button("SAVE TO DB"):
        if note_input:
            conn.execute("INSERT INTO notebook (time, content) VALUES (?,?)", (datetime.now().strftime("%H:%M"), note_input))
            conn.commit()
            st.toast("INTEL LOGGED")
    
    st.markdown("---")
    st.markdown("### 📡 ACTIVE NODES")
    nodes = pd.read_sql_query("SELECT * FROM assets", conn)
    for _, node in nodes.iterrows():
        status_color = "#00FF41" if node['status'] == "SECURE" else "#FF0000"
        st.markdown(f"**{node['name']}**<br><span style='color:{status_color}'>[{node['status']}]</span> - Patch: {node['patch']}%", unsafe_content_safe=True)

# --- 5. MAIN INTERFACE ---
st.title("ENISA COMMAND | LEGION v5.0")
st.markdown("<hr style='border: 0.5px solid #00FF41;'>", unsafe_content_safe=True)

tab1, tab2, tab3 = st.tabs(["[ THEATER OVERWATCH ]", "[ KNOWLEDGE GRAPH ]", "[ SENTINEL SHIELD ]"])

# --- TAB 1: CCTV FEED & GLOBAL MAP ---
with tab1:
    col_map, col_eye = st.columns([1, 1])
    
    with col_map:
        st.markdown("### 🌍 GLOBAL THREAT THEATER")
        # Simulating a basic threat map
        fig = go.Figure(go.Scattergeo(lat=[9.03, 11.2, 5.0], lon=[38.7, 34.9, 45.0], 
                                      mode='markers', marker=dict(size=15, color='#00FF41', symbol='square')))
        fig.update_layout(geo=dict(projection_type="orthographic", bgcolor="#000", showland=True, landcolor="#111"),
                          margin=dict(l=0,r=0,t=0,b=0), height=400, paper_bgcolor="#000")
        st.plotly_chart(fig, use_container_width=True)

    with col_eye:
        st.markdown("### 👁️ SENTINEL EYE (CCTV)")
        cam_url = st.text_input("RTSP URL (Enter 0 for Webcam)", value="0", type="password")
        optics = st.selectbox("SENSOR MODE", ["STANDARD", "NIGHT VISION", "THERMAL"])
        run_cam = st.checkbox("ACTIVATE UPLINK")
        
        frame_window = st.empty()
        
        if run_cam:
            target = int(cam_url) if cam_url == "0" else cam_url
            cap = cv2.VideoCapture(target)
            while run_cam:
                ret, frame = cap.read()
                if not ret: break
                
                # Apply Optics Filters
                if optics == "NIGHT VISION":
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    green = np.zeros_like(frame)
                    frame = cv2.merge([green, frame, green])
                elif optics == "THERMAL":
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame = cv2.applyColorMap(frame, cv2.COLORMAP_INFERNO)
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Overlay Telemetry
                cv2.putText(frame, f"LEGION-C2 | {datetime.now().strftime('%H:%M:%S')}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 65), 2)
                
                frame_window.image(frame, use_container_width=True)
                time.sleep(0.03) # Limit FPS to save CPU
            cap.release()

# --- TAB 2: PALANTIR KNOWLEDGE GRAPH ---
with tab2:
    st.markdown("### 🕸️ KNOWLEDGE GRAPH (ENTITY FUSION)")
    G = nx.Graph()
    # Mocking entities for visualization
    G.add_edge("LEGION-HQ", "ADDIS-ABABA")
    G.add_edge("ADDIS-ABABA", "INTERCEPT-01")
    G.add_edge("INTERCEPT-01", "TARGET-DELTA")
    
    pos = nx.spring_layout(G)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]; x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None]); edge_y.extend([y0, y1, None])

    node_x, node_y = [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x); node_y.append(y)

    fig_graph = go.Figure(data=[
        go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#333'), hoverinfo='none', mode='lines'),
        go.Scatter(x=node_x, y=node_y, mode='markers+text', text=list(G.nodes()), 
                   marker=dict(size=20, color='#00FF41'), textfont=dict(color="#FFF"))
    ], layout=go.Layout(showlegend=False, plot_bgcolor='black', paper_bgcolor='black', 
                         xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False)))
    st.plotly_chart(fig_graph, use_container_width=True)

# --- TAB 3: SENTINEL SHIELD (CYBER DEFENSE) ---
with tab3:
    st.markdown("### 🛡️ SENTINEL SHIELD | DEFENSE GRID")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("VULNERABILITY SCORE", "9.2", "CRITICAL", delta_color="inverse")
        if st.button("RUN GLOBAL CVE SCAN"):
            st.error("NEW ZERO-DAY DETECTED: CVE-2026-X11 - RCE FOUND IN GATEWAY.")
    with c2:
        st.write("**Risk Matrix Calculation**")
        st.latex(r"Risk = \frac{Threat \times Vulnerability}{Defense}")
        st.info("System is hardening Blue Force nodes in real-time.")

# --- FOOTER ---
st.markdown("<p style='text-align: center; color: #333; margin-top: 50px;'>TERMINAL ID: ANON-77-LEGION</p>", unsafe_content_safe=True)
