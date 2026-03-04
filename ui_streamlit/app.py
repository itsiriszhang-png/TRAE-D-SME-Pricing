import os
import random
import sys
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from agentic_ai.reasoner import run_trae_for_sme
from pricing_model.engine import compute_pricing


st.set_page_config(
    page_title="TRAE-D-SME Pricing Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg: #f4f6fb;
    --panel: #ffffff;
    --ink: #0f1b2d;
    --muted: #5e6b82;
    --brand: #0f4c81;
    --brand-2: #1aa3a3;
    --good: #1f9d55;
    --warn: #c77900;
    --bad: #c53030;
}

.stApp {
    background:
      radial-gradient(1100px 320px at 10% -20%, #dceeff 10%, transparent 50%),
      radial-gradient(1000px 300px at 90% -30%, #dcfff4 10%, transparent 55%),
      var(--bg);
    color: var(--ink);
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 0.2px;
}

p, li, label, div, span {
    font-family: 'Space Grotesk', sans-serif;
}

code {
    font-family: 'JetBrains Mono', monospace;
}

.hero {
    padding: 1rem 1.2rem;
    border-radius: 16px;
    background: linear-gradient(120deg, #0f4c81 0%, #11698e 45%, #1aa3a3 100%);
    color: white;
    margin-bottom: 0.6rem;
    box-shadow: 0 12px 30px rgba(15, 76, 129, 0.16);
}

.hero .title {
    font-size: 1.45rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.hero .sub {
    opacity: 0.95;
    font-size: 0.95rem;
}

.kpi {
    background: var(--panel);
    border-radius: 14px;
    border: 1px solid #e5ebf5;
    padding: 0.75rem 0.9rem;
    box-shadow: 0 8px 24px rgba(15, 27, 45, 0.04);
}

.caption-chip {
    display: inline-block;
    font-size: 0.77rem;
    color: #15446b;
    background: #eaf4ff;
    border: 1px solid #d5e8fb;
    border-radius: 999px;
    padding: 0.18rem 0.5rem;
    margin-right: 0.35rem;
}

.section {
    background: var(--panel);
    border: 1px solid #e5ebf5;
    border-radius: 16px;
    padding: 0.9rem 1rem;
    box-shadow: 0 8px 24px rgba(15, 27, 45, 0.04);
}

.small-note {
    color: var(--muted);
    font-size: 0.82rem;
}

.block-good {
    border-left: 4px solid var(--good);
    background: #f2fbf6;
    padding: 0.7rem 0.8rem;
    border-radius: 8px;
}

.block-warn {
    border-left: 4px solid var(--warn);
    background: #fff7ea;
    padding: 0.7rem 0.8rem;
    border-radius: 8px;
}

.block-bad {
    border-left: 4px solid var(--bad);
    background: #fff1f1;
    padding: 0.7rem 0.8rem;
    border-radius: 8px;
}

.stButton > button {
    border-radius: 10px;
    border: 0;
    background: linear-gradient(120deg, #0f4c81 0%, #11698e 100%);
    color: white;
    font-weight: 600;
}

.stButton > button:hover {
    filter: brightness(1.06);
}

div[data-testid="stMetricValue"] {
    font-size: 2.0rem;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <div class="title">TRAE-D-SME Pricing Studio</div>
  <div class="sub">Cross-border SME Risk Decision Demo · Transform -> Reason -> Act -> Explain</div>
</div>
""",
    unsafe_allow_html=True,
)

st.sidebar.header("Simulation Controls")
profile = st.sidebar.selectbox(
    "SME Profile",
    ["GBA_Eco_Standard", "GBA_Eco_HighRisk", "HK_TMT_SME"],
)
scenario = st.sidebar.selectbox(
    "Business Scenario",
    ["Baseline", "High Growth", "Liquidity Stress", "Compliance Risk"],
)
macro = st.sidebar.slider("Macro Multiplier", 0.80, 1.20, 1.00, 0.05)
noise_toggle = st.sidebar.toggle("Inject Data Jitter", value=False)
noise_seed = st.sidebar.number_input("Noise Seed", min_value=0, max_value=9999, value=2026, step=1)

st.sidebar.markdown("---")
st.sidebar.caption("Model Boundary")
st.sidebar.markdown("- Implemented: scoring, pricing, explain, audit")
st.sidebar.markdown("- Simulated: settlement route mapping")

run = st.sidebar.button("Run Assessment", use_container_width=True)

if "history" not in st.session_state:
    st.session_state.history = []

input_signature = (profile, scenario, macro, noise_toggle, int(noise_seed))
input_changed = st.session_state.get("last_input_signature") != input_signature

if run or "result" not in st.session_state or input_changed:
    base_result = run_trae_for_sme(profile, scenario)
    if "error" in base_result:
        st.error(base_result["error"])
        st.stop()

    features = dict(base_result.get("features", {}))
    raw_score = float(base_result.get("score", 0.0))

    if noise_toggle:
        random.seed(noise_seed)
        features["customs_alignment_score"] = round(
            max(0.0, min(1.0, features.get("customs_alignment_score", 0.8) + random.uniform(-0.06, 0.06))), 2
        )
        features["collection_period"] = max(1, int(features.get("collection_period", 30) + random.uniform(-6, 6)))
        features["refund_rate"] = round(
            max(0.0, min(0.30, features.get("refund_rate", 0.05) + random.uniform(-0.015, 0.018))), 3
        )

    adjusted_score = max(0.0, min(100.0, round(raw_score * macro, 1)))

    pricing = compute_pricing(
        score=adjusted_score,
        scenario=scenario,
        data_freshness_days=int(features.get("data_freshness_days", 0)),
        sme_size_factor=1.0,
    )

    result = dict(base_result)
    result["features"] = features
    result["score_raw"] = raw_score
    result["score"] = adjusted_score
    result["pricing"] = {
        "credit_limit": pricing.credit_limit,
        "base_rate_str": pricing.base_rate_str,
        "risk_grade": pricing.risk_grade,
        "need_manual_review": pricing.need_manual_review,
        "settlement_path": pricing.settlement_path,
    }

    st.session_state.result = result
    st.session_state.last_input_signature = input_signature
    st.session_state.history.append(
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "profile": profile,
            "scenario": scenario,
            "score": adjusted_score,
            "grade": pricing.risk_grade,
            "review": "Yes" if pricing.need_manual_review else "No",
            "limit": pricing.credit_limit,
            "rate": pricing.base_rate_str,
        }
    )

result = st.session_state.result
pricing = result["pricing"]
score = result["score"]

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown('<div class="kpi">Risk Score</div>', unsafe_allow_html=True)
    st.metric("Risk Score", f"{score:.1f}/100", delta=f"raw {result.get('score_raw', score):.1f}", label_visibility="collapsed")
with c2:
    st.markdown('<div class="kpi">Risk Grade</div>', unsafe_allow_html=True)
    st.metric("Risk Grade", pricing["risk_grade"], label_visibility="collapsed")
with c3:
    st.markdown('<div class="kpi">Credit Limit</div>', unsafe_allow_html=True)
    st.metric("Credit Limit", f"${pricing['credit_limit']/1_000_000:.1f}M", label_visibility="collapsed")
    st.caption(f"Full: ${pricing['credit_limit']:,.0f}")
with c4:
    st.markdown('<div class="kpi">Pricing</div>', unsafe_allow_html=True)
    st.metric("Pricing", pricing["base_rate_str"], label_visibility="collapsed")
    st.caption(f"Full: {pricing['base_rate_str']}")
with c5:
    st.markdown('<div class="kpi">Manual Review</div>', unsafe_allow_html=True)
    st.metric("Manual Review", "Yes" if pricing["need_manual_review"] else "No", label_visibility="collapsed")
    st.caption("Yes = Analyst Review Gate")

st.markdown(
    '<span class="caption-chip">Profile: {}</span><span class="caption-chip">Scenario: {}</span><span class="caption-chip">Macro: {:.2f}x</span>'.format(
        profile, scenario, macro
    ),
    unsafe_allow_html=True,
)

with st.expander("PRD Alignment (Scoring -> Pricing Matrix)", expanded=False):
    base_score = result.get("base_score", score)
    penalties = result.get("penalties", [])
    st.markdown(f"- Base Score (from derived features): `{base_score:.1f}`")
    if penalties:
        for p in penalties:
            st.markdown(f"- Penalty: `{p['name']}` => `{p['delta']}`")
    else:
        st.markdown("- Penalty: `None`")
    st.markdown(f"- Final Score: `{score:.1f}`")
    st.markdown("- Pricing Matrix: `A>=90`, `B=80-89`, `C=65-79`, `D<65`")
    st.markdown("- Limit Bands: `A 8-12M`, `B 4-8M`, `C 1-4M`, `D <=2.5M`")

left, right = st.columns([1.15, 1])

with left:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("Decision Cockpit")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " /100"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#0f4c81"},
                "steps": [
                    {"range": [0, 65], "color": "#fde8e8"},
                    {"range": [65, 80], "color": "#fff4d6"},
                    {"range": [80, 90], "color": "#e7f8ef"},
                    {"range": [90, 100], "color": "#d9f3ff"},
                ],
                "threshold": {"line": {"color": "#1aa3a3", "width": 4}, "value": 90},
            },
        )
    )
    gauge.update_layout(height=280, margin=dict(l=20, r=20, t=20, b=0))
    st.plotly_chart(gauge, use_container_width=True)

    features = result.get("features", {})
    radar_categories = ["GMV Growth", "Refund Quality", "Collection Speed", "Compliance"]
    radar_values = [
        min(features.get("gmv_growth", 0) * 2, 1.0),
        max(0, 1.0 - (features.get("refund_rate", 0) * 8)),
        max(0, 1.0 - (features.get("collection_period", 90) / 100.0)),
        features.get("customs_alignment_score", 0),
    ]
    radar_values += [radar_values[0]]
    radar_categories += [radar_categories[0]]

    radar = go.Figure()
    radar.add_trace(
        go.Scatterpolar(r=radar_values, theta=radar_categories, fill="toself", line=dict(color="#11698e", width=2))
    )
    radar.update_layout(
        showlegend=False,
        polar={"radialaxis": {"visible": True, "range": [0, 1]}, "angularaxis": {"tickfont": {"size": 13}}},
        height=320,
        margin=dict(l=40, r=40, t=20, b=30),
    )
    st.plotly_chart(radar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("Action and Controls")

    settlement = pricing["settlement_path"]
    if pricing["need_manual_review"]:
        st.markdown("<div class='block-bad'><b>Decision:</b> Manual Review Required</div>", unsafe_allow_html=True)
    elif pricing["risk_grade"] in ["A", "B"]:
        st.markdown("<div class='block-good'><b>Decision:</b> Auto-Approved</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='block-warn'><b>Decision:</b> Conditional Approval</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown(f"**Settlement Path:** `{settlement}`")
    st.markdown(f"**Suggested Limit:** `${pricing['credit_limit']:,.0f}`")
    st.markdown(f"**Suggested Rate:** `{pricing['base_rate_str']}`")

    st.write("")
    st.caption("Input feature snapshot")
    df_features = pd.DataFrame(
        {
            "feature": list(features.keys()),
            "value": [str(v) for v in features.values()],
        }
    )
    st.dataframe(df_features, use_container_width=True, hide_index=True, height=240)
    st.markdown("</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Explainability", "CDI Data Trace", "Audit Log", "Run History"])

with tab1:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("Explainability View")
    explanation = result.get("explanation", {})
    st.info(explanation.get("narrative", "No explanation generated."))

    imp = explanation.get("feature_importance", [])
    if imp:
        df_imp = pd.DataFrame(imp)
        if "Contribution" in df_imp.columns:
            fig = px.bar(
                df_imp.sort_values("Contribution"),
                x="Contribution",
                y="Feature",
                orientation="h",
                color="Direction",
                color_discrete_map={"Positive": "#1f9d55", "Negative": "#c53030"},
                height=320,
            )
            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("CDI Source Data and Feature Lineage")
    st.caption("This section shows how bank flow, e-commerce flow, customs/tax and logistics signals are transformed into risk features.")

    source_data = result.get("cdi_sources", {})
    lineage = result.get("feature_lineage", [])

    if source_data:
        for source_name, source_metrics in source_data.items():
            st.markdown(f"**{source_name}**")
            source_df = pd.DataFrame([{"metric": k, "value": v} for k, v in source_metrics.items()])
            st.dataframe(source_df, use_container_width=True, hide_index=True, height=140)

    if lineage:
        st.markdown("**Derived Feature Mapping**")
        st.dataframe(pd.DataFrame(lineage), use_container_width=True, hide_index=True, height=220)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("Regulatory Audit Payload")
    st.json(result.get("explanation", {}).get("audit_payload", {}))
    st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("Scenario Run History")
    history = pd.DataFrame(st.session_state.history)
    st.dataframe(history.iloc[::-1], use_container_width=True, hide_index=True, height=260)
    st.markdown(
        "<div class='small-note'>Tip: show this table in interviews to demonstrate scenario-based stress testing and product iteration thinking.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
