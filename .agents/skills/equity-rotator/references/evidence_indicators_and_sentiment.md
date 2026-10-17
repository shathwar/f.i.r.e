# Evidence-Based Sentiment, Liquidity & Market Breadth Indicators

This reference specifies the quantitative indicators, mathematical thresholds, and data lineage required to validate tactical equity rotations **3 to 5 trading days ahead of consensus**.

---

## 1. Institutional Flow & Derivative Sentiment (Smart Money Signals)

### A. FII Index Futures Long-to-Short Ratio (India)
* **The Metric**: Foreign Institutional Investor (FII) net open interest contracts in Index Futures (Nifty & Bank Nifty).
* **Historical Mean**: Typically hovers between **40% and 55%**.
* **Inflection Extremes**:
  * **Oversold Reversal Trigger (FII L/S $< 15\%$)**: FII positioning is excessively short. Triggers an aggressive short-covering rally within **2 to 5 trading days**.
    * *Tactical Action*: Front-run short squeeze by rotating capital into **high-beta banking (Nifty Bank, Private Banks)** and cyclicals.
  * **Overbought Exhaustion Trigger (FII L/S $> 75\% - 80\%$)**: Institutional positioning is crowded long. Any negative catalyst causes rapid unwind.
    * *Tactical Action*: Trim high-beta cyclicals; rotate into **defensive FMCG, Pharma, or Arbitrage funds**.

### B. Put-Call Ratio (PCR - Open Interest)
* Calculated as total open interest in Put options divided by Call options:
  $$\text{PCR} = \frac{\sum \text{Put Open Interest}}{\sum \text{Call Open Interest}}$$
* **Contrarian Sentiment Bands**:
  * $\text{PCR} \le 0.70$: Extreme call writing / retail complacency (Market vulnerable to pullback).
  * $0.90 \le \text{PCR} \le 1.20$: Neutral / healthy trend equilibrium.
  * $\text{PCR} \ge 1.40 - 1.60$: Extreme put accumulation / panic hedging (Imminent bottom formation within 48–72 hours).

### C. Volatility Index (India VIX & CBOE VIX)
* **VIX $< 12.0$ (Complacency Zone)**: Options pricing implies low risk. Risk-reward for buying beta is poor; initiate hedge rotations.
* **$13.0 \le \text{VIX} \le 17.0$ (Orderly Bull Regime)**: Optimal environment for momentum and broad-based sectoral trend following.
* **VIX $> 22.0$ (Stress Zone)**: Sharp spike in implied volatility. Rotate immediately into low-beta defensives (Pharma/FMCG) and sovereign cash equivalents.

---

## 2. Market Breadth & Internal Participation Signals

### A. Sectoral Advance-Decline (A/D) Divergence
* **The Warning Sign**: When the headline benchmark (Nifty 50 or S&P 500) hits fresh all-time highs, but fewer than **45% of constituent stocks are trading above their 50-day moving average (50-DMA)**.
* **Interpretation**: The rally is concentrated in a handful of mega-caps (e.g. Reliance, HDFC Bank, Apple, Nvidia), masking underlying decay in broader market participation.
* **Rotation Playbook**: Rotate out of **overheated Small/Mid-Caps** into **Large-Cap Value & Quality**.

### B. Nifty 50 vs. Nifty Smallcap 250 Valuation Spread
* **Smallcap-to-Largecap P/E Ratio**:
  $$\text{Valuation Multiple Ratio} = \frac{\text{Nifty Smallcap 250 P/E}}{\text{Nifty 50 P/E}}$$
* **Historical Norm**: Typically trades at a **10% to 20% discount** ($\approx 0.80 - 0.90$).
* **Danger Zone ($> 1.25$)**: When Smallcap P/E trades at a premium over Largecap P/E, retail froth is peak.
  * *Evidence Rule*: Mandates an immediate **20%–30% tactical rotation from Small-Cap mutual funds into Large-Cap / Flexi-Cap funds** to avoid severe multi-quarter drawdowns.

---

## 3. Macroeconomic Yield Gap (Equity Risk Premium)

* **The Yield Gap Formula**:
  $$\text{Yield Gap} = \text{10-Year Government Bond Yield} - \text{Equity Earnings Yield} = Y_{10\text{Y}} - \left(\frac{1}{\text{Index P/E}} \times 100\right)$$
* **Benchmark Conditions (India)**:
  * When Nifty 50 P/E is 24.0 $\rightarrow$ Earnings Yield is $\frac{1}{24} = 4.17\%$.
  * India 10Y G-Sec Yield is **6.85%**.
  * $\text{Yield Gap} = 6.85\% - 4.17\% = \mathbf{+2.68\%}$.
* **Institutional Interpretation**:
  * An elevated yield gap ($> +2.5\%$) indicates equities are expensive relative to risk-free sovereign debt.
  * *Rotation Mandate*: Tactical equity allocation should be tightened from aggressive (70%) to neutral (55%–60%), shifting the difference into Arbitrage Funds or Dynamic Asset Allocation.

---

## 4. Evidence-Based Rotation Scorecard

Before recommending any sector or style rotation, evaluate these 5 dimensions:

```text
┌────────────────────────────────────────────────────────────────────────┐
│               EVIDENCE-BASED ROTATION EVALUATION MATRIX                │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ Dimension          │ Quantitative Data  │ Decision Signal              │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 1. Macro Regime    │ GDP, PMI, Rates    │ Overweight cycle winners     │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 2. Institutional   │ FII Long/Short,    │ Contrarian mean-reversion    │
│    Positioning     │ DII Flows, PCR     │ (buy oversold / sell crowded)│
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 3. Market Breadth  │ % Stocks > 50-DMA  │ Broad rally vs fakeout       │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 4. Valuation       │ Yield Gap, P/E vs  │ Reject over-extended froth   │
│    Spreads         │ 5Y historical mean │                              │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 5. Relative        │ Sector/Index ratio │ Confirm trend momentum       │
│    Strength (RS)   │ 20-DMA vs 50-DMA   │                              │
└────────────────────┴────────────────────┴──────────────────────────────┘
```
