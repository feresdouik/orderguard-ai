# OrderGuard AI — Design

## MVP flow
1. Operator opens the dashboard.
2. Operator uses synthetic sample orders or uploads a CSV.
3. The app validates the schema.
4. A deterministic scoring function evaluates each order.
5. The dashboard displays aggregate counts and a prioritized order table.
6. Operator selects an order to inspect contributing indicators and the recommended manual action.
7. Operator downloads the analyzed CSV if needed.

## Risk scoring (initial heuristic)
- Missing phone: +30
- Missing delivery address: +25
- No previous orders recorded: +15
- Order total at or above 250 (currency units supplied by the seller): +10
- Notes include urgent, cancel, fake, or change address: +20
- Cap final score at 100.

Risk levels:
- Low: 0–24
- Medium: 25–49
- High: 50–100

These thresholds are an initial demo heuristic, not a statistically validated fraud model. They must be configurable and evaluated with real, consented, appropriately governed data before production use.

## Future agent-oriented architecture
The product may later introduce specialized agents for order-field extraction, completeness checks, risk explanation, and verification workflow recommendations. Each agent must return evidence and uncertainty; no agent may claim external identity or address verification without an integration.
