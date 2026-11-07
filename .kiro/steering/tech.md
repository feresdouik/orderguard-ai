# Technical Steering

## Stack
- Python 3.11+
- Streamlit for the web interface
- pandas for CSV handling and tabular analysis

## Architecture
Keep the first prototype small and readable. Separate data validation, risk assessment, and UI rendering as the product grows. The initial MVP may keep these in app.py while the workflow is validated.

## Engineering rules
- Validate uploaded CSV columns before analysis.
- Convert numeric fields safely and handle missing values.
- Keep risk rules deterministic and explainable.
- Do not require API keys or paid external services to run the demo.
- Use synthetic data only in the repository.
- Keep dependencies minimal.
- Add tests for scoring rules before adding more complex behavior.

## Local run
1. Create and activate a virtual environment.
2. Install requirements with pip.
3. Run `streamlit run app.py`.
