# 产品需求文档 (PRD): TRAE-D-SME-Pricing 跨境中小企业智能风险定价引擎

| 版本 | 日期 | 作者 | 更新内容 | 状态 |
| :--- | :--- | :--- | :--- | :--- |
| v1.2 | 2026-03-04 | Yixin Zhang | 面试版重构：统一阈值、量化验收、明确实现边界 | Interview Edition |

---

## 0. 实现边界说明（面试必读）

为避免“概念大于落地”，本项目按以下边界展示：

- Implemented（已实现于 Demo）
  - 多源数据模拟接入（CDI理念映射）
  - 动态评分（0-100）与分级定价（A-D）
  - 数据新鲜度惩罚、人工复核触发
  - 可解释输出（原因码 + 自然语言摘要）
  - Streamlit可视化与审计日志展示
- Simulated（模拟实现）
  - mBridge 结算路径推荐与可视化
  - ISO 20022-compatible 审计字段映射
- Planned（规划项，未在本版实现）
  - 银行真实生产数据联调
  - HKMA FSS正式试点接入
  - MPC生产级隐私计算框架

---

## 1. 功能背景 (Context)

### 1.1 问题陈述
香港跨境 SME 常见“融资难、融资贵”问题。传统授信更依赖财务报表和抵押资产，而跨境电商类 SME 往往有高质量交易与物流行为数据，但难以被传统模型充分利用。

### 1.2 目标与价值
构建基于 HKMA CDI 思路的智能风险定价引擎，实现：
1. 数据驱动授信：用替代数据增强信用识别。
2. 动态精准定价：根据风险变化调整额度和利率。
3. 合规可解释：输出可追溯决策依据与审计记录。
4. 风险闭环迭代：支持策略复盘与阈值优化。

---

## 2. 用户场景 (User Scenarios)

### 场景一：优质跨境商户快速获批
- 用户：成熟跨境电商（如 `GBA_Eco_Standard`）
- 情境：海关申报稳定、流水增长，旺季前需备货资金
- 结果：系统评为 Grade A，建议高额度、低加点定价，并推荐低摩擦结算路径

### 场景二：异常交易触发风控收敛
- 用户：新注册商户（如 `GBA_Eco_HighRisk`）
- 情境：交易突增且回款周期显著拉长，数据新鲜度不足
- 结果：系统触发惩罚与降级，进入人工复核，不自动放款

---

## 3. 需求描述 (Functional Requirements)

### 3.1 Transform（数据层）
- R-001 多源数据接入
  - 输入源：IADS类流水、CDI-CDEG类海关信息、电商交易、物流履约
- R-002 特征工程
  - 输出指标：`gmv_growth`、`refund_rate`、`collection_period`、`customs_alignment_score`
- R-003 数据新鲜度校验
  - 规则：`data_freshness_days > 30` 标记 `Stale Data`，并触发评分惩罚

### 3.2 Reason & Act（决策层）
- R-004 动态评分模型（0-100）
  - 新鲜度惩罚：`Stale Data` 扣 5 分
  - 流动性压力场景惩罚：命中 `Liquidity Stress` 扣 3-8 分（区间可配置）
- R-005 定价矩阵（统一阈值）
  - Grade A（Score >= 90）：Limit 8-12M，Rate Prime + 1.5%
  - Grade B（80 <= Score < 90）：Limit 4-8M，Rate Prime + 2.0%~2.8%
  - Grade C（65 <= Score < 80）：Limit 1-4M，Rate Prime + 3.0%~3.8%，建议人工复核
  - Grade D（Score < 65）：拒绝自动放款，仅人工审批

### 3.3 Explain（解释与合规）
- R-006 自然语言解释
  - 为每笔决策输出英文 explanation，包含关键因子、惩罚项、建议动作
- R-007 隐私声明
  - 审计区明确数据最小化原则与脱敏处理方式
- R-008 审计结构
  - 输出 ISO 20022-compatible 字段映射（Demo级），不宣称生产报文直连

### 3.4 UI（交互层）
- R-009 实时模拟
  - 支持 `Simulate New CDI Feed`，触发重算并刷新图表
- R-010 路径可视化
  - 结算建议路径可视化（mBridge 为模拟推荐通道）

---

## 4. 验收标准 (Acceptance Criteria)

### AC-001 优质商户自动审批路径
- Given：选择 `GBA_Eco_Standard`，场景 `Baseline`
- When：点击 `Run TRAE Assessment`
- Then：
  - 风险评分 `>= 90`
  - 决策结果为 `Auto-Approved`
  - 返回建议额度区间 `8-12M`
  - Explain 字段完整率 = 100%（含至少 3 个因子 + 1 个动作建议）

### AC-002 数据滞后惩罚生效
- Given：选择 `GBA_Eco_HighRisk`，`data_freshness_days = 45`
- When：点击 `Run TRAE Assessment`
- Then：
  - 触发 `Stale Data` 标记
  - 评分扣减 5 分（日志可追溯）
  - 决策结果为 `Manual Review Required` 或拒绝自动放款

### AC-003 审计与可追溯性
- Given：任意评估完成
- When：展开 `Regulatory Audit Log`
- Then：
  - 输出请求ID、评分版本、规则命中、定价结果
  - 支持 ISO 20022-compatible 映射字段展示
  - 所有关键字段可回溯到本次评估输入

### AC-004 非功能指标
- 单次评估响应时间（本地演示环境）P95 < 2s
- 评分-定价-解释链路成功率 >= 99%

---

## 5. 指标体系与复盘机制

### 5.1 核心指标
- 通过率（Approval Rate）
- 人工复核率（Manual Review Rate）
- 预期逾期率（Expected Delinquency）
- 风险调整后收益（Risk-adjusted Yield）

### 5.2 策略迭代
- 每轮迭代记录：版本号、阈值变更、影响样本、回滚条件
- 回滚条件：通过率下降 > 5pp 且风险指标未改善

---

## 6. 风险与限制

- 风险1：替代数据缺失或延迟导致评分抖动
- 风险2：高增长商户被误判（误杀）
- 风险3：跨市场规则迁移时阈值失真

应对：
- 增加数据质量门控和降级策略
- 保留人工复核兜底
- 分市场维护参数并做灰度验证

---

## 7. 附录
- 架构说明：`docs/architecture.md`
- 数据字典：`docs/data_dictionary.md`
- API规格：`docs/api_spec.md`
