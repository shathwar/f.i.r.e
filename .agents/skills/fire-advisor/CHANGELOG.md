# Changelog - UK & India F.I.R.E. Advisor Skill

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
