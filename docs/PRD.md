# 产品需求文档 (PRD): TRAE-D-SME-Pricing 跨境中小企业智能风险定价引擎

| 版本 | 日期 | 作者 | 更新内容 | 状态 |
| :--- | :--- | :--- | :--- | :--- |
| v1.0 | 2024-05-20 | TRAE Assistant | 初始版本 (MVP) | 已发布 |

---

## 1. 功能背景 (Context)

### 1.1 问题陈述
香港作为国际金融中心，众多跨境中小企业（SME）面临“融资难、融资贵”的痛点。传统银行依赖财务报表和抵押品进行信贷评估，而跨境电商等新兴 SME 往往缺乏这些传统资产，但拥有丰富的流水和海关数据。银行缺乏有效的手段将这些“替代数据”转化为可信的风险评估。

### 1.2 目标与价值
构建一套基于 **HKMA CDI (商业数据通)** 理念的智能风险定价引擎，利用 **TRAE (Transform-Reason-Act-Explain)** 框架，实现：
1.  **数据驱动授信**：整合海关、电商、支付流等多源数据，替代传统财报。
2.  **动态精准定价**：根据实时风险场景（如回款延迟、合规度）动态调整利率和额度。
3.  **合规可解释性**：提供符合 HKMA GenAI Sandbox 要求的模型解释（XAI）和 ISO 20022 审计日志。
4.  **原子结算能力**：针对优质客户，通过 mBridge (DLT) 实现资金实时跨境结算。

---

## 2. 用户场景 (User Scenarios)

### 场景一：优质电商企业的快速获批
*   **用户**：一家在深圳运营、通过香港收款的成熟跨境电商（类似 `GBA_Eco_Standard`）。
*   **情境**：企业近期海关申报规范，流水稳定增长，急需资金备货旺季。
*   **流程**：RM（客户经理）在系统输入 SME ID -> 系统拉取 CDI 数据 -> **Reasoning** 引擎判定为 Grade A -> **Act** 引擎自动批核 800万额度，利率 Prime+1.5% -> **Explain** 模块提示“海关一致性高” -> 系统推荐走 **mBridge** 结算通道。

### 场景二：异常交易的风控拦截
*   **用户**：一家新注册的贸易公司（类似 `GBA_Eco_HighRisk`）。
*   **情境**：交易量突然翻倍，但回款周期拉长至 85 天。
*   **流程**：系统检测到“GMV 激增”但“数据滞后 45 天” -> **Reasoning** 引擎扣除新鲜度分数 -> **Act** 引擎降级为 Grade C，触发“人工复核” -> **Explain** 模块警示“数据陈旧且回款异常” -> 系统拒绝自动放款，建议走 SWIFT gpi 并加强尽职调查。

---

## 3. 需求描述 (Functional Requirements)

### 3.1 数据转换层 (Transform)
*   **R-001 多源数据接入**：系统需支持从模拟的 CDI 接口接入数据，包括：
    *   IADS (银行间账户数据)：流水、余额。
    *   CDI-CDEG (海关数据)：报关单量、退税率。
*   **R-002 特征工程**：自动计算关键风控指标，包括 `gmv_growth` (GMV增长率), `refund_rate` (退款率), `collection_period` (回款周期), `customs_alignment_score` (海关一致性)。
*   **R-003 数据新鲜度校验**：系统需检查数据时间戳，若 `data_freshness_days > 30`，自动标记为“Stale Data”。

### 3.2 智能决策层 (Reason & Act)
*   **R-004 动态评分模型**：基于加权规则计算 0-100 信用分。
    *   新鲜度惩罚：陈旧数据扣 5 分。
    *   场景调整：检测到“Liquidity Stress”场景扣分。
*   **R-005 定价矩阵**：
    *   **Grade A (Score >= 90)**: Limit ~8-12M, Rate Prime+1.5%, **Settlement: mBridge**.
    *   **Grade B/B+**: Limit ~4-8M, Rate Prime+2.0-2.8%.
    *   **Grade C/D**: Limit < 4M, Rate Prime+3.8%+, **Need Manual Review**.

### 3.3 可解释性与合规 (Explain)
*   **R-006 自然语言解释 (NLG)**：为每笔定价生成面向 RM 的英文解释，包含 "Gone Fintech", "Responsible AI" 等战略术语。
*   **R-007 MPC 隐私声明**：在解释中明确标注计算过程采用了 MPC 技术，原始数据未出库。
*   **R-008 ISO 20022 审计**：生成的 Audit Payload 必须符合 `camt.053` 标准，包含 `<RmtInf><Strd>` 标签以携带风控元数据。

### 3.4 前端交互 (UI)
*   **R-009 实时模拟**：提供 "Simulate New CDI Feed" 按钮，支持用户手动触发数据更新，图表需实时响应。
*   **R-010 结算路径可视化**：对于 mBridge 路径，使用绿色高亮标识，并提供 "View DLT Ledger" 模拟入口。

---

## 4. 验收标准 (Acceptance Criteria)

### AC-001: 优质客户的自动化流程
*   **Given**: 选择样本 `GBA_Eco_Standard` (Grade A)，场景为 "Baseline"。
*   **When**: 点击 "Run TRAE Assessment"。
*   **Then**:
    *   风险评分应 > 85 分。
    *   显示 "Auto-Approved"。
    *   结算路径显示为绿色的 "mBridge (DLT Atomic Settlement)"。
    *   AI 解释中包含 "Gone Fintech" 关键词。

### AC-002: 数据滞后的风控惩罚
*   **Given**: 选择样本 `GBA_Eco_HighRisk`，其数据新鲜度设置为 45 天。
*   **When**: 点击 "Run TRAE Assessment"。
*   **Then**:
    *   风险评分应受到 "Data Freshness" 惩罚（例如扣 5 分）。
    *   定价结果显示 "Manual Review Required"。
    *   结算路径回退为 "SWIFT gpi"。

### AC-003: 合规审计日志格式
*   **Given**: 任意评估完成。
*   **When**: 展开 "Regulatory Audit Log"。
*   **Then**:
    *   JSON 结构中应包含 `Document.BkToCstmrStmt.GrpHdr` 等 ISO 20022 标准标签。
    *   `<RmtInf><Strd>` 字段中应包含评分和欺诈检查结果。
    *   底部应有 MPC 隐私声明。

---

## 5. 附录
*   **架构图**: 详见 `docs/architecture.md`
*   **HKMA 对齐说明**: 详见 `docs/hkma_mapping.md`
