"""Transparent, explainable order-risk heuristics for the OrderGuard prototype."""

import pandas as pd

REQUIRED_COLUMNS = ["order_id", "customer", "phone", "address", "total", "previous_orders", "notes"]


def assess_order(row):
    """Return a bounded score, risk label, reasons, and human-review action."""
    score = 0
    reasons = []
    checks = [
        (not str(row.phone).strip(), 30, "Phone number is missing"),
        (not str(row.address).strip(), 25, "Delivery address is missing"),
        (row.previous_orders <= 0, 15, "No previous successful orders recorded"),
        (row.total >= 250, 10, "Order value is relatively high"),
        (
            any(word in str(row.notes).lower() for word in ["urgent", "cancel", "fake", "change address"]),
            20,
            "Order note needs manual review",
        ),
    ]
    for condition, points, reason in checks:
        if condition:
            score += points
            reasons.append(reason)

    score = min(score, 100)
    level = "High" if score >= 50 else "Medium" if score >= 25 else "Low"
    actions = {
        "High": "Contact the customer and confirm the phone number and full address before dispatch.",
        "Medium": "Review the flagged details and send a customer confirmation message.",
        "Low": "Continue with the normal order-confirmation workflow.",
    }
    explanation = " • ".join(reasons) if reasons else "No rule-based warning detected"
    return score, level, explanation, actions[level]


def prepare_orders(source):
    """Normalize imported rows, flag data-quality problems, and assess every order."""
    frame = source.copy()
    for column in ["order_id", "customer", "phone", "address", "notes"]:
        frame[column] = frame[column].fillna("").astype(str).str.strip()

    frame["total"] = pd.to_numeric(frame["total"], errors="coerce")
    frame["previous_orders"] = pd.to_numeric(frame["previous_orders"], errors="coerce")

    issues = []
    for _, row in frame.iterrows():
        problems = []
        if not row["order_id"]:
            problems.append("Missing order ID")
        if not row["customer"]:
            problems.append("Missing customer name")
        if pd.isna(row["total"]):
            problems.append("Invalid order value")
        elif row["total"] < 0:
            problems.append("Negative order value")
        if pd.isna(row["previous_orders"]):
            problems.append("Invalid order history")
        elif row["previous_orders"] < 0:
            problems.append("Negative order history")
        issues.append(" • ".join(problems))

    frame["data_issues"] = issues
    frame["total"] = frame["total"].fillna(0)
    frame["previous_orders"] = frame["previous_orders"].fillna(0)

    assessed = frame.apply(
        lambda row: pd.Series(
            assess_order(row),
            index=["risk_score", "risk_level", "risk_reasons", "recommended_action"],
        ),
        axis=1,
    )
    frame[assessed.columns] = assessed
    flagged = frame["data_issues"] != ""
    frame.loc[flagged, "risk_reasons"] = frame.loc[flagged, "risk_reasons"].apply(
        lambda value: (value + " • " if value else "") + "Data quality issue needs correction"
    )
    return frame.sort_values(["risk_score", "order_id"], ascending=[False, True]).reset_index(drop=True)
