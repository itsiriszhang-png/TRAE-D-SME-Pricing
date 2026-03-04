# Data Dictionary (Demo)

## Core Tables

### merchant_profile
| Field | Type | Description |
| :--- | :--- | :--- |
| merchant_id | string | Merchant primary key |
| registration_country | string | ISO country code |
| industry_code | string | Industry category |
| business_age_months | int | Months since registration |

### merchant_txn_daily
| Field | Type | Description |
| :--- | :--- | :--- |
| merchant_id | string | Merchant primary key |
| biz_date | date | Business date |
| gmv_usd | decimal | Daily GMV |
| refund_amount_usd | decimal | Daily refund amount |
| chargeback_count | int | Chargeback events |

### merchant_custom_tax
| Field | Type | Description |
| :--- | :--- | :--- |
| merchant_id | string | Merchant primary key |
| period_yyyymm | string | Reporting period |
| customs_decl_count | int | Declaration count |
| tax_filing_on_time_rate | decimal | On-time filing ratio |
| severe_violation_count_12m | int | Severe violations |

### merchant_logistics
| Field | Type | Description |
| :--- | :--- | :--- |
| merchant_id | string | Merchant primary key |
| biz_date | date | Business date |
| shipment_count | int | Shipment count |
| ontime_delivery_rate | decimal | On-time ratio |
| exception_rate | decimal | Exception ratio |

### risk_score_snapshot
| Field | Type | Description |
| :--- | :--- | :--- |
| score_id | string | Score snapshot ID |
| merchant_id | string | Merchant primary key |
| total_score | decimal | Final risk score |
| risk_level | string | A/B/C/D |
| strategy_version | string | Model/strategy version |

### pricing_decision_log
| Field | Type | Description |
| :--- | :--- | :--- |
| decision_id | string | Decision record ID |
| merchant_id | string | Merchant primary key |
| score_id | string | Linked score snapshot |
| recommended_limit_usd | decimal | Suggested limit |
| recommended_rate | decimal | Suggested rate |
| decision_status | string | approve/review/reject |
