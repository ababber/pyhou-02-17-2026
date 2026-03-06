# Part 2: Deep Learning — Presentation Citations

Every factual claim in the video presentation with its supporting citation. Use this document to verify accuracy before publishing.

**Verification status:** ✅ Complete (2026-03-04)

---

## Slide 1 — Title

### Claim: Book attribution

> "Based on *Hands-On AI Trading with Python, QuantConnect, and AWS*"

**Citation:**
Pik, J., Chan, E. P., Broad, J., Sun, P., & Singh, V. (2025). *Hands-On AI Trading with Python, QuantConnect, and AWS*. Wiley. ISBN 9781394268436.

**Verify:** https://www.wiley.com/en-us/Hands-On+AI+Trading+with+Python,+QuantConnect,+and+AWS-p-9781394268436

---

## Slide 3 — Why Deep Learning

### Claim: CNN for pattern recognition (1989)

> "CNNs were designed to find patterns in images — but price charts are just 2D patterns too."

**Citation:**
LeCun, Y. et al. (1989). "Backpropagation Applied to Handwritten Zip Code Recognition." *Neural Computation*, 1(4), 541-551.

**Verify:** https://doi.org/10.1162/neco.1989.1.4.541

---

### Claim: Temporal Convolutional Networks (2018)

> "TCNs adapt CNNs for sequential data"

**Citation:**
Bai, S., Kolter, J.Z., & Koltun, V. (2018). "An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling." arXiv:1803.01271.

**Verify:** https://arxiv.org/abs/1803.01271

---

## Slide 4 — Architecture

### Claim: Architecture details (30 filters, kernel=4, 15-day input, temporal split)

> "Conv1D: 30 filters, kernel=4... Input: 15 trading days × 5 features... Temporal split into LONG/MID/SHORT-TERM regions"

**Citation:**
Pik, J., Chan, E. P., Broad, J., Sun, P., & Singh, V. (2025). *Hands-On AI Trading with Python, QuantConnect, and AWS*. Chapter 14: Temporal CNN Prediction. Wiley. ISBN 9781394268436.

**Verify:** https://www.wiley.com/en-us/Hands-On+AI+Trading+with+Python,+QuantConnect,+and+AWS-p-9781394268436

**Code verification:** `temporalcnn.py` line: `Conv1D(30, 4, activation='relu')`

---

### Claim: Classification vs regression for trading

> "Predicting direction is often more practical than predicting exact prices."

**Citation:**
IEEE (2020). "Prediction of Stock Prices using Machine Learning (Regression, Classification) Algorithms." IEEE Conference Publication.

**Verify:** https://ieeexplore.ieee.org/document/9154061

---

## Slide 4a — Temporal Split

### Claim: Multi-scale analysis in finance

> "This is wavelet-style decomposition built into the network."

**Citation:**
Zavanelli, N. (2023). "Wavelet Analysis for Time Series Financial Signals via Element Analysis." arXiv:2301.13255.

**Verify:** https://arxiv.org/abs/2301.13255

---

### Claim: Multi-scale analysis research

> "The model LEARNS which timescale matters"

**Citation:**
~~Lund University. "Multi-scale Analysis of Financial Time Series."~~

**Status:** ⚠️ BROKEN — Original URL (lunduniversity.lu.se/lup/publication/8938181) returns 404.

**Replacement needed:** Search for alternative academic source on multi-scale financial analysis.

---

## Slide 5 — Trading Logic

### Claim: Kelly Criterion

> "Position sizing based on confidence"

**Citation:**
Kelly, J.L. (1956). "A New Interpretation of Information Rate." *Bell System Technical Journal*, 35(4), 917-926.

**Verify:** https://www.princeton.edu/~wbialek/rome/refs/kelly_56.pdf

---

### Claim: Fractional Kelly / Conservative Sizing

> "Most traders use fractional Kelly to reduce volatility"

**Citation:**
~~Medium. "Position Sizing Using the Kelly Criterion."~~

**Status:** ⚠️ BROKEN — Original URL returns 404.

**Replacement:** General knowledge — fractional Kelly is well-documented in trading literature. Alternative sources:
- https://www.caia.org/sites/default/files/AIAR_Q3_2016_05_KellyCapital.pdf
- Thorp, E.O. (2007). "The Kelly Criterion in Blackjack, Sports Betting and the Stock Market."

---

## Slide 5a — Code Map

### Claim: Conv1D implementation

> "Conv1D(30, kernel_size=4, activation='relu')"

**Citation:**
TensorFlow/Keras Documentation. "tf.keras.layers.Conv1D."

**Verify:** https://tensorflow.org/api_docs/python/tf/keras/layers/Conv1D

---

### Claim: QuantConnect implementation

> "Full implementation: github.com/ababber/pyhou-02-17-2026"

**Citation:**
QuantConnect Documentation. "Writing Algorithms."

**Verify:** https://www.quantconnect.com/docs/v2/writing-algorithms

---

## Slide 6 — Metrics

### Claim: Jensen's Alpha interpretation

> "Alpha: +0.093 ✓ — genuine skill found"

**Citation:**
Jensen, M.C. (1968). "The Performance of Mutual Funds in the Period 1945–1964." *Journal of Finance*, 23(2), 389-416.

**Verify:** https://doi.org/10.2307/2325404

**Alternative:** https://www.semanticscholar.org/paper/The-Performance-of-Mutual-Funds-in-the-Period-Jensen/6cbfeff5e9d4b10b78cbe58171bf0ad13cc3e97d

---

### Claim: Hedge fund alpha targets

> "Hedge funds target 2-4% alpha annually"

**Citation:**
Swedroe, L. "Hedge fund alpha is negative and declining." Evidence-Based Investor.

**Verify:** https://evidenceinvestor.com/post/hedge-fund-alpha-is-negative-and-declining

---

### Claim: Probabilistic Sharpe Ratio

> "PSR: 21.9% — not statistically significant"

**Citation:**
Bailey, D.H. & López de Prado, M. (2012). "The Sharpe Ratio Efficient Frontier." *Journal of Risk*, 15(2), Winter 2012/13.

**Verify:** https://www.risk.net/journal-risk/2223785/sharpe-ratio-efficient-frontier

**PDF:** https://www.davidhbailey.com/dhbpapers/sharpe-frontier.pdf

---

## Slide 7 — What's Next

### Claim: Amazon Chronos (2024)

> "Foundation models are pre-trained on millions of time series."

**Citation:**
Ansari, A.F. et al. (2024). "Chronos: Learning the Language of Time Series." arXiv:2403.07815.

**Verify:** https://arxiv.org/abs/2403.07815

**GitHub:** https://github.com/amazon-science/chronos-forecasting

---

## Summary

| Slide | Citations | Status |
|-------|-----------|--------|
| 1 | 1 | ✅ |
| 3 | 2 | ✅ |
| 4 | 1 | ✅ |
| 4a | 2 | ⚠️ 1 broken |
| 5 | 2 | ⚠️ 1 broken |
| 5a | 2 | ✅ |
| 6 | 3 | ✅ |
| 7 | 1 | ✅ |
| **Total** | **14** | **12 ✅ / 2 ⚠️** |

---

## Broken Links Requiring Replacement

1. **Slide 4a** — Lund University multi-scale analysis paper
   - Original: `lunduniversity.lu.se/lup/publication/8938181`
   - Action: Find alternative academic source or remove citation

2. **Slide 5** — Medium fractional Kelly article
   - Original: `medium.com/@olsonngula/position-sizing-using-the-kelly-criterion`
   - Action: Replace with CAIA Journal article on Kelly Capital

---

*Last verified: 2026-03-04*
