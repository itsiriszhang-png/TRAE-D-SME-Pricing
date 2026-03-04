# TRAE-D-SME-Pricing

Cross-border SME dynamic risk pricing demo aligned with HKMA CDI concepts.

## What This Project Does
- Ingests multi-source SME signals (bank flow, customs/tax, e-commerce, logistics).
- Computes a transparent risk score with configurable penalties.
- Recommends credit limit and pricing bands by risk grade.
- Produces explainable output and audit-ready decision logs.
- Visualizes the full loop in a Streamlit dashboard.

## Implementation Boundary
- Implemented:
  - Data simulation + feature engineering
  - Risk scoring + pricing recommendation
  - Explain output + audit log rendering
  - Dashboard interaction loop
- Simulated:
  - Settlement path suggestion (mBridge vs SWIFT gpi)
  - ISO 20022-compatible audit field mapping
- Planned:
  - Production banking data integration
  - HKMA FSS onboarding
  - MPC at production scale

## Quick Start
```bash
git clone https://github.com/itsiriszhang-png/TRAE-D-SME-Pricing.git
cd TRAE-D-SME-Pricing
pip install -r requirements.txt
streamlit run ui_streamlit/app.py
```

## Key Documents
- Product Requirements: `docs/PRD.md`
- Architecture: `docs/architecture.md`
- HKMA Alignment: `docs/hkma_mapping.md`
- Pitch Script: `docs/PITCH_SCRIPT.md`
- Deployment Guide: `DEPLOY.md`

## Repository Structure
```text
TRAE-D-SME-Pricing/
  agentic_ai/         # Orchestration and scoring logic
  data_pipeline/      # Mock CDI-like data loader
  pricing_model/      # Pricing decision engine
  explainability/     # Explain output + audit payload
  ui_streamlit/       # Streamlit dashboard
  docs/               # Product and architecture docs
```

## Disclaimer
This repository is a product demo for interview and learning purposes.
It does not represent production underwriting policy, legal advice, or compliance certification.
