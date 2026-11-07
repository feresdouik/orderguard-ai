# OrderGuard AI MVP — Design

## Architecture
The prototype is a single-process Streamlit application with a separately testable Python risk engine.

- `app.py`: page configuration, navigation, CSV upload, dashboard metrics, charts, order search/filter/detail, CSV export.
- `risk_engine.py`: required-column validation, normalization, data-quality diagnostics, deterministic scoring, explanation, recommended action.
- `tests/test_risk_engine.py`: unit tests for core scoring and validation.
- `sample_orders.csv`: synthetic upload-ready example dataset.

## Data flow
1. The operator uploads a CSV or uses the built-in synthetic sample.
2. The UI checks required column names.
3. `prepare_orders` normalizes text and numeric fields and creates data-quality diagnostics.
4. `assess_order` applies transparent rules and returns score, risk band, explanation, and manual next step.
5. The UI renders summaries and order-level details.
6. The operator can export the filtered rows.

## Risk rules
- Missing phone: +30
- Missing address: +25
- No previous successful orders recorded: +15
- Order total at or above 250: +10
- Notes containing selected review keywords: +20
- Score capped at 100.

Bands: Low 0–24, Medium 25–49, High 50–100.

These values are initial heuristics, not statistically validated thresholds. Data-quality flags and risk signals are separate concepts.

## Current non-goals
- User accounts or authentication
- Persistent database
- Storefront integrations
- SMS, WhatsApp, or shipping integrations
- Machine-learning fraud classification
- Automatic order rejection
- Production-grade security or privacy certification

## Failure handling
- Missing CSV columns stop processing with a readable message.
- Invalid numeric cells are flagged and safely replaced with zero for calculations.
- Duplicate order IDs are flagged; the order inspector uses row identity rather than assuming IDs are unique.
- Empty or non-matching filtered views show a clear empty state.
