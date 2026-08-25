# payments_fraud_analytics

A small end-to-end exercise on a synthetic Paytm-style payments dataset: spreadsheet
lookups, SQL fraud queries, a Python reconciliation function, and a 4-layer chart
dashboard. Data is generated once with a fixed seed so results are reproducible.

## What's in here

```
generate_data.py          # builds merchants.csv, users.csv, ledger.csv, gateway_export.csv (seed=42)
merchants.csv / users.csv / ledger.csv / gateway_export.csv
merchant_workbook.xlsx    # Part A — VLOOKUP/HLOOKUP/IF/pivot in Excel
paytm_payments.db         # Part B — SQLite database + SQL_Queries.txt (6 queries, output included)
reconcile.py              # Part C — reconcile_payments(ledger_df, gateway_df)
dashboard.ipynb           # Part D — headline/trends/breakdown/details charts
layer1_headline.png, layer2_trends.png, layer3_breakdown.png, layer4_details_table.png
```

## Running it

```bash
pip install pandas matplotlib seaborn openpyxl
python generate_data.py          # regenerates the 4 CSVs (seed 42, deterministic)
python reconcile.py              # prints the 4 discrepancy counts
sqlite3 paytm_payments.db < schema_and_load.sql   
# re-runs Part D and re-saves the 4 PNGs
```

`merchant_workbook.xlsx` is a plain Excel file — open it directly, no macros needed.

## Part A — merchant_workbook.xlsx

- **VLOOKUP** on `TransactionsView` pulls `merchant_name`, `category`, `region` from the
  `Merchants` sheet using a fixed range (`$A$2:$D$41` style absolute refs), wrapped in
  `IFERROR` so an unmatched `merchant_id` shows `"Merchant not found"` instead of `#N/A`.
- **HLOOKUP** reads fee percentages off a one-row `FeeTiers` table (payment methods laid
  out across columns). Fee assumptions are made up for the exercise, not real MDR rates:
  UPI 1%, Wallet 2%, Card 3%, Netbanking 3%.
- **Classification rule** (nested `IF`/`AND`): a transaction is `"High-Value Merchant Day"`
  when that merchant's same-day transaction total (`merchant_daily_total`, from the pivot)
  is **> ₹5,000** *and* the merchant's region is **not East**. 10 of 547 rows qualify.
  Everything else is `"Standard Day"`.
- **Pivots**: `Pivot_MerchantStatus` — total `amount_inr` and transaction count by
  `merchant_id` × `status`. `Pivot_UniqueDays` — total transactions vs. unique days
  transacted per merchant (covers all 40 merchants, well past the 5 required).

## Part B — SQL (paytm_payments.db)

Schema: `merchants(merchant_id PK, merchant_name, category, region)`,
`users(user_id PK, signup_date)`, `transactions(transaction_id PK, user_id FK, merchant_id FK, transaction_time, amount_inr, payment_method, status, risk_score)`.

Six queries in `SQL_Queries.txt`, each with output:

1. **Chargeback impact** — `SELECT`/`WHERE`/`DISTINCT`: 28 chargeback transactions, 27
   unique users affected, ₹54,472 total.
2. **High-risk merchants** — `GROUP BY`/`HAVING chargeback_count > 0`, `ORDER BY`.
3. **Burner accounts** — `INNER JOIN` users↔transactions, boundary written as
   `t.transaction_time >= u.signup_date AND t.transaction_time < signup_date + 30 days`
   (never negative age, never exactly 30). Surfaces all 15 seeded rows.
4. **User profile audit** — `LEFT JOIN` users→transactions so zero-transaction users
   still show up, `ORDER BY`/`LIMIT`.
5. **Velocity attacks** — groups by `user_id` + a floored 10-minute time bucket
   (`FLOOR(UNIX_TIMESTAMP/600)*600`), `HAVING count >= 3`. Surfaces all 8 seeded clusters
   (each a distinct user_id + cluster start time).
6. **Payment method risk** — combined aggregation of failed/chargeback counts and avg
   risk score per `payment_method`.

*Note:* these were drafted/tested on db-fiddle in MySQL syntax (`DATEDIFF`,
`FROM_UNIXTIME`, `DATE_ADD`). If `paytm_payments.db` is genuinely SQLite, swap those for
`julianday()`/`strftime()` equivalents before final submission — logic is identical,
only the date functions differ.

## Part C — reconcile.py

`reconcile_payments(ledger_df, gateway_df)` does two set operations on `transaction_id`
(ledger-only, gateway-only) plus a merge-and-compare on the common IDs for amount and
status mismatches. Run against the committed CSVs:

| category | count | % of 547 | target |
|---|---|---|---|
| Missing in gateway | 27 | 4.9% | ~5% |
| Missing in ledger (extra in gateway) | 10 | 1.8% | ~2% |
| Amount mismatches | 16 | 2.9% | ~3% |
| Status mismatches | 9 | 1.6% | ~2% |

All four land right on the injected rates.

## Part D — dashboard

Four saved chart images, matplotlib/seaborn, no live BI tool.

**Headline** (`layer1_headline.png`) — Total GMV ₹3,82,603, 85.56% success rate, 90.49%
reconciliation match rate, 5.12% chargeback ratio. GMV here is the sum of `amount_inr`
across *all* ledger rows regardless of status, not captured-only — worth knowing if you
compare this number to a different pull later. Match rate uses the strict definition
(same amount **and** same status in both files), so it reads worse than the four Part C
categories individually — that's expected, not a bug, since ~1 in 10 rows fails on at
least one field even where each individual category looks small.

**Trends** (`layer2_trends.png`) — Daily GMV bounces around with no real monthly trend,
roughly ₹4k–23k a day. Chargebacks stay near zero through the first half of January,
then climb noticeably after Jan 20 — worth flagging to risk/ops as the one thing in this
window that isn't flat.

**Breakdown** (`layer3_breakdown.png`) — UPI alone is ₹1,72,274, about 45% of total GMV
and more than Card, Wallet, and Netbanking combined, which tracks with real UPI usage
share in India. By category, ecommerce, travel, and grocery are all close together at
the top (₹72k–80k); recharge is the smallest slice at ₹15k.

**Details** (`layer4_details_table.png`) — Of the top 10 merchants by transaction count,
7 exceed the 1% per-merchant chargeback-ratio flag. merchant_id 27 and 29 are the
standouts at 18.75% and 15.79%, but both are on a base of only 16–19 transactions, so
treat those ratios as "watch this account" rather than confirmed fraud — the sample is
too small to be conclusive on its own.


