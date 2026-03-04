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


def _clamp(x: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, x))


def calculate_dimension_scores(features: dict, cdi_sources: dict) -> dict:
    """
    Build five-dimension scores (0-100):
    1) Ecommerce behavior
    2) Customs/Tax compliance
    3) Bank flow stability
    4) Logistics fulfillment
    5) Data freshness reliability
    """
    growth = float(features.get("gmv_growth", 0))
    refund = float(features.get("refund_rate", 0))
    collection_days = float(features.get("collection_period", 90))
    customs_align = float(features.get("customs_alignment_score", 0))
    freshness_days = float(features.get("data_freshness_days", 90))

    # 1) Ecommerce behavior
    if 0.05 <= growth <= 0.5:
        growth_score = 95.0
    elif growth > 0.5:
        growth_score = 55.0
    else:
        growth_score = 45.0

    if refund <= 0.03:
        refund_score = 95.0
    elif refund <= 0.1:
        refund_score = 60.0
    else:
        refund_score = 25.0
    ecommerce_score = _clamp(0.6 * growth_score + 0.4 * refund_score)

    # 2) Customs/Tax compliance
    customs_score = _clamp(customs_align * 100.0)

    # 3) Bank flow stability (proxy by collection period)
    if collection_days <= 45:
        bankflow_score = 95.0
    elif collection_days <= 75:
        bankflow_score = 65.0
    else:
        bankflow_score = 25.0

    # 4) Logistics fulfillment (from CDI logistics source)
    logistics = cdi_sources.get("Logistics_Fulfillment", {})
    ontime = float(logistics.get("ontime_delivery_rate_30d", 0.8))
    lost_damage = float(logistics.get("lost_damage_ratio_30d", 0.02))
    logistics_score = _clamp((ontime * 100.0) * 0.8 + (100.0 - lost_damage * 1000.0) * 0.2)

    # 5) Data freshness reliability
    freshness_score = _clamp(100.0 - freshness_days * 2.0)

    return {
        "ecommerce_behavior": round(ecommerce_score, 1),
        "customs_tax_compliance": round(customs_score, 1),
        "bankflow_stability": round(bankflow_score, 1),
        "logistics_fulfillment": round(logistics_score, 1),
        "data_freshness_reliability": round(freshness_score, 1),
    }


def run_trae_for_sme(sme_id: str, scenario: str) -> dict:
    """Run Transform -> Reason -> Act -> Explain for one SME."""
    payload = load_sme_payload(sme_id)
    features = payload.get("features", {})
    if not features:
        return {"error": f"SME {sme_id} not found"}

    cdi_sources = payload.get("cdi_sources", {})
    dimension_scores = calculate_dimension_scores(features, cdi_sources)
    dimension_weights = {
        "ecommerce_behavior": 0.35,
        "customs_tax_compliance": 0.25,
        "bankflow_stability": 0.20,
        "logistics_fulfillment": 0.10,
        "data_freshness_reliability": 0.10,
    }

    base_score = round(
        sum(dimension_scores[k] * w for k, w in dimension_weights.items()),
        1,
    )
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
        "dimension_scores": dimension_scores,
        "dimension_weights": dimension_weights,
        "pricing": asdict(pricing_result),
        "explanation": {
            "narrative": explanation_result.narrative,
            "feature_importance": explanation_result.feature_importance_df.to_dict(orient="records"),
            "audit_payload": explanation_result.audit_payload,
        },
        "features": features,
        "cdi_sources": cdi_sources,
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
