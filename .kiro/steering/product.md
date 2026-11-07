# OrderGuard AI — Product Steering

## Product vision
Help small e-commerce sellers review incoming orders consistently, prioritize manual confirmation, and reduce avoidable cash-on-delivery dispatch mistakes.

## Target users
- Small online shops and social-commerce sellers.
- Businesses that accept cash on delivery.
- Operators who review orders manually through messages, spreadsheets, or order exports.

## Core user problem
A seller may receive many order requests but lack a simple way to spot incomplete information or orders that deserve an additional confirmation step.

## MVP scope
- Import a CSV using the documented schema.
- Analyze each order using transparent, explainable rules.
- Show a risk score, contributing indicators, and a suggested next action.
- Filter and export analyzed orders.
- Include synthetic sample data for a safe public demo.

## Product principles
- Never present a risk score as proof of fraud.
- Never claim to verify a customer's identity, phone, or address without a real verification integration.
- Keep human review in the loop.
- Do not include real customer personal data in sample files, screenshots, or demos.
- Make limitations visible to users.

## Out of scope for the first MVP
- Sending SMS or WhatsApp messages.
- Connecting to shipping-company APIs.
- Automated order rejection.
- Claims of guaranteed delivery or fraud prevention.
