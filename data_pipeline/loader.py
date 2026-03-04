from typing import Any, Dict


def load_sme_payload(sme_id: str) -> Dict[str, Any]:
    """Return mock raw-source signals + derived features for one SME."""
    mock_payload = {
        "GBA_Eco_Standard": {
            "features": {
                "sme_id": "GBA_Eco_Standard",
                "gmv_growth": 0.15,
                "refund_rate": 0.02,
                "collection_period": 45,
                "customs_alignment_score": 0.95,
                "data_freshness_days": 2,
                "description": "Cross-border e-commerce, stable growth, high compliance.",
            },
            "cdi_sources": {
                "IADS_BankFlow": {
                    "avg_monthly_inflow_usd": 420000,
                    "avg_monthly_outflow_usd": 367000,
                    "net_flow_volatility_90d": 0.17,
                    "overdue_days_90d": 1,
                },
                "Ecommerce_Transactions": {
                    "gmv_30d_usd": 980000,
                    "order_count_30d": 12450,
                    "refund_ratio_30d": 0.02,
                    "chargeback_ratio_30d": 0.004,
                },
                "CDI_CDEG_CustomsTax": {
                    "customs_declaration_pass_rate": 0.97,
                    "tax_filing_ontime_rate": 0.98,
                    "customs_anomaly_count_90d": 0,
                },
                "Logistics_Fulfillment": {
                    "ontime_delivery_rate_30d": 0.96,
                    "lost_damage_ratio_30d": 0.008,
                    "avg_delivery_days_crossborder": 5.2,
                },
            },
        },
        "GBA_Eco_HighRisk": {
            "features": {
                "sme_id": "GBA_Eco_HighRisk",
                "gmv_growth": 2.0,
                "refund_rate": 0.12,
                "collection_period": 85,
                "customs_alignment_score": 0.60,
                "data_freshness_days": 45,
                "description": "Sudden volume spike, slow repayment, potential fraud risk.",
            },
            "cdi_sources": {
                "IADS_BankFlow": {
                    "avg_monthly_inflow_usd": 205000,
                    "avg_monthly_outflow_usd": 244000,
                    "net_flow_volatility_90d": 0.49,
                    "overdue_days_90d": 11,
                },
                "Ecommerce_Transactions": {
                    "gmv_30d_usd": 1240000,
                    "order_count_30d": 17620,
                    "refund_ratio_30d": 0.12,
                    "chargeback_ratio_30d": 0.028,
                },
                "CDI_CDEG_CustomsTax": {
                    "customs_declaration_pass_rate": 0.74,
                    "tax_filing_ontime_rate": 0.79,
                    "customs_anomaly_count_90d": 6,
                },
                "Logistics_Fulfillment": {
                    "ontime_delivery_rate_30d": 0.71,
                    "lost_damage_ratio_30d": 0.041,
                    "avg_delivery_days_crossborder": 11.8,
                },
            },
        },
        "HK_TMT_SME": {
            "features": {
                "sme_id": "HK_TMT_SME",
                "gmv_growth": 0.05,
                "refund_rate": 0.01,
                "collection_period": 30,
                "customs_alignment_score": 0.88,
                "data_freshness_days": 5,
                "description": "Mature TMT company with stable cash flow.",
            },
            "cdi_sources": {
                "IADS_BankFlow": {
                    "avg_monthly_inflow_usd": 510000,
                    "avg_monthly_outflow_usd": 452000,
                    "net_flow_volatility_90d": 0.12,
                    "overdue_days_90d": 0,
                },
                "Ecommerce_Transactions": {
                    "gmv_30d_usd": 730000,
                    "order_count_30d": 8960,
                    "refund_ratio_30d": 0.01,
                    "chargeback_ratio_30d": 0.003,
                },
                "CDI_CDEG_CustomsTax": {
                    "customs_declaration_pass_rate": 0.92,
                    "tax_filing_ontime_rate": 0.94,
                    "customs_anomaly_count_90d": 1,
                },
                "Logistics_Fulfillment": {
                    "ontime_delivery_rate_30d": 0.94,
                    "lost_damage_ratio_30d": 0.009,
                    "avg_delivery_days_crossborder": 4.6,
                },
            },
        },
    }
    return mock_payload.get(sme_id, {})


def load_sme_features(sme_id: str) -> Dict[str, Any]:
    """Return mock features for a selected SME profile."""
    payload = load_sme_payload(sme_id)
    return payload.get("features", {})


if __name__ == "__main__":
    print(load_sme_features("GBA_Eco_Standard"))
