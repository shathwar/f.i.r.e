# Market Data Lineage & Authoritative Primary Sources

This reference establishes the institutional data sources, statutory benchmarks, and primary feeds used by the **F.I.R.E. Advisor**, delineating the difference between **live spot pricing** and **long-term expected compounding rates (CAGR)**.

---

## 1. Primary Benchmark Sources by Asset Class

| Asset Class | Authoritative Primary Source | Statutory / Institutional Role | Live Feed / Verification Ticker | Default Long-Term F.I.R.E. Parameter |
| :--- | :--- | :--- | :--- | :--- |
| **Currency (GBP/INR, USD/INR)** | **Reserve Bank of India (RBI)** & **Bank of England (BoE)** | Official Reference Rates published daily at 13:30 IST by FBIL (Financial Benchmark India Pvt Ltd). | `GBPINR=X`, `USDINR=X` (Yahoo Finance / Reuters / Bloomberg) | Compounding difference: ~3.0%–3.5% annual INR depreciation vs USD/GBP over 20+ years. |
| **Equity Indices (India)** | **National Stock Exchange (NSE)** & **BSE India** | **Nifty 50 Total Return Index (TRI)** (includes reinvested dividends) and **BSE Sensex TRI**. | `^NSEI` (Nifty 50), `^BSESN` (Sensex), `NIFTY_TRI` via AMFI | **11.5% – 12.5% nominal CAGR** (25-year historical Nifty 50 TRI CAGR is ~13.2%). |
| **Equity Indices (UK / US)** | **London Stock Exchange (LSE)** & **S&P Dow Jones Indices** | **FTSE 100 / FTSE All-Share Total Return** and **S&P 500 TRI**. | `^FTSE` (FTSE 100), `^GSPC` (S&P 500) | UK: **6.5% – 7.5% nominal**; US: **9.0% – 10.0% nominal** (real return ~4.5%–6.5%). |
| **Gold (India)** | **India Bullion and Jewellers Association (IBJA)** | **IBJA 24 Karat (999 purity) benchmark rate**. Used by the **RBI and Government of India** to fix Sovereign Gold Bond (SGB) issue prices and redemption values. | IBJA daily 12:00 & 17:00 rates; MCX Gold Futures (`MCX: GOLD`); `GOLDBEES.NS` | **9.0% – 10.5% nominal in INR** (reflects USD spot gold compounding @ 5-6% + ~3.5% INR currency depreciation). |
| **Silver (India)** | **IBJA** & **Multi Commodity Exchange (MCX)** | Official IBJA 999 silver closing price and MCX Silver 30kg contract spot benchmark. | MCX Silver (`MCX: SILVER`); `SILVERBEES.NS` | **10.0% – 12.0% nominal in INR** (cyclical industrial beta). |
| **Fixed Deposits (India)** | **Reserve Bank of India (RBI)** & **Tier-1 SCBs (SBI, HDFC, ICICI)** | RBI Policy Repo Rate (Monetary Policy Committee) + Retail Term Deposit (< ₹3 Cr) Card Rates. | State Bank of India (SBI) 1-yr to 3-yr retail term deposit interest schedule. | **6.75% – 7.50% nominal** (pre-tax). Yields **4.99% post-tax** in the 30% slab. |
| **Residential Real Estate (India)** | **National Housing Bank (NHB RESIDEX)** & **RBI Housing Price Index (HPI)** | Statutory quarterly price movement indices across 50 Indian cities. Commercial research from **Knight Frank India, Anarock, and JLL**. | NHB RESIDEX Market Price Index; Knight Frank India Real Estate Sentiment Index. | **Rental Yield: 2.0% – 2.8% gross (1.8% – 2.2% net)** in Tier-1 metros. Capital growth: ~5%–6%. |
| **Commercial Real Estate / REITs** | **Securities and Exchange Board of India (SEBI)** & Stock Exchanges | SEBI-regulated Listed REITs (Embassy Office Parks, Mindspace, Brookfield, Nexus Select Trust). | `EMBASSY.NS`, `MINDSPACE.NS`, `BIRET.NS`, `NXST.NS` | **6.5% – 7.8% distribution yield** + 3%–4% capital appreciation. |
| **Inflation (India & UK)** | **Ministry of Statistics & Programme Implementation (MoSPI - India)** & **ONS (UK)** | Consumer Price Index (CPI Combined) for India; CPIH / CPI for UK. | RBI MPC Inflation Projections; ONS UK CPI monthly bulletins. | India CPI: **6.0% – 6.5% long-term**; UK CPI: **2.0% – 2.5% long-term**. |

---

## 2. Spot Price vs. F.I.R.E. Modeling: The Fundamental Distinction

A quantitative retirement advisor makes a critical distinction:

1. **Spot Prices (Point-in-Time Net Worth)**:
   * Used for determining **today's starting capital** $NW_0$.
   * e.g., Gold spot ₹76,000/10g, Nifty 50 at 25,000, GBP/INR at 108.50.
   * *Client Input Contract*: The client inputs their actual portfolio values or property market value at today's prices.

2. **Long-Term CAGRs & Cyclical Spreads (Multi-Decade Decumulation)**:
   * Used for **30–40 year retirement projections, Monte Carlo simulations, and Safe Withdrawal Rates**.
   * Day-to-day volatility must never be mistaken for long-term expected returns. For instance, even if gold jumped 25% in a single year during geopolitical conflict, a prudent financial advisor models a conservative **9.0%–10.0% INR CAGR** over a 20-year horizon.
   * Fixed deposits must be modeled with real post-tax yield ($r_{\text{post-tax}} - \text{inflation} = -1.5\%$), not headline promotional rates.

---

## 3. How the Advisor Verifies & Overrides Market Data

The quantitative tools allow users and automated scripts to supply exact current rates or custom assumptions:

```bash
# Override mortgage / loan rate with client's exact bank card rate (e.g. 8.5% instead of default 8.75%)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py loan-prepay \
  --principal 5000000 --rate 8.50 --tenure 20

# Override real estate purchase price and exact current market rental quote
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py real-estate-eval \
  --price 18000000 --rent 42000 --loan-rate 0.085 --tenure 20

# Run asset comparison with customized inflation assumptions (e.g. 7.0% education/healthcare heavy)
python3 .agents/skills/fire-advisor/scripts/fire_calculator.py asset-compare \
  --tax-bracket 30 --inflation 0.070
```

---

## 4. Statutory & Audit Integrity
Whenever clients ask about market pricing or data lineage:
- **Cite the primary institutional source** (e.g. IBJA for gold, RBI for repo/FD context, NHB RESIDEX for property yields, NSE TRI for equity).
- **Explain the rationale behind the assumed CAGR** (why 12% for equity, why 9.5% for gold in INR, why 2.2% net for residential rent).
- **Never guess or use ungrounded figures**.
