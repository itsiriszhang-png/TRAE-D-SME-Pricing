# TRAE-D-SME-Pricing: Cross-border SME Risk Pricing Engine
# 跨境 SME 动态风险定价引擎 (TRAE 架构)

![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/streamlit-1.32-red)

## Overview / 概览

**TRAE-D-SME-Pricing** is a prototype fintech solution designed for the Hong Kong market, leveraging the **HKMA Commercial Data Interchange (CDI)** concept. It utilizes the **TRAE (Transform-Reason-Act-Explain)** agentic framework to provide real-time, explainable credit scoring and pricing for cross-border SMEs.

本项目是一个面向香港市场的金融科技原型，基于 **金管局商业数据通 (CDI)** 概念设计。它采用 **TRAE (Transform-Reason-Act-Explain)** 智能体框架，为跨境中小企业提供实时、可解释的信用评分与动态定价。

---

## Product Context / 产品背景

Aligned with **HKMA's Fintech 2030 Strategy** and the **Fintech Promotion Blueprint**, this project addresses the financing gap for SMEs. Traditional banks often lack visibility into cross-border e-commerce flows. This engine integrates alternative data (customs, logistics, payment flows) to enable:

响应 **HKMA 金融科技 2030 策略** 与 **金融科技推广路线图**，本项目旨在解决中小企业融资难点。传统银行缺乏对跨境电商流水的透视能力，本引擎通过整合替代数据（报关、物流、支付流），实现：

1.  **Data-Driven Decisions**: Replacing collateral-based lending with cash-flow-based lending.
2.  **Responsible AI**: Providing "Explainable AI" narratives for Relationship Managers (RMs) and auditors.
3.  **Dynamic Pricing**: Adjusting rates and limits based on real-time risk scenarios.

---

## The TRAE Framework / TRAE 框架

The system follows a four-stage cognitive process suitable for financial-grade AI:

系统遵循适用于金融级 AI 的四阶段认知流程：

1.  **Transform (数据转换)**: Ingests raw data from CDI (mocked) and normalizes it into feature vectors.
2.  **Reason (推理决策)**: Calculates a composite risk score using weighted logic and scenario analysis.
3.  **Act (行动执行)**: Maps risk scores to concrete pricing terms (Interest Rate, Credit Limit) and Risk Grades (A-D).
4.  **Explain (解释合规)**: Generates natural language narratives and audit logs (SHAP-like importance) for regulatory compliance.

---

## Key Features / 核心特性

### 🌐 ISO 20022 & mBridge Ready
The system is built on the **ISO 20022** data model.
*   **Audit Trails**: Generated in `camt.053` XML format with `<Strd>` remittance info for fraud prevention.
*   **Atomic Settlement**: High-quality SMEs (Grade A/B+) are automatically routed to **mBridge** for DLT-based real-time settlement, eliminating T+N delays.

### 🛡️ Privacy & MPC (HKMA Sandbox)
Aligned with **Gen.A.I. Sandbox** requirements:
*   **Data Minimization**: Supports Multi-Party Computation (MPC) patterns where only risk signals (not raw data) cross borders.
*   **Responsible AI**: Includes strict guardrails and "Human-in-the-loop" review triggers.

---

## Quick Start / 快速开始

### Prerequisites / 前置条件

- Python 3.9+
- pip

### Installation / 安装

```bash
# Clone the repository
git clone https://github.com/your-username/TRAE-D-SME-Pricing.git
cd TRAE-D-SME-Pricing

# Install dependencies
pip install -r requirements.txt
```

### Run the Demo / 运行演示

```bash
streamlit run ui_streamlit/app.py
```

Open your browser at `http://localhost:8501` to access the Pricing Pilot Dashboard.

---

## Impact / 业务价值

*   **Efficiency**: Reduces approval time from days to minutes. (审批时效：天 -> 分钟)
*   **Inclusion**: Increases approval rates for SMEs with thin credit files but strong cash flow. (普惠金融：覆盖征信薄弱但流水优质的企业)
*   **Risk Control**: Proactively identifies anomalies (e.g., sudden GMV spikes or collection delays). (主动风控：识别异常激增或回款延迟)

---

## Architecture / 架构设计

For a detailed technical view of the data flow and decision logic, please refer to the [Architecture Document](docs/architecture.md).

关于数据流向与决策逻辑的详细技术视图，请参阅 [架构文档](docs/architecture.md)。

---

## Directory Structure / 目录结构

```
TRAE-D-SME-Pricing/
├── agentic_ai/         # Orchestrator (Reasoning Loop)
├── data_pipeline/      # Mock Data Loader (CDI Interface)
├── pricing_model/      # Core Financial Logic (Engine)
├── explainability/     # XAI & Natural Language Generation
├── ui_streamlit/       # Frontend Dashboard
└── docs/               # Documentation
```
