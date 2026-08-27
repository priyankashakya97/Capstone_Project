import math
from stock_universe import STOCK_UNIVERSE


class AdvisoryAgent:
    """A portfolio advisory agent that recommends allocations based on risk tolerance.

    The agent calculates CAPM-expected return and portfolio variance, escalating
    to a human advisor if volatility exceeds a predefined threshold.
    """

    # Class-level data and assumptions
    STOCK_UNIVERSE = STOCK_UNIVERSE

    ALLOCATION_LOOKUP = {
        "Conservative": ["PAYBOND", "PAYGOLD", "PAYRETAIL"],
        "Moderate": ["PAYRETAIL", "PAYINFRA", "PAYGOLD"],
        "Aggressive": ["PAYTECH", "PAYFIN", "PAYINFRA"],
    }

    R_F = 0.03  # Risk-free rate (3%)
    E_R_M = 0.08  # Expected market return (8%)
    PAIRWISE_RHO = 0.3  # Pairwise correlation constant
    ESCALATION_THRESHOLD = 0.20  # 20% standard deviation

    def __init__(self, mock_llm: int = 1):
        self.mock_llm = mock_llm

    def _get_stock_data(self, ticker: str) -> dict:
        """Helper to simulate fetching data from STOCK_UNIVERSE."""
        return self.STOCK_UNIVERSE.get(ticker, {})

    def run_advisory(self, investor_profile: dict) -> dict:
        """Executes the agent loop to provide a portfolio recommendation."""
        investor_id = investor_profile.get("investor_id")
        risk_tolerance = investor_profile.get("risk_tolerance")

        # STAGE 1: THINK (Determine allocation)
        if risk_tolerance not in self.ALLOCATION_LOOKUP:
            raise ValueError(f"Unknown risk tolerance: {risk_tolerance}")

        tickers = self.ALLOCATION_LOOKUP[risk_tolerance]
        weight = 1.0 / len(tickers)  # Equal weighting

        # STAGE 2: ACT (Tool Calls)
        stock_data = {ticker: self._get_stock_data(ticker) for ticker in tickers}

        # STAGE 3: OBSERVE -> DECIDE (Compute CAPM return and portfolio variance)
        capm_returns = []
        std_devs = []

        for ticker in tickers:
            beta = stock_data[ticker]["beta"]
            sigma = stock_data[ticker]["std_dev"]

            capm_r = self.R_F + beta * (self.E_R_M - self.R_F)
            capm_returns.append(capm_r)
            std_devs.append(sigma)

        portfolio_return = sum(weight * r for r in capm_returns)

        var_sum = sum((weight**2) * (s**2) for s in std_devs)

        covariance_sum = 0.0
        n = len(tickers)
        for i in range(n):
            for j in range(i + 1, n):
                cov_ij = self.PAIRWISE_RHO * std_devs[i] * std_devs[j]
                covariance_sum += 2 * (weight * weight * cov_ij)

        portfolio_variance = var_sum + covariance_sum
        portfolio_std_dev = math.sqrt(portfolio_variance)

        # HUMAN-IN-THE-LOOP ESCALATION
        if portfolio_std_dev > self.ESCALATION_THRESHOLD:
            return {
                "status": "ESCALATED_TO_HUMAN_ADVISOR",
                "investor_id": investor_id,
                "risk_tolerance": risk_tolerance,
                "expected_return": portfolio_return,
                "volatility": portfolio_std_dev,
            }

        # FINAL NARRATIVE GENERATION
        tickers_str = ", ".join(tickers)

        if self.mock_llm == 1:
            narrative = (
                f"For {risk_tolerance} investor {investor_id}, we recommend an allocation "
                f"across {tickers_str} with an expected portfolio return of {portfolio_return:.1%} "
                f"and volatility of {portfolio_std_dev:.1%}."
            )
        else:
            narrative = (
                f"Based on your {risk_tolerance.lower()} risk profile, investor {investor_id}, "
                f"we advise a balanced split across {tickers_str}. This portfolio yields an anticipated "
                f"return of {portfolio_return:.1%} with an annualized volatility of {portfolio_std_dev:.1%}."
            )

        return {
            "status": "FINALIZED",
            "investor_id": investor_id,
            "recommendation": narrative,
            "expected_return": portfolio_return,
            "volatility": portfolio_std_dev,
        }


# Test runner using the refactored AdvisoryAgent class
if __name__ == "__main__":
    profiles = [
        {"investor_id": "INV01", "risk_tolerance": "Conservative"},
        {"investor_id": "INV02", "risk_tolerance": "Moderate"},
        {"investor_id": "INV03", "risk_tolerance": "Aggressive"},
        {"investor_id": "INV04", "risk_tolerance": "Moderate"},
        {"investor_id": "INV05", "risk_tolerance": "Aggressive"},
    ]

    # Instantiate the agent
    agent = AdvisoryAgent(mock_llm=1)

    for profile in profiles:
        result = agent.run_advisory(profile)
        print(f"[{profile['investor_id']}] Output:", result)
