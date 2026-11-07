# Technical Steering

## Stack
- Python 3.11+
- Streamlit for the web interface
- pandas for CSV handling and tabular analysis
- Altair for charts
- unittest for automated tests

## Architecture
- `app.py` owns the Streamlit UI, navigation, upload workflow, and presentation.
- `risk_engine.py` owns required-column checks, data normalization, data-quality flags, deterministic scoring, and recommendations.
- `tests/test_risk_engine.py` verifies core scoring and data-validation behavior.
- Keep scoring logic independent from Streamlit so it remains testable.

## Engineering rules
- Validate uploaded CSV columns before analysis.
- Read UTF-8 CSVs with BOM support.
- Convert numeric fields safely and flag invalid or negative values.
- Flag duplicate non-empty order IDs.
- Keep risk rules deterministic and explainable.
- Never present a risk score as proof of fraud.
- Never claim identity, phone ownership, or address verification without a real integration.
- Keep a human in the loop; do not automatically reject orders.
- Do not require API keys or paid external services to run the demo.
- Use synthetic data only in the repository and public demos.
- Add tests for scoring and validation changes.

## Local run
1. Create and activate a virtual environment.
2. Install requirements with pip.
3. Run `streamlit run app.py`.
4. Run tests with `python -m unittest discover -s tests -v`.
