# Streamlit UI assembly (imports sim_engine and ai_rules)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import threading
from datetime import datetime
from collections import deque

from sim_engine import init_state, step
from ai_rules import analyze_ladle_snapshot

UPDATE_INTERVAL = 3.0

def run_app():
    st.set_page_config(page_title="SLTHMS Prototype", layout="wide")
    if 'sim_state' not in st.session_state:
        st.session_state.sim_state = init_state()
        st.session_state.running = False
        st.session_state.auto_refresh = True
        st.session_state.alert_log = deque(maxlen=200)
        st.session_state.lock = threading.Lock()

    def update_one(force_anomaly=None):
        with st.session_state.lock:
            st.session_state.sim_state = step(st.session_state.sim_state, force_anomaly=force_anomaly)
            # generate alerts
            for lid, ladle in st.session_state.sim_state.items():
                analysis = analyze_ladle_snapshot(ladle)
                if analysis["status"] == "Critical":
                    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    msg = f"{ts} — {lid} at {ladle['location']}: {analysis['explanation']} Rec: {analysis['recommendation']}"
                    st.session_state.alert_log.appendleft(msg)

    def sim_thread():
        while st.session_state.running:
            update_one()
            time.sleep(UPDATE_INTERVAL)

    st.markdown("<h1 style='color:orange;background:#222;padding:10px;border-radius:6px;'>Smart Ladle Tracking & Health Monitoring System (SLTHMS)</h1>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("Controls")
        if st.button("Run Simulation"):
            if not st.session_state.running:
                st.session_state.running = True
                threading.Thread(target=sim_thread, daemon=True).start()
                st.success("Simulation started.")
        if st.button("Pause Simulation"):
            st.session_state.running = False
            st.success("Simulation paused.")
        st.session_state.auto_refresh = st.checkbox("Auto-refresh UI (3s)", value=st.session_state.auto_refresh)
        st.markdown("---")
        if st.button("Force L-02 Overheat"):
            update_one(force_anomaly={"ladle_id": "L-02", "temperature": 1625, "stress": 86, "vibration": 0.8})
            st.success("Forced L-02 anomaly injected.")
        st.markdown("---")
        st.write("Prepared by Duck — run locally or deploy to Loveable AI")

    sim = st.session_state.sim_state
    rows = []
    for lid, ladle in sim.items():
        analysis = analyze_ladle_snapshot(ladle)
        rows.append({
            "ID": lid,
            "Temp (°C)": ladle["temperature"],
            "Stress": ladle["stress"],
            "Vibration": ladle["vibration"],
            "Location": ladle["location"],
            "Status": analysis["status"],
            "Recommendation": analysis["recommendation"]
        })
    df = pd.DataFrame(rows).set_index("ID")
    counts = df["Status"].value_counts().to_dict()
    c1, c2, c3, c4 = st.columns([1,1,1,2])
    c1.metric("Total ladles", len(df))
    c2.metric("Normal", counts.get("Normal", 0))
    c3.metric("Warning", counts.get("Warning", 0))
    c4.metric("Critical", counts.get("Critical", 0))
    st.markdown("### Ladle Status Table")
    st.dataframe(df, height=280)
    sel = st.selectbox("Select ladle for AI Analysis Panel", options=list(sim.keys()), index=0)
    ladle = sim[sel]
    analysis = analyze_ladle_snapshot(ladle)
    left, right = st.columns([3,2])
    with left:
        st.subheader(f"Ladle {sel} — {ladle['location']}")
        fig = go.Figure(go.Scatter(x=list(ladle["times"]), y=list(ladle["temps"]), mode="lines+markers", line=dict(color="orange")))
        fig.update_layout(yaxis_title="Temperature (°C)", xaxis_title="Time", margin=dict(t=30,l=10,r=10,b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"- **Temp:** {ladle['temperature']} °C")
        st.markdown(f"- **Stress:** {ladle['stress']}")
        st.markdown(f"- **Vibration:** {ladle['vibration']}")
        st.markdown(f"- **Location:** {ladle['location']}")
    with right:
        st.subheader("AI Analysis Panel")
        st.markdown(f"**Status:** {analysis['status']}")
        st.markdown(f"**Recommendation:** {analysis['recommendation']}")
        st.markdown(f"**Explanation:** {analysis['explanation']}")
        st.markdown("---")
        st.subheader("Alert Log (most recent)")
        for msg in list(st.session_state.alert_log)[:10]:
            st.markdown(f"- {msg}")

    if st.session_state.auto_refresh:
        st.experimental_rerun()
