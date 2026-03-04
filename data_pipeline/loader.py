from typing import Any, Dict


def load_sme_features(sme_id: str) -> Dict[str, Any]:
    """Return mock features for a selected SME profile."""
    mock_data = {
        "GBA_Eco_Standard": {
            "sme_id": "GBA_Eco_Standard",
            "gmv_growth": 0.15,
            "refund_rate": 0.02,
            "collection_period": 45,
            "customs_alignment_score": 0.95,
            "data_freshness_days": 2,
            "description": "Cross-border e-commerce, stable growth, high compliance.",
        },
        "GBA_Eco_HighRisk": {
            "sme_id": "GBA_Eco_HighRisk",
            "gmv_growth": 2.0,
            "refund_rate": 0.12,
            "collection_period": 85,
            "customs_alignment_score": 0.60,
            "data_freshness_days": 45,
            "description": "Sudden volume spike, slow repayment, potential fraud risk.",
        },
        "HK_TMT_SME": {
            "sme_id": "HK_TMT_SME",
            "gmv_growth": 0.05,
            "refund_rate": 0.01,
            "collection_period": 30,
            "customs_alignment_score": 0.88,
            "data_freshness_days": 5,
            "description": "Mature TMT company with stable cash flow.",
        },
    }
    return mock_data.get(sme_id, {})


if __name__ == "__main__":
    print(load_sme_features("GBA_Eco_Standard"))
