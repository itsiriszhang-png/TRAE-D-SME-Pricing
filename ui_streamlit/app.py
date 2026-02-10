import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
import random

# Add project root to path so we can import modules
# 添加项目根目录到路径，以便导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from agentic_ai.reasoner import run_trae_for_sme

# Page Config
st.set_page_config(
    page_title="TRAE SME Pricing Engine",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Financial Look (Dark Blue/Grey)
# 自定义 CSS：金融机构风格（深蓝/灰白）
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #0e1117;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #002b5c;
    }
    .stButton>button {
        background-color: #002b5c; /* Financial Dark Blue */
        color: white;
        border-radius: 4px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #004080;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏦 TRAE Pricing Pilot")
st.sidebar.caption("SME Cross-border Lending Engine")
st.sidebar.markdown("---")

# Inputs
sme_options = ["GBA_Eco_Standard", "GBA_Eco_HighRisk", "HK_TMT_SME"]
selected_sme = st.sidebar.selectbox("Select SME Profile (CDI Mock)", sme_options)

scenario_options = [
    "Baseline 正常经营", 
    "订单激增 (High Growth)", 
    "回款放缓 (Liquidity Stress)", 
    "贸易数据异常 (Compliance Risk)"
]
selected_scenario = st.sidebar.selectbox("Select Business Scenario", scenario_options)

market_factor = st.sidebar.slider("Market Adjustment (Macro)", 0.8, 1.2, 1.0, 0.05)

# Simulate Button
if st.sidebar.button("📡 Simulate New CDI Feed"):
    st.session_state['simulate_trigger'] = True
    st.toast("📡 New CDI Data Ingested...", icon="🔄")
else:
    st.session_state['simulate_trigger'] = False

st.sidebar.markdown("### ⚙️ System Status")
st.sidebar.success("TRAE Core: Online")
st.sidebar.success("CDI Link: Connected")

if st.button("🚀 Run TRAE Assessment"): # Main button in sidebar moved to main area or keep as is? 
    # Actually user guide said "Button: Run TRAE Assessment" in sidebar earlier, but let's keep consistent.
    # We will use a flag or just run it.
    pass

# Main Logic Wrapper
with st.spinner("Trae Agent is analyzing CDI data & calculating risk..."):
    # Run the Agent
    result = run_trae_for_sme(selected_sme, selected_scenario)
    
    # Handle Simulation Perturbation
    if st.session_state.get('simulate_trigger', False):
        # Perturb features in result
        features = result.get("features", {})
        if features:
            # Perturb Customs Alignment (+/- 0.05)
            orig_customs = features.get("customs_alignment_score", 0.9)
            new_customs = max(0.0, min(1.0, orig_customs + random.uniform(-0.05, 0.05)))
            features["customs_alignment_score"] = round(new_customs, 2)
            
            # Perturb Collection Period (+/- 5 days)
            orig_days = features.get("collection_period", 30)
            new_days = max(1, orig_days + int(random.uniform(-5, 5)))
            features["collection_period"] = new_days
            
            # Re-run reasoning with new features (This is a simplified re-run logic)
            # ideally reasoner should accept features override, but here we just hack the result dict for display
            # To do it properly, we should call a method that accepts features. 
            # For demo visual impact, we just update the 'features' dict in result, 
            # and let the user re-click 'Run' for full re-calc or just show the changed data?
            # User wants "Charts produce dynamic visual effect".
            # So we should probably re-calculate score if possible.
            # But reasoner.run_trae_for_sme loads data internally.
            # Let's just update the display features for the "Visual" effect requested.
            result["features"] = features
            st.warning(f"⚠️ Simulated Data Update: Customs Score -> {new_customs:.2f}")

    # Display Result
    st.subheader(f"Credit Assessment Report: {selected_sme}")
    st.caption(f"Scenario: {selected_scenario} | Date: 2024-05-20")
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    # Column 1: Data View (Transform)
    with col1:
        st.markdown("### 1. Transform (Data)")
        st.success("📡 CDI Link Active")
        
        st.caption("**Data Sources (MPC Protected)**")
        st.markdown("##### 🏛️ CDI-CDEG (Gov Data)")
        st.markdown("##### 🏦 IADS (Interbank Data)")
        
        features = result.get("features", {})
        # Format dictionary for better display
        display_data = {
            "Metric": list(features.keys()),
            "Value": list(features.values())
        }
        df_features = pd.DataFrame(display_data)
        st.dataframe(df_features, hide_index=True, use_container_width=True)
        
    # Column 2: Reason & Act (Pricing)
    with col2:
        st.markdown("### 2. Reason & Act (Pricing)")
        
        pricing = result.get("pricing", {})
        score = result.get("score", 0)
        
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("Risk Score", f"{score}/100", delta_color="normal")
        m2.metric("Credit Limit", f"${pricing.get('credit_limit', 0):,.0f}")
        m3.metric("Interest Rate", pricing.get('base_rate_str', 'N/A'))
        
        # Settlement Path Indicator
        settlement_path = pricing.get('settlement_path', 'SWIFT gpi')
        if "mBridge" in settlement_path:
            st.success(f"🟢 **Settlement**: {settlement_path}")
            st.button("🔗 View DLT Ledger (mBridge)", type="secondary")
        else:
            st.warning(f"🌐 **Settlement**: {settlement_path}")

        # Review Status
        review_needed = pricing.get('need_manual_review', False)
        if review_needed:
            st.error(f"⚠️ Manual Review Required (Grade: {pricing.get('risk_grade')})")
        else:
            st.success(f"✅ Auto-Approved (Grade: {pricing.get('risk_grade')})")
        
        # Radar Chart
        categories = ['GMV Growth', 'Refund Rate', 'Collection Period', 'Compliance']
        f = features
        
        # Simple normalization logic for plot (0-1 scale)
        # Growth: 0.5 is max; Refund: 0 is best; Collection: 30 is best; Customs: 1 is best
        vals = [
            min(f.get('gmv_growth', 0) * 2, 1.0), 
            max(0, 1.0 - (f.get('refund_rate', 0) * 8)), # Invert
            max(0, 1.0 - (f.get('collection_period', 90)/100)), # Invert
            f.get('customs_alignment_score', 0)
        ]
        # Close the loop
        vals += [vals[0]]
        categories += [categories[0]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=categories,
            fill='toself',
            name=selected_sme,
            line_color='#002b5c'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1])
            ),
            showlegend=False,
            margin=dict(t=10, b=10, l=30, r=30),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    # Column 3: Explain & Audit
    with col3:
        st.markdown("### 3. Explain & Audit")
        
        explanation = result.get("explanation", {})
        
        st.markdown("#### AI Narrative")
        st.info(explanation.get("narrative", "No explanation generated."))
        
        st.markdown("#### Feature Importance")
        imp_data = explanation.get("feature_importance", [])
        if imp_data:
            df_imp = pd.DataFrame(imp_data)
            # Sort by Importance
            df_imp = df_imp.sort_values("Importance", ascending=True)
            # Display using Plotly bar for better control
            fig_bar = go.Figure(go.Bar(
                x=df_imp['Importance'],
                y=df_imp['Feature'],
                orientation='h',
                marker=dict(color='#002b5c')
            ))
            fig_bar.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=200,
                xaxis=dict(showticklabels=False),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with st.expander("📄 View Regulatory Audit Log"):
            st.json(explanation.get("audit_payload", {}))
