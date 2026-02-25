# Presentation Verification Report

_Pre-recording accuracy review for `hoait-presentation.ipynb`_

Generated: 2026-02-24

---

## Summary

**Status:** PASS with minor fixes required

- **External citations:** All verified ✓
- **Numerical consistency:** All values match between slides and summary table ✓
- **Typos found:** 3 (must fix before recording)

---

## Typos to Fix

| Location | Error | Correction |
|----------|-------|------------|
| Slide 1 intro | "presenatation" | "presentation" |
| Slide 1 intro | "likliehood" | "likelihood" |
| Slide 1 intro | "availble" | "available" |

**Cell:** First markdown cell after title (intro paragraph)

---

## External Citations Verified

| Claim | Source | Status |
|-------|--------|--------|
| Ridge regression (1970) | Hoerl & Kennard, *Technometrics* 12(1), 55–67 | ✓ Verified |
| CNN backprop (1989) | LeCun et al., *Neural Computation* 1(4), 541–551 | ✓ Verified |
| Chronos (2024) | Ansari et al., arXiv:2403.07815 | ✓ Verified (March 12, 2024) |
| Chronos-tiny ~8M params | Amazon documentation | ✓ Verified (8M parameters) |
| PSR metric (2012) | Bailey & López de Prado, *J. of Risk* 15(2) | ✓ Verified |
| Sharpe ratio (1966) | Sharpe, *J. of Business* 39(1), 119–138 | ✓ Standard reference |
| Jensen's alpha (1968) | Jensen, *J. of Finance* 23(2), 389–416 | ✓ Standard reference |

---

## Numerical Consistency

### Ridge Regression (Ex11)
| Metric | Slide 6 | Summary Table | Match |
|--------|---------|---------------|-------|
| Sharpe | 0.212 | 0.212 | ✓ |
| Net Profit | +34.8% | +35% | ✓ (rounded) |
| Alpha | -0.062 | -0.062 | ✓ |
| Beta | 1.146 | 1.146 | ✓ |
| Max DD | 54.7% | 54.7% | ✓ |

### Temporal CNN (Ex14)
| Metric | Slide 10 | Summary Table | Match |
|--------|----------|---------------|-------|
| Sharpe | 0.649 | 0.649 | ✓ |
| Net Profit | +145.2% | +145% | ✓ (rounded) |
| Alpha | 0.093 | 0.093 | ✓ |
| Beta | 0.278 | 0.278 | ✓ |
| Max DD | 26.3% | 26.3% | ✓ |
| PSR | 21.9% | — | ✓ |

### Chronos Base (Ex18)
| Metric | Slide 15 | Summary Table | Match |
|--------|----------|---------------|-------|
| Sharpe | 0.727 | 0.727 | ✓ |
| Net Profit | +200% | +200% | ✓ |
| Alpha | 0.040 | 0.040 | ✓ |
| Beta | 1.125 | 1.125 | ✓ |
| Max DD | 41.2% | 41.2% | ✓ |

### Chronos Fine-Tuned (Ex18 FT)
| Metric | Slide 15 | Summary Table | Match |
|--------|----------|---------------|-------|
| Sharpe | 0.846 | 0.846 | ✓ |
| Net Profit | +266% | +266% | ✓ |
| Alpha | 0.076 | 0.076 | ✓ |
| Beta | 1.110 | 1.110 | ✓ |
| Max DD | 49.5% | 49.5% | ✓ |

---

## Caveats Acknowledged

The presentation correctly discloses:

1. **Lookahead bias** — Chronos released 2024, backtest 2019–2024 overlap acknowledged
2. **Statistical significance** — PSR < 95% for all strategies acknowledged
3. **Different universes** — Futures ≠ QQQ stocks ≠ top-5 liquid acknowledged
4. **Survivorship bias** — Current constituents, not historical, acknowledged
5. **Small universes** — 3-5 stocks limitation acknowledged

---

## Recommended Actions

1. **Fix 3 typos** in Slide 1 intro paragraph
2. **Re-export HTML** after typo fixes
3. **Ready for recording** after fixes

---

*Verification performed by cross-referencing web sources and internal notebook consistency.*
