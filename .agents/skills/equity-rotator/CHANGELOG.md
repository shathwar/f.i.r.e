# Changelog - Equity Rotator Skill

## [1.0.0] - 2026-10-17

### Initial Release
- **4-Quadrant Macroeconomic Business Cycle Model**:
  - Classifies growth (accelerating/decelerating) and inflation/interest rates (rising/falling) into Early, Mid, Late, and Recession regimes.
  - Sector sensitivity mappings for Indian markets (Nifty Bank, IT, Auto, FMCG, Pharma, Metals, Capital Goods) and Global/UK markets (FTSE Financials, Energy, Tech, Healthcare).
- **Smart Money Sentiment & Positioning Signals**:
  - FII Index Futures Long/Short ratio contrarian triggers: oversold mean-reversion squeeze (< 18%) vs. crowded overbought exhaustion (> 75%).
  - Options Put-Call Ratio (PCR) and Volatility Index (VIX) sentiment gauges.
- **Market Breadth & Froth Detection**:
  - Advance-Decline divergence (% stocks above 50-DMA).
  - Smallcap-to-Largecap PE ratio froth gauge (alerts when multiple ratio > 1.25x).
  - Equity Risk Premium / Yield Gap (10Y G-Sec vs. earnings yield).
- **Core-Satellite Tactical Architecture**:
  - Caps tactical rotation to 20%–30% of portfolio, protecting the 70% core buy-and-hold foundation.
- **Tax-Smart Execution Models**:
  - Advises execution through Balanced Advantage / Multi-Asset funds for Indian investors to bypass 20% STCG / 12.5% LTCG.
  - Advises 100% tax-free ISA execution for UK investors.
- **Quantitative Engine CLI**:
  - `rotation_engine.py` with `analyze`, `regime`, `sentiment-check`, and `spread-check` commands.
- **Reference Guides**:
  - `references/macro_regimes_and_business_cycle.md`
  - `references/evidence_indicators_and_sentiment.md`
  - `references/rotation_playbooks.md`
- **Behavioral Evaluation Suite**:
  - Added 6 structured evaluation scenarios covering cyclical rotation, defensive safe-haven, small-cap de-frothing, and contrarian short squeezes.
