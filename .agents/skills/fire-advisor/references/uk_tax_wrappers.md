# UK Tax Wrappers, Contribution Rules & Estate Arbitrage Reference

This guide details the tax mechanics, contribution rules, and withdrawal dynamics of UK investment accounts relevant to Financial Independence, Retire Early (F.I.R.E.), incorporating the latest statutory changes (including the 6 April 2027 Inheritance Tax inversion).

---

## 1. Pension Architecture (SIPP & Workplace DC)

### Tax Relief at Source & Net Pay
* **Basic Rate Relief (20%)**: Automatically added to SIPP contributions (£80 personal contribution becomes £100 in the pension).
* **Higher Rate Relief (40%)**: Extra 20% claimed via Self Assessment or tax code adjustment (£100 contribution effectively costs £60).
* **Additional Rate Relief (45%)**: Extra 25% claimed via Self Assessment (£100 contribution effectively costs £55).

### Salary Sacrifice (The Gold Standard)
* By agreeing to reduce gross salary in exchange for an employer pension contribution:
  * Avoid Income Tax (20%, 40%, or 45%).
  * Avoid Employee National Insurance (NI) (8% for basic rate, 2% for higher/additional rate).
  * Employers save 13.8% Employer NI (forward-thinking employers rebate part or all of this back into your pension).

### The 60% Marginal Tax Trap (£100,000 – £125,140)
* Between £100,000 and £125,140, the £12,570 Personal Allowance is reduced by £1 for every £2 of adjusted net income.
* Effective rate:
  * 40% Income Tax + 20% lost Personal Allowance value + 2% Employee NI = **62% marginal tax**.
* **F.I.R.E. Strategy**: Every £1 contributed to a pension in this bracket yields an immediate 60%–62% return by restoring the Personal Allowance.

### The Fundamental Contribution Law: $r > 0.75m$
* A pound of pension pot costs $(1 - r)$ in foregone take-home pay (where $r$ is relief going in).
* With PCLS available (25% tax-free, 75% taxed at retirement marginal rate $m$), it comes out worth:
  $$\text{Value at Drawdown} = 0.25 + 0.75(1 - m)$$
* **Break-Even Marginal Drawdown Rate**:
  $$m_{\text{break-even}} = \frac{r}{0.75} \quad (\approx 26.7\% \text{ for basic rate } r=20\%)$$
* **Implications**:
  * For basic-rate taxpayers ($r=20\%$), contributing makes sense if drawn at basic rate (+6.25% instant gain) or within Personal Allowance (+25% gain).
  * If a non-earning spouse will retire into higher-rate tax (e.g. from a generous DB scheme), paying £2,880 net into their pension **destroys money (-12.5%)**. Always check projected retirement tax brackets!

---

## 2. April 2027 Inverts the Traditional Decumulation Advice

### The Old Rule vs. The New Rule
* **The Old Advice ("Pensions Last")**: Spend ISAs first, leave private pensions untouched because pensions sat outside the estate for Inheritance Tax (IHT).
* **The New Rule ("Pensions First")**: From **6 April 2027 (Finance Act 2026)**, unused pension funds enter the deceased's estate for IHT.

### The Death Tax Math: Inherited Pension vs. Inherited ISA
Upon death after age 75, beneficiaries pay income tax at their own marginal rate on pension withdrawals. When stacked with 40% IHT, the effective tax rate is:
$$\text{Net Received} = (1 - \text{IHT}) \times (1 - \text{Beneficiary Tax Rate})$$

| Beneficiary Marginal Rate | Effective Tax on Inherited Pension | Effective Tax on Inherited ISA |
| :--- | :--- | :--- |
| **Basic Rate (20%)** | **52.0%** | **40.0%** |
| **Higher Rate (40%)** | **64.0%** | **40.0%** |
| **Additional Rate (45%)** | **67.0%** | **40.0%** |

> **The Golden Decumulation Decision Rule**:
> **Move money from Pension to ISA during life whenever your current marginal tax rate is lower than your beneficiary's expected marginal tax rate later ($m_{\text{retiree}} < b_{\text{beneficiary}}$).**

* *Worked Example*: If you are a retired basic-rate taxpayer (20%) with adult children working in higher-rate bands (40%):
  * Drawing £1,000 from your pension incurs 20% tax (£200), leaving £800 to fund spending or recycle into your £20,000 ISA. At your death, the £800 ISA bears 40% IHT $\rightarrow$ Children receive **£480**.
  * If you leave the £1,000 in your pension untouched, it bears 40% IHT and 40% income tax $\rightarrow$ Children receive **£360**.
  * **Systematic pension drawdown preserves 33% more wealth for heirs!**

---

## 3. The Optimal Decumulation Draw Order

To maximize lifetime wealth and minimize estate shrinkage:

1. **Fill the Personal Allowance (£12,570)** from the pension every single year (use it or lose it).
2. **Draw Pension up to the Basic Rate Ceiling (£50,270)**: 20% tax now beats the 64% death tax.
3. **Recycle Surplus into Stocks & Shares ISAs**: Funnel up to £20,000/year per spouse into ISAs.
4. **PCLS Strategy (The £268,275 LSA Cap)**: Take the 25% tax-free lump sum strategically to fund the pre-57 bridge or shelter within ISAs. A PCLS left inside an inherited pension after 2027 is effectively squandered.
5. **Drain GIAs before ISAs**: Selling down taxable GIA holdings early terminates annual dividend tax drag (up to 35.75% for higher-rate earners) and harvests the £3,000 annual CGT exemption. Preserve the tax-exempt ISA wrapper until last.
6. **Hard Stop at £100,000**: Never blindly draw pension between £100,000 and £125,140 during retirement, as the Personal Allowance taper creates an artificial 60% income tax spike.

---

## 4. Current Allowances & Thresholds Register

| Allowance / Threshold | Current Value | Uprating Policy |
| :--- | :--- | :--- |
| **Personal Allowance** | £12,570 | Frozen in cash terms until April 2031 |
| **Basic Rate Band Ceiling** | £50,270 | Frozen in cash terms until April 2031 |
| **Additional Rate Threshold** | £125,140 | Frozen in cash terms |
| **Pension Normal Minimum Access Age** | **57** from 6 April 2028 | Legislated statutory threshold |
| **Pension Annual Allowance** | £60,000 | Tapers above £260k adjusted income down to £10k |
| **Money Purchase Annual Allowance (MPAA)** | £10,000 | Triggered once flexible drawdown begins |
| **Lump Sum Allowance (LSA / PCLS Cap)** | £268,275 | Fixed; zero indexation mechanism (fiscal drag) |
| **Lump Sum & Death Benefit Allowance** | £1,073,100 | Fixed |
| **Stocks & Shares ISA Limit** | £20,000 / adult / yr | Fixed since 2017; eroded by inflation |
| **Lifetime ISA (LISA) Limit** | £4,000 / yr | 25% bonus; accessible age 60 or first home |
| **Capital Gains Tax Exemption** | £3,000 / adult / yr | Fixed |
| **CGT Rate (Shares)** | 18% Basic / 24% Higher | Set post-30 Oct 2024 budget |
| **Dividend Allowance** | £500 / yr | 10.75% basic, 35.75% higher, 39.35% additional |
| **IHT Nil-Rate Band** | £325,000 | Transferable; frozen to April 2031 |
| **Residence Nil-Rate Band (RNRB)** | £175,000 | Tapers £1 per £2 on estates over £2.0M |
| **Unused Pensions in Estate for IHT** | **6 April 2027** | Finance Act 2026 |
