# OrderGuard AI — Hackathon Submission Draft

## Tagline
Explainable order review for cash-on-delivery e-commerce.

## Short description
OrderGuard AI is a prototype workspace that helps small e-commerce sellers organize incoming COD orders, identify incomplete or unusual records, understand transparent review signals, and prioritize manual customer confirmation.

## Problem
Small social-commerce sellers often handle orders from messages, spreadsheets, and exported files. Reviewing every order consistently can be difficult, especially when contact details are missing, order history is limited, or notes require clarification.

## Solution
OrderGuard imports a seller's CSV, checks data quality, calculates a deterministic and explainable review score, displays the reasons behind each score, and suggests a manual next step. Operators can search, filter, inspect, analyze, and export their current batch.

## What is built
- Streamlit workspace with Overview, Orders, Analytics, and How it works pages.
- CSV upload with required-column checks and UTF-8 BOM support.
- Data-quality flags for missing values, invalid/negative numeric values, and duplicate non-empty order IDs.
- Rule-based score from 0 to 100 with Low, Medium, and High bands.
- Per-order explanations and human-review recommendations.
- Search, filters, order inspection, and filtered CSV export.
- Synthetic sample dataset and unit tests.
- Kiro product/technical steering and MVP requirements/design/tasks in `.kiro/`.

## Technology
Python, Streamlit, pandas, Altair, and unittest.

## Responsible-use note
OrderGuard AI is an early prototype. Its thresholds are illustrative and have not been statistically validated. Scores are not proof of fraud. The app does not verify identity, phone ownership, or delivery addresses, and it does not automatically reject orders. Human review remains essential. Public demos should use synthetic data only.

## Kiro development evidence
Describe only the Kiro features actually used in the build. Add genuine screenshots or a short explanation of your actual Kiro IDE workflow before submission. Do not claim agent, hook, MCP, property-based testing, or other feature usage unless it happened and can be demonstrated.

## Before submitting
- [ ] Run unit tests and capture the passing result.
- [ ] Test all four pages in a browser.
- [ ] Test upload with `sample_orders.csv`.
- [ ] Test a CSV with missing columns and a CSV with duplicate IDs.
- [ ] Deploy and verify a public app URL.
- [ ] Record an unlisted/public YouTube demo under the event's time limit.
- [ ] Add authentic Kiro usage evidence.
- [ ] Confirm all event-specific eligibility and submission rules.
