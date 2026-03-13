# Part 3: Foundation Models — Citations

## Primary Sources

### Chronos Paper
- Ansari, A. F. et al. (2024). "Chronos: Learning the Language of Time Series." arXiv:2403.07815.
- https://arxiv.org/abs/2403.07815

### HOAIT Book
- Pik, J., Chan, E. P., Broad, J., Sun, P., & Singh, V. (2025). *Hands-On AI Trading with Python, QuantConnect, and AWS.* Wiley. ISBN 9781394268436.
- Exercise 18: Amazon Chronos Model (pp. 422–432)

### T5 Architecture
- Raffel, C. et al. (2020). "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer." JMLR 21(140).
- https://arxiv.org/abs/1910.10683

## Statistical Foundations

### Sharpe Ratio
- Sharpe, W. F. (1994). "The Sharpe Ratio." The Journal of Portfolio Management, 21(1), 49-58.

### Probabilistic Sharpe Ratio
- Bailey, D. H., & López de Prado, M. (2012). "The Sharpe Ratio Efficient Frontier." Journal of Risk, 15(2).

### Portfolio Theory
- Markowitz, H. (1952). "Portfolio Selection." The Journal of Finance, 7(1), 77-91.

## Backtest Verification

### QuantConnect Project IDs
- Base Model: Project 28164872, Backtest 47b676375c05c6b3d71798dc775f7753
- Fine-Tuned: Project 28164873, Backtest f23c48d8f90bd2e5d39706e0b447fee8

### Metrics (from QC API)

| Metric | Base | Fine-Tuned |
|--------|------|------------|
| Sharpe | 0.727 | 0.846 |
| Alpha | 0.040 | 0.076 |
| Beta | 1.125 | 1.110 |
| PSR | 25.738% | 34.641% |
| Net Profit | +199.9% | +266.4% |
| Max Drawdown | 41.2% | 49.5% |

## Tools & Resources

- QuantConnect: https://www.quantconnect.com/
- Chronos on HuggingFace: https://huggingface.co/amazon/chronos-t5-tiny
- GitHub Repo: https://github.com/ababber/pyhou-02-17-2026
