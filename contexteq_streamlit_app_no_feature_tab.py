
# ContextEQ — Where Ads and Brand Safety Meets Business Growth at Enterprise Scale
# Streamlit single-file product demo (dashboard-only, no Feature Matrix tab)
# Pages: Upload & Index • Safety Radar • Context Match • Creative Brief • Campaign Explainer • Real-Time Bot
# Notes:
# - Works in Demo Mode without API keys (uses sample data)
# - Replace `call_video_api` with a real provider (e.g., TwelveLabs) for live integration.

import os
import io
import time
import json
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =======================
# App Config & Styling
# =======================
st.set_page_config(page_title="ContextEQ — Contextual & Safe Video Intelligence", page_icon="🎬", layout="wide")

APP_NAME = "ContextEQ"
DEMO_MODE = st.session_state.get("DEMO_MODE", True)

CUSTOM_CSS = '''
<style>
.small { font-size:0.9rem; color:#6b7280; }
.kpi { font-weight:700; font-size:1.1rem; }
.card { padding:1rem; border:1px solid rgba(148,163,184,0.28); border-radius:12px; background:rgba(255,255,255,0.65); }
.badge { display:inline-block; padding:.2rem .5rem; border-radius:999px; border:1px solid rgba(148,163,184,0.32); margin-right:.35rem; }
code { background:#f4f6f8; padding:.15rem .35rem; border-radius:6px; }
</style>
'''
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =======================
# Sidebar
# =======================
with st.sidebar:
    st.title("🎬 ContextEQ")
    st.caption("Where Ads & Brand Safety Meets Business Growth at Enterprise Scale")
    st.divider()
    api_key = st.text_input("Video Intelligence API Key (optional)", type="password", help="Leave empty to run in Demo Mode with sample data.")
    DEMO_MODE = (api_key == "")
    st.session_state["DEMO_MODE"] = DEMO_MODE
    if DEMO_MODE:
        st.markdown("**Mode:** Demo (sample data)")
    else:
        st.markdown("**Mode:** Live API")
    st.divider()
    st.markdown("**Dashboard**")
    st.markdown("- Upload & Index\n- Safety Radar\n- Context Match\n- Creative Brief\n- Campaign Explainer\n- Real-Time Bot")
    st.divider()
    st.markdown("<span class='small'>Tip: Replace the placeholders in `call_video_api` to integrate a real provider.</span>", unsafe_allow_html=True)

# =======================
# Helpers & Demo Data
# =======================

def load_demo_json(name: str) -> Dict[str, Any]:
    samples = {
        "analyze": {
            "video_id": "vid_demo_001",
            "brand_safety_score": 0.84,
            "flags": [
                {"label":"mild_violence","start":"00:23","end":"00:27","evidence":"crowd push", "severity":"low"},
                {"label":"sarcasm_audio","start":"00:54","end":"00:59","evidence":"voice tone", "severity":"low"}
            ],
            "objects":[
                {"label":"logo_visible","start":"00:12","end":"00:18"},
                {"label":"smiling_people","start":"00:30","end":"00:37"},
                {"label":"soccer_ball","start":"00:44","end":"00:47"}
            ],
            "emotions":[
                {"label":"joy","start":"00:30","end":"00:37"},
                {"label":"excitement","start":"00:44","end":"00:47"}
            ],
            "summary":"Energetic outdoor scenes with smiling people, a visible brand logo early on, and a short sports moment."
        },
        "search": {
            "query":"sports",
            "matches":[
                {"start":"00:41","end":"00:49","confidence":0.91,"evidence":"soccer play, cheering"},
                {"start":"01:18","end":"01:27","confidence":0.86,"evidence":"stadium crowd, fast motion"}
            ]
        },
        "kpi": [
            {"moment":"logo_visible@00:12-00:18","CTR":2.8,"Retention":42,"ROAS":1.4},
            {"moment":"smile@00:30-00:37","CTR":3.4,"Retention":57,"ROAS":1.8},
            {"moment":"sports@00:44-00:47","CTR":3.1,"Retention":51,"ROAS":1.6}
        ]
    }
    return samples.get(name, {})

def call_video_api(endpoint: str, payload: Dict[str, Any], api_key: Optional[str]) -> Dict[str, Any]:
    # Demo response (replace with real API wiring)
    time.sleep(0.6)
    if endpoint == "analyze":
        return load_demo_json("analyze")
    if endpoint == "search":
        out = load_demo_json("search")
        out["query"] = payload.get("query", out.get("query"))
        return out
    if endpoint == "embed":
        return {"vector":[random.random() for _ in range(16)]}
    return {"ok": True}

# =======================
# Header & Tabs
# =======================
st.title("ContextEQ — Where Ads and Brand Safety Meets Business Growth at Enterprise Scale")
st.markdown("**AI-powered contextual and safety intelligence for video advertising — with explainable insights, creative acceleration, and ROI mapping.**")

tabs = st.tabs(["Upload & Index","Safety Radar","Context Match","Creative Brief","Campaign Explainer","Real-Time Bot"])

# =======================
# Upload & Index
# =======================
with tabs[0]:
    st.subheader("Upload & Index")
    st.markdown("Upload a video asset and create an index for analysis, search, and embeddings.")
    uploaded = st.file_uploader("Upload a video file", type=["mp4","mov","mkv","webm"])
    col1, col2 = st.columns(2)
    with col1:
        model_id = st.text_input("Model (example)", "marengo-2.7")
    with col2:
        st.text_input("Library / Index Name", "default-library")
    if st.button("Create Index"):
        st.success("Index job created.")
        st.json({"video_id":"vid_demo_001","model":model_id,"status":"indexed"})

# =======================
# Safety Radar
# =======================
with tabs[1]:
    st.subheader("Safety Radar — Brand Safety & Suitability")
    st.caption("Automated detection with transparent, time-stamped evidence.")
    payload = {"video_id":"vid_demo_001","tasks":["safety","summary","objects","emotions"]}
    if st.button("Run Safety Analysis"):
        res = call_video_api("analyze", payload, st.session_state.get("api_key"))
        st.metric("Brand Safety Score", f"{int(res.get('brand_safety_score',0)*100)}%")
        st.markdown("**Summary**")
        st.write(res.get("summary",""))
        st.markdown("**Flags**")
        flags = res.get("flags", [])
        if len(flags)==0:
            st.success("No issues detected.")
        else:
            for f in flags:
                with st.expander(f"⚠️ {f['label']} • {f['start']}–{f['end']} (severity: {f['severity']})"):
                    st.write(f"Evidence: {f['evidence']}")
        st.markdown("**Detected Objects & Emotions**")
        colA, colB = st.columns(2)
        with colA:
            st.json(res.get("objects", []))
        with colB:
            st.json(res.get("emotions", []))

# =======================
# Context Match
# =======================
with tabs[2]:
    st.subheader("Context Match — Find the Best Scenes for Placement")
    st.caption("Semantic search over video to suggest high-fit moments.")
    query = st.text_input("Context query (e.g., 'sports', 'family', 'outdoor')", value="sports")
    if st.button("Search Scenes"):
        res = call_video_api("search", {"video_id":"vid_demo_001","query":query}, st.session_state.get("api_key"))
        matches = res.get("matches", [])
        if matches:
            st.success(f"Found {len(matches)} scene(s) for '{query}'.")
            st.json(matches)
        else:
            st.warning("No scenes found for this query. Try another term.")

# =======================
# Creative Brief
# =======================
with tabs[3]:
    st.subheader("Creative Brief — Scene-by-Scene Intelligence")
    st.caption("Accelerate production and A/B testing with AI-generated briefs.")
    res = load_demo_json("analyze")
    brief_rows = []
    for o in res["objects"]:
        brief_rows.append({"Type":"Object","Label":o["label"],"Start":o["start"],"End":o["end"],"Notes":"Potential brand cue"})
    for e in res["emotions"]:
        brief_rows.append({"Type":"Emotion","Label":e["label"],"Start":e["start"],"End":e["end"],"Notes":"Positive audience resonance"})
    brief_df = pd.DataFrame(brief_rows)
    st.dataframe(brief_df, use_container_width=True)
    st.markdown("**Suggested A/B Test Ideas**")
    st.markdown("- Cut A: Emphasize early logo visibility (00:12–00:18)")
    st.markdown("- Cut B: Highlight smiling crowd (00:30–00:37)")
    st.markdown("- Cut C: Sports action hook (00:44–00:47)")

# =======================
# Campaign Explainer
# =======================
with tabs[4]:
    st.subheader("Campaign Explainer — Map Moments to KPIs")
    st.caption("Explain *why* a campaign worked by linking scenes to CTR/Retention/ROAS.")
    kpi = pd.DataFrame(load_demo_json("kpi"))
    st.dataframe(kpi, use_container_width=True)
    metric = st.selectbox("Metric to visualize", ["CTR","Retention","ROAS"])
    fig, ax = plt.subplots()
    ax.bar(kpi["moment"], kpi[metric])
    ax.set_xlabel("Moment")
    ax.set_ylabel(metric)
    ax.set_title(f"{metric} by Video Moment")
    st.pyplot(fig, clear_figure=True)
    st.markdown("<span class='small'>Insight: smiling people segment shows highest Retention; early logo aligns with CTR lift.</span>", unsafe_allow_html=True)

# =======================
# Real-Time Bot
# =======================
with tabs[5]:
    st.subheader("Real-Time Intelligence Bot")
    st.caption("Automatically analyze new uploads and return safety/context scores.")
    st.markdown("**Drop a new file to simulate real-time analysis**")
    new_file = st.file_uploader("New asset (simulate)", type=["mp4","mov","mkv","webm"], key="rt_upload")
    if st.button("Analyze New Upload"):
        st.info("Processing…")
        time.sleep(0.8)
        res = call_video_api("analyze", {"video_id":"vid_new_001","tasks":["safety","summary"]}, st.session_state.get("api_key"))
        st.success("Analysis complete.")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Safety Score", f"{int(res.get('brand_safety_score',0)*100)}%")
        with col2:
            st.write("Top Contexts: ", ", ".join(sorted(set([o['label'] for o in res.get('objects',[])]))))
        with st.expander("Details"):
            st.write(res.get("summary",""))
            st.json(res.get("flags", []))

st.divider()
st.caption("© {} ContextEQ • AI-powered contextual & safety intelligence for video advertising".format(datetime.now().year))
