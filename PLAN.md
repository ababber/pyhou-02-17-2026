# Presentation Plan — Predicting the Future: Classical → Deep → Foundation

_PyHou Feb 17, 2026. 40-minute talk. Jupyter notebook walkthroughs._

## Talk Overview

**Title:** Predicting the Future: Classical → Deep → Foundation

**Punchline:** Each ML generation improves — ridge regression fails → CNN generates genuine alpha → foundation model delivers with zero training.

**Audience:** Mixed (quant + general). Includes people who have never used QuantConnect.

**Format:** Two layers of Jupyter notebooks — a main walkthrough (the talk itself) and background scaffolding (QC onboarding for newcomers).

---

## Repo Structure

```
pyhou-02-17-2026/
├── README.md                         # Navigation guide + 3 reading paths
├── requirements.txt                  # Python deps for notebooks
├── lean.json                         # LEAN CLI config (optional: run backtests locally)
├── .gitignore                        # QC-specific ignores
│
├── walkthrough.ipynb                 # Main presentation notebook (3-act structure)
│
├── background/                       # QC scaffolding for newcomers
│   ├── 01-qc-platform.ipynb          # What is QC? Cloud IDE, algo lifecycle, QuantBook
│   ├── 02-data-and-universes.ipynb   # Market data, universe selection, history API
│   └── 03-ml-on-qc.ipynb            # ML integration: train, persist, load, optimize
│
├── exercises/                        # Actual QC algorithm source (runnable via LEAN CLI)
│   ├── ex11-ridge/
│   │   ├── main.py
│   │   ├── config.json
│   │   └── research.ipynb
│   ├── ex14-cnn/
│   │   ├── main.py
│   │   ├── temporalcnn.py
│   │   ├── config.json
│   │   └── research.ipynb
│   ├── ex18-chronos-base/
│   │   ├── main.py
│   │   ├── config.json
│   │   └── research.ipynb
│   └── ex18-chronos-finetuned/
│       ├── main.py
│       ├── config.json
│       └── research.ipynb
│
└── results/                          # Pre-computed backtest outputs + equity curves
    ├── ex11/
    ├── ex14/
    ├── ex18-base/
    └── ex18-finetuned/
```

---

## Reading Paths

Three ways into the material, depending on audience background:

- **"I'm here for the talk"** → `walkthrough.ipynb` — self-contained, runs top-to-bottom without QC installed
- **"I've never used QuantConnect"** → `background/01` → `02` → `03` → then `walkthrough.ipynb`
- **"I want to run the code myself"** → Setup section in README (LEAN CLI + Docker) → `exercises/`

---

## Main Walkthrough (`walkthrough.ipynb`)

Self-contained notebook that follows the 3-act presentation structure. Shows code inline with pre-computed results. Does not import from `exercises/` — someone can read the entire presentation without installing anything.

### Opening (2 min)

"Can machine learning predict financial markets? We're going to try three generations of ML — linear models, deep learning, and pre-trained foundation models — and see if the results actually improve."

### Act 1 — Classical ML: Ridge Regression (Ex11, 10 min)

- **What:** Ridge regression predicts next-week volatility for 12 futures contracts
- **Strategy:** Inverse volatility weighting — allocate more to less volatile contracts
- **Show:** Ridge cost function `J(θ) = MSE(θ) + (α/m) Σᵢ θᵢ²`, the 12-contract universe (indices, energy, grains)
- **Result:** Sharpe 0.212, alpha -0.062 — strategy fails to add value
- **Takeaway:** "A linear model on a simple signal doesn't generate alpha. It just tracks the market with extra drawdown."

### Act 2 — Deep Learning: Temporal CNN (Ex14, 10 min)

- **What:** 1D CNN predicts price direction (up/down/stationary) for top QQQ stocks
- **Architecture:** Conv1D → 3-way temporal split (long/mid/short) → separate 1×1 convolutions → concatenate → Dense(3)
- **Show:** Architecture diagram (Figure 6.45), confidence threshold (55%), temporal split concept
- **Result:** Sharpe 0.649, alpha 0.093, beta 0.278 — genuine alpha with low market exposure
- **Takeaway:** "The temporal split lets the model weight recent vs historical patterns differently — this is why it generates real alpha."

### Act 3 — Foundation Model: Amazon Chronos (Ex18, 20 min)

- **What:** Pre-trained transformer for time series. Zero training on financial data.
- **Hook:** "What if you could skip the training entirely?"
- **Show:** Chronos tokenization (continuous → discrete → T5), SciPy portfolio optimization, base vs fine-tuned side by side, the 3-step fine-tuning pipeline
- **Results:**
  - Base (zero training): Sharpe 0.727, +200% net, 23.2% CAGR
  - Fine-tuned (3 steps): Sharpe 0.846, +266% net, 28.0% CAGR
- **Takeaway:** "Zero code changes for the base model. Zero training. Sharpe 0.727."

### Closing (3 min)

- Sharpe progression: 0.212 → 0.649 → 0.727 → 0.846
- Less effort, better results: manual features → weekly retraining → zero training
- Caveats: lookahead bias (Chronos), no PSR > 95%, beta vs alpha distinction

---

## Background Scaffolding (`background/`)

Numbered notebooks for QC newcomers. Each builds on the previous.

### `01-qc-platform.ipynb` — What is QuantConnect?

Target: someone who has never seen QC before.

- What the platform is (free cloud-based algorithmic trading platform)
- Free account, cloud IDE, no local install required
- The `QCAlgorithm` lifecycle: `Initialize()` → `OnData()` loop
- `QuantBook` for research (interactive exploration vs live algo)
- How a backtest works: historical data replay, simulated broker
- Key vocabulary: Symbol, Security, Resolution, Algorithm
- Hands-on: create a simple QuantBook, load SPY, plot a price chart

### `02-data-and-universes.ipynb` — Data & Universes

Target: someone who understands QC basics but hasn't worked with data.

- How QC provides institutional-grade market data (equities, futures, options, crypto)
- Static vs dynamic universe selection
- History API: `self.history()` / `qb.history()` — get OHLCV data
- Consolidators: aggregate intraday → daily/weekly
- Equities vs futures: margin, rollovers, multipliers
- Patterns used in the presentation exercises:
  - Ex11: 12 fixed futures contracts + daily consolidation
  - Ex14: top 3 QQQ constituents by ETF weight (dynamic, weekly)
  - Ex18: top 5 by dollar volume (dynamic, monthly)

### `03-ml-on-qc.ipynb` — ML on QuantConnect

Target: someone who knows ML basics but hasn't integrated with QC.

- Training inside the algorithm: scheduled events, `Train()` method
- Persisting models: `ObjectStore` for saving/loading between runs
- Loading pre-trained models: HuggingFace on QC cloud
- Portfolio optimization: SciPy in the algo
- Patterns used in the presentation exercises:
  - Ex11: sklearn Ridge in `OnData`, retrain on schedule
  - Ex14: Keras CNN, weekly retrain, confidence threshold trading
  - Ex18: HuggingFace Chronos, ObjectStore persistence, SciPy optimization

---

## Results Summary

| Exercise | Sharpe | CAGR | Net | Alpha | Beta | Max DD |
|----------|--------|------|-----|-------|------|--------|
| Ex11 — Ridge | 0.212 | 5.85% | +34.8% | -0.062 | 1.146 | 54.7% |
| Ex14 — CNN | 0.649 | 18.6% | +145.2% | 0.093 | 0.278 | 26.3% |
| Ex18 Base — Chronos | 0.727 | 23.2% | +200.0% | 0.040 | 1.125 | 41.2% |
| Ex18 Fine-tuned — Chronos | 0.846 | 28.0% | +266.4% | 0.076 | 1.110 | 49.5% |

---

## QC Setup (for `exercises/`)

For attendees who want to reproduce backtests locally:

- **Prerequisites:** Docker Desktop, Python 3.11+, LEAN CLI (`pip install lean`)
- **Quick start:**
  1. `git clone` this repo
  2. `pip install -r requirements.txt`
  3. `lean login` (free QC account)
  4. `lean research exercises/ex11-ridge` (opens Jupyter with QC kernel)
  5. `lean backtest exercises/ex11-ridge` (runs backtest via Docker)
- **No local setup needed for the notebooks** — `walkthrough.ipynb` and `background/` are self-contained with pre-computed results

---

## Implementation Steps

1. **Update `.gitignore`** — add QC ignores: `data/`, `object-store/`, `storage/`, notebook checkpoints
2. **Create `lean.json`** — minimal LEAN CLI config (org-id, data-folder, backtesting env)
3. **Create `requirements.txt`** — notebook deps (numpy, pandas, matplotlib, seaborn, scikit-learn, torch, chronos-forecasting)
4. **Copy exercise source** from `qc-org-workspace/` → `exercises/` (Ex11, Ex14, Ex18-base, Ex18-finetuned)
5. **Create `background/01-qc-platform.ipynb`** — platform intro notebook
6. **Create `background/02-data-and-universes.ipynb`** — data patterns notebook
7. **Create `background/03-ml-on-qc.ipynb`** — ML integration notebook
8. **Create `walkthrough.ipynb`** — main presentation notebook (3-act structure)
9. **Create `results/`** — directory structure for equity curves (populated later from QC)
10. **Create `README.md`** — navigation guide with 3 reading paths + setup instructions

---

## Design Decisions

- **`walkthrough.ipynb` is self-contained** — shows code inline with pre-computed results. No QC install needed to read.
- **`background/` is numbered** — clear reading order. Each builds on the previous.
- **`exercises/` are real QC projects** — anyone with LEAN CLI can reproduce results.
- **`results/` is pre-computed** — equity curves committed so notebooks render on GitHub.
- **`lean.json` is minimal** — not the 500-line default. Just what LEAN CLI needs.
