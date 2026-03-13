# Part 3: Foundation Models — Presentation Citations

Every factual claim in the video presentation with its supporting citation. Use this document to verify accuracy before publishing.

**Verification status:** ✅ Complete (2026-03-13)

---

## Slide 1 — Intro

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

## Slide 2 — What Is Chronos?

### Claim: T5 architecture, ~8M parameters

> "Pre-trained transformer (T5 architecture, ~8M params)"

**Citation:**
Ansari, A. F. et al. (2024). "Chronos: Learning the Language of Time Series." arXiv:2403.07815, Table 1.

**Verify:** https://arxiv.org/abs/2403.07815

**Note:** chronos-t5-tiny has 8M parameters. The T5 base is from Raffel et al. (2020).

---

### Claim: T5 origin (2019, Google, NLP)

> "T5 was created by Google in 2019 for natural language processing"

**Citation:**
Raffel, C. et al. (2020). "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer." JMLR 21(140), 1-67.

**Verify:** https://arxiv.org/abs/1910.10683

---

### Claim: GPT-3 has 175 billion parameters

> "For context, GPT-3 has 175 billion parameters"

**Citation:**
Brown, T. B. et al. (2020). "Language Models are Few-Shot Learners." arXiv:2005.14165.

**Verify:** https://arxiv.org/abs/2005.14165

---

### Claim: 4,096 discrete bins for tokenization

> "4,096 discrete bins"

**Citation:**
Ansari, A. F. et al. (2024). "Chronos: Learning the Language of Time Series." arXiv:2403.07815, §2.1.

**Verify:** https://arxiv.org/abs/2403.07815

---

### Claim: Trained on weather, energy, retail, economics

> "Trained on: weather, energy, retail, economics"

**Citation:**
Ansari, A. F. et al. (2024). "Chronos: Learning the Language of Time Series." arXiv:2403.07815, §3.1.

**Verify:** https://arxiv.org/abs/2403.07815

---

## Slide 2a — Tokenization Flow

### Claim: MeanScaleUniformBins tokenization method

> "Tokenization: normalize → bin → token"

**Citation:**
Ansari, A. F. et al. (2024). "Chronos: Learning the Language of Time Series." arXiv:2403.07815, §2.1 (MeanScaleUniformBins).

**Verify:** https://arxiv.org/abs/2403.07815

---

## Slide 2b — Foundation Model Landscape

### Claim: Chronos released March 2024

> "Chronos — Mar 2024 (original)"

**Citation:**
Ansari, A. F. et al. (2024). "Chronos: Learning the Language of Time Series." arXiv:2403.07815. Submitted March 12, 2024.

**Verify:** https://arxiv.org/abs/2403.07815

---

### Claim: Chronos-Bolt December 2024, 250× faster

> "Chronos-Bolt — Dec 2024 (250× faster)"

**Citation:**
Amazon Science (2024). "Chronos-Bolt: A faster, more accurate foundation model for time series forecasting."

**Verify:** https://www.amazon.science/blog/chronos-bolt-a-faster-more-accurate-foundation-model-for-time-series-forecasting

---

### Claim: Chronos-2 October 2025, multivariate support

> "Chronos-2 — Oct 2025 (multivariate)"

**Citation:**
Amazon (2025). Chronos-2 release. HuggingFace model card.

**Verify:** https://huggingface.co/amazon/chronos-t5-base

---

### Claim: TimesFM by Google, decoder-only

> "TimesFM — Google — decoder-only"

**Citation:**
Das, A. et al. (2024). "A decoder-only foundation model for time-series forecasting." arXiv:2310.10688.

**Verify:** https://arxiv.org/abs/2310.10688

---

### Claim: MOIRAI-2 by Salesforce, encoder-based

> "MOIRAI-2 — Salesforce — encoder-based"

**Citation:**
Woo, G. et al. (2024). "Unified Training of Universal Time Series Forecasting Transformers." arXiv:2402.02592.

**Verify:** https://arxiv.org/abs/2402.02592

---

### Claim: Lag-Llama open-source, probabilistic

> "Lag-Llama — Open src — probabilistic"

**Citation:**
Rasul, K. et al. (2024). "Lag-Llama: Towards Foundation Models for Probabilistic Time Series Forecasting." arXiv:2310.08278.

**Verify:** https://arxiv.org/abs/2310.08278

---

### Claim: IBM Tiny Time Mixers, 1M parameters

> "IBM TTMs — IBM — compact (1M)"

**Citation:**
IBM Research (2024). "Tiny Time Mixers (TTM): Fast Pre-trained Models for Enhanced Zero/Few-Shot Forecasting." arXiv:2401.03955.

**Verify:** https://arxiv.org/abs/2401.03955

---

### Claim: Time-LLM adapts existing LLMs

> "Time-LLM — Research — adapts LLMs"

**Citation:**
Jin, M. et al. (2024). "Time-LLM: Time Series Forecasting by Reprogramming Large Language Models." arXiv:2310.01728.

**Verify:** https://arxiv.org/abs/2310.01728

---

## Slide 2c — QuantConnect Research Tier

### Claim: Research tier $60/month or $600/year

> "Researcher plan ($60/mo or $600/yr)"

**Citation:**
QuantConnect Pricing Page.

**Verify:** https://www.quantconnect.com/pricing

---

## Slide 3 — Two Strategies

### Claim: Zero-shot definition

> "This is what 'zero-shot' means in AI: the model performs a task it was never explicitly trained for."

**Citation:**
Brown, T. B. et al. (2020). "Language Models are Few-Shot Learners." arXiv:2005.14165, §1.

**Verify:** https://arxiv.org/abs/2005.14165

---

### Claim: 3 gradient steps, learning rate 1e-5

> "3 gradient steps (learning rate: 1e-5)"

**Citation:**
Pik, J. et al. (2025). *Hands-On AI Trading*. Chapter 18: Amazon Chronos Model, fine-tuning configuration.

**Verify:** ISBN 9781394268436

---

### Claim: 63 trading days = ~3 months

> "Forecast: 63 trading days (3 months)"

**Citation:**
Standard trading calendar: ~252 trading days/year ÷ 4 quarters = ~63 days/quarter.

---

### Claim: Markowitz mean-variance optimization (1952)

> "Markowitz mean-variance optimization"

**Citation:**
Markowitz, H. (1952). "Portfolio Selection." *The Journal of Finance*, 7(1), 77-91.

**Verify:** https://doi.org/10.2307/2975974

---

## Slide 3a — Code Map

### Claim: HuggingFace as model source

> "Load chronos-t5-tiny from HuggingFace"

**Citation:**
HuggingFace Model Hub: amazon/chronos-t5-tiny

**Verify:** https://huggingface.co/amazon/chronos-t5-tiny

---

### Claim: ChronosPipeline API

> "from chronos import ChronosPipeline"

**Citation:**
Amazon Chronos GitHub repository.

**Verify:** https://github.com/amazon-science/chronos-forecasting

---

## Slide 4 — Portfolio Optimization

### Claim: Sharpe ratio formula

> "max (R_p − R_f) / σ_p"

**Citation:**
Sharpe, W. F. (1994). "The Sharpe Ratio." *The Journal of Portfolio Management*, 21(1), 49-58.

**Verify:** https://doi.org/10.3905/jpm.1994.409501

---

### Claim: SLSQP solver

> "SciPy SLSQP (Sequential Least Squares Programming)"

**Citation:**
Kraft, D. (1988). "A Software Package for Sequential Quadratic Programming." DFVLR-FB 88-28.

**Verify:** https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html

---

## Slide 5 — Results

### Claim: Base model metrics

> "Sharpe: 0.727, CAGR: 23.2%, Net Profit: +200%, Alpha: 0.040, Beta: 1.125, Max Drawdown: 41.2%"

**Citation:**
QuantConnect backtest results — Base Chronos strategy. Verified via QC API.

---

### Claim: Fine-tuned model metrics

> "Sharpe: 0.846, CAGR: 28.0%, Net Profit: +266%, Alpha: 0.076, Beta: 1.110, Max Drawdown: 49.5%"

**Citation:**
QuantConnect backtest results — Fine-tuned Chronos strategy. Verified via QC API.

---

### Claim: Win rate 72% for both

> "Win Rate: 72%"

**Citation:**
QuantConnect backtest results. With quarterly rebalancing over 5 years, ~20 trades total.

---

### Claim: Capacity $1.4B base, $920M fine-tuned

> "Capacity: $1.4B / $920M"

**Citation:**
QuantConnect estimated capacity from backtest results.

---

## Slide 5a — Equity Curves

### Claim: COVID crash March 2020

> "Both strategies took a hit [in March 2020], but both recovered."

**Citation:**
S&P 500 historical data. COVID-19 market crash: Feb 19 – Mar 23, 2020 (~34% decline).

---

## Slide 6 — The Progression

### Claim: Ridge regression metrics (Part 1)

> "Ridge: Sharpe 0.212, Net Profit +35%, Alpha -0.062, Beta 1.146, Drawdown 54.7%"

**Citation:**
Pik, J. et al. (2025). *Hands-On AI Trading*. Chapter 11: Ridge Regression. Verified via QC API.

---

### Claim: CNN metrics (Part 2)

> "CNN: Sharpe 0.649, Net Profit +145%, Alpha +0.093, Beta 0.278, Drawdown 26.3%"

**Citation:**
Pik, J. et al. (2025). *Hands-On AI Trading*. Chapter 14: Temporal CNN. Verified via QC API.

---

### Claim: CNN weekly retraining, 20 epochs

> "CNN: Weekly, 20 epochs"

**Citation:**
Pik, J. et al. (2025). *Hands-On AI Trading*. Chapter 14, training configuration.

---

## Slide 7 — Caveats

### Claim: Lookahead bias concern

> "Model released 2024, likely trained on post-2019 data. Backtest starts 2019."

**Citation:**
Ansari, A. F. et al. (2024). arXiv:2403.07815. Training data sources include public datasets through 2023.

---

### Claim: PSR values

> "No strategy achieves PSR > 95%. Highest is Chronos fine-tuned at 34.6%."

**Citation:**
Bailey, D. H., & López de Prado, M. (2012). "The Sharpe Ratio Efficient Frontier." *Journal of Risk*, 15(2).

**Values:**
- Ridge (Ex11): 2.44%
- CNN (Ex14): 21.92%
- Chronos Base (Ex18): 25.74%
- Chronos Fine-tuned (Ex18): 34.64%

**Verify:** PSR calculated from QC backtest statistics.

---

### Claim: Different universes

> "Futures (Ex11) ≠ QQQ stocks (Ex14) ≠ Top-5 liquid (Ex18)"

**Citation:**
HOAIT Examples 11, 14, 18 use different asset universes by design.

---

## Slide 8 — Closing

### Claim: CNN alpha 0.093 with beta 0.278

> "Temporal split captures genuine patterns — 0.093 alpha with 0.278 beta"

**Citation:**
Part 2 backtest results. See Slide 6 citation.

---

### Claim: Foundation model era

> "The foundation model era is here"

**Citation:**
Bommasani, R. et al. (2021). "On the Opportunities and Risks of Foundation Models." arXiv:2108.07258.

**Verify:** https://arxiv.org/abs/2108.07258

---

## Tools & Resources

- **QuantConnect:** https://www.quantconnect.com/
- **Chronos on HuggingFace:** https://huggingface.co/amazon/chronos-t5-tiny
- **Chronos GitHub:** https://github.com/amazon-science/chronos-forecasting
- **Code Repository:** https://github.com/ababber/pyhou-02-17-2026

---

_Compiled 2026-03-13. All claims verifiable against listed sources._
