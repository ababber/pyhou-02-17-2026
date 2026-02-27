# QuantConnect — Getting Started & Lessons Learned

A practitioner's reference for working with [QuantConnect](https://www.quantconnect.com/) (QC), compiled while building strategies from *Hands-On AI Trading with Python, QuantConnect, and AWS* (Pik, J. et al., 2025, Wiley).

---

## What is QuantConnect?

QuantConnect is a cloud platform for algorithmic trading. You write Python (or C#), and it handles data, execution, backtesting, and live trading. Under the hood, it runs [LEAN](https://github.com/QuantConnect/Lean) — an open-source algorithmic trading engine. You can use LEAN locally or through QC's cloud.

## Ways to Use QuantConnect

There are four main access paths. Pick the one that fits your workflow.

### 1. Web IDE (quantconnect.com)

The default starting point. Full browser-based IDE with code editor, backtesting, research notebooks, and results visualization.

- **Best for:** Quick prototyping, exploring data, running backtests, viewing equity curves and debug logs
- **Limitations:** No local version control, limited editor features compared to a real IDE

### 2. LEAN CLI

Command-line tool for local development with cloud or local execution.

```bash
pip install lean
lean init                          # Initialize a LEAN workspace
lean cloud push --project "Name"   # Push local code to cloud
lean cloud backtest "Name"         # Run backtest on cloud
lean backtest "Name"               # Run backtest locally (Docker required)
```

- **Best for:** Local development with your preferred editor, CI/CD pipelines, version control
- **Limitations:** Local backtesting requires Docker and can be resource-intensive; some data only available on cloud
- **Tip:** `lean cloud push/pull` keeps local and cloud in sync

### 3. VS Code Extension

The [QuantConnect extension](https://marketplace.visualstudio.com/items?itemName=quantconnect.quantconnect) brings the cloud IDE experience into VS Code.

- **Best for:** Developers who live in VS Code and want autocomplete, local editing with cloud execution
- **Limitations:** Still runs backtests on cloud; extension maturity varies

### 4. REST API

Direct HTTP access to `quantconnect.com/api/v2`. Authenticate with your User ID and API Token (from Account → API Access).

```
GET  /api/v2/projects                          # List projects
POST /api/v2/projects/create                   # Create project
GET  /api/v2/projects/{id}/files               # List files
POST /api/v2/files/create                      # Upload file
POST /api/v2/compile/create                    # Compile project
POST /api/v2/backtests/create                  # Run backtest
GET  /api/v2/backtests/read                    # Get results
```

- **Best for:** Automation, scripting workflows, integrating QC into larger pipelines
- **Limitations:** No debug logs via API; equity curves and visual output require the web interface

## Development Principles

1. **Research first, deploy second.** Prototype in QuantBook (research notebooks), validate interactively, then convert to `main.py`.
2. **Use `get_parameter()` for sweepable values.** Algorithms should use `self.get_parameter("name", default)` for any tunable parameter — this enables optimization sweeps without code changes.
3. **Type checker warnings are noise.** QC stubs produce IDE warnings that don't affect runtime. Don't chase them.
4. **No debug logs via API.** If you need runtime diagnostics, use `self.runtime_statistics["key"] = "value"` to surface values in backtest results, or check the web IDE for full debug logs.

---

## Known Book Source Code Bugs (HOAIT)

If you're working through the book's exercises, these are bugs we encountered. The book's code doesn't always run cleanly on the current QC platform.

### Bug Summary

| Exercise | Issue | Fix |
|----------|-------|-----|
| Ex07 | `IndexError` — `.iloc[-1]` on empty indicator history | Guard: `if slice.empty: continue` |
| Ex08 | `KeyError: 'value'` in VIX history + 0-sample Lasso | See CBOE VIX pattern below |
| Ex10 | Row count mismatch in `model.fit()` (23,092 vs 22,400) | See timestamp normalization pattern below |
| Ex11 | `ValueError` — sklearn rejects mixed column name types | Convert to `.values` before `model.fit()` |
| Ex12 | `RuntimeError` — variable assigned in branch, used at function scope | Initialize before conditional |
| Ex15 | Empty index intersection + `None` model race condition (two bugs) | See patterns below |
| Ex18 | Missing `typer_config` module + DataLoader crashes + Symbol mismatch (three bugs) | See patterns below |
| Ex19 | OOM — TF + BERT exceeds QC container memory (~3GB) | See TF/PyTorch pattern below |

### Seven Bug Classes

1. **Indicator warmup gaps** (Ex07): Book code assumes indicator history covers the full training lookback, but early data points predate warmup.
2. **Timestamp convention mismatches** (Ex08, Ex10): `daily_precise_end_time` differences between data sources cause index alignment failures.
3. **Unscoped variables** (Ex12): Variables assigned inside conditional branches but referenced at function scope — crashes when the branch isn't taken.
4. **Dynamic universe membership gaps** (Ex15): When universe selection changes between training periods, index intersection can be empty.
5. **Deferred training race condition** (Ex15): `on_data` fires for securities before `_train()` has ever run, leaving `model` as `None`.
6. **QC environment compatibility** (Ex18): Transitive dependency gaps in HuggingFace imports, DataLoader multiprocess failures in containers.
7. **TF/PyTorch framework memory** (Ex19): TF + PyTorch + BERT exceeds QC's ~3GB container limit.

---

## Patterns & Workarounds

### CBOE VIX History (Ex08+)

Book code uses `self.history(symbol, timedelta, Resolution.DAILY).loc[symbol]['value']`. Two bugs:

1. **Column rename:** CBOE data returns `close`, not `value`. Fix: use `['close']` in DataFrame access; keep `data[symbol].value` in `on_data` (that's an object property, not a column).
2. **Timestamp mismatch:** VIX history uses same-day midnight, equity bars use next-day midnight. Exact match always fails → indicators stay NaN. Fix: use nearest-previous lookup `self._samples.index[self._samples.index <= t][-1]`.

### Timestamp Normalization (Ex10+)

When `daily_precise_end_time = False` (the default), fundamental and price data use different time-of-day conventions. Merging produces row count mismatches.

**Fix:** Normalize both indices to date-only with `pd.Timestamp.normalize()`, then deduplicate with `.drop_duplicates()`. Add `min(len(X), len(y))` truncation before `model.fit()` as a safety guard.

### Dynamic Universe Gaps (Ex15)

In algorithms with periodic universe rebalancing, securities enter at different times. Index intersection can be empty.

**Fix:** Guard: `if not idx: return` in `_train()`. The previous model remains valid until next successful training.

**Impact was dramatic:** With both Ex15 bugs present: Sharpe 0.693, Net 149%. Clean: Sharpe 0.886, Net 311.5%.

### Deferred Training Race Condition (Ex15)

Securities receive `on_data` before `_train()` runs. `security.model` is `None`.

**Fix:** Guard trade logic: `if security.model is None: continue`.

### QC Environment Compatibility (Ex18)

Chronos fine-tuning imports require `typer_config` (not in QC runtime), DataLoader multiprocess crashes, and Symbol string representation mismatches.

**Three fixes:**
1. `sys.modules['typer_config'] = MagicMock()` before import
2. `dataloader_num_workers=0`
3. Positional column rename: `df.columns = ['time', 'target']`

### TF/PyTorch Memory (Ex19)

Book uses `TFBertForSequenceClassification` — too large for QC's container.

**What works:**
1. Set `USE_TF=0`, `USE_FLAX=0` env vars before any `transformers` import
2. Use PyTorch with `torch.float16` for inference
3. Defer model loading to `on_warmup_finished()`
4. For fine-tuning: freeze BERT encoder, train only the classifier head (~2K params)

**General rule:** For any large transformer on QC — always `USE_TF=0`, always float16, always freeze encoder for fine-tuning, always defer loading past `initialize()`.

### Two-Project Comparison (Ex12)

When the book uses a `_benchmark = True/False` flag, split into two separate QC projects for cleaner separation and independent backtest IDs. Both can write to Object Store; a research notebook loads both CSVs for comparison.

### Object Store Model Persistence (Ex17+)

When the book's workflow requires a research notebook to train a model (which can't be automated via API), convert the notebook logic into a **trainer algorithm**:

1. Upload trainer as `main.py` → run backtest (trains model, saves to Object Store)
2. Upload trading algo as `main.py` → run backtest (loads model from Object Store)

Same project, sequential backtests. Object Store persists across backtests.

### Custom Slippage Model

QC's default slippage model may not reflect real microstructure. Override when execution quality matters:

```python
class SpreadSlippageModel:
    def get_slippage_approximation(self, asset, order):
        return asset.ask_price - asset.bid_price

self._security.set_slippage_model(SpreadSlippageModel())
```

### External API Dependencies (Ex16+)

Some exercises require paid APIs (e.g., OpenAI GPT-4 for sentiment). These can't run inside QC backtests directly. Use a **two-backtest pattern**: a generator backtest calls the API and writes results to Object Store, then the trading backtest reads from Object Store.

Free alternatives for Ex16: GPT-4o-mini (~10x cheaper), FinBERT (free, via `transformers`), or word-based sentiment dictionaries.

---

## Caveats

### Lookahead Bias in Foundation Models (Ex18+)

Pre-trained HuggingFace models (Chronos, FinBERT, etc.) may contain **architectural lookahead bias** — their weights encode patterns from the entire pre-training corpus, which likely includes data from the backtest period. This is distinct from classical lookahead bias (future data in features) and cannot be fixed by adjusting backtest code.

**Example:** Chronos T5-Tiny was released 2024, backtest runs 2019–2024. The base model's weights likely encode post-2019 financial patterns. Base model results (Sharpe 0.727) should be interpreted as an upper bound. Fine-tuning partially mitigates by adapting to local data.

**General rule:** For any exercise using pre-trained models, note the model's release date vs. backtest period. If they overlap, flag the lookahead risk.

### Chart API Downsampling

QC's `/backtests/chart/read` endpoint returns uniformly-resampled data — not raw daily returns. For a 5-year backtest, QC returns ~375 points at uniform 5.12-day intervals regardless of request parameters. This is server-side interpolation for visualization.

**Impact:** If you export equity curve data and recalculate metrics (Sharpe, volatility), you'll get different values than QC reports. The interpolation smooths volatility, artificially inflating Sharpe. QC's reported Sharpe uses actual daily trading returns internally.

**Example:** In Part 1, QC reports Sharpe 0.212. Recalculating from exported chart data gives 0.29–0.34 — the smoothed data has lower volatility. The conclusion doesn't change (still half the market's Sharpe), but the numbers differ.

**Workaround:** For accurate return statistics, use QC's reported metrics directly. For full-resolution data, run backtests locally via LEAN CLI or add `self.Plot("DailyEquity", "Value", self.Portfolio.TotalPortfolioValue)` in your algorithm's `on_end_of_day()` to create a custom daily series.

### Crypto Data

Bybit BTCUSDC data available on QC from July 2017 via CoinAPI. 956 cryptocurrency pairs supported. Resolutions: tick, second, minute, hourly, daily. Access: `self.add_crypto("BTCUSDC", market=Market.BYBIT)`. Free on cloud for backtesting.

---

*Compiled from working through 19 exercises in HOAIT. Exercises 13, 14, 16, and 17 had zero bugs. Last updated: 2026-02-26.*
