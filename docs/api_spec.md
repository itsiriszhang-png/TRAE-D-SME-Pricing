# API Spec (Demo)

## Base
- Base path: `/api/v1`
- Content-Type: `application/json`
- Auth: `Bearer token`

## POST /risk/score
Input:
```json
{
  "merchant_id": "M123",
  "country": "HK",
  "apply_amount": 500000,
  "tenor_days": 90
}
```
Output:
```json
{
  "score_id": "RS_20260304_0001",
  "total_score": 76.4,
  "risk_level": "B",
  "sub_scores": {
    "ecom": 81,
    "custom_tax": 73,
    "bank_flow": 70,
    "logistics": 78,
    "industry": 65
  },
  "rule_hit_codes": ["RISK_RULE_023"],
  "strategy_version": "risk_v1.0.0"
}
```

## POST /pricing/recommend
Input:
```json
{
  "merchant_id": "M123",
  "score_id": "RS_20260304_0001",
  "apply_amount": 500000,
  "tenor_days": 90
}
```
Output:
```json
{
  "pricing_id": "PR_20260304_0091",
  "recommended_limit_usd": 120000,
  "recommended_rate": 0.118,
  "risk_margin_ratio": 0.06,
  "reason_codes": ["RISK_TIER_B", "RULE_023_HIT"]
}
```

## POST /decision/submit
Input:
```json
{
  "merchant_id": "M123",
  "score_id": "RS_20260304_0001",
  "pricing_id": "PR_20260304_0091",
  "decision_status": "review",
  "decision_reason_codes": ["DOC_MISSING", "RULE_023_HIT"],
  "reviewer_id": "u_9821"
}
```
Output:
```json
{
  "decision_id": "PD_20260304_0188",
  "decision_status": "review"
}
```
