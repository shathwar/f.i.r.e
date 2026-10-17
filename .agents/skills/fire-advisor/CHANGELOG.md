# Changelog - UK & India F.I.R.E. Advisor Skill

## [1.3.0] - 2026-10-17

### Added Traditional & Tangible Indian Asset Classes:
- **Bank Fixed Deposits (FDs) vs. Arbitrage Funds**:
  - Detailed post-tax real return modeling: 7.25% FD at 31.2% tax yields 4.99% net, producing a **-1.5% negative real return** against 6.5% inflation.
  - Arbitrage Mutual Funds modeled as a tax-efficient parking instrument (12.5% LTCG, ~6.1% net, +1.2% net alpha over FDs).
- **Gold & Silver Precious Metals Architecture**:
  - Sovereign Gold Bonds (SGB): 2.5% annual coupon + **100% tax-free capital gains** upon 8-year RBI redemption under Section 47(viic).
  - Gold & Silver ETFs: Post-Budget 2024 **12.5% LTCG after 24 months** (no indexation).
  - Asset role sizing: 5%–10% Gold (geopolitical & INR depreciation moat), 2%–5% Silver (high-beta industrial commodity).
- **Real Estate & Buy vs. Rent Quantitative Modeling**:
  - Residential Rental Yield Reality: 2.0%–2.8% gross (1.8%–2.2% net after maintenance, property tax, and vacancy).
  - Real Estate vs. SWR Capital Efficiency: Generating ₹1L/month in rental cash flow requires **₹5.45 Crores in property** vs. **₹3.64 Crores in a 3.3% SWR financial portfolio** (freeing ₹1.82 Crores in capital).
  - Buy vs. Rent Engine: 20-year cash flow simulation demonstrating the compound wealth creation of investing the down payment and monthly EMI surplus into equity.
  - Post-Budget 2024 Section 112 Real Estate Tax: 12.5% without indexation (pre-July 2024 purchases retain grandfathered option of 20% with indexation).
  - Commercial Real Estate & Listed REITs (6.5%–7.8% distribution yield) as fractional liquid real estate exposure.
- **New CLI Tools in `fire_calculator.py`**:
  - `asset-compare`: Post-tax nominal and real return ranking across FDs, Arbitrage, Equity, Gold SGB, Gold ETF, Silver ETF, Real Estate, and REITs.
  - `real-estate-eval`: Detailed Buy vs. Rent calculator and capital requirement comparison.
- **Evals Updated**:
  - Added test cases `eval_13` (FD, Arbitrage, Gold, Silver) and `eval_14` (Real Estate Buy vs Rent).

## [1.2.0] - 2026-10-17

### Enhanced with core capabilities from `jaineejain/ArthMitra` for India investments:
- **The Protection-First Rule (Arth Protocol Invariant)**:
  - Strictly prohibits aggressive equity investing or SIP escalation before confirming a 6-month Emergency Shield and Pure Term Insurance (15x–20x annual income).
- **Indian F.I.R.E. Calculus**:
  - Compounding at **6.5% domestic inflation** and conservative **3.0%–3.3% SWR** (30x–33.3x future expenses).
  - Target corpus output in ₹ Crores with required monthly SIP gap calculator assuming 12% equity CAGR.
- **India Tax Optimizer (Old vs. New Regime)**:
  - Supports FY 2024-25 / FY 2025-26 statutory slabs with Section 87A rebate.
  - Standard deduction: ₹75,000 (New Regime) vs. ₹50,000 (Old Regime).
  - Accurate HRA exemption calculator: $\min(\text{HRA Received}, \text{Rent} - 10\%\text{ Basic}, 50\%/40\%\text{ Basic})$.
  - Section 80C, 80CCD(1B) NPS, 80D health insurance, and 24(b) home loan interest deductions.
- **Couple's Financial Optimization (Indian Context)**:
  - Strategic HRA claim: higher-slab earner pays rent for maximum marginal relief.
  - Joint home loan double-dip: ₹4L interest (24b) + ₹3L principal (80C) combined deductions.
- **Loan Prepayment Analyzer**:
  - Reducing-balance monthly compounding EMI simulator.
  - Calculates interest saved and tenure reduction from extra monthly payments or lump-sum prepayments.
- **Money Health Score (MHS)**:
  - 6-dimension weighted diagnostic (Emergency 20%, Insurance 25%, Debt/FOIR 15%, Investment 20%, Discipline 20%).
- **New CLI Subcommands in `fire_calculator.py`**:
  - `india-tax`: Compares Old vs New regime.
  - `india-fire`: Calculates Indian FIRE corpus, inflation compounding, and SIP gap.
  - `loan-prepay`: Simulates reducing-balance loan prepayment and interest saved.
  - `mhs`: Calculates 0–100 Money Health Score.
- **References Added**:
  - `references/india_investments_and_tax.md`
  - `references/financial_health_and_protection.md`
- **Evals Updated**:
  - Added 4 comprehensive Indian FIRE and financial health scenarios (`eval_cases.json`).

## [1.1.0] - 2026-10-17

### Enhanced with core principles from `SimonHaynes/claude_fire`:
- The April 2027 Inheritance Tax Inversion ("Pensions First" rule).
- Effective death tax calculation post-75 (52%/64%/67% on inherited pension vs 40% on ISA).
- The $r > 0.75m$ contribution law.
- First death & survivor financial shock modeling.
- GIA before ISA drawdown ordering.
- Strict "Compute, don't eyeball" advisory standards.

## [1.0.0] - 2026-10-17

### Added
- Complete UK F.I.R.E. advisory capability matrix across 8 core domains.
- Core references: `uk_tax_wrappers.md`, `pension_bridge_and_sorr.md`, `mortgage_vs_investing.md`, `household_optimization.md`.
- Deterministic Python CLI calculation engine.
- Structured evaluation test cases.
