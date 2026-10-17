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

## 2. Standard Client Profile Schema with Source Tracking

Each client profile captures full balance sheet details, income, expenses, protection parameters, and **explicit institution/source tracking metadata** for every asset and liability.

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
      {
        "name": "SBI Savings & FD",
        "type": "fd",
        "amount": 600000,
        "rate": 0.0725,
        "source": "State Bank of India (SBI YONO)",
        "account_id": "FD-984729184",
        "portal_url": "https://retail.onlinesbi.sbi"
      },
      {
        "name": "Tata Arbitrage Fund",
        "type": "arbitrage",
        "amount": 400000,
        "rate": 0.07,
        "source": "Zerodha Coin / CAMS",
        "folio_number": "1849204/92",
        "portal_url": "https://coin.zerodha.com"
      }
    ],
    "equities": [
      {
        "name": "UTI Nifty 50 Index Fund",
        "amount": 2500000,
        "expected_cagr": 0.12,
        "source": "Kuvera / CAMS",
        "folio_number": "UTI-8924719",
        "isin": "INF209K01167"
      },
      {
        "name": "Parag Parikh Flexi Cap Fund",
        "amount": 1500000,
        "expected_cagr": 0.12,
        "source": "Groww / KFintech",
        "folio_number": "PPFAS-559102",
        "isin": "INF879O01019"
      }
    ],
    "pensions_and_retirement": [
      {
        "name": "EPF Balance",
        "amount": 1200000,
        "rate": 0.0825,
        "source": "EPFO Member Portal",
        "uan": "100984721940",
        "portal_url": "https://unifiedportal-mem.epfindia.gov.in"
      },
      {
        "name": "PPF",
        "amount": 500000,
        "rate": 0.071,
        "source": "SBI Koramangala Branch",
        "account_id": "PPF-309482109",
        "portal_url": "https://retail.onlinesbi.sbi"
      },
      {
        "name": "NPS Tier 1",
        "amount": 350000,
        "source": "Protean CRA (NSDL)",
        "pran": "110098472109",
        "portal_url": "https://cra-nsdl.com"
      }
    ],
    "precious_metals": [
      {
        "name": "Sovereign Gold Bonds (SGB)",
        "amount": 450000,
        "source": "RBI Retail Direct / Zerodha Demat",
        "isin_or_certificate": "IN0020200270 (SGB 2028 Series)",
        "portal_url": "https://rbiretaildirect.org.in"
      },
      {
        "name": "Silver ETF",
        "amount": 100000,
        "source": "Zerodha Kite",
        "ticker": "SILVERBEES.NS"
      }
    ],
    "real_estate": [
      {
        "name": "Primary 3BHK Apartment",
        "amount": 15000000,
        "is_primary": true,
        "source": "Sub-Registrar Office Indiranagar / Title Deed",
        "property_id": "BBMP Khata #8921/42A"
      },
      {
        "name": "Nexus Select REIT",
        "amount": 300000,
        "distribution_yield": 0.075,
        "source": "Zerodha Demat",
        "ticker": "NXST.NS"
      }
    ],
    "digital_assets": [
      {
        "name": "Bitcoin (Cold Storage)",
        "amount": 400000,
        "cost_basis": 200000,
        "source": "Ledger Nano X Hardware Wallet (Cold Storage)",
        "tracking_label": "HODL Vault 1"
      }
    ]
  },
  "liabilities": [
    {
      "name": "SBI Home Loan",
      "principal_outstanding": 4800000,
      "interest_rate": 0.0875,
      "remaining_tenure_years": 18,
      "monthly_emi": 43500,
      "source": "State Bank of India Home Finance",
      "loan_account_id": "HL-9982341209"
    }
  ],
  "protection": {
    "term_insurance_cover": 30000000,
    "has_health_insurance": true,
    "has_revolving_credit_card_debt": false,
    "term_insurance_source": "HDFC Life Click2Protect (Policy #9847120)",
    "health_insurance_source": "Care Health Supreme (Policy #CH-389102)"
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
      {
        "name": "Marcus Easy Access",
        "amount": 25000,
        "source": "Marcus by Goldman Sachs",
        "account_id": "MC-8849201"
      }
    ],
    "isas": [
      {
        "name": "Vanguard FTSE Global All Cap ISA",
        "amount": 190000,
        "source": "Vanguard Investor UK",
        "account_id": "VG-100984",
        "isin": "GB00BD3RZ582"
      }
    ],
    "pensions": [
      {
        "name": "SIPP (Interactive Investor)",
        "amount": 340000,
        "source": "Interactive Investor (ii)",
        "account_id": "SIPP-ii-94821"
      },
      {
        "name": "Workplace DC Pension",
        "amount": 160000,
        "source": "Aviva MyWorkplace",
        "policy_id": "AV-489201"
      }
    ],
    "gias": [
      {
        "name": "Taxable GIA",
        "amount": 35000,
        "source": "Hargreaves Lansdown",
        "account_id": "HL-GIA-3910"
      }
    ],
    "digital_assets": [
      {
        "name": "Bitcoin",
        "amount": 15000,
        "source": "Trezor Safe 3 Hardware Wallet"
      }
    ],
    "real_estate": [
      {
        "name": "Main Residence",
        "amount": 600000,
        "is_primary": true,
        "source": "HM Land Registry Title Deed",
        "title_number": "NGL849210"
      }
    ]
  },
  "liabilities": [
    {
      "name": "Residential Mortgage",
      "principal_outstanding": 175000,
      "interest_rate": 0.045,
      "monthly_emi": 1100,
      "source": "NatWest Mortgage Services",
      "mortgage_account_id": "NW-MTG-88912"
    }
  ],
  "protection": {
    "term_insurance_cover": 1500000,
    "has_health_insurance": true,
    "has_revolving_credit_card_debt": false,
    "term_insurance_source": "Legal & General Life (Policy #LG-489201)",
    "health_insurance_source": "Bupa Corporate Scheme"
  }
}
```

---

## 3. Profile Management CLI Commands

Users manage their local profiles with deterministic subcommands in [`scripts/fire_calculator.py`](../scripts/fire_calculator.py):

```bash
# 1. Generate a blank template in your chosen directory
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-template \
  --jurisdiction india \
  --output ./profiles/anita.json

# 2. View/Inspect a profile stored in a custom local directory
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-show \
  --file ./profiles/anita.json

# 3. List all profiles in a custom local directory
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-list \
  --dir ./profiles/

# 4. Run full F.I.R.E. evaluation & diagnostic directly from a stored profile
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py profile-eval \
  --file ./profiles/anita.json
```

---

## 4. Automatic Balance Sheet Diagnostics

When a profile is loaded or evaluated, the engine automatically:
1. **Tallies Liquid Financial Wealth**: Excludes primary illiquid residence.
2. **Calculates Total Net Worth**: Assets minus Liabilities.
3. **Calculates Asset Allocation %**: Cash, Equities, Pensions, Debt, Gold, Silver, Crypto, Real Estate.
4. **Calculates FIRE Readiness**: Current portfolio vs. inflation-adjusted FIRE Target corpus.
5. **Computes Money Health Score (MHS)**: Emergency coverage, FOIR %, protection gap, and savings rate.
