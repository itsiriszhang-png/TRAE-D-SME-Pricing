import os
import random
import sys
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from agentic_ai.reasoner import run_trae_for_sme

st.set_page_config(
    page_title="TRAE SME Pricing Engine",
    page_icon="USD",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .stApp { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { color: #002b5c; }
    .stButton>button {
        background-color: #002b5c;
        color: white;
        border-radius: 4px;
        height: 2.8em;
        width: 100%;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #004080; color: white; }
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.title("TRAE Pricing Pilot")
st.sidebar.caption("Cross-border SME Risk Pricing Demo")
st.sidebar.markdown("---")

sme_options = ["GBA_Eco_Standard", "GBA_Eco_HighRisk", "HK_TMT_SME"]
selected_sme = st.sidebar.selectbox("SME Profile", sme_options)

scenario_options = [
    "Baseline",
    "High Growth",
    "Liquidity Stress",
    "Compliance Risk",
]
selected_scenario = st.sidebar.selectbox("Business Scenario", scenario_options)

market_factor = st.sidebar.slider("Market Adjustment", 0.8, 1.2, 1.0, 0.05)
_ = market_factor  # reserved for future use

simulate_clicked = st.sidebar.button("Simulate New CDI Feed")
st.sidebar.markdown("### System Status")
st.sidebar.success("TRAE Core: Online")
st.sidebar.success("CDI Link: Connected")

run_clicked = st.button("Run TRAE Assessment")

if run_clicked or "last_result" not in st.session_state:
    with st.spinner("Analyzing data and computing risk/pricing..."):
        result = run_trae_for_sme(selected_sme, selected_scenario)
        st.session_state["last_result"] = result
else:
    result = st.session_state["last_result"]

if not result:
    st.info("Select inputs and run the assessment.")
    st.stop()

if simulate_clicked:
    features = result.get("features", {})
    if features:
        features["customs_alignment_score"] = round(
            max(0.0, min(1.0, features.get("customs_alignment_score", 0.9) + random.uniform(-0.05, 0.05))), 2
        )
        features["collection_period"] = max(1, features.get("collection_period", 30) + int(random.uniform(-5, 5)))
        result["features"] = features
        st.warning("Simulated data update applied. Re-run to refresh full decision package.")

st.subheader(f"Credit Assessment Report: {selected_sme}")
st.caption(f"Scenario: {selected_scenario} | Date: {date.today().isoformat()}")

col1, col2, col3 = st.columns([1, 1.2, 1])
features = result.get("features", {})
pricing = result.get("pricing", {})
score = result.get("score", 0)

with col1:
    st.markdown("### 1. Transform (Data)")
    st.success("CDI Link Active")
    st.caption("Data Sources: CDI-CDEG, IADS, e-commerce, logistics")

    df_features = pd.DataFrame({"Metric": list(features.keys()), "Value": list(features.values())})
    st.dataframe(df_features, hide_index=True, use_container_width=True)

with col2:
    st.markdown("### 2. Reason & Act (Pricing)")
    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Score", f"{score}/100")
    m2.metric("Credit Limit", f"${pricing.get('credit_limit', 0):,.0f}")
    m3.metric("Interest Rate", pricing.get("base_rate_str", "N/A"))

    settlement_path = pricing.get("settlement_path", "SWIFT gpi")
    if "mBridge" in settlement_path:
        st.success(f"Settlement: {settlement_path}")
        st.button("View DLT Ledger (simulated)", type="secondary")
    else:
        st.warning(f"Settlement: {settlement_path}")

    if pricing.get("need_manual_review", False):
        st.error(f"Manual Review Required (Grade: {pricing.get('risk_grade')})")
    else:
        st.success(f"Auto-Approved (Grade: {pricing.get('risk_grade')})")

    categories = ["GMV Growth", "Refund Rate", "Collection Period", "Compliance"]
    vals = [
        min(features.get("gmv_growth", 0) * 2, 1.0),
        max(0, 1.0 - (features.get("refund_rate", 0) * 8)),
        max(0, 1.0 - (features.get("collection_period", 90) / 100)),
        features.get("customs_alignment_score", 0),
    ]
    vals += [vals[0]]
    categories += [categories[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(r=vals, theta=categories, fill="toself", name=selected_sme, line_color="#002b5c")
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        margin=dict(t=10, b=10, l=30, r=30),
        height=300,
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown("### 3. Explain & Audit")
    explanation = result.get("explanation", {})
    st.markdown("#### AI Narrative")
    st.info(explanation.get("narrative", "No explanation generated."))

    st.markdown("#### Feature Importance")
    imp_data = explanation.get("feature_importance", [])
    if imp_data:
        df_imp = pd.DataFrame(imp_data).sort_values("Importance", ascending=True)
        fig_bar = go.Figure(
            go.Bar(
                x=df_imp["Importance"],
                y=df_imp["Feature"],
                orientation="h",
                marker=dict(color="#002b5c"),
            )
        )
        fig_bar.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=220, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander("View Regulatory Audit Log"):
        st.json(explanation.get("audit_payload", {}))
