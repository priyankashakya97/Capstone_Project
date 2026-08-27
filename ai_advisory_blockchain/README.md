# AI-Augmented FinTech Advisory + Blockchain Risk

This part builds a small set of agentic finance tools on top of a shared stock and investor dataset: a CAPM-based portfolio advisory agent with human-in-the-loop escalation, a rule-based disclosure signal extractor, a 3-agent (bull/bear/synthesizer) debate demo, a DCF valuation calculator with a WACC/terminal-growth sensitivity table, and a written appendix on crypto and fraud risk. All example runs below were recorded with `MOCK_LLM` left at its default (`mock_llm=1`, i.e. rule-based/mock mode, no live LLM calls).

## Files

- `stock_universe.py` — shared ticker data (beta, expected return, std dev) plus risk-free/market return assumptions.
- `investor_profiles.py` — sample investor records used by the advisory agent.
- `disclosure_snippets.py` — sample disclosure text snippets used by the extractor.
- `advisory_agent.py` — `AdvisoryAgent` class: CAPM portfolio return/volatility by risk tolerance, escalates to a human advisor above a 20% volatility threshold.
- `extract_disclosure.py` — `extract_signals`: pulls risk flags, hedging language, and sentiment out of disclosure text.
- `debate.py` — `run_debate`: generates a bull case, bear case, and balanced synthesis for a chosen ticker.
- `dcf_calculator.py` — `calculate_dcf`: FCFF/WACC-based DCF valuation with a 3x3 sensitivity grid and an EV/EBITDA cross-check.
- `blockchain_risk_note.md` — written appendix on stablecoin/DeFi risk, a crypto allocation recommendation for Paytm Money, and a T.A.N.G. fraud-vector analysis for a UPI/wallet + lending + wealth platform.

**Known discrepancy to review:** `debate.py` keeps its own local `STOCK_UNIVERSE` copy (as it did in the original notebook cell), and its beta/return/std-dev values don't match `stock_universe.py` — e.g. PAYFIN is beta 1.3 there vs. 1.35 in the shared file. Similarly, `dcf_calculator.py` hardcodes `beta = 1.30` in a comment that says it's "chosen from PAYFIN," but PAYFIN's beta in `stock_universe.py` is 1.35. Both are left as-is here to match the recorded transcripts below — worth deciding whether to consolidate onto the shared `stock_universe.py` before submitting.

## Example run transcripts

### `advisory_agent.py`

```
[INV01] Output: {'status': 'FINALIZED', 'investor_id': 'INV01', 'recommendation': 'For Conservative investor INV01, we recommend an allocation across PAYBOND, PAYGOLD, PAYRETAIL with an expected portfolio return of 4.8% and volatility of 8.4%.', 'expected_return': 0.04833333333333334, 'volatility': 0.08439325934114775}
[INV02] Output: {'status': 'FINALIZED', 'investor_id': 'INV02', 'recommendation': 'For Moderate investor INV02, we recommend an allocation across PAYRETAIL, PAYINFRA, PAYGOLD with an expected portfolio return of 6.6% and volatility of 12.6%.', 'expected_return': 0.06583333333333334, 'volatility': 0.12570689011435382}
[INV03] Output: {'status': 'ESCALATED_TO_HUMAN_ADVISOR', 'investor_id': 'INV03', 'risk_tolerance': 'Aggressive', 'expected_return': 0.09666666666666666, 'volatility': 0.20584784024451977}
[INV04] Output: {'status': 'FINALIZED', 'investor_id': 'INV04', 'recommendation': 'For Moderate investor INV04, we recommend an allocation across PAYRETAIL, PAYINFRA, PAYGOLD with an expected portfolio return of 6.6% and volatility of 12.6%.', 'expected_return': 0.06583333333333334, 'volatility': 0.12570689011435382}
[INV05] Output: {'status': 'ESCALATED_TO_HUMAN_ADVISOR', 'investor_id': 'INV05', 'risk_tolerance': 'Aggressive', 'expected_return': 0.09666666666666666, 'volatility': 0.20584784024451977}
```

### `extract_disclosure.py`

```
=== Structured Disclosure Extraction ===
Snippet 1:
  Text:   "doc_01: Assuming input costs remain stable through the next two quarters, we expect margins to hold at current levels."
  Output: {'risk_flags': [], 'hedging_detected': True, 'sentiment': 'cautious'}

Snippet 2:
  Text:   "doc_02: The company faces an ongoing litigation matter related to a former vendor contract; management believes the exposure is not material."
  Output: {'risk_flags': ['litigation'], 'hedging_detected': False, 'sentiment': 'neutral'}

Snippet 3:
  Text:   "doc_03: Our top three customers together account for approximately 42 percent of total revenue this year."
  Output: {'risk_flags': [], 'hedging_detected': False, 'sentiment': 'neutral'}

Snippet 4:
  Text:   "doc_04: We remain cautiously optimistic about demand recovery, though visibility beyond the next quarter is limited given macro uncertainty."
  Output: {'risk_flags': [], 'hedging_detected': True, 'sentiment': 'cautious'}

Snippet 5:
  Text:   "doc_05: The board is confident in the long-term strategy and has approved an expanded capital expenditure plan for the coming year."
  Output: {'risk_flags': [], 'hedging_detected': False, 'sentiment': 'confident'}

Snippet 6:
  Text:   "doc_06: A recent regulatory notice has been received regarding data-localization compliance; the company is in active dialogue with the regulator."
  Output: {'risk_flags': ['regulatory'], 'hedging_detected': False, 'sentiment': 'neutral'}
```

### `debate.py`

```
=== Multi-Agent Debate for PAYTECH ===
🐂 Bull Agent:
With an expected return of 18.0% against a beta of 1.50, this offers attractive risk-adjusted upside.

🐻 Bear Agent:
However, a volatility (std_dev) of 30.0% presents significant risk and potential downside exposure under volatile market conditions.

⚖️ Synthesizer Agent:
While PAYTECH demonstrates strong upside potential with an expected return of 18.0%, its standard deviation of 30.0% highlights non-trivial volatility risk. Investors should balance the 1.50 beta exposure against their overall portfolio risk tolerance.
```

### `dcf_calculator.py`

```
=== ASSUMPTIONS & SANITY CHECKS ===
Base FCFF: ₹340.00 Crores
Calculated Cost of Equity: 14.80%
Calculated Base WACC: 13.19%
Base Terminal Growth: 5.00%
Worst-case Cell Spread (WACC - 1pp) - (g + 1pp): 6.19%
✅ Constraint Passed: WACC exceeds terminal growth by at least 1pp in all 9 grid cells.

=== MULTIPLE CROSS-CHECK ===
EBITDA: ₹550.00 Crores
EV / EBITDA Multiple: 12.0x
Multiple-based Enterprise Value: ₹6600.00 Crores
DCF Base Enterprise Value: ₹5608.88 Crores

=== COMMENTARY ===
The DCF valuation yields a base Enterprise Value of ₹5608.88 Crores, which aligns closely with the peer EV/EBITDA multiple approach valuation of ₹6600.00 Crores (a difference of -15.0%). This close alignment confirms that our 5-year cash flow forecast, conservative 13.19% WACC, and 5.0% terminal growth rate provide a realistic valuation anchor grounded in market trading multiples.
```

#### DCF sensitivity table (Enterprise Value, INR Crores)

| WACC \ Terminal g | 4.00% | 5.00% | 6.00% |
|---|---|---|---|
| 12.19% | ₹5,792.76 | ₹6,405.90 | ₹7,217.15 |
| 13.19% (base) | ₹5,145.90 | ₹5,608.88 | ₹6,200.63 |
| 14.19% | ₹4,626.47 | ₹4,985.71 | ₹5,432.68 |

## Blockchain risk appendix

See `blockchain_risk_note.md` for the written analysis (stablecoin/DeFi risk for a hypothetical "Paytm Crypto Insights" feature, a CAPM-based crypto allocation recommendation for Paytm Money, and a T.A.N.G. fraud-vector analysis).
