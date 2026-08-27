# NOTE: this local STOCK_UNIVERSE mirrors the dataset used in the notebook's
# debate demo. It differs slightly from stock_universe.py (see project README) --
# kept as-is here to match the notebook's original recorded transcript.
STOCK_UNIVERSE = {
    "PAYBOND": {"beta": 0.3, "analyst_expected_return": 0.05, "std_dev": 0.08},
    "PAYGOLD": {"beta": 0.2, "analyst_expected_return": 0.04, "std_dev": 0.10},
    "PAYRETAIL": {"beta": 0.8, "analyst_expected_return": 0.10, "std_dev": 0.15},
    "PAYINFRA": {"beta": 0.9, "analyst_expected_return": 0.11, "std_dev": 0.18},
    "PAYTECH": {"beta": 1.5, "analyst_expected_return": 0.18, "std_dev": 0.30},
    "PAYFIN": {"beta": 1.3, "analyst_expected_return": 0.15, "std_dev": 0.25},
}


def run_debate(ticker: str, mock_llm: int = 1) -> dict:
    """Runs a 3-agent debate (Bull, Bear, Synthesizer) for a chosen ticker.

    Returns:
        {
            "ticker": str,
            "bull_case": str,
            "bear_case": str,
            "synthesis": str
        }
    """
    if ticker not in STOCK_UNIVERSE:
        raise ValueError(f"Ticker '{ticker}' not found in STOCK_UNIVERSE.")

    data = STOCK_UNIVERSE[ticker]

    if mock_llm == 1:
        return _run_debate_mock(ticker, data)
    else:
        return _run_debate_llm(ticker, data)


def _run_debate_mock(ticker: str, data: dict) -> dict:
    """Mock mode implementation (graded baseline) using string templates."""
    r = data["analyst_expected_return"]
    b = data["beta"]
    s = data["std_dev"]

    # 1. Bull Agent
    bull_case = (
        f"With an expected return of {r:.1%} against a beta of {b:.2f}, "
        f"this offers attractive risk-adjusted upside."
    )

    # 2. Bear Agent
    bear_case = (
        f"However, a volatility (std_dev) of {s:.1%} presents significant risk "
        f"and potential downside exposure under volatile market conditions."
    )

    # 3. Synthesizer Agent (2-3 sentence balanced summary)
    synthesis = (
        f"While {ticker} demonstrates strong upside potential with an expected return of {r:.1%}, "
        f"its standard deviation of {s:.1%} highlights non-trivial volatility risk. "
        f"Investors should balance the {b:.2f} beta exposure against their overall portfolio risk tolerance."
    )

    return {
        "ticker": ticker,
        "bull_case": bull_case,
        "bear_case": bear_case,
        "synthesis": synthesis,
    }


def _run_debate_llm(ticker: str, data: dict) -> dict:
    """Optional MOCK_LLM=0 extension: calls LLMs for richer debate arguments."""
    # Placeholder for actual LLM calls using prompts tailored for each persona
    # e.g., prompt_bull(ticker, data), prompt_bear(ticker, data), prompt_synthesizer(bull, bear)
    return _run_debate_mock(ticker, data)


# -----------------------------------------------------------------------------
# Test runner for a single ticker debate
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    chosen_ticker = "PAYTECH"
    result = run_debate(chosen_ticker, mock_llm=1)

    print(f"=== Multi-Agent Debate for {result['ticker']} ===")
    print(f"🐂 Bull Agent:\n{result['bull_case']}\n")
    print(f"🐻 Bear Agent:\n{result['bear_case']}\n")
    print(f"⚖️ Synthesizer Agent:\n{result['synthesis']}\n")
