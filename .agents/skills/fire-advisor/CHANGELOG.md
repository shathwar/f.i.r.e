# Changelog - UK & India F.I.R.E. Advisor Skill

## [1.5.0] - 2026-10-17

### Added Local Client Profile Storage & Private Asset Management:
- **Strict Privacy & Zero Cloud Leakage Invariant**:
  - All client asset balances, liabilities, income, and personal goals are stored exclusively on the user's local filesystem in any location they specify.
- **Unified Multi-Jurisdiction JSON Asset Schema**:
  - Encapsulates Cash & Emergency (FDs, Arbitrage, Savings), Equities (Index funds, Flexicap, ISAs, GIAs), Pensions (SIPP, DC, EPF, PPF, NPS), Precious Metals (Gold SGB, Silver), Real Estate (Primary vs. REITs/Investment), Digital Assets (Bitcoin, ETH), Liabilities (Mortgages, Home loans), and Protection (Term life, Health insurance).
- **Automated Profile Evaluation Engine (`profile-eval`)**:
  - Tallies liquid financial portfolio vs. illiquid primary residence.
  - Automatically computes asset allocation percentages across all 7 asset classes.
  - Projects portfolio compounding vs. inflation-adjusted FIRE Target and computes required monthly savings/SIP gap.
  - Computes comprehensive 0–100 Money Health Score (MHS) with Protection-First rule validation.
- **New CLI Subcommands in `fire_calculator.py`**:
  - `profile-template`: Generates a blank UK or Indian profile template in the user's chosen local directory/file path.
  - `profile-list`: Lists all profiles in a user-specified directory.
  - `profile-show`: Inspects a local profile JSON.
  - `profile-eval`: Directly evaluates a stored profile for FIRE readiness and financial health.
- **Documentation & References**:
  - Added `references/local_profile_storage.md`.
  - Added test case `eval_17` to `eval_cases.json`.

## [1.4.0] - 2026-10-17

### Added Digital Assets & Cryptocurrencies (Bitcoin, Ethereum):
- **Fiduciary F.I.R.E. Principles for Digital Assets**:
  - The **1%–5% Asymmetric Satellite Sizing Rule**: Never backs the core retirement living floor or the emergency shield.
  - Volatility & Sequence of Returns Risk (SORR) stress-testing: Selling crypto during 50%–80% cyclical drawdowns to fund living costs leads to irreversible capital failure.
  - "House Money" systematic rebalancing into tax-free wrappers (ISAs / Arbitrage Funds).
- **UK Cryptoasset Tax Framework (HMRC Manual CRYPTO20000)**:
  - Subject to Capital Gains Tax (CGT) at **18% (basic) / 24% (higher/additional)** above the £3,000 exemption.
  - Share pooling rules (Same-day, 30-day Bed & Breakfast, Section 104 general pool).
  - Staking / mining rewards taxed as Miscellaneous Income at marginal rates.
  - Ineligibility for ISA or SIPP wrappers (held in taxable GIAs or cold storage).
- **Indian Virtual Digital Assets (VDA) Tax Framework (Section 115BBH & 194S)**:
  - **Flat 30% Tax (+4% cess = 31.2% effective)** on all gross gains, regardless of income slab or holding period.
  - **The Strict Zero Loss Set-Off Rule**: Section 115BBH(2)(b) strictly prohibits setting off losses in one coin against gains in another coin.
  - **Zero Loss Carry Forward & Zero Deductions**: No deductions for electricity, exchange commissions, or software.
  - **1% TDS under Section 194S** on transfers > ₹50,000 to establish an unbroken PAN audit trail.
- **New CLI Subcommand in `fire_calculator.py`**:
  - `crypto-tax`: Computes exact tax, real net profit, TDS, and effective tax rates for both UK and Indian jurisdictions.
- **Reference & Data Lineage**:
  - Added `references/crypto_and_digital_assets.md`.
  - Updated `references/market_data_sources.md` with CoinGecko, CoinMarketCap, CME, and FIU-IND domestic exchanges.
- **Evals Updated**:
  - Added test cases `eval_15` (India VDA tax trap) and `eval_16` (UK crypto CGT & portfolio sizing).

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
