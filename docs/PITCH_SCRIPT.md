# Interview Pitch Script (TRAE-D-SME-Pricing)

## 1) 30-second opening
I built a cross-border SME risk-pricing demo aligned with HKMA CDI concepts.
It converts multi-source operational signals into explainable risk and pricing decisions,
with a clear manual-review fallback for higher-risk cases.

## 2) 90-second walkthrough
- Transform: ingest bank flow, customs/tax, e-commerce, and logistics-like data.
- Reason: compute a transparent 0-100 risk score with scenario penalties.
- Act: map score to grade and return limit/rate recommendation.
- Explain: output key drivers, reason codes, and audit payload.
- UI: show end-to-end decision flow in Streamlit.

## 3) What is implemented vs simulated
- Implemented: scoring, pricing, explainability, and dashboard.
- Simulated: mBridge route suggestion and ISO 20022-compatible mapping.
- Planned: production data integration and FSS onboarding.

## 4) Impact framing
- Faster decision support for SME credit review.
- Better transparency for product, risk, and audit stakeholders.
- Clear iteration loop via traceable decisions and configurable thresholds.

## 5) Likely follow-up answer
If asked ?is this production-ready??, answer:
"No, this is an interview-grade MVP focused on product logic, explainability, and controllability.
The next step is small-scale pilot data validation and threshold calibration."
