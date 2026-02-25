# Quantitative Trading: A First Look

**Three Generations of Machine Learning Applied to Quantitative Trading**

Can machine learning predict financial markets? This repo accompanies a video series where I test three generations of ML — from a 1970 linear model to a 2024 foundation model — on the same backtesting platform.

<!-- TODO: Add video embed when published -->
<!-- [![Watch on YouTube](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtu.be/VIDEO_ID) -->

---

## Quick Navigation

| What you want | Where to go |
|---------------|-------------|
| Watch the video explanation | [YouTube](#) *(coming soon)* |
| Part 1 research notebook | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ababber/pyhou-02-17-2026/blob/main/part-1-classical-ml/research-notebook.ipynb) or [GitHub](part-1-classical-ml/research-notebook.ipynb) |
| Part 2 research notebook | *Planned* |
| Part 3 research notebook | *Planned* |
| Run notebooks locally | [Local Setup](#local-setup) |
| Run the strategies on QuantConnect | [QuantConnect Setup](#quantconnect-setup) |
| Original live presentation | [pyhou-live-presentation-material/](pyhou-live-presentation-material/) |

---

## Part 1: Classical ML (Ridge Regression)

The first video covers ridge regression — a classical linear model from 1970 — applied to inverse volatility weighting on 12 futures contracts.

**The strategy:**
- Trade 12 futures (indices, energy, grains)
- Predict next-week volatility using ridge regression
- Allocate inversely: less volatile contracts get more capital
- Rebalance weekly

**The result:** Sharpe 0.212, Alpha -0.062. The model tracks the market with extra drawdown. It doesn't generate alpha.

**Why it matters:** Understanding *why* a simple model fails sets up everything that follows. Linear models can't capture the nonlinear patterns in financial data.

---

## Local Setup

The notebooks use `plotly` for interactive charts. Everything else is narrative + embedded QuantConnect code.

```bash
# Clone the repo
git clone https://github.com/ababber/pyhou-02-17-2026.git
cd pyhou-02-17-2026

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install numpy scikit-learn plotly jupyter

# Launch Jupyter and open any notebook
jupyter notebook
```

**Requirements:**
- Python 3.9+
- numpy
- scikit-learn
- plotly
- jupyter

**Note:** Google Colab has all dependencies pre-installed. For local setup, you need the packages above.

---

## QuantConnect Setup

The actual trading strategies run on [QuantConnect](https://www.quantconnect.com/), a cloud-based algorithmic trading platform.

**To run the strategies yourself:**

1. Create a free QuantConnect account at [quantconnect.com](https://www.quantconnect.com/)
2. Navigate to Algorithm Lab → Create New Algorithm
3. Copy the algorithm code from the notebook (each technique has its full source)
4. Run a backtest

**Note:** QuantConnect provides free backtesting with delayed data. The strategies in this series use futures contracts, which require a QuantConnect subscription for live trading but are free for backtesting.

For detailed QuantConnect setup, see [pyhou-live-presentation-material/QC.md](pyhou-live-presentation-material/QC.md).

---

## Video Series

| Part | Topic | Model | Research Notebook | QC Tier | Status |
|------|-------|-------|-------------------|---------|--------|
| 1 | Classical ML | Ridge Regression (1970) | [part-1-classical-ml/](part-1-classical-ml/) | **Free** | Ready |
| 2 | Deep Learning | Temporal CNN (1989) | `part-2-deep-learning/` | **Free** | *Planned* |
| 3 | Foundation Model | Amazon Chronos (2024) | `part-3-foundation-model/` | **Research**¹ | *Planned* |

¹ Part 3 requires a [QuantConnect Research subscription](https://www.quantconnect.com/pricing) (~$8/mo) for fine-tuning exercises. Backtesting the pre-trained model works on free tier.

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

## Origin

This material is based on a live presentation I gave at [PyHou (Houston Python Meetup)](https://www.meetup.com/python-14/) on February 17, 2026.

- [Original Meetup Event](https://www.meetup.com/python-14/events/312872749/)
- [PyHou Meetup Page](https://www.meetup.com/python-14/)

---

## Disclaimer

**This content is for educational purposes only.** Nothing here is financial advice. Quantitative trading involves substantial risk of loss. Past performance does not guarantee future results. The strategies shown here lost money relative to a simple buy-and-hold benchmark.

---

## License

MIT — see [LICENSE](LICENSE) for details.
