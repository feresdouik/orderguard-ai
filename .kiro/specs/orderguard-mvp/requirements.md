# OrderGuard AI MVP — Requirements

## Goal
Provide a small e-commerce operator with a clear, explainable workflow to import COD orders, identify records that need manual review, inspect reasons, and export results.

## User stories and acceptance criteria

### 1. Import order data
As an operator, I want to upload a CSV so I can analyze a batch of orders.
- The app accepts CSV files.
- The app checks for all required columns: `order_id`, `customer`, `phone`, `address`, `total`, `previous_orders`, and `notes`.
- Missing columns produce a readable error before scoring.
- UTF-8 CSV files with a BOM are supported.
- The built-in sample contains synthetic data only.

### 2. Validate data quality
As an operator, I want invalid or incomplete records flagged so I can correct them.
- Missing order IDs and customer names are flagged.
- Invalid or negative order totals and order-history values are flagged.
- Duplicate non-empty order IDs are flagged on each affected row.
- Invalid numeric inputs do not crash the application.

### 3. Review explainable risk signals
As an operator, I want to understand why an order is prioritized.
- The app calculates a deterministic score from documented rules.
- The app displays score, risk band, contributing reasons, and a suggested manual action.
- Risk bands are Low (0–24), Medium (25–49), and High (50–100).
- The app does not describe a score as proof of fraud or automatically reject an order.

### 4. Manage and export orders
As an operator, I want to find and inspect specific orders.
- I can search order ID, customer, phone, and address.
- I can filter by risk band and data-quality status.
- I can inspect an order and see its review reasons.
- I can export the currently filtered result set as CSV.

### 5. Understand the batch
As an operator, I want a concise overview.
- Overview metrics show order count, high-risk count, medium-risk count, and data-quality issue count.
- Charts and analytics are calculated from the currently loaded dataset.

## Safety and privacy
- Public demos use synthetic data.
- Phone numbers and addresses are personal data; real customer data must not be committed or exposed in public demos.
- A human operator remains responsible for confirmation and dispatch decisions.
- No identity, phone ownership, or address verification is claimed.
