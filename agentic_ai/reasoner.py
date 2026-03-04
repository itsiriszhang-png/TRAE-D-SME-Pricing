import os
import sys
from dataclasses import asdict

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from data_pipeline.loader import load_sme_payload
from explainability.shap_explainer import get_explanations
from pricing_model.engine import compute_pricing


def calculate_score(features: dict) -> float:
    """Simple weighted score (0-100) for demo purposes."""
    if not features:
        return 0.0

    score = 0.0

    growth = features.get("gmv_growth", 0)
    if 0.05 <= growth <= 0.5:
        score += 20
    elif growth > 0.5:
        score += 12
    else:
        score += 6

    refund = features.get("refund_rate", 0)
    if refund < 0.03:
        score += 20
    elif refund < 0.1:
        score += 10

    days = features.get("collection_period", 90)
    if days <= 45:
        score += 20
    elif days <= 75:
        score += 12

    align = features.get("customs_alignment_score", 0)
    score += 40 * align

    return round(score, 1)


def run_trae_for_sme(sme_id: str, scenario: str) -> dict:
    """Run Transform -> Reason -> Act -> Explain for one SME."""
    payload = load_sme_payload(sme_id)
    features = payload.get("features", {})
    if not features:
        return {"error": f"SME {sme_id} not found"}

    base_score = calculate_score(features)
    score = base_score
    penalties = []

    scenario_text = (scenario or "").lower()
    if "compliance risk" in scenario_text:
        score -= 15.0
        penalties.append({"name": "Compliance Risk Scenario", "delta": -15.0})
    elif "liquidity stress" in scenario_text:
        score -= 5.0
        penalties.append({"name": "Liquidity Stress Scenario", "delta": -5.0})

    if features.get("data_freshness_days", 0) > 30:
        score -= 5.0
        penalties.append({"name": "Stale Data Penalty (>30d)", "delta": -5.0})

    score = max(0, min(100, score))

    pricing_result = compute_pricing(
        score=score,
        sme_size_factor=1.0,
        scenario=scenario,
        data_freshness_days=features.get("data_freshness_days", 0),
    )

    explanation_result = get_explanations(
        sme_id=sme_id,
        scenario=scenario,
        score=score,
        features=features,
    )

    return {
        "sme_id": sme_id,
        "scenario": scenario,
        "base_score": base_score,
        "score": score,
        "penalties": penalties,
        "pricing": asdict(pricing_result),
        "explanation": {
            "narrative": explanation_result.narrative,
            "feature_importance": explanation_result.feature_importance_df.to_dict(orient="records"),
            "audit_payload": explanation_result.audit_payload,
        },
        "features": features,
        "cdi_sources": payload.get("cdi_sources", {}),
        "feature_lineage": [
            {"derived_feature": "gmv_growth", "source_domain": "Ecommerce_Transactions", "source_fields": "gmv_30d_usd, order_count_30d"},
            {"derived_feature": "refund_rate", "source_domain": "Ecommerce_Transactions", "source_fields": "refund_ratio_30d, chargeback_ratio_30d"},
            {"derived_feature": "collection_period", "source_domain": "IADS_BankFlow", "source_fields": "avg_monthly_inflow_usd, avg_monthly_outflow_usd, overdue_days_90d"},
            {"derived_feature": "customs_alignment_score", "source_domain": "CDI_CDEG_CustomsTax", "source_fields": "customs_declaration_pass_rate, tax_filing_ontime_rate, customs_anomaly_count_90d"},
            {"derived_feature": "data_freshness_days", "source_domain": "CDI Metadata", "source_fields": "ingestion_timestamp"},
        ],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_trae_for_sme("GBA_Eco_Standard", "Baseline"), indent=2, ensure_ascii=False))
