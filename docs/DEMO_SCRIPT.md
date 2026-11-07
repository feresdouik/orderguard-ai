# OrderGuard AI — Demo Video Script (Target: 2:30)

> Record only after the latest version has been tested in a browser. Use synthetic data only.

## 0:00–0:20 — Problem
"Small online sellers often receive COD orders from social channels and have to review each one manually. Incomplete phone numbers, unclear addresses, and unusual notes can make dispatch decisions harder. OrderGuard AI gives sellers a consistent way to organize these checks."

## 0:20–0:40 — Product overview
"OrderGuard is an explainable order-review workspace. It is a prototype built with Streamlit and Python. It does not claim to prove fraud or verify a customer's identity."

Show the Overview page and its order count, high/medium risk counts, data-quality count, and risk distribution.

## 0:40–1:15 — Import and data validation
"An operator can use the built-in synthetic sample or upload a CSV with the documented columns."

Show the sidebar CSV uploader. Upload `sample_orders.csv`. Show the required columns and the loaded file state.

## 1:15–1:50 — Investigate an order
"Each risk score is based on transparent rules. The operator can see which signals contributed and what manual step is suggested."

Open Orders. Search or filter an order. Inspect its score, reasons, data-quality flags, and suggested action. Emphasize that this is a review aid, not an automatic rejection.

## 1:50–2:10 — Analytics and export
"Analytics summarize the current batch. The operator can export the filtered results for their existing workflow."

Show Analytics, return to Orders, and click Export filtered orders.

## 2:10–2:30 — Kiro and next steps
"Development is guided by product and technical steering plus MVP requirements, design, and task documents in the `.kiro` directory. The scoring engine is separated from the interface and covered by unit tests."

Only mention Kiro IDE, specs, agents, hooks, MCP, or other capabilities if you personally used them and can show authentic evidence.

Close with: "OrderGuard AI keeps order review explainable and human-led."
