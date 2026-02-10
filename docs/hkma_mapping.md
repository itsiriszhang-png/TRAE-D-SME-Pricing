# HKMA Regulatory Alignment & Gen.A.I. Sandbox

## Overview
This document details how **TRAE-D-SME-Pricing** aligns with the Hong Kong Monetary Authority (HKMA) standards, specifically focusing on the **GenA.I. Sandbox**, **CDI**, and **Data Privacy**.

---

## 1. Gen.A.I. Sandbox Alignment
Our architecture is specifically designed to meet the entry requirements for the HKMA Gen.A.I. Sandbox, focusing on "Responsible AI" and "Human-in-the-loop".

### A. Model Explainability (XAI)
The **Explain** module acts as a compliance layer between the AI reasoning core and the human decision-maker.
*   **Transparency**: Every credit decision is accompanied by a SHAP-based feature importance vector, ensuring no decision is a "black box".
*   **Narrative Generation**: The system generates natural language rationales (e.g., "Given high customs consistency...") that allow Relationship Managers to validate the AI's logic against their domain expertise.

### B. Risk Defense Mechanisms
To prevent AI hallucinations or bias, we implement strict guardrails:
*   **Deterministic Pricing**: While the *score* may be influenced by AI, the final *pricing* (Spread & Limit) is governed by deterministic rules in the `pricing_model`.
*   **Bias Monitoring**: The system explicitly tracks sensitive attributes (though not used in this demo) to ensure fair lending practices across different SME sectors.

---

## 2. Privacy & Data Minimization (MPC)
To address data privacy concerns in cross-border data sharing (e.g., GBA data crossing to HK), the system architecture supports **Multi-Party Computation (MPC)** principles.

*   **Data Minimization**: The `data_pipeline` is designed to ingest only *derived features* (e.g., "Customs Consistency Score") rather than raw transaction logs.
*   **Federated Logic**: Sensitive data (e.g., granular invoice details) remains on the **CDI-CDEG** (Government) or **IADS** (Interbank) nodes. Only the risk signals are transmitted to the pricing engine.
*   **Privacy-Preserving Computation**: The architecture allows for the risk score to be computed without the bank seeing the underlying raw data, satisfying **PDPO** (Personal Data (Privacy) Ordinance) requirements.

---

## 3. ISO 20022 Interoperability
The system's audit trails are native to **ISO 20022** standards, ensuring seamless integration with the global financial ecosystem.

*   **camt.053 Mapping**: The `audit_payload` is structured as a `BankToCustomerStatement`.
*   **Structured Remittance Info (`<Strd>`)**: We utilize the `<RmtInf>` tag to embed risk assessment metadata directly into the payment instruction/report. This allows the **mBridge** nodes to perform real-time AML/CFT checks based on the credit score attached to the settlement request.

---

## 4. Data Scoring Logic & Strategic Alignment
The following table outlines how technical risk metrics map to strategic business health indicators and their authoritative data sources within the HKMA ecosystem.

| 评分项 (Metric) | 战略对标 (Strategic Alignment) | 数据来源 (Data Source) |
| :--- | :--- | :--- |
| **GMV Growth** | 经营活力 (Operational Vitality) | CDI / 支付平台流水 |
| **Refund Rate** | 贸易真实性 (Trade Integrity) | 跨境电商 API / 退款指令 |
| **Collection Period** | 资金链韧性 (Cashflow Resilience) | IADS (银行间流水分享) |
| **Customs Compliance** | 监管合规 (Regulatory Alignment) | CDI-CDEG (海关/物流数据) |
| **Data Freshness** | 动态监控 (Real-time Resilience) | CDI 系统元数据时间戳 |
