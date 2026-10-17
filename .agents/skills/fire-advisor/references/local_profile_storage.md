# Local Client Profile Storage & Asset Management Reference

This reference establishes the **Private Local Storage Architecture** for client financial profiles within the **F.I.R.E. Advisor**.

---

## 1. Local Storage Invariant: Privacy & Zero Cloud Leakage

> [!IMPORTANT]
> **Complete Client Data Privacy**: All client financial profiles, asset balances, liabilities, and income figures are stored **exclusively in a local directory chosen by the user**. No data is ever transmitted to external servers, cloud databases, or third-party APIs.

### User-Specified Storage Locations
The user can specify their preferred local directory or file path at any time:
1. **Via CLI Argument**: `--storage-dir /path/to/my/profiles` or `--file /path/to/profile.json`
2. **Via Config File**: `.fire_advisor_config.json` containing `{"profiles_directory": "/path/to/custom/dir"}`
3. **Via Environment Variable**: `FIRE_PROFILES_DIR=/path/to/custom/dir`
4. **Default Location**: `./profiles/` inside the user's current project or workspace directory.

---

## 2. Standard Client Profile Schema (JSON)

Each client profile captures full balance sheet details, income, expenses, and protection parameters across both **UK** and **India / NRI** jurisdictions.

### Example: India / NRI Profile (`client_anita_india.json`)
```json
{
  "profile_name": "Anita_Bengaluru",
  "jurisdiction": "India",
  "client_info": {
    "age": 32,
    "target_retirement_age": 47,
    "monthly_expenses": 75000,
    "annual_income": 2400000,
    "tax_bracket": "30",
    "tax_regime": "New"
  },
  "assets": {
    "cash_and_emergency": [
      {"name": "SBI Savings & FD", "type": "fd", "amount": 600000, "rate": 0.0725},
      {"name": "Tata Arbitrage Fund", "type": "arbitrage", "amount": 400000, "rate": 0.07}
    ],
    "equities": [
      {"name": "UTI Nifty 50 Index Fund", "amount": 2500000, "expected_cagr": 0.12},
      {"name": "Parag Parikh Flexi Cap Fund", "amount": 1500000, "expected_cagr": 0.12}
    ],
    "pensions_and_retirement": [
      {"name": "EPF Balance", "amount": 1200000, "rate": 0.0825},
      {"name": "PPF", "amount": 500000, "rate": 0.071},
      {"name": "NPS Tier 1", "amount": 350000}
    ],
    "precious_metals": [
      {"name": "Sovereign Gold Bonds (SGB)", "amount": 450000},
      {"name": "Silver ETF", "amount": 100000}
    ],
    "real_estate": [
      {"name": "Primary 3BHK Apartment", "amount": 15000000, "is_primary": true},
      {"name": "Nexus Select REIT", "amount": 300000, "distribution_yield": 0.075}
    ],
    "digital_assets": [
      {"name": "Bitcoin (Cold Storage)", "amount": 400000, "cost_basis": 200000}
    ]
  },
  "liabilities": [
    {
      "name": "SBI Home Loan",
      "principal_outstanding": 4800000,
      "interest_rate": 0.0875,
      "remaining_tenure_years": 18,
      "monthly_emi": 43500
    }
  ],
  "protection": {
    "term_insurance_cover": 30000000,
    "has_health_insurance": true,
    "has_revolving_credit_card_debt": false
  }
}
```

### Example: UK Profile (`client_oliver_uk.json`)
```json
{
  "profile_name": "Oliver_London",
  "jurisdiction": "UK",
  "client_info": {
    "age": 42,
    "target_retirement_age": 52,
    "annual_spend": 45000,
    "gross_annual_income": 115000,
    "tax_bracket": "60_trap"
  },
  "assets": {
    "cash_and_emergency": [
      {"name": "Marcus Easy Access", "amount": 25000}
    ],
    "isas": [
      {"name": "Vanguard FTSE Global All Cap ISA", "amount": 190000}
    ],
    "pensions": [
      {"name": "SIPP (Interactive Investor)", "amount": 340000},
      {"name": "Workplace DC Pension", "amount": 160000}
    ],
    "gias": [
      {"name": "Taxable GIA", "amount": 35000}
    ],
    "digital_assets": [
      {"name": "Bitcoin", "amount": 15000}
    ],
    "real_estate": [
      {"name": "Main Residence", "amount": 600000, "is_primary": true}
    ]
  },
  "liabilities": [
    {
      "name": "Residential Mortgage",
      "principal_outstanding": 175000,
      "interest_rate": 0.045,
      "monthly_emi": 1100
    }
  ],
  "protection": {
    "term_insurance_cover": 1500000,
    "has_health_insurance": true,
    "has_revolving_credit_card_debt": false
  }
}
```

---

## 3. Profile Management CLI Commands

Users manage their local profiles with deterministic subcommands in [`fire_calculator.py`](file:///Users/Sumanth/Documents/Projects/FireAdvisor/.agents/skills/fire-advisor/scripts/fire_calculator.py):

```bash
# 1. Generate a blank template in your chosen directory
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-template \
  --jurisdiction india \
  --output /Users/Sumanth/Documents/MyFIREProfiles/anita.json

# 2. View/Inspect a profile stored in a custom local directory
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-show \
  --file /Users/Sumanth/Documents/MyFIREProfiles/anita.json

# 3. List all profiles in a custom local directory
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-list \
  --dir /Users/Sumanth/Documents/MyFIREProfiles/

# 4. Run full F.I.R.E. evaluation & diagnostic directly from a stored profile
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-eval \
  --file /Users/Sumanth/Documents/MyFIREProfiles/anita.json
```

---

## 4. Automatic Balance Sheet Diagnostics

When a profile is loaded or evaluated, the engine automatically:
1. **Tallies Liquid Financial Wealth**: Excludes primary illiquid residence.
2. **Calculates Total Net Worth**: Assets minus Liabilities.
3. **Calculates Asset Allocation %**: Cash, Equities, Pensions, Debt, Gold, Silver, Crypto, Real Estate.
4. **Calculates FIRE Readiness**: Current portfolio vs. inflation-adjusted FIRE Target corpus.
5. **Computes Money Health Score (MHS)**: Emergency coverage, FOIR %, protection gap, and savings rate.
