# System Architecture: TRAE SME Pricing Engine

## Overview
This document outlines the architecture of the TRAE-D-SME-Pricing engine, demonstrating how it aligns with the HKMA Commercial Data Interchange (CDI) initiative and Responsible AI principles.

## Data Flow Diagram (Mermaid)

```mermaid
graph TD
    subgraph "External Ecosystem (CDI)"
        E_Comm[E-commerce Platform] --> CDI[Commercial Data Interchange]
        Customs[Customs/Logistics] --> CDI
        Bank[Bank Internal Data] --> CDI
    end

    subgraph "TRAE Intelligence Core"
        CDI --> |JSON/API| Transform[Transform: Feature Engineering]
        Transform --> |Feature Vector| Reason[Reason: Risk Scoring Model]
        
        Reason --> |Risk Score| Act[Act: Pricing Engine]
        Reason --> |Score & Features| Explain[Explain: XAI Module]
        
        Act --> |Limit & Rate| Decision[Final Decision Package]
        Explain --> |Narrative & Audit| Decision
    end

    subgraph "User Interface & Consumption"
        Decision --> |Display| UI[Streamlit Dashboard]
        Decision --> |Log| Audit[Regulatory Audit Log]
    end
    
    style CDI fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Reason fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style Act fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Explain fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
```

## Component Details

### 1. Transform (Data Pipeline)
*   **Role**: Simulates the ingestion of alternative data via CDI.
*   **Key Metrics**: GMV Growth, Refund Rate, Collection Period, Customs Alignment.
*   **HKMA Alignment**: Demonstrates the use of "Alternative Data" to assess creditworthiness beyond traditional financial statements.

### 2. Reason & Act (Decision Engine)
*   **Reasoning**: A weighted scoring model that evaluates business health and compliance.
*   **Action**: Maps scores to standardized risk grades (A-D) and pricing terms (Spread over Prime).
*   **Logic**:
    *   **Grade A**: Prime + 1.5% (High Quality)
    *   **Grade C/D**: Prime + 3.8%+ (Watch List)
    *   **Manual Review**: Triggered by high risk or anomalies.

### 3. Explain (Responsible AI)
*   **Role**: Ensures the "Black Box" is transparent.
*   **Output**:
    *   **RM Narrative**: Natural language explanation for relationship managers.
    *   **Feature Importance**: Quantifies which factors drove the decision (Global/Local interpretability).
    *   **Audit Payload**: Immutable record of the decision context for regulatory review.

## Future Evolution (Roadmap)

*   **Sandbox**: Deploy to HKMA Fintech Supervisory Sandbox (FSS) for pilot testing with real bank data.
*   **Model Upgrade**: Replace rule-based scoring with Gradient Boosting (XGBoost) or LLM-based reasoning for unstructured data.
*   **Live CDI**: Connect to live CDI APIs via API Gateway.
