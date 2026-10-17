# UK & India F.I.R.E. Advisor (Financial Independence, Retire Early)

A Senior Chartered Financial Planner (CFP®) and Quantitative F.I.R.E. advisory skill for the Antigravity agent system, customized for **both the UK and Indian (Bharat) & NRI financial landscapes**.

Combines the rigorous decumulation, IHT, and Monte Carlo planning frameworks from [`SimonHaynes/claude_fire`](https://github.com/SimonHaynes/claude_fire) with the Indian tax optimization, SIP compounding, loan prepayment, and Money Health Score (MHS) engines from [`jaineejain/ArthMitra`](https://github.com/jaineejain/ArthMitra).

---

## 🎯 Dual-Jurisdiction Capabilities

### 🇬🇧 UK F.I.R.E. Focus
* **FIRE Target & SWR**: Sizing portfolios with 3.25%–3.50% safe withdrawal rates.
* **Pre-57 Pension Bridge**: Funding early retirement before NMPA 57 using a 3-bucket ISA/cash architecture.
* **Tax Optimization & 60% Trap**: Reclaiming personal allowance between £100k–£125k via Salary Sacrifice/SIPP (+62% relief).
* **April 2027 IHT & Scenario-Based Decumulation**: Models multi-wrapper decumulation based on estate size, Nil-Rate Bands (£325k–£1,000,000), 100% Spousal Exemption on first death, retiree vs. heir tax brackets, and draining taxable GIAs before pensions.
* **First Death & Survivor Shock**: Modeling the loss of 1 personal allowance, 1 state pension, and DB pension halving.

### 🇮🇳 India (Bharat) & NRI F.I.R.E. Focus
* **India FIRE Calculus**: Compounding expenses at **6.5% inflation** with a conservative **3.0%–3.3% SWR**; outputs corpus targets in ₹ Crores and calculates monthly equity SIP gaps at 12% CAGR.
* **Tax Optimization (Versioned AY 2026-27 & CTC Distinction)**: Official guidance for AY 2026-27 (Union Budget 2025) with ₹12 Lakh Taxable Income Section 87A rebate threshold (zero tax up to ₹12.75L Gross Salary), statutory marginal relief, revised slabs up to ₹24L, and rigorous distinction between CTC, Gross Salary, and Taxable Income.
* **Couple's Optimization**: Strategic HRA claims by higher-earning spouse and joint home loan double-dipping (₹4L interest / ₹3L principal deductions).
* **Loan Prepayment vs. Equity SIP**: Reducing-balance monthly compounding EMI simulator; shows tenure reduction and lakhs saved in interest.
* **The Protection-First Rule**: Enforces the Arth Protocol—never prescribes aggressive equity SIPs without a 6-month Emergency Shield and 15x–20x Pure Term Life Insurance.
* **Money Health Score (MHS)**: 6-dimension diagnostic (0–100) assessing Emergency, Insurance, Debt/FOIR, Investment, and Savings discipline.
* **Fixed Deposits (FDs) vs. Arbitrage Funds**: Exposes the FD inflation trap (4.99% post-tax in 30% slab vs 6.5% inflation = -1.5% negative real return); positions Arbitrage Funds (12.5% LTCG) as the tax-efficient cash parking alternative.
* **Gold & Silver**: Sovereign Gold Bonds (SGB) with 2.5% coupon + 100% tax-free capital gains at RBI maturity vs. Gold/Silver ETFs (12.5% LTCG after 24m). Sizing: 5%–10% Gold, 2%–5% Silver.
* **Real Estate & Buy vs. Rent**: 2.0%–2.8% gross rental yields vs. financial portfolio SWR (saving ~₹1.8 Cr in required capital); 20-year Buy vs. Rent simulator; listed REITs (6.5%–7.8% yield); post-Budget 2024 Section 112 tax rules.
* **Digital Assets & Cryptocurrencies (UK & India)**:
  * 1%–5% asymmetric satellite sizing rule; never part of the core retirement floor or emergency fund.
  * UK: 18%/24% CGT above £3,000 exemption, HMRC pooling, lack of ISA/SIPP wrapping.
  * India: Flat 30% (+4% cess = 31.2%) tax under Section 115BBH, strict zero loss set-off, 1% TDS under Section 194S.
* **Local Client Profile Storage & Asset Management**:
  * 100% private, local storage on the user's filesystem in any directory they specify (`--dir`, `--file`, `FIRE_PROFILES_DIR`).
  * Automated balance sheet aggregator: liquid portfolio, illiquid primary residence, debt, net worth.
  * Automated asset allocation across all 7 asset classes (Cash, Equity, Pension, Gold, Silver, Crypto, Real Estate).
  * One-command FIRE readiness & Money Health Score evaluation (`profile-eval`).

---

## 📁 Skills Architecture in This Repository

This workspace contains two specialized, complementary financial advisory skills:

```text
.agents/skills/
├── fire-advisor/                   # Strategic F.I.R.E. Planning & Wealth Architecture
│   ├── SKILL.md                    # Primary advisory prompt, CFP persona & runbooks
│   ├── VERSION                     # 1.7.0
│   ├── CHANGELOG.md                # Semantic version changelog
│   ├── references/
│   │   ├── uk_tax_wrappers.md      # SIPP, Salary Sacrifice, 60% trap, April 2027 IHT & r > 0.75m law
│   │   ├── pension_bridge_and_sorr.md # Pre-57 bridge, multi-bucket design, 30% crash & care costs
│   │   ├── mortgage_vs_investing.md   # Mathematical models comparing mortgage paydown vs. investing
│   │   ├── household_optimization.md  # Spousal allowances, equalizing pots, survivor shock & transfers
│   │   ├── india_investments_and_tax.md # MFs, FDs, Gold, Silver, Real Estate, REITs, Old vs New, HRA
│   │   ├── crypto_and_digital_assets.md # Digital assets in F.I.R.E., UK HMRC CGT, India Sec 115BBH & 194S
│   │   ├── market_data_sources.md       # Primary statutory benchmarks, data lineage, spot vs CAGR
│   │   ├── local_profile_storage.md     # Private local JSON profile schema & storage runbook
│   │   └── financial_health_and_protection.md # Money Health Score (MHS), Arth Protocol & protection moats
│   ├── scripts/
│   │   └── fire_calculator.py      # Multi-jurisdiction CLI calculation engine (UK & India)
│   └── evals/
│       └── eval_cases.json         # Comprehensive evaluation suite (17 test scenarios)
│
└── equity-rotator/                 # Tactical Sector & Style Equity Rotation Engine
    ├── SKILL.md                    # Chief Investment Officer (CIO) persona & rotation contracts
    ├── VERSION                     # 1.0.0
    ├── CHANGELOG.md                # Semantic version changelog
    ├── references/
    │   ├── macro_regimes_and_business_cycle.md # 4-Quadrant macro model & sector sensitivity
    │   ├── evidence_indicators_and_sentiment.md # FII/DII flows, PCR, VIX, breadth & yield gaps
    │   └── rotation_playbooks.md   # Tactical sector runbooks & tax-sheltered execution (ISAs/BAFs)
    ├── scripts/
    │   └── rotation_engine.py      # Quantitative sector scoring & sentiment CLI engine
    └── evals/
        └── eval_cases.json         # Evaluation suite for market regime & rotation signals
```

---

## 🧮 Running the Multi-Jurisdiction Calculator CLI

### F.I.R.E. Advisory Calculations (`fire_calculator.py`)

```bash
# --- UK & GLOBAL CALCULATIONS ---

# 1. UK FIRE Target (£40k spend at 3.5% SWR)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py target --spend 40000 --swr 0.035

# 2. UK Pension Bridge (Retiring at 47, £45k spend to age 57)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py bridge --retire-age 47 --spend 45000

# 3. Post-April 2027 Effective Death Tax (Inherited Pension vs ISA on £500k pot)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py death-tax --pot 500000 --beneficiary-rate 0.40

# 4. First Death Survivor Shock (£45,000 couple spend, £10,000 DB pension)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py survivor --spend 45000 --db 10000

# 5. UK Crypto CGT Calculator (£15,000 gains, £4,000 losses, Higher-rate taxpayer)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py crypto-tax \
  --jurisdiction uk --gain 15000 --loss 4000 --bracket higher


# --- INDIA (BHARAT) & NRI CALCULATIONS ---

# 6. India Tax Regime Comparator (CTC ₹20 Lakhs, HRA, 80C, 80CCD, 80D)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py india-tax \
  --gross 2000000 --basic 1000000 --hra 400000 --rent 360000 --metro \
  --sec-80c 150000 --sec-80ccd 50000 --sec-80d 25000

# 7. India FIRE Corpus & Monthly SIP Gap (Age 32 -> 47, ₹75k/mo spend, ₹25L portfolio)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py india-fire \
  --age 32 --retire-age 47 --monthly-spend 75000 --portfolio 2500000

# 8. Reducing-Balance Home Loan Prepayment (₹50 Lakhs @ 8.75% for 20 yrs, extra ₹10k/mo)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py loan-prepay \
  --principal 5000000 --rate 8.75 --tenure 20 --extra-monthly 10000

# 9. Money Health Score Diagnostic (0-100)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py mhs \
  --income 150000 --expenses 60000 --emi 35000 --liquid 600000 --term-cover 25000000 --age 32

# 10. India Asset Class Post-Tax Real Return Comparison (30% slab vs 6.5% inflation)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py asset-compare --tax-bracket 30

# 11. Buy vs. Rent & Real Estate Capital Efficiency (₹1.5 Cr property vs ₹35k/mo rent)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py real-estate-eval --price 15000000 --rent 35000

# 12. India VDA Crypto Tax Trap (₹10L profit on BTC, ₹4L loss on ETH, 1% TDS)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py crypto-tax \
  --jurisdiction india --gain 1000000 --loss 400000 --transfer-value 1000000

# 13. Cross-Border UK-India DTAA, FTC & Currency PPP
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py cross-border \
  --uk-pension 40000 --india-nro 500000 --rate 105 --has-trc

# --- LOCAL CLIENT PROFILE STORAGE & ASSET MANAGEMENT ---

# 14. Generate blank profile template in your chosen directory
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-template \
  --jurisdiction india --output /Users/Sumanth/Documents/MyFIREProfiles/anita.json

# 15. List profiles in your chosen directory
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-list \
  --dir /Users/Sumanth/Documents/MyFIREProfiles/

# 16. Run full F.I.R.E. evaluation & Money Health Score on a stored profile
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-eval \
  --file /Users/Sumanth/Documents/MyFIREProfiles/anita.json
```

---

### 🧪 Independent Mathematical Proof Test Suite

The mathematical models and statutory tax rules are independently proved by an extensive automated test suite (`tests/test_independent_proofs.py`). Every calculation—Indian tax slabs, Section 87A marginal relief cliff edges, SIP sinking fund equations, UK pension taper, reducing-balance loan amortization, and cross-border FTC ceilings—is computed from closed-form first principles and asserted down to the exact Rupee/Penny:

```bash
# Execute independent mathematical proofs and boundary regressions
python3 -m unittest discover tests
```


---

### Tactical Equity Rotation Calculations (`rotation_engine.py`)

```bash
# 1. Full 5-Factor Sector Rotation Analysis (India)
python3 .agents/skills/equity-rotator/scripts/rotation_engine.py analyze \
  --market india --growth accelerating --inflation falling --fii-long-short 0.16 --pcr 1.10

# 2. Evaluate Macro Regime & Business Cycle Sector Mapping
python3 .agents/skills/equity-rotator/scripts/rotation_engine.py regime \
  --growth accelerating --inflation falling

# 3. Smart Money Contrarian Sentiment Diagnostic (FII Long/Short, PCR, VIX)
python3 .agents/skills/equity-rotator/scripts/rotation_engine.py sentiment-check \
  --fii-long-short 0.15 --pcr 1.45 --vix 16.2

# 4. Smallcap Valuation Froth & Yield Gap Check
python3 .agents/skills/equity-rotator/scripts/rotation_engine.py spread-check \
  --small-large-pe 1.28 --breadth-50dma 42.0 --yield-gap 2.70
```
