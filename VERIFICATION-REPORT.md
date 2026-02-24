# Presentation Verification Report

_Pre-recording accuracy review for hoait-presentation.ipynb_

Generated: 2026-02-24

---

## Summary

**Status:** PASS with minor fixes required

- **External citations:** All verified
- **Numerical consistency:** All values match between slides and summary table
- **Typos found:** 3 (must fix before recording)

---

## Typos to Fix

| Location | Error | Correction |
|----------|-------|------------|
| Slide 1 intro | presenatation | presentation |
| Slide 1 intro | likliehood | likelihood |
| Slide 1 intro | availble | available |

**Cell:** First markdown cell after title (intro paragraph)

---

## External Citations Verified

- Ridge regression (1970): Hoerl & Kennard, Technometrics 12(1), 55-67 - VERIFIED
- CNN backprop (1989): LeCun et al., Neural Computation 1(4), 541-551 - VERIFIED
- Chronos (2024): Ansari et al., arXiv:2403.07815 (March 12, 2024) - VERIFIED
- Chronos-tiny 8M params: Amazon documentation - VERIFIED
- PSR metric (2012): Bailey & Lopez de Prado, J. of Risk 15(2) - VERIFIED
- Sharpe ratio (1966): Sharpe, J. of Business 39(1), 119-138 - VERIFIED
- Jensen alpha (1968): Jensen, J. of Finance 23(2), 389-416 - VERIFIED

---

## Numerical Consistency

All metrics match between detailed slides and summary table:

- Ridge (Ex11): Sharpe 0.212, Net +34.8%/+35%, Alpha -0.062, Beta 1.146, DD 54.7% - ALL MATCH
- CNN (Ex14): Sharpe 0.649, Net +145.2%/+145%, Alpha 0.093, Beta 0.278, DD 26.3% - ALL MATCH
- Chronos Base: Sharpe 0.727, Net +200%, Alpha 0.040, Beta 1.125, DD 41.2% - ALL MATCH
- Chronos FT: Sharpe 0.846, Net +266%, Alpha 0.076, Beta 1.110, DD 49.5% - ALL MATCH

---

## Caveats Acknowledged

The presentation correctly discloses:

1. Lookahead bias - Chronos released 2024, backtest 2019-2024 overlap
2. Statistical significance - PSR < 95% for all strategies
3. Different universes - Futures vs QQQ stocks vs top-5 liquid
4. Survivorship bias - Current constituents, not historical
5. Small universes - 3-5 stocks limitation

---

## Recommended Actions

1. Fix 3 typos in Slide 1 intro paragraph
2. Re-export HTML after typo fixes
3. Ready for recording after fixes
