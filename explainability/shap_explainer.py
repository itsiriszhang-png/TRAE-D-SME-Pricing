import datetime
import uuid
from dataclasses import dataclass
from typing import Any, Dict

import pandas as pd


@dataclass
class ExplanationResult:
    narrative: str
    feature_importance_df: pd.DataFrame
    audit_payload: Dict[str, Any]


def get_explanations(
    sme_id: str,
    scenario: str,
    score: float,
    features: Dict[str, Any],
    model_version: str = "v1.0-demo",
) -> ExplanationResult:
    """Generate explainability output using lightweight rule-based logic."""

    feature_configs = {
        "gmv_growth": {"weight": 30, "type": "benefit", "threshold": 0.1, "label": "GMV Growth"},
        "refund_rate": {"weight": 20, "type": "cost", "threshold": 0.05, "label": "Refund Rate"},
        "collection_period": {"weight": 20, "type": "cost", "threshold": 60, "label": "Collection Period"},
        "customs_alignment_score": {
            "weight": 30,
            "type": "benefit",
            "threshold": 0.8,
            "label": "Customs Compliance",
        },
        "data_freshness_days": {"weight": 10, "type": "cost", "threshold": 30, "label": "Data Freshness"},
    }

    importance_data = []
    positives = []
    negatives = []

    for key, val in features.items():
        if key not in feature_configs:
            continue

        config = feature_configs[key]
        label = config["label"]
        is_strength = val >= config["threshold"] if config["type"] == "benefit" else val <= config["threshold"]

        if is_strength:
            positives.append(label)
            contribution = config["weight"] * (1.0 + abs(val))
        else:
            negatives.append(label)
            contribution = -(config["weight"] * (1.0 + abs(val)))

        importance_data.append(
            {
                "Feature": label,
                "Importance": abs(contribution),
                "Contribution": contribution,
                "Direction": "Positive" if contribution > 0 else "Negative",
            }
        )

    df = pd.DataFrame(importance_data)

    narrative = f"Assessment Summary for {sme_id}\n"
    narrative += f"Scenario: {scenario} | Score: {score:.1f}\n\n"
    if positives:
        narrative += f"Strengths: {', '.join(positives)}.\n"
    if negatives:
        narrative += f"Risk Factors: {', '.join(negatives)}.\n"

    if score >= 90:
        narrative += "Recommendation: low-risk pricing tier with standard monitoring."
    elif score >= 75:
        narrative += "Recommendation: standard pricing tier with periodic review."
    else:
        narrative += "Recommendation: conservative limit and manual review due to elevated risk signals."

    narrative += "\n\nNote: Demo uses derived signals; raw source data is not exposed in this flow."

    msg_id = str(uuid.uuid4())
    cre_dt_tm = datetime.datetime.now().isoformat()

    audit_payload = {
        "Document": {
            "BkToCstmrStmt": {
                "GrpHdr": {
                    "MsgId": msg_id,
                    "CreDtTm": cre_dt_tm,
                    "MsgPgntn": {"PgNb": "1", "LastPgInd": "true"},
                },
                "Stmt": {
                    "Id": f"TRAE-AUDIT-{sme_id}",
                    "ElctrncSeqNb": "1",
                    "CreDtTm": cre_dt_tm,
                    "Ntry": {
                        "NtryRef": f"SCORE-{score}",
                        "Amt": {"@Ccy": "HKD", "#text": "0.00"},
                        "CdtDbtInd": "CRDT",
                        "Sts": "BOOK",
                        "NtryDtls": {
                            "TxDtls": {
                                "Refs": {
                                    "MsgId": msg_id,
                                    "AcctSvcrRef": "TRAE-ENGINE-DEMO",
                                    "EndToEndId": sme_id,
                                },
                                "RmtInf": {
                                    "Strd": {
                                        "AddtlRmtInf": [
                                            f"Score={score}",
                                            f"TopDriver={positives[0] if positives else 'N/A'}",
                                            f"ModelVersion={model_version}",
                                        ]
                                    }
                                },
                            }
                        },
                    },
                },
            }
        },
        "_meta": {
            "description": "ISO 20022-compatible audit payload for demonstration.",
            "note": "Demo mapping only; not a production payment-message pipeline.",
        },
    }

    return ExplanationResult(narrative=narrative, feature_importance_df=df, audit_payload=audit_payload)
