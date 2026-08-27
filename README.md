# Capstone Project — Executive Certification in FinTech & Artificial Intelligence

A single repository covering three parts: payments fraud analytics (spreadsheet + SQL +
Python + dashboard), a credit-risk lending ML pipeline, and an AI-augmented advisory /
blockchain-risk exercise. All monetary figures across the project are in INR.

```
payments_fraud_analytics/     Part 1 — spreadsheet, SQL, reconciliation, dashboard
credit_risk_lending_ml/       Part 2 — EDA, classification, anomaly detection, bias note
ai_advisory_blockchain/       Part 3 — advisory agent, disclosure extraction, debate, DCF, crypto risk note
```

Each part folder also has its own `README.md` with full detail; this file is the
entry point — setup, how to run everything end to end, and a short summary of the
design decisions in each part.

## Setup

One **consolidated `requirements.txt` at the repo root** covers all Python
dependencies needed across all three parts (Part 3 uses only the standard library, so
nothing extra is needed for it specifically).

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Part 1's `merchant_workbook.xlsx` is a plain spreadsheet file — open it directly in
Excel, Google Sheets, or LibreOffice Calc, no install or macros needed.

## Running each part end to end

### Part 1 — `payments_fraud_analytics/`

Seed data is generated with a fixed seed (42) so results are reproducible. The
generator writes its CSVs via relative paths, so it must be run from inside this
folder:

```bash
cd payments_fraud_analytics
python generate_data.py      # regenerates merchants.csv, users.csv, ledger.csv, gateway_export.csv
python reconcile.py          # prints the 4 reconciliation discrepancy counts
```

Then open `merchant_workbook.xlsx` directly for the spreadsheet part (VLOOKUP,
HLOOKUP, nested IF, pivot tables). `SQL_Queries.txt` is a self-contained text file —
schema DDL, seed `INSERT`s, and all 6 queries with their output already included, so
it can be read end to end without a live database. `Dashboard.ipynb` reproduces Part
D when run top to bottom: the headline layer prints its 4 KPIs directly (no image),
and the trends/breakdown/details layers each save a chart PNG.

### Part 2 — `credit_risk_lending_ml/`

Also generated with a fixed seed, also run from inside its own folder:

```bash
cd credit_risk_lending_ml
python generate_data.py      # regenerates credit_applicants.csv, txn_behaviour.csv
```

Then open `credit_risk_lending_ml.ipynb` and run all cells top to bottom — it covers
EDA/preprocessing, the two classification models with the ROC comparison (saved as
`roc_curve_comparison.png`), Isolation Forest anomaly detection plus optional K-Means
segmentation, and the bias/governance write-up in the final Markdown cells.

### Part 3 — `ai_advisory_blockchain/`

No seed data step — each script is standalone and runs directly from inside the
folder (all default to `mock_llm=1`, fully deterministic, no API key or paid service
required):

```bash
cd ai_advisory_blockchain
python advisory_agent.py       # CAPM portfolio advisory agent, 5 sample investors
python extract_disclosure.py   # structured signal extraction over 6 disclosure snippets
python debate.py               # bull/bear/synthesizer debate for PAYTECH
python dcf_calculator.py       # DCF valuation + 3x3 WACC/terminal-growth sensitivity table
```

`blockchain_risk_note.md` is the written appendix (stablecoin/DeFi risk, a crypto
allocation recommendation, and a T.A.N.G. fraud-vector analysis) — no code to run for
that piece.

## Design decisions

### Part 1 — Payments fraud analytics

The Excel workbook uses VLOOKUP with `IFERROR` to gracefully label unmatched
merchant IDs instead of surfacing raw `#N/A`, and HLOOKUP against a one-row fee-tier
table for made-up (not real-world) MDR assumptions. The SQL queries were written and
verified separately (see the note in `payments_fraud_analytics/README.md` about
MySQL vs. SQLite date-function syntax before final submission). `reconcile.py` does a
straightforward two-way set comparison on `transaction_id` between the ledger and
gateway export, plus a merge-and-compare for amount/status mismatches on the common
IDs — deliberately simple rather than clever, since reconciliation logic needs to be
easy to audit. The dashboard is four static chart layers (headline KPIs, trends,
breakdown, flagged-merchant detail table) rather than a live BI tool, matching the
"no paid services" constraint.

### Part 2 — Credit risk lending ML

Missing `credit_bureau_score` values (20% of rows) are imputed with the **train-only**
median rather than dropped or imputed from the full dataset, to avoid leaking test-set
information — and a `is_thin_file` flag preserves the fact that a value was missing
rather than hiding it. Logistic Regression is recommended over the Decision Tree
specifically on ROC AUC (0.72 vs. 0.52) rather than accuracy, since the test set is
80% non-default and accuracy alone rewards a lazy "always predict no default" model.
The bias note calls out `employment_type`, `monthly_income_inr`, and even
`credit_bureau_score` itself as potential proxies for demographic factors not directly
in the data, and recommends routing declined thin-file applicants through a human
reviewer before final rejection, since that's the segment with the weakest signal and
the most proxy-risk overlap.

### Part 3 — AI-augmented advisory & blockchain risk

The advisory agent follows a think-act-observe pattern: pick an allocation by risk
tolerance, pull CAPM inputs per ticker, compute portfolio return/variance, and
escalate to a human advisor above a 20% volatility threshold rather than ever auto-
finalizing a high-risk recommendation. Disclosure-signal extraction and the bull/bear
debate both run in fully deterministic mock mode by default (`mock_llm=1`) — no live
LLM calls, no API key, so the whole part runs offline and reproducibly. The DCF
calculator includes an explicit sanity check that terminal growth stays at least 1
percentage point below WACC across all 9 sensitivity-grid cells before proceeding.
The written appendix recommends a **zero allocation to crypto** in any default/advised
Paytm Money portfolio, reasoning from CAPM's requirement of cash-flow-generating
assets, crypto's heavy-tailed/skewed returns, survivorship bias in historical crypto
return data, and transaction costs — and applies the T.A.N.G. fraud framework to flag
Authority (impersonation) and Greed (fake investment schemes) as the two vectors most
relevant to a UPI/wallet + lending + wealth platform, each paired with a concrete
real-time bank-side defense.

## Known gaps to review before submitting

- **Part 1 `reconcile.py`:** was a raw Colab export and called the notebook-only
  `display()` function, which crashes with a `NameError` when run as a plain script —
  exactly how the README tells you to run it. Fixed here (swapped for `print()`); the
  reconciliation logic itself was untouched and verified to still produce the same 4
  discrepancy counts documented in `payments_fraud_analytics/README.md`.
- **Part 1 spreadsheet:** `Pivot_MerchantStatus` is a genuine Excel PivotTable
  object, but `Pivot_UniqueDays` is currently a static summary sheet, not a live
  PivotTable — worth rebuilding as an actual PivotTable (Insert → PivotTable) so both
  required pivots are the real feature, not just pivot-shaped output.
- **Part 1 SQL:** the queries in `SQL_Queries.txt` were drafted/tested in MySQL
  syntax (`DATEDIFF`, `FROM_UNIXTIME`, `DATE_ADD`) — if you run them against a real
  SQLite database, swap in `julianday()`/`strftime()` equivalents first; the logic is
  unchanged, only the date functions differ.
- **Part 3:** `debate.py` carries its own local ticker dataset that differs slightly
  from `stock_universe.py` (e.g. PAYFIN beta 1.3 vs. 1.35), and `dcf_calculator.py`'s
  beta comment says "chosen from PAYFIN" but uses 1.30 against PAYFIN's actual 1.35 in
  `stock_universe.py`. Both are left as-is to match already-recorded output — see
  `ai_advisory_blockchain/README.md` for detail, and consolidate onto one canonical
  dataset if you'd rather not have two different numbers under the same ticker name.

## Academic integrity

All code, analysis, and written interpretations in this repository are original work
for this evaluation.
