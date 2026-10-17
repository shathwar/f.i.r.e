# Pension Bridge, Sequence of Returns Risk (SORR) & Critical Stress-Testing

This reference outlines the mechanics of engineering a UK pre-57 bridge, managing early-retirement drawdowns under historical volatility, and stress-testing against real-world vulnerabilities (late-life care, first death, and fiscal drag).

---

## 1. Sizing the Pre-57 Pension Bridge

### The Problem
The Normal Minimum Pension Age (NMPA) is statutory at **57 from 6 April 2028**. An individual retiring early at age 45 faces a **12-year gap** where private pensions cannot be touched without a 55% unauthorized payment penalty.

### Bridge Formula
To fund $N$ years before age 57 with annual target expenditure $C$, assuming an annual inflation rate $i$ and conservative real return on the bridge $r_b$:

$$\text{Bridge Required} = \sum_{t=1}^{N} \frac{C \cdot (1 + i)^t}{(1 + r_{\text{bridge}})^t}$$

If $r_{\text{bridge}}$ matches inflation (a conservative assumption when holding cash/short-term bonds), the formula simplifies to:
$$\text{Bridge Required} \approx N \times C$$

*Example*: Retiring at age 47 with £45,000/year spending.
* Gap to age 57 = $57 - 47 = 10$ years.
* Base bridge required = $10 \times £45,000 = £450,000$.
* Buffer for market drop / unexpected costs (10–15%) = **£495,000 to £517,500 in liquid ISAs / cash**.
* The remaining portion of the overall FIRE target remains inside SIPPs/workplace DC pensions compounding tax-sheltered until age 57.

---

## 2. Multi-Bucket Bridge Architecture

To prevent selling depressed equities during the bridge years, structure the bridge into three buckets:

```text
[Bucket 1: Cash / MMF]   --> 1 to 2 Years of Spending (Liquid, Zero Volatility)
        ^
        | Replenish on rebalancing
[Bucket 2: Short Bonds]  --> 3 to 5 Years of Spending (Gilts / Ultra-Short Fixed Income)
        ^
        | Harvested when equities are up
[Bucket 3: S&S ISA]      --> 6+ Years of Spending (Broad Market Global Equity Index)
```

---

## 3. Sequence of Returns Risk (SORR) & The 30% Crash

### Why SORR Kills Early Retirement
If a portfolio drops 30% in Year 1 of retirement:
* A £1,000,000 portfolio drops to £700,000.
* If the retiree withdraws £40,000 (4%), the remaining capital is £660,000.
* To return to £1,000,000, the remaining portfolio must gain **+51.5%** just to break even in nominal terms.
* Repeated withdrawals during this dip permanently deplete unit counts.

### The 4 Stress-Test Defense Mechanisms

#### 1. Cash Buffer Isolation
* Maintain 24 months of essential expenses in Cash ISA / Money Market Funds.
* In a 30% downturn, draw 100% of living expenses from Bucket 1.
* Zero shares are sold at distressed valuations, granting equities 24–36 months to recover.

#### 2. Guyton-Klinger Capital Preservation Guardrails
* **Capital Preservation Rule**: If the current withdrawal rate rises more than 20% above the initial withdrawal rate (e.g., initial SWR was 3.5%, but market drop pushes it above $3.5\% \times 1.2 = 4.2\%$), cut current annual withdrawal by 10%.
* **Prosperity Rule**: If the current withdrawal rate falls 20% below initial SWR, increase annual withdrawal by 10%.
* **Inflation Freeze**: In any year following a negative portfolio total return, skip the annual inflation step-up.

#### 3. Core vs. Discretionary Spending Flex
* Classify expenditure into **Floor (Essential: housing, council tax, food, utilities)** and **Ceiling (Discretionary: holidays, restaurants, upgrades)**.
* Typical healthy split: 65% Floor, 35% Ceiling.
* In a severe downturn, reduce the Ceiling by 30%–50%. A £40,000 budget with £14,000 discretionary spend can immediately contract to £33,000, drastically curbing portfolio drain.

#### 4. Barista / Consulting Buffer
* Earning just £10,000–£15,000/year through low-stress consulting, freelance work, or hobbies during the first 3 years of an unexpected crash completely offsets the portfolio drawdown, neutralizing SORR.

---

## 4. Advanced Stress Tests: Care Costs & Fiscal Drag

### Late-Life Care Costs (The End-of-Life Shock)
* **The Reality**: Residential and nursing care in the UK costs **£50,000–£75,000+ per year** (averaging 2.5–4 years per person in late life).
* **Means Testing in England**:
  * Capital over £23,250: Self-funded in full (including the value of your home unless a spouse still lives in it).
  * Capital between £14,250 and £23,250: Tapered local authority support.
  * Capital under £14,250: Maximum local authority support.
* **Planning Rule**: Ensure the surviving partner's residual estate can withstand a £150,000–£200,000 late-life care expense without exhausting essential income.

### Fiscal Drag: The Silent Allowance Erosion
* The £20,000 ISA limit, £3,000 CGT exemption, and £268,275 Lump Sum Allowance have **no statutory inflation indexation**.
* Over a 30-year retirement at 2.5% inflation, the real purchasing power of the £20,000 ISA limit shrinks to under **£9,500**.
* **Planning Rule**: Maximize wrappers early. Do not delay Bed & ISA or pension tax-free cash extraction assuming future allowances will buy the same tax shelter.
