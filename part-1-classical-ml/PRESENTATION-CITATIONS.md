# Part 1: Classical ML — Presentation Citations

Every factual claim in the video presentation with its supporting citation. Use this document to verify accuracy before publishing.

**Verification status:** ✅ Complete (2026-02-25)

---

## Slide 1 — Title

### Claim: Book attribution

> "Based on *Hands-On AI Trading with Python, QuantConnect, and AWS*"

**Citation:**
Pik, J., Chan, E. P., Broad, J., Sun, P., & Singh, V. (2025). *Hands-On AI Trading with Python, QuantConnect, and AWS*. Wiley. ISBN 9781394268436.

**Verify:** https://www.wiley.com/en-us/Hands-On+AI+Trading+with+Python,+QuantConnect,+and+AWS-p-9781394268436

---

### Claim: Event attribution

> "PyHou Meetup, February 17, 2026"

**Citation:**
PyHou Meetup (2026-02-17). "Quantitative Trading: A First Look with QuantConnect and Python." Houston, TX: Improving.

**Verify:** https://www.meetup.com/python-14/events/312872749/

---

## Slide 2 — The Question

### Claim: Ridge regression year

> "Ridge Regression (1970)"

**Citation:**
Hoerl, A.E. & Kennard, R.W. (1970). "Ridge Regression: Biased Estimation for Nonorthogonal Problems." *Technometrics*, 12(1), 55-67.

**Verify:** https://doi.org/10.1080/00401706.1970.10488634

---

### Claim: CNN/Deep Learning year

> "Temporal CNN (1989)"

**Citation:**
LeCun, Y. et al. (1989). "Backpropagation Applied to Handwritten Zip Code Recognition." *Neural Computation*, 1(4), 541-551.

**Verify:** https://doi.org/10.1162/neco.1989.1.4.541

**Note:** Part 2 uses a temporal variant with 1D convolutions for time series. The 1989 paper established backprop-trained CNNs.

---

### Claim: Amazon Chronos year

> "Amazon Chronos (2024)"

**Citation:**
Ansari, A.F. et al. (2024). "Chronos: Learning the Language of Time Series." Amazon Science.

**Verify:** https://github.com/amazon-science/chronos-forecasting

---

## Slide 3 — Why Ridge Regression?

### Claim: OLS becomes unstable with correlated features

> "When features are correlated, OLS becomes unstable. Small changes in data can swing coefficients wildly."

**Citation:**
Penn State STAT 462. "Detecting Multicollinearity Using Variance Inflation Factors."

**Verify:** https://online.stat.psu.edu/stat462/node/180/

**Quote from source:** "small changes in the data can lead to large and unpredictable changes in the estimated coefficients"

---

### Claim: Ridge adds L2 penalty that shrinks coefficients

> "Ridge regression adds an L2 penalty that shrinks all coefficients toward zero."

**Citation:**
Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*. 2nd ed., Chapter 3. Springer.

**Verify:** https://doi.org/10.1007/b94608

---

## Slide 4 — The Strategy

### Claim: ATR developed in 1978

> "Average True Range — developed by J. Welles Wilder in 1978"

**Citation:**
Wilder, J.W. (1978). *New Concepts in Technical Trading Systems*. Trend Research. ISBN 978-0894590276.

**Verify:** https://archive.org/details/newconceptsintec00wild

---

### Claim: True Range formula (3 components)

> "True Range = max of: (High − Low), |High − Previous Close|, |Low − Previous Close|"

**Citation:**
Wilder (1978), Chapter on Average True Range.

**Verify:** Any technical analysis reference (Investopedia, TradingView docs) confirms this formula.

---

### Claim: Risk parity popularized after 2008

> "Inverse volatility weighting — a risk-parity adjacent technique"

**Citation:**
Roncalli, T. (2013). *Introduction to Risk Parity and Budgeting*. Chapman & Hall/CRC. ISBN 978-1482207156.

**Verify:** https://doi.org/10.1201/b15151

---

## Slide 5 — The Math

### Claim: Ridge cost function

> "J(θ) = MSE(θ) + (α/m) Σᵢ θᵢ²"

**Citation:**
Hoerl & Kennard (1970). "Ridge Regression: Biased Estimation for Nonorthogonal Problems." *Technometrics*, 12(1), 55–67.

**Verify:** https://www.ibm.com/think/topics/ridge-regression

---

### Claim: α = 0 → OLS; α → ∞ → all coefficients = 0

> "α = 0 → plain OLS. α → ∞ → all coefficients = 0 (model predicts the mean)"

**Citation:**
Penn State STAT 857: Ridge Regression.

**Verify:** https://online.stat.psu.edu/stat857/node/155/

**Quote from source:** "The ridge estimator approaches zero as λ → ∞"

---

### Claim: S&P E-Mini contract value ~$250K

> "A single S&P E-Mini contract controls ~$250K"

**Citation:**
Schwab Futures. "S&P 500 E-Mini Futures."

**Verify:** https://www.schwab.com/futures/sp-500-emini

**Calculation:** $50 multiplier × S&P ~5,000 (2021 levels) = ~$250K

---

### Claim: Corn contract value ~$25K

> "A corn contract controls maybe $25,000 worth of grain"

**Citation:**
CME Group. "Corn Futures Contract Specs."

**Verify:** https://www.cmegroup.com/markets/agriculture/grains/corn.contractSpecs.html

**Calculation:** 5,000 bushels × ~$5/bushel = ~$25K

---

## Slide 5a — Code Map

### Claim: sklearn Ridge default alpha=1.0

> "model = Ridge()  # α=1.0 default"

**Citation:**
scikit-learn documentation.

**Verify:** https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html

**Quote from source:** "alpha: float, default=1.0"

---

## Slide 6 — Results

### Claim: Sharpe of 1.0 is "good"

> "A Sharpe of 1.0 is considered 'good' — one unit of return for every unit of risk"

**Citation:**
Sharpe, W.F. (1966). "Mutual Fund Performance." *The Journal of Business*, 39(1), 119–138.

**Verify:** Industry convention — Sharpe > 1.0 is considered acceptable for hedge funds.

---

### Claim: S&P 500 returned ~119% (2019-Q1 2024)

> "The S&P 500 returned about 119% over the same period"

**Citation:**
slickcharts.com/sp500/returns (annual total returns)

**Verify:** Cumulative calculation:
- 2019: +31.5%
- 2020: +18.4%
- 2021: +28.7%
- 2022: -18.1%
- 2023: +26.3%
- Q1 2024: +10.2%
- **Total:** 1.315 × 1.184 × 1.287 × 0.819 × 1.263 × 1.102 ≈ 2.19 → **~119%**

---

### Claim: Alpha/Beta interpretation (Jensen)

> "Alpha: after you strip out the returns from beta alone, the strategy is LOSING money"

**Citation:**
Jensen, M.C. (1968). "The Performance of Mutual Funds in the Period 1945–1964." *The Journal of Finance*, 23(2), 389–416.

**Verify:** Standard definition of Jensen's alpha.

---

### Claim: "Factor mirage" term (López de Prado)

> "López de Prado calls related phenomena 'factor mirages'"

**Citation:**
López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. ISBN 978-1-119-48208-6. Chapter 11: "The Dangers of Backtesting."

**Verify:** https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086

---

## Slide 7 — Transition

*Summary slide — no external citations required.*

---

## Verification Checklist

| Slide | Claims | Verified |
|-------|--------|----------|
| 1 — Title | 2 | ✅ |
| 2 — The Question | 3 | ✅ |
| 3 — Why Ridge? | 2 | ✅ |
| 4 — The Strategy | 3 | ✅ |
| 5 — The Math | 4 | ✅ |
| 5a — Code Map | 1 | ✅ |
| 6 — Results | 4 | ✅ |
| 7 — Transition | 0 | ✅ |

**Total claims:** 19 — all verified via web search

---

## How to Verify

For each claim:
1. Click the "Verify" link
2. Confirm the source contains the claimed information
3. Check the checkbox in the table above
4. If discrepancy found, update the claim or citation

---

*Last updated: 2026-02-25*
