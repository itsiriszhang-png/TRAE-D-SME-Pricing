from dataclasses import dataclass
from typing import Optional


@dataclass
class PricingResult:
    credit_limit: float
    base_rate_str: str
    risk_grade: str
    need_manual_review: bool
    settlement_path: str


def compute_pricing(
    score: float,
    sme_size_factor: float = 1.0,
    scenario: Optional[str] = None,
    data_freshness_days: int = 0,
) -> PricingResult:
    """Map risk score to grade, pricing spread, and credit limit recommendation."""
    if score >= 90:
        risk_grade, base_spread = "A", 1.5
        floor_limit, cap_limit = 8_000_000, 12_000_000
    elif score >= 80:
        risk_grade, base_spread = "B", 2.4
        floor_limit, cap_limit = 4_000_000, 8_000_000
    elif score >= 65:
        risk_grade, base_spread = "C", 3.4
        floor_limit, cap_limit = 1_000_000, 4_000_000
    else:
        risk_grade, base_spread = "D", 5.0
        floor_limit, cap_limit = 1_000_000, 2_500_000

    limit_adjustment = 1.0
    manual_review_triggered = risk_grade in ["C", "D"]
    scenario_text = (scenario or "").lower()

    if "liquidity stress" in scenario_text:
        base_spread += 0.5
        limit_adjustment *= 0.8
    elif "compliance risk" in scenario_text:
        base_spread += 1.2
        limit_adjustment *= 0.6
        manual_review_triggered = True
    elif "high growth" in scenario_text:
        base_spread += 0.2
        limit_adjustment *= 1.1

    raw_limit = (floor_limit + cap_limit) / 2 * (score / 100) * sme_size_factor * limit_adjustment
    calculated_limit = max(floor_limit, min(raw_limit, cap_limit))
    calculated_limit = round(calculated_limit / 100000) * 100000

    if base_spread >= 3.5:
        manual_review_triggered = True

    settlement_path = "mBridge (simulated)" if risk_grade in ["A", "B"] and not manual_review_triggered else "SWIFT gpi"

    return PricingResult(
        credit_limit=float(calculated_limit),
        base_rate_str=f"Prime + {base_spread:.1f}%",
        risk_grade=risk_grade,
        need_manual_review=manual_review_triggered,
        settlement_path=settlement_path,
    )
