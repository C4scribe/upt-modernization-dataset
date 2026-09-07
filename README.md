# United Public Trust (UPT) — Modernization Sandbox Dataset

This repository contains the synthetic relational dataset and Python data generation engine built to support the **United Public Trust (UPT) Enterprise Platform Modernization** case study. 

It simulates a high-scale, public-sector benefits administration platform migrating from a legacy mainframe environment (Mainframe Core Ledger) to a modern, relational SQL backend. This dataset provides a clean, privacy-compliant sandbox for testing database schemas, business rules engines, and Power BI reporting.

---

## Repository Contents

This repository is structured as a fully normalized relational database consisting of five core transactional tables and the python generator script:

1. **`employer-groups.csv`**: Master profiles of public sector employer units (school districts, municipalities) with their active billing types (Fully-Insured, Self-Funded, Self-Billed) and banking metadata.
2. **`benefit-subscribers.csv`**: Active and COBRA subscriber registry including coverage effective dates, fake SSNs, and enrollment state controls.
3. **`subscriber-dependents.csv`**: Child table linking spouses, children, and higher-education students (with academic term certification dates) to primary subscribers.
4. **`group-premium-ledger.csv`**: A 12-month historical transactional ledger (Oct 2025–Sep 2026) capturing expected premiums, cash postings, variances, and reconciliation statuses (Underpaid, Delinquent, Paid-in-Advance).
5. **`ach-bank-statement.csv`**: A "payee-blind" incoming bank statement feed designed to test automated ACH reconciliation algorithms.
6. **`upt-data-generator.py`**: The clean Python engine (written in pandas/NumPy) used to programmatically model the database and enforce business rules.

---

## Implemented Systems Logic & Business Rules

Unlike randomly generated mock data, this dataset dynamically enforces the complex backend business rules defined in the UPT modernization specification:

### 1. Automated Billing Tier Rules Engine
Before generating monthly invoices, the data generator parses the child dependent registry (`subscriber-dependents.csv`) for every active subscriber. It automatically calculates and assigns their monthly contract billing tier based on the following relational rules:
*   **Single**: Subscriber has 0 active dependents.
*   **Member & Spouse**: Subscriber has exactly 1 dependent of type `Spouse`.
*   **Single w/ Dependent**: Subscriber has exactly 1 dependent of type `Child` or `FT Student`.
*   **Family**: Subscriber has $\ge 2$ dependents.

### 2. ACH 3-Rank Matching Ingestion Simulation
The `ach-bank-statement.csv` file features realistic, messy bank-end transit strings. It is designed to test the **3-Rank Reconciliation Query Logic** highlighted in the case study:
*   **Rank 1 (Exact Match)**: Matches routing numbers and exact expected invoice amounts.
*   **Rank 2 (Template Match)**: Uses known historical bank wire configurations to link accounts.
*   **Rank 3 (Heuristic Text Match)**: Simulates fuzzy name/string matching (e.g., matching a bank wire from `"MAPLE VLY SD PMT"` to `"Maple Valley School District"` on the ledger).

---

## Case Study Portfolio
This dataset is a companion to the master case study. To read the full Product Owner roadmap, Gherkin user stories, and technical requirements analysis, visit my portfolio page:
https://wakelessriverpress.com/case-study-enterprise-modernization/
----

## How to Run the Data Generator

To regenerate the dataset locally or modify the scaling factors (e.g., generating 10,000+ rows for high-volume database performance testing), ensure you have `pandas` installed and run:

```bash
python3 upt-data-generator.py


