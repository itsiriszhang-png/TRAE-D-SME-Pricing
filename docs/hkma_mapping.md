# HKMA Alignment Notes

This document explains how the demo maps to HKMA-relevant themes.

## 1. CDI Concept Alignment
- Uses a CDI-style approach to combine alternative data sources:
  - Bank flow (IADS-like)
  - Customs/tax (CDEG-like)
  - E-commerce and logistics signals
- Goal: evaluate SME risk beyond traditional collateral and static statements.

## 2. Responsible AI Alignment
- Human-in-the-loop path exists via `Manual Review Required`.
- Explain output includes key drivers, penalties, and decision rationale.
- Decision logs are traceable by request context and model/strategy version.

## 3. Privacy and Data Minimization
- Demo works on derived feature signals instead of raw transaction payloads.
- PII is not required for the scoring flow shown in this repository.
- MPC is treated as a future production architecture option, not a completed implementation.

## 4. Audit Interoperability
- Audit payload uses ISO 20022-compatible structure for demonstration.
- It is not a production payment-message integration.

## 5. Metric Mapping Table
| Metric | Business Meaning | Typical Source |
| :--- | :--- | :--- |
| `gmv_growth` | Operational momentum | E-commerce transactions |
| `refund_rate` | Trade quality risk | E-commerce platform/refund feed |
| `collection_period` | Cashflow resilience | Bank flow / receivable signals |
| `customs_alignment_score` | Compliance stability | Customs/tax feed |
| `data_freshness_days` | Data reliability | Ingestion metadata |
