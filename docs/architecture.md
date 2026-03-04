# System Architecture: TRAE-D-SME-Pricing

## 1. Overview
This document defines the architecture of the TRAE-D-SME-Pricing engine and clarifies implementation boundaries for interview/demo usage.

## 2. Implementation Boundary
- Implemented
  - Multi-source data simulation and feature engineering
  - Rule-based risk scoring and pricing recommendation
  - Explain output and audit log rendering
  - Streamlit dashboard interaction loop
- Simulated
  - mBridge settlement route recommendation
  - ISO 20022-compatible audit field mapping
- Planned
  - Production-grade banking data connectivity
  - HKMA FSS integration
  - MPC-based privacy-preserving computation at scale

## 3. End-to-End Data Flow

```mermaid
graph TD
    subgraph External Data (CDI-aligned)
        EComm[E-commerce Feed] --> Ingest[Data Ingestion]
        Customs[Customs/Tax Feed] --> Ingest
        Bank[Bank Flow Feed] --> Ingest
        Logistics[Logistics Feed] --> Ingest
    end

    subgraph TRAE Core
        Ingest --> FE[Feature Engineering]
        FE --> Scoring[Risk Scoring Engine]
        Scoring --> Pricing[Pricing Engine]
        Scoring --> Explain[Explainability Engine]
        Pricing --> Decision[Decision Composer]
        Explain --> Decision
    end

    subgraph Serving Layer
        Decision --> UI[Streamlit Dashboard]
        Decision --> Audit[Audit Log Store]
        Decision --> Monitor[Monitoring Metrics]
    end
```

## 4. Component Responsibilities

### 4.1 Data Ingestion & Feature Engineering
- Normalize inputs into unified merchant-level feature vectors.
- Validate freshness and completeness.
- Key features: `gmv_growth`, `refund_rate`, `collection_period`, `customs_alignment_score`.

### 4.2 Risk Scoring Engine
- Compute score in range 0-100.
- Apply configurable penalties for stale data and risk scenarios.
- Output score, grade, and hit rules.

### 4.3 Pricing Engine
- Map risk grade to recommended limit/rate bands.
- Return pricing plus reason codes for traceability.

### 4.4 Explainability Engine
- Generate analyst-facing natural language explanation.
- Include top contributing factors and triggered penalties.

### 4.5 Decision Composer
- Consolidate scoring + pricing + explain output.
- Mark decision status: `Auto-Approved`, `Manual Review`, or `Reject`.

### 4.6 Audit & Monitoring
- Persist request/response snapshots by request id.
- Track approval rate, review rate, expected delinquency, and latency.

## 5. Reliability and Controls
- Data quality gate before scoring.
- Graceful degradation when fields are missing.
- Versioned strategy config and rollback support.
- Full decision traceability for each assessment run.

## 6. Security and Compliance Notes
- Demo environment uses masked/sample data only.
- Audit schema is ISO 20022-compatible for demonstration; not a production payment message pipeline.
- Privacy statement included in decision logs.

## 7. Deployment (Demo)
- Runtime: Streamlit app
- Packaging: Python app with local config and sample datasets
- Intended usage: interview demonstration and product discussion
