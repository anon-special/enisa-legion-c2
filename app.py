import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import sqlite3
import time
from datetime import datetime

# ==========================================
# ENISA | v6.2 FINAL PRO BUILD
# ==========================================

st.set_page_config(layout="wide", page_title="ENISA | LEGION", page_icon="👤")

# --- 1. PRO-GRADE SHADOW CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&display=swap');
    
    /* GLOBAL OVERRIDE */
    html, body, [class*="css"], .stApp { 
        background-color: #000000 !important; 
        color: #00FF41 !important; 
        font-family: 'JetBrains Mono', monospace !important; 
    }

    /* THE ANONYMOUS SUIT LOGO */
    .anon-logo { font-size: 140px; text-align: center; color: #FFF; text-shadow: 0 0 30px #00FF41; padding-top: 50px; line-height: 1; }
    
    /* SCROLLING TICKER */
    .ticker-wrap { width: 100%; overflow: hidden; background: #080808; border-top: 1px solid #00FF41; border-bottom: 1px solid #00FF41; padding: 8px 0; margin-bottom: 25px; }
    .ticker { white-space: nowrap; animation: ticker 25s linear infinite; font-weight: bold; color: #00FF41; letter-spacing: 2px; text-transform: uppercase; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* UI ELEMENTS */
    .stButton>button { 
        background-color: #000 !important; border: 1px solid #00FF41 !important; color: #00FF41 !important;
        font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000 !important; box-shadow: 0 0 20px #00FF41; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #00FF41 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #00FF41; }
    .stTabs [data-baseweb="tab"] { color: #555; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #00FF41 !important; }
    h1, h2, h3 { color: #FFF !important; text-shadow: 0 0 10px #00FF41; letter-spacing: 4px; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATABASE CORE ---
def init_db():
    conn = sqlite3.connect('enisa_pro.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS sigint (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, data TEXT)')
    conn.commit()
    return conn

conn = init_db()

# --- 3. GATEKEEPER LOCK SCREEN ---
if "auth" not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="anon-logo">👤</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>ANONYMOUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; letter-spacing: 5px;'>SYSTEM ENCRYPTED. ENTER COMMAND CODE.</p>", unsafe_allow_html=True)
    
    _, col_c, _ = st.columns([1, 1.2, 1])
    with col_c:
        with st.form("uplink"):
            pwd = st.text_input("DIRECTOR KEY", type="password")
            if st.form_submit_button("AUTHORIZE"):
                if pwd == "ENISA-ZERO":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("SIGNAL BLOCKED. UNAUTHORIZED.")
    st.stop()

# --- 4. TACTICAL INTEL TICKER ---
intel_feed = " | ".join([
    "[ALERT] SAT-LINK 07 ACTIVE", 
    "[INTEL] DEEP-SEA CABLE PROBE DETECTED IN NORTH ATLANTIC", 
    "[STATUS] ETHIOPIAN HUB GREEN", 
    "[OVERWATCH] TARGET DELTA LOCATED IN GENEVA",
    "WE ARE LEGION. EXPECT US."
])
st.markdown(f'<div class="ticker-wrap"><div class="ticker">{intel_feed}</div></div>', unsafe_allow_html=True)

# --- 5. SIDEBAR: SIGINT LOGGING ---
with st.sidebar:
    st.markdown("### 📝 SIGINT RECORDER")
    new_entry = st.text_area("Record Intercept...", height=100)
    if st.button("LOG DATA"):
        if new_entry:
            conn.execute("INSERT INTO sigint (ts, data) VALUES (?,?)", (datetime.now().strftime("%H:%M:%S"), new_entry))
            conn.commit()
            st.toast("DATA ENCRYPTED")
    
    st.markdown("---")
    st.markdown("### 📂 ARCHIVED LOGS")
    history = pd.read_sql_query("SELECT * FROM sigint ORDER BY id DESC LIMIT 3", conn)
    for _, item in history.iterrows():
        st.markdown(f"**{item['ts']}**<br><span style='color:#888'>{item['data']}</span>", unsafe_allow_html=True)

# --- 6. MAIN COMMAND CENTER ---
st.title("ENISA COMMAND | PRO OVERWATCH")

tab1, tab2, tab3 = st.tabs(["THEATER MAP", "SENTINEL EYE", "CYBER DEFENSE"])

# --- TAB 1: REAL SATELLITE MAP ---
with tab1:
    col_map, col_stats = st.columns([2, 1])
    with col_map:
        st.markdown("### 🛰️ GLOBAL TACTICAL GRID")
        
        # Origin and Target Data
        t_lats, t_lons = [55.75, 39.9, 40.71], [37.61, 116.4, -74.00] # Moscow, Beijing, NYC
        base_lat, base_lon = [9.03], [38.74] # Addis Ababa
        
        fig = go.Figure()
        
        # Threat Markers (Red)
        fig.add_trace(go.Scattermapbox(lat=t_lats, lon=t_lons, mode='markers', 
            marker=dict(size=12, color='#FF003C'), name="Threat Origin"))
        
        # Base Marker (Green)
        fig.add_trace(go.Scattermapbox(lat=base_lat, lon=base_lon, mode='markers', 
            marker=dict(size=18, color='#00FF41'), name="ENISA Hub"))
        
        # Attack Vectors (Lines)
        for i in range(len(t_lats)):
            fig.add_trace(go.Scattermapbox(mode="lines", lat=[t_lats[i], base_lat[0]], lon=[t_lons[i], base_lon[0]],
                                        line=dict(width=2, color='#FF003C')))

        # ESRI SATELLITE UPLINK
        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_layers=[{
                "below": 'traces', "sourcetype": "raster",
                "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]
            }],
            mapbox=dict(center=go.layout.mapbox.Center(lat=20, lon=30), zoom=1.5, pitch=40),
            margin=dict(l=0, r=0, t=0, b=0), height=550, paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_stats:
        st.markdown("### 📊 SIGNAL STRENGTH")
        st.metric("ENCRYPTION STRENGTH", "4096-BIT", "SECURE")
        st.metric("LATENCY", "14ms", "-2ms", delta_color="normal")
        st.info("Satellite Uplink: LOCKED. You can zoom to street level on the grid.")

# --- TAB 2: SENTINEL EYE (CCTV) ---
with tab2:
    col_eye, col_optics = st.columns([2, 1])
    with col_eye:
        st.markdown("### 👁️ OPTICAL FEED")
        cam_url = st.text_input("INPUT STREAM (0 for WebCam)", value="0", type="password")
        run_eye = st.checkbox("ACTIVATE SENSOR")
        feed = st.empty()
        
        mode = st.radio("OPTIC MODE", ["STD", "NIGHT", "THERMAL"], horizontal=True)
        
        if run_eye:
            cap = cv2.VideoCapture(int(cam_url) if cam_url == "0" else cam_url)
            while run_eye:
                ret, frame = cap.read()
                if not ret: break
                
                # OPTIC FILTERS
                if mode == "NIGHT":
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    g = np.zeros_like(frame)
                    frame = cv2.merge([g, frame, g])
                elif mode == "THERMAL":
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # HUD OVERLAY
                cv2.putText(frame, f"S-EYE | {datetime.now().strftime('%H:%M:%S')}", (15, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 65), 2)
                
                feed.image(frame, use_container_width=True)
                time.sleep(0.01)
            cap.release()

# --- TAB 3: SHIELD & KNOWLEDGE ---
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🛡️ DEFENSE SHIELD")
        st.latex(r"RiskScore = \frac{Threat \cdot Vulnerability}{Defense^{2}}")
        st.metric("VULNERABILITY", "1.2", "STABLE", delta_color="inverse")
    with c2:
        st.markdown("### 🕸️ ENTITY GRAPH")
        # Visual Linkage
        G = nx.Graph()
        G.add_edges_from([("YOU", "ENISA-HQ"), ("ENISA-HQ", "SAT-07"), ("SAT-07", "TARGET")])
        pos = nx.spring_layout(G)
        edge_x, edge_y = [], []
        for e in G.edges():
            x0, y0 = pos[e[0]]; x1, y1 = pos[e[1]]
            edge_x.extend([x0, x1, None]); edge_y.extend([y0, y1, None])
        
        fig_g = go.Figure(data=[
            go.Scatter(x=edge_x, y=edge_y, line=dict(color='#333'), mode='lines'),
            go.Scatter(x=[pos[n][0] for n in G.nodes()], y=[pos[n][1] for n in G.nodes()], 
                       mode='markers+text', text=list(G.nodes()), marker=dict(size=20, color='#00FF41'))
        ])
        fig_g.update_layout(showlegend=False, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)",
                            xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_g, use_container_width=True)

# FOOTER
st.markdown("<p style='text-align: center; color: #222; margin-top: 100px;'>SYSTEM ID: 77-LEGION-PRO</p>", unsafe_allow_html=True)
