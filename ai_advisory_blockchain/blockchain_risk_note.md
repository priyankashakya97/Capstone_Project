# Blockchain / Crypto Risk-Analysis Appendix

## 1. What "Paytm Crypto Insights" would need to get right

The biggest risk is treating all stablecoins as the same. Fiat-collateralized stablecoins (like USDC or USDT) are backed by real cash reserves — the risk there is whether the issuer is solvent and the reserves are real. Algorithmic stablecoins hold their peg through code and market confidence, not a hard reserve. TerraUSD showed how fast that can fail: it lost its peg in days and wiped out tens of billions of dollars. If Paytm shows both types the same way, users can't tell a safe stablecoin from a fragile one. The feature needs to clearly label reserve type (fiat-backed vs. algorithmic), show audit/attestation status, and flag any history of depegging.

The same logic applies to DeFi and DAO tokens. Many DAOs are governed by token voting, so whoever holds the most tokens can control decisions — sometimes even through a short-term flash loan. A DAO vote can drain a treasury or change the rules overnight, and there's no prospectus or legal recourse like a regular company. Before showing DeFi tokens, Paytm needs audit status, how recent that audit is, and a flag when a small number of wallets control governance.

## 2. Crypto allocation recommendation for Paytm Money

CAPM and standard portfolio theory are built around assets that generate cash flow — dividends, interest, earnings. Crypto has none of that; its price is just what the next buyer will pay. Crypto's low correlation with stocks and bonds looks like a diversification benefit, but three things undercut that: returns are heavy-tailed and skewed, not normal, so the usual risk math understates the downside; the historical return numbers suffer from survivorship bias, since the coins and platforms that collapsed (Terra, FTX, Celsius) drop out of the data; and trading, custody, and spread costs eat into returns.

Given this, the recommendation is a zero allocation to crypto in any default or advised Paytm Money portfolio. This isn't saying crypto has no place in anyone's life — it's saying an advisory product serving retail investors shouldn't be the one recommending it, especially without a track record long enough to properly measure the risk. If Paytm wants a crypto product at all, it should be a separate, clearly opt-in section, capped at 1–2% of net worth, with an explicit risk warning, and kept fully outside the "optimized portfolio" recommendation shown to advised clients.

## 3. T.A.N.G. fraud framework for a UPI + lending + wealth platform

The two biggest risks here are Authority and Greed.

**Authority:** Scammers pose as Paytm, bank, or RBI support, telling users their KYC or loan will fail unless they share an OTP or install a screen-sharing app. This works because Paytm really does send KYC and loan alerts, so the fake ones blend in easily. Defense: detect and block OTP entry or UPI approval when a screen-mirroring app (AnyDesk, TeamViewer) is running, or when a call is live during authentication — genuine support never needs either.

**Greed:** Fake investment tips and crypto trading groups promise guaranteed returns and ask users to send money to a "trading account" via UPI, often through a referral chain that makes the scheme feel more credible. Defense: real-time risk scoring on the receiving UPI ID — flag accounts suddenly getting many small transfers from unrelated senders (a classic mule-account pattern) — and add a cooling-off delay plus a clear warning for a user's first large transfer to a new, unverified beneficiary.
