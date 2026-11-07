# OrderGuard AI

An early-stage, explainable order-review dashboard for e-commerce sellers, with a focus on cash-on-delivery workflows.

> **Current status:** Working Streamlit MVP. The current risk score is a deterministic demo heuristic, not an AI fraud model and not proof that an order is fraudulent.

## What it does

- Loads synthetic sample orders or a seller-provided CSV.
- Checks required order fields.
- Calculates an explainable 0–100 risk indicator from configurable-style demo rules.
- Shows the reasons behind each score and suggests a manual verification step.
- Filters orders by risk level and exports the analyzed data to CSV.

## Run locally

Requires Python 3.11 or newer.

```bash
git clone https://github.com/feresdouik/orderguard-ai.git
cd orderguard-ai
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## CSV format

The uploaded CSV must contain these columns:

| Column | Description |
|---|---|
| `order_id` | Unique order reference |
| `customer` | Customer display name |
| `phone` | Phone number as text |
| `address` | Delivery address |
| `total` | Order total (numeric) |
| `previous_orders` | Number of previous orders |
| `notes` | Optional order notes |

Use synthetic or properly authorized data in demos. Do not commit real customer data.

## Risk indicator (demo rules)

- Missing phone: +30
- Missing address: +25
- No previous orders recorded: +15
- Order total >= 250: +10
- Notes containing selected review keywords: +20
- Final score is capped at 100.

Risk levels: Low (0–24), Medium (25–49), High (50–100).

These are initial illustrative rules. They have not been statistically validated and should not be used as the sole basis for rejecting orders. The operator remains responsible for reviewing each case.

## Kiro project files

The `.kiro/` directory contains product and technical steering plus the requirements, design, and task breakdown for the MVP.

## Roadmap

- Add automated tests for risk-scoring boundaries.
- Separate data processing from the Streamlit interface.
- Improve the review workflow and localization.
- Explore agent-assisted extraction and explanations with clear evidence and human oversight.
- Deploy and validate a public demo.

## License

MIT. See [LICENSE](LICENSE).
