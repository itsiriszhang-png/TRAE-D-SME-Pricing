from dataclasses import dataclass
from typing import Optional

@dataclass
class PricingResult:
    """
    Data class to hold the results of the pricing engine.
    定价结果数据类。
    """
    credit_limit: float          # 授信额度 (HKD)
    base_rate_str: str           # 利率展示字符串 (e.g., "Prime + 1.8%")
    risk_grade: str              # 风险等级 (A - D)
    need_manual_review: bool     # 是否需要人工复核
    settlement_path: str         # 结算路径 (e.g., "SWIFT gpi", "mBridge DLT")

def compute_pricing(score: float, sme_size_factor: float = 1.0, scenario: Optional[str] = None, data_freshness_days: int = 0) -> PricingResult:
    """
    Computes pricing and credit limits based on risk score and scenarios.
    根据风险评分和场景计算定价及授信额度。
    
    Args:
        score (float): 0-100 Comprehensive Risk Score.
        sme_size_factor (float): Factor representing SME business scale (default 1.0).
        scenario (str): Scenario description (e.g., "Baseline", "Slow Repayment").
        data_freshness_days (int): Age of the data in days. >30 days incurs penalty.
        
    Returns:
        PricingResult: Calculated pricing details.
    """
    
    # 0. Data Freshness Penalty
    # 数据新鲜度惩罚
    if data_freshness_days > 30:
        score = max(0, score - 5.0)

    # 1. Base Mapping from Score to Grade & Spread
    # 评分映射风险等级与基准加点
    if score >= 90:
        risk_grade = "A"
        base_spread = 1.5
    elif score >= 80:
        risk_grade = "B+"
        base_spread = 2.0
    elif score >= 70:
        risk_grade = "B"
        base_spread = 2.8
    elif score >= 60:
        risk_grade = "C"
        base_spread = 3.8
    else:
        risk_grade = "D"
        base_spread = 5.5

    # 2. Scenario Adjustments
    # 场景调整
    limit_adjustment = 1.0
    manual_review_triggered = False
    
    if scenario:
        # Handle Chinese and English keywords for robustness
        scenario_str = scenario.lower()
        
        if "回款放缓" in scenario or "slow repayment" in scenario_str or "资金紧张" in scenario:
            base_spread += 0.5
            limit_adjustment = 0.8
            
        elif "异常" in scenario or "abnormal" in scenario_str or "risk" in scenario_str:
             base_spread += 1.5
             limit_adjustment = 0.5
             manual_review_triggered = True # Always review for anomalies (异常情况必审)
             
        elif "激增" in scenario or "surge" in scenario_str or "growth" in scenario_str:
             # Growth scenario: slightly higher risk premium, but supportive limit
             # 增长场景：略微增加风险溢价，但支持更高额度
             base_spread += 0.2 
             limit_adjustment = 1.2 
    
    # 3. Calculate Credit Limit
    # 计算授信额度 (Range: 1M - 12M HKD)
    # Logic: Base * (Score Factor) * Size * Adjustment
    base_limit_cap = 12_000_000
    
    # Score factor: 1.0 at 100, 0.5 at 50 roughly
    score_factor = (score / 100.0) ** 1.5
    
    calculated_limit = 8_000_000 * score_factor * sme_size_factor * limit_adjustment
    
    # Clamp limit to [1M, 12M]
    calculated_limit = max(1_000_000, min(calculated_limit, base_limit_cap))
    
    # Round to nearest 100,000 for clean numbers
    calculated_limit = round(calculated_limit / 100000) * 100000

    # 4. Final Review Logic
    # 最终复核逻辑 triggers
    if risk_grade in ["C", "D"]:
        manual_review_triggered = True
        
    if base_spread >= 3.5:
        manual_review_triggered = True

    # 5. Determine Settlement Path
    # 确定结算路径
    if risk_grade in ["A", "B+"] and not manual_review_triggered:
        settlement_path = "mBridge (DLT-based Atomic Settlement)"
    else:
        settlement_path = "SWIFT gpi"

    return PricingResult(
        credit_limit=float(calculated_limit),
        base_rate_str=f"Prime + {base_spread:.1f}%",
        risk_grade=risk_grade,
        need_manual_review=manual_review_triggered,
        settlement_path=settlement_path
    )
