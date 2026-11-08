"""Transparent, explainable order-risk heuristics for the OrderGuard prototype."""

import math

import pandas as pd

REQUIRED_COLUMNS = ["order_id", "customer", "phone", "address", "total", "previous_orders", "notes"]


def _is_finite_number(value):
    """Return whether a parsed numeric value is finite and usable."""
    return pd.notna(value) and math.isfinite(float(value))


def _is_blank(value):
    """Return True when a contact field is absent, NaN, or whitespace-only."""
    return pd.isna(value) or not str(value).strip()


def assess_order(row):
    """Return a bounded score, risk label, reasons, and human-review action."""
    score = 0
    reasons = []
    checks = [
        (_is_blank(row.phone), 30, "Phone number is missing"),
        (_is_blank(row.address), 25, "Delivery address is missing"),
        # Guard with pd.notna so that NaN previous_orders (invalid/missing data) does NOT
        # trigger the no-history penalty — only a genuine zero or negative value does.
        (pd.notna(row.previous_orders) and row.previous_orders <= 0, 15, "No previous successful orders recorded"),
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
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in source.columns]
    if missing_columns:
        raise ValueError("Missing required columns: " + ", ".join(missing_columns))

    frame = source[REQUIRED_COLUMNS].copy()
    for column in ["order_id", "customer", "phone", "address", "notes"]:
        frame[column] = frame[column].fillna("").astype(str).str.strip()

    frame["total"] = pd.to_numeric(frame["total"], errors="coerce")
    frame["previous_orders"] = pd.to_numeric(frame["previous_orders"], errors="coerce")

    duplicate_ids = frame["order_id"].ne("") & frame["order_id"].duplicated(keep=False)
    issues = []
    for position, (_, row) in enumerate(frame.iterrows()):
        problems = []
        if not row["order_id"]:
            problems.append("Missing order ID")
        elif duplicate_ids.iloc[position]:
            problems.append("Duplicate order ID")
        if not row["customer"]:
            problems.append("Missing customer name")
        if not _is_finite_number(row["total"]):
            problems.append("Invalid order value")
        elif row["total"] < 0:
            problems.append("Negative order value")
        if not _is_finite_number(row["previous_orders"]):
            problems.append("Invalid order history")
        elif row["previous_orders"] < 0:
            problems.append("Negative order history")
        issues.append(" • ".join(problems))

    frame["data_issues"] = issues
    frame["total"] = frame["total"].where(frame["total"].map(_is_finite_number), 0)

    # previous_orders NaN replacement is deferred until after assess_order so that
    # invalid/missing history does not silently trigger the no-history risk penalty.
    # assess_order guards with pd.notna() and skips the penalty for NaN values.
    assessed_cols = ["risk_score", "risk_level", "risk_reasons", "recommended_action"]
    if frame.empty:
        # apply() on an empty DataFrame does not create the assessed columns;
        # add them explicitly so callers always receive a consistent schema.
        for col in assessed_cols:
            frame[col] = pd.Series(dtype="object")
    else:
        assessed = frame.apply(
            lambda row: pd.Series(
                assess_order(row),
                index=assessed_cols,
            ),
            axis=1,
        )
        frame[assessed_cols] = assessed

    # Replace NaN/inf previous_orders with 0 now that scoring is complete.
    frame["previous_orders"] = frame["previous_orders"].where(
        frame["previous_orders"].map(_is_finite_number), 0
    )

    flagged = frame["data_issues"] != ""
    frame.loc[flagged, "risk_reasons"] = frame.loc[flagged, "risk_reasons"].apply(
        lambda value: (value + " • " if value else "") + "Data quality issue needs correction"
    )
    return frame.sort_values(["risk_score", "order_id"], ascending=[False, True]).reset_index(drop=True)
