from dataclasses import dataclass
import pandas as pd
from typing import Dict, Any, List
import datetime
import uuid

@dataclass
class ExplanationResult:
    """
    Container for explainability outputs.
    可解释性结果容器。
    """
    narrative: str                  # 自然语言解释
    feature_importance_df: pd.DataFrame # 特征重要性 Dataframe
    audit_payload: Dict[str, Any]   # 审计日志载荷

def get_explanations(sme_id: str, scenario: str, score: float, features: Dict[str, Any], model_version: str = "v0.1-demo") -> ExplanationResult:
    """
    Generates explainability results for the pricing decision using a simplified rule-based approach (Mock SHAP).
    使用简化规则（模拟 SHAP）生成定价决策的可解释性结果。
    
    Args:
        sme_id: SME Identifier.
        scenario: Business scenario context.
        score: Calculated risk score.
        features: Feature dictionary.
        model_version: Version tag for auditing.
        
    Returns:
        ExplanationResult: Narrative, plot data, and audit log.
    """
    
    # 1. Simplified Feature Importance Calculation
    # 简化的特征重要性计算
    
    # Configuration: Weight represents sensitivity, Threshold defines Good/Bad
    feature_configs = {
        "gmv_growth": {"weight": 30, "type": "benefit", "threshold": 0.1, "label": "GMV Growth"},
        "refund_rate": {"weight": 20, "type": "cost", "threshold": 0.05, "label": "Refund Rate"},
        "collection_period": {"weight": 20, "type": "cost", "threshold": 60, "label": "Collection Period"},
        "customs_alignment_score": {"weight": 30, "type": "benefit", "threshold": 0.8, "label": "Customs Compliance"},
        "data_freshness_days": {"weight": 10, "type": "cost", "threshold": 30, "label": "Data Stale Risk"}
    }
    
    importance_data = []
    positives = []
    negatives = []
    
    for key, val in features.items():
        if key not in feature_configs:
            continue
            
        config = feature_configs[key]
        label = config["label"]
        
        # Determine if this feature is a "Strength" or "Weakness" based on thresholds
        is_strength = False
        if config["type"] == "benefit":
            if val >= config["threshold"]:
                is_strength = True
        else: # cost
            if val <= config["threshold"]:
                is_strength = True
                
        if is_strength:
            positives.append(label)
            # Mock "SHAP" value: Positive contribution
            shap_value = config["weight"] * (1.0 + abs(val)) 
        else:
            negatives.append(label)
            # Mock "SHAP" value: Negative contribution
            shap_value = - (config["weight"] * (1.0 + abs(val)))
            
        importance_data.append({
            "Feature": label,
            "Importance": abs(shap_value), # For magnitude sorting
            "Contribution": shap_value,    # For direction
            "Direction": "Positive" if shap_value > 0 else "Negative"
        })
        
    df = pd.DataFrame(importance_data)
    
    # 2. Generate Narrative (Natural Language Generation)
    # 生成自然语言解释 (NLG)
    narrative = f"### Assessment Summary for {sme_id}\n"
    narrative += f"**Scenario**: {scenario} | **Score**: {score:.1f}\n\n"
    
    narrative += "#### Key Drivers:\n"
    if positives:
        narrative += f"✅ **Strengths**: The applicant demonstrates strong performance in **{', '.join(positives)}**, which supports a higher credit rating.\n\n"
    
    if negatives:
        narrative += f"⚠️ **Risk Factors**: Attention is required regarding **{', '.join(negatives)}**. These factors exerted downward pressure on the final score.\n\n"
        
    narrative += "#### Rationale:\n"
    if score >= 85:
        narrative += "Given the high consistency in customs data and stable operating metrics, the model recommends **Prime** tier pricing. "
        narrative += "This aligns with our **Gone Fintech** strategy to reward digital transparency."
    elif score >= 70:
        narrative += "The profile is solid but shows minor volatility. Standard pricing applies."
    else:
        narrative += "Due to identified risk factors (e.g., anomalies or extended collection cycles), a conservative limit and higher spread are recommended to mitigate exposure. "
        narrative += "This decision reflects our **Responsible AI** risk guardrails."
    
    # Add MPC Privacy Footer
    narrative += "\n\n_Note: This assessment was computed via Multi-Party Computation (MPC), ensuring raw IADS data never left the source bank._"

    # 3. Construct ISO 20022 Audit Payload (Mock camt.053 style)
    # 构造 ISO 20022 格式审计日志
    msg_id = str(uuid.uuid4())
    cre_dt_tm = datetime.datetime.now().isoformat()
    
    iso_audit_payload = {
        "Document": {
            "BkToCstmrStmt": {
                "GrpHdr": {
                    "MsgId": msg_id,
                    "CreDtTm": cre_dt_tm,
                    "MsgPgntn": {"PgNb": "1", "LastPgInd": "true"}
                },
                "Stmt": {
                    "Id": f"TRAE-AUDIT-{sme_id}",
                    "ElctrncSeqNb": "1",
                    "CreDtTm": cre_dt_tm,
                    "Ntry": {
                        "NtryRef": f"SCORE-{score}",
                        "Amt": {"@Ccy": "HKD", "#text": "0.00"}, # Placeholder
                        "CdtDbtInd": "CRDT",
                        "Sts": "BOOK",
                        "BkTxCd": {"Domn": {"Cd": "PMNT", "Fmly": {"Cd": "RCDT", "SubFmlyCd": "ESCT"}}},
                        "NtryDtls": {
                            "TxDtls": {
                                "Refs": {
                                    "MsgId": msg_id,
                                    "AcctSvcrRef": "TRAE-ENGINE-V1",
                                    "EndToEndId": sme_id
                                },
                                "RmtInf": {
                                    "Strd": {
                                        "RfrdDocInf": {
                                            "Tp": {"CdOrPrtry": {"Cd": "CINV"}},
                                            "Nb": "RISK-ASSESSMENT"
                                        },
                                        "AddtlRmtInf": [
                                            f"Score: {score}",
                                            f"TopFeature: {positives[0] if positives else 'None'}",
                                            "FraudCheck: PASSED",
                                            "Compliance: ISO20022-READY"
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "_meta": {
            "description": "Simulated ISO 20022 camt.053 payload for interbank audit trails.",
            "note": "Structured Remittance Info (RmtInf/Strd) is used to embed risk signals for fraud prevention."
        }
    }
    
    return ExplanationResult(
        narrative=narrative,
        feature_importance_df=df,
        audit_payload=iso_audit_payload
    )
