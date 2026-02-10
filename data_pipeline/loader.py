from typing import Dict, Any

def load_sme_features(sme_id: str) -> Dict[str, Any]:
    """
    Simulates loading SME features from a CDI (Commercial Data Interchange) source.
    模拟从商业数据通 (CDI) 加载中小企业特征数据。
    
    Args:
        sme_id (str): The ID of the SME to load.
        
    Returns:
        Dict[str, Any]: A dictionary containing the SME's features.
    """
    
    # Mock data for different SME profiles
    # 仿真数据：模拟不同类型的跨境 SME
    mock_data = {
        "GBA_Eco_Standard": {
            "sme_id": "GBA_Eco_Standard",
            "gmv_growth": 0.15,          # Stable growth 15% (稳健增长)
            "refund_rate": 0.02,         # Low refund rate (低退款率)
            "collection_period": 45,     # Standard collection period (days) (标准回款周期)
            "customs_alignment_score": 0.95, # High compliance (海关一致性高)
            "data_freshness_days": 2,    # Real-time data (实时数据)
            "description": "Cross-border e-commerce, stable growth, high compliance."
        },
        "GBA_Eco_HighRisk": {
            "sme_id": "GBA_Eco_HighRisk",
            "gmv_growth": 2.0,           # Suspicious 3x growth (200% increase) (GMV 翻3倍)
            "refund_rate": 0.12,         # High refund rate (高退款率)
            "collection_period": 85,     # Long collection period (回款周期长)
            "customs_alignment_score": 0.60, # Low compliance (海关一致性低)
            "data_freshness_days": 45,   # Stale data (数据滞后)
            "description": "Sudden volume spike, slow repayment, potential fraud risk."
        },
        "HK_TMT_SME": {
            "sme_id": "HK_TMT_SME",
            "gmv_growth": 0.05,          # Low volatility (低波动)
            "refund_rate": 0.01,         # Very low refund rate
            "collection_period": 30,     # Fast collection (中等/快回款周期)
            "customs_alignment_score": 0.88, # Good compliance (合规良好)
            "data_freshness_days": 5,    # Fresh data
            "description": "Mature TMT company, stable cash flow."
        }
    }
    
    # Return the data for the requested SME, or an empty dict if not found
    return mock_data.get(sme_id, {})

# Test function to verify data loading
if __name__ == "__main__":
    print("Testing Data Loader...")
    sample = load_sme_features("GBA_Eco_Standard")
    print(f"Loaded sample: {sample}")
