# OrderGuard AI — Requirements

## User stories

### 1. Import orders
As a shop operator, I want to upload a CSV of orders so I can review multiple orders in one place.

Acceptance criteria:
- The app accepts CSV files.
- The app checks for order_id, customer, phone, address, total, previous_orders, and notes.
- Missing required columns produce a clear error rather than a crash.

### 2. Assess order risk
As a shop operator, I want to see why an order needs attention so I can decide what to verify.

Acceptance criteria:
- Each order receives a score from 0 to 100.
- The interface shows the rules that contributed to the score.
- Risk labels are Low, Medium, or High.
- The interface explains that scores are indicators, not proof of fraud.

### 3. Recommend a next step
As a shop operator, I want a suggested verification action so I can handle risky orders consistently.

Acceptance criteria:
- High-risk orders recommend manual confirmation of phone and address before dispatch.
- Medium-risk orders recommend reviewing missing details.
- Low-risk orders can follow the normal confirmation workflow.
- No order is automatically rejected.

### 4. Review and export
As a shop operator, I want to filter and export analyzed orders.

Acceptance criteria:
- The dashboard can filter by risk level.
- The operator can inspect an individual order's reasons and suggested action.
- The analyzed dataset can be downloaded as CSV.

## Non-functional requirements
- The demo runs without API keys.
- Sample data is synthetic.
- The UI is usable on a desktop browser.
