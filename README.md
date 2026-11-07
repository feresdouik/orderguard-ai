# OrderGuard AI

**Explainable order-review workspace for e-commerce sellers handling cash-on-delivery (COD) orders.**

OrderGuard AI helps an operator organize incoming orders, highlight incomplete or unusual records, understand transparent review signals, and decide which customers may need manual confirmation.

> **Prototype status:** This is a working Streamlit MVP. Risk scores are deterministic, illustrative heuristics. They are not a trained fraud model, a fraud verdict, identity verification, or a guarantee of delivery outcomes. A human operator must review every order.

## Demo features

- **Overview:** order totals, risk distribution, review workload, and priority queue.
- **Orders:** search by order ID/customer/phone/address, filter by risk and data quality, inspect an individual order, and export filtered results.
- **Analytics:** average order value and risk-level breakdowns.
- **CSV import:** required-column validation, numeric normalization, missing-field checks, negative-value checks, and duplicate order-ID detection.
- **Explainable review signals:** every score is accompanied by the rules that contributed to it and a suggested manual next step.
- **Synthetic demo data:** the app works immediately without API keys or external services.

## Screens and navigation

Use the sidebar to switch between Overview, Orders, Analytics, and How it works. Upload a CSV in the sidebar to replace the built-in synthetic sample.

## CSV schema

The uploaded CSV must include these exact column names:

| Column | Meaning | Example |
|---|---|---|
| `order_id` | Order reference | `OG-1001` |
| `customer` | Customer display name | `Demo Customer` |
| `phone` | Phone as text | `20123456` |
| `address` | Delivery address | `Sousse, Tunisia` |
| `total` | Numeric order total | `89.00` |
| `previous_orders` | Number of previous orders | `2` |
| `notes` | Optional operator note | `Confirm size` |

A ready-to-upload synthetic file is available at `sample_orders.csv`. Do not upload real customer data to public demos, screenshots, or untrusted services. Phone numbers and addresses are personal data.

## Risk indicator (illustrative rules)

| Signal | Points |
|---|---:|
| Missing phone | +30 |
| Missing delivery address | +25 |
| No previous successful orders recorded | +15 |
| Order total at or above 250 | +10 |
| Notes contain selected review keywords | +20 |

- **Low:** 0–24
- **Medium:** 25–49
- **High:** 50–100

The rules are illustrative and have not been statistically validated. A high score does not mean an order is fraudulent. The prototype does not contact customers, verify phone ownership, validate addresses, or automatically reject orders.

## Run locally

Python 3.11 or newer is recommended.

### Windows (Command Prompt)

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

If Python 3.12 is not installed, use `python` instead of `py -3.12`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

Tests cover clean orders, risk thresholds, score bounds, missing/invalid values, negative values, missing columns, and duplicate order IDs.

## Project structure

```text
.
├── app.py                 # Streamlit interface and workflows
├── risk_engine.py         # CSV validation and explainable scoring
├── sample_orders.csv      # Synthetic CSV for upload demos
├── tests/
│   └── test_risk_engine.py
├── .kiro/
│   └── steering/          # Product and technical guidance for Kiro
├── requirements.txt
├── README.md
└── LICENSE
```

## Demo and deployment preparation

- [Demo video script](docs/DEMO_SCRIPT.md)
- [Hackathon submission draft](docs/HACKATHON_SUBMISSION.md)
- [Deployment guide](DEPLOYMENT.md)

## Kiro usage

The `.kiro/steering/` files define the product vision, scope, technical stack, and safety principles used to guide development. The project separates the scoring logic from the Streamlit interface and includes automated tests for core behavior.

When preparing the hackathon submission, describe only the Kiro features actually used during development (for example, specs, steering, hooks, agents, or MCP) and include genuine evidence from your workflow.

## Current limitations and next steps

- No user accounts, authentication, or persistent database.
- No live store, shipping, SMS, or WhatsApp integrations.
- No trained machine-learning model or statistically validated thresholds.
- No production deployment or security review is included by this repository alone.

## License

MIT. See [LICENSE](LICENSE).
