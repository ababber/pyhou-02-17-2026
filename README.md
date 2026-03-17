# Quantitative Trading: A First Look With QuantConnect

*Can machine learning predict financial markets? This repo accompanies a 3-part video series where I test three generations of ML — from a 1970 linear model to a 2024 foundation model — on the same backtesting platform.*

📺 **[Click here to watch the full playlist on YouTube!](https://www.youtube.com/playlist?list=PLBfBLYe88LVVhpUMeBLzqXWWw90vT6_A6)**

---

## Quick Navigation

**Part 1: Classical ML (Ridge Regression)**

[![YouTube](https://img.shields.io/badge/YouTube-Watch_Video-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=jnleuAGZTsY&list=PLBfBLYe88LVVhpUMeBLzqXWWw90vT6_A6)
[![GitHub](https://img.shields.io/badge/GitHub-View_Notebook-181717?style=for-the-badge&logo=github)](part-1-classical-ml/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ababber/pyhou-02-17-2026/blob/main/part-1-classical-ml/research-notebook.ipynb)

**Part 2: Deep Learning (Temporal CNN)**

[![YouTube](https://img.shields.io/badge/YouTube-Watch_Video-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=CwGqyTc-PgA&list=PLBfBLYe88LVVhpUMeBLzqXWWw90vT6_A6)
[![GitHub](https://img.shields.io/badge/GitHub-View_Notebook-181717?style=for-the-badge&logo=github)](part-2-deep-learning/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ababber/pyhou-02-17-2026/blob/main/part-2-deep-learning/research-notebook.ipynb)

**Part 3: Foundation Models (Amazon Chronos)**

[![YouTube](https://img.shields.io/badge/YouTube-Watch_Video-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=paaaUnfbp5g&list=PLBfBLYe88LVVhpUMeBLzqXWWw90vT6_A6)
[![GitHub](https://img.shields.io/badge/GitHub-View_Notebook-181717?style=for-the-badge&logo=github)](part-3-foundation-models/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ababber/pyhou-02-17-2026/blob/main/part-3-foundation-models/research-notebook.ipynb)

> **Note:** When opening in Colab, you'll see a "This notebook was not authored by Google" warning — click **Run anyway** to proceed.

---

## Part 1: Classical ML (Ridge Regression)

▶️ **[Watch the Part 1 Video](https://www.youtube.com/watch?v=jnleuAGZTsY&list=PLBfBLYe88LVVhpUMeBLzqXWWw90vT6_A6)**

The first video covers ridge regression — a classical linear model from 1970 — applied to inverse volatility weighting on 12 futures contracts.

**The strategy:**
- Trade 12 futures (indices, energy, grains)
- Predict next-week volatility using ridge regression
- Allocate inversely: less volatile contracts get more capital
- Rebalance weekly

**The result:** Sharpe 0.212, Alpha -0.062. The model tracks the market with extra drawdown. It doesn't generate alpha.

**Why it matters:** Understanding *why* a simple model fails sets up everything that follows. Linear models can't capture the nonlinear patterns in financial data.

---

## Part 2: Deep Learning (Temporal CNN)

▶️ **[Watch the Part 2 Video](https://www.youtube.com/watch?v=CwGqyTc-PgA&list=PLBfBLYe88LVVhpUMeBLzqXWWw90vT6_A6)**

The second video covers temporal convolutional networks — detecting patterns across multiple timescales in price data.

**The strategy:**
- Trade top 3 QQQ holdings (AAPL, MSFT, NVDA)
- 15-day OHLCV features → 3-class prediction (up/down/stationary)
- Temporal split: long/mid/short-term signals with separate learned weights
- Weekly retraining, confidence-weighted position sizing

**The result:** Sharpe 0.649, Alpha +0.093. The CNN found genuine signal with lower drawdown (26% vs 55%) and positive alpha — beating the market with less risk.

**Why it matters:** Nonlinear pattern detection works — but PSR 21.9% means we'd need a longer backtest to confirm it isn't noise. The forensic analysis in the notebook explores this limitation.

---

## Part 3: Foundation Models (Amazon Chronos)

▶️ **[Watch the Part 3 Video](https://www.youtube.com/watch?v=paaaUnfbp5g&list=PLBfBLYe88LVVhpUMeBLzqXWWw90vT6_A6)**

The third video covers zero-shot time series forecasting — using a pre-trained transformer that has never seen financial data.

**The strategy:**
- Trade top 5 stocks by dollar volume (AAPL, MSFT, NVDA, GOOGL, AMZN)
- Use Amazon Chronos to forecast 63-day price trajectories
- Sharpe-optimal portfolio weights via SciPy SLSQP
- Quarterly rebalancing

**The result:** Base model: Sharpe 0.727, Alpha +0.040. Fine-tuned (3 gradient steps): Sharpe 0.846, Alpha +0.076. Both beat ridge regression with zero training effort.

**Why it matters:** Foundation models transfer temporal patterns learned from weather, retail, and energy data to finance. But high beta (1.1) means most returns come from market exposure, and PSR 34.6% still isn't statistically significant. The notebook includes caveats on tokenization lookahead bias and trading frictions.

> **Note:** The end-to-end pipeline cell requires a T4 GPU in Colab. Go to Runtime → Change runtime type → T4 GPU.

---

## Local Setup

The notebooks use `plotly` for interactive charts. Everything else is narrative + embedded QuantConnect code.

```bash
git clone https://github.com/ababber/pyhou-02-17-2026.git
cd pyhou-02-17-2026

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install numpy scikit-learn plotly jupyter tensorflow pandas matplotlib

jupyter notebook
```

**Requirements:**
- Python 3.9+
- numpy, scikit-learn, plotly, jupyter
- tensorflow, pandas, matplotlib (Part 2)
- torch, chronos-forecasting (Part 3)

**Note:** Google Colab has most dependencies pre-installed. For Part 3, run `!pip install chronos-forecasting` in Colab. The end-to-end pipeline requires a T4 GPU runtime.

---

## QuantConnect Setup

The actual trading strategies run on [QuantConnect](https://www.quantconnect.com/), a cloud-based algorithmic trading platform.

**To run the strategies yourself:**

1. Create a free QuantConnect account at [quantconnect.com](https://www.quantconnect.com/)
2. Navigate to Algorithm Lab → Create New Algorithm
3. Copy the algorithm code from the notebook (each technique has its full source)
4. Run a backtest

**Note:** QuantConnect provides free backtesting with delayed data. The strategies in this series use futures contracts, which require a QuantConnect subscription for live trading but are free for backtesting.

| Part | QC Tier Required |
|------|------------------|
| 1 | **Free** |
| 2 | **Free** |
| 3 | **Research**¹ (fine-tuning only) |

¹ Part 3 requires a [QuantConnect Researcher plan](https://www.quantconnect.com/pricing) ($60/mo or $600/yr) for fine-tuning exercises. Backtesting the pre-trained model works on free tier.

For detailed QuantConnect setup, see [pyhou-live-presentation-material/QC.md](pyhou-live-presentation-material/QC.md).

---

## Origin

This material is based on a live presentation I gave at [PyHou (Houston Python Meetup)](https://www.meetup.com/python-14/) on February 17, 2026.

- [Original Meetup Event](https://www.meetup.com/python-14/events/312872749/)
- [PyHou Meetup Page](https://www.meetup.com/python-14/)

---

## References

**Primary source:**
- Pik, J., Chan, E. P., Broad, J., Sun, P., & Singh, V. (2025). *Hands-On AI Trading with Python, QuantConnect, and AWS*. Wiley. ISBN 978-1394268436.

**Model origins:**
- Hoerl, A. E. & Kennard, R. W. (1970). "Ridge Regression: Biased Estimation for Nonorthogonal Problems." *Technometrics*, 12(1), 55–67.
- LeCun, Y. et al. (1989). "Backpropagation Applied to Handwritten Zip Code Recognition." *Neural Computation*, 1(4), 541–551.
- Ansari, A. F. et al. (2024). "Chronos: Learning the Language of Time Series." [arXiv:2403.07815](https://arxiv.org/abs/2403.07815).

**Further reading:**
- López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley.
- Jansen, S. (2020). *Machine Learning for Algorithmic Trading*. Packt.

---

## Disclaimer

**This content is for educational purposes only.** Nothing here is financial advice. Quantitative trading involves substantial risk of loss. Past performance does not guarantee future results. The strategies shown here lost money relative to a simple buy-and-hold benchmark.

---

## License

MIT — see [LICENSE](LICENSE) for details.
