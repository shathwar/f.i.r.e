#!/usr/bin/env python3
"""
Tactical Equity Rotation Engine
Quantitative Sector Allocation, Sentiment & Macro Regime Diagnostic Tool
Multi-Market: India (NSE Sectoral Indices) & UK/Global (FTSE/MSCI Sectors)

Evaluates:
  1. Macroeconomic Business Cycle Regime (4-Quadrant Model)
  2. Smart Money Institutional Positioning (FII Long/Short Ratio, PCR)
  3. Market Breadth & Participation (Percent stocks > 50-DMA)
  4. Valuation Spreads & Yield Gaps (Smallcap/Largecap PE, Equity Risk Premium)
  5. Pre-Emptive Rotation Recommendations (3 to 5 days ahead of consensus)
"""

import argparse
import json
import sys
from typing import Dict, Any, List


# ==============================================================================
# MACRO REGIME DIAGNOSTIC
# ==============================================================================

def detect_macro_regime(growth: str = "accelerating", inflation: str = "falling") -> Dict[str, Any]:
    """Detects macroeconomic cycle quadrant and maps primary sector tilts."""
    growth = growth.lower().strip()
    inflation = inflation.lower().strip()

    if growth == "accelerating" and inflation == "falling":
        quadrant = "Quadrant 1: Early Cycle (Reflation / Recovery)"
        characteristics = "Growth accelerating with low or falling interest rates and accommodative central banks."
        overweight_india = ["Nifty Bank / Financial Services", "Nifty Auto & Consumer Discretionary", "Nifty IT (if US tech bottoms)"]
        underweight_india = ["Nifty FMCG (Staples)", "Nifty Pharma"]
        overweight_global = ["Global Technology / Discretionary", "Financials", "Industrials"]
        underweight_global = ["Consumer Staples", "Utilities"]
        strategy = "High beta, cyclical expansion, credit growth beneficiaries."

    elif growth == "accelerating" and inflation == "rising":
        quadrant = "Quadrant 2: Mid Cycle (Robust Expansion)"
        characteristics = "Economic growth robust, capacity utilization high (>75%), inflation firming, policy rates neutral."
        overweight_india = ["Nifty Capital Goods / Industrials", "Nifty Infra & Manufacturing", "Nifty Auto", "Nifty Metal"]
        underweight_india = ["Nifty IT (margin pressure)", "Defensives"]
        overweight_global = ["Industrials & Machinery", "Energy", "Materials / Miners"]
        underweight_global = ["Long-duration tech", "Utilities"]
        strategy = "Capex plays, order-book compounding, domestic industrial investment."

    elif growth == "decelerating" and inflation == "rising":
        quadrant = "Quadrant 3: Late Cycle (Stagflationary Pressure)"
        characteristics = "Growth peaking and slowing; sticky inflation; central bank rates tight."
        overweight_india = ["Nifty Energy / Oil & Gas", "Nifty FMCG", "Nifty Pharma & Healthcare", "Gold SGB / Arbitrage"]
        underweight_india = ["Nifty Metal (demand cliff)", "High-debt Real Estate", "Small-Caps"]
        overweight_global = ["Energy & Commodities", "Healthcare", "Consumer Staples", "Cash equivalents"]
        underweight_global = ["High-beta Cyclicals", "Discretionary Retail"]
        strategy = "Capital preservation, pricing power, balance sheet quality, cash-generative value."

    else: # decelerating and falling
        quadrant = "Quadrant 4: Recession / Contraction"
        characteristics = "Economic activity contracting, yield curve normalizing, central banks cutting rates."
        overweight_india = ["Nifty Pharma", "Nifty FMCG (Rural staples)", "Sovereign Gold Bonds (SGB)", "Arbitrage Funds"]
        underweight_india = ["Nifty Bank (credit cost fears)", "Nifty Auto", "Metals & Real Estate"]
        overweight_global = ["Healthcare", "Utilities", "Long-term Sovereign Bonds"]
        underweight_global = ["Banks / Financials", "Automotive", "High-yield Credit"]
        strategy = "Pure defense, minimum volatility, high dividend yield, safe havens."

    return {
        "macro_quadrant": quadrant,
        "growth_vector": growth,
        "inflation_vector": inflation,
        "regime_characteristics": characteristics,
        "india_sector_recommendations": {
            "overweight": overweight_india,
            "underweight": underweight_india
        },
        "global_sector_recommendations": {
            "overweight": overweight_global,
            "underweight": underweight_global
        },
        "tactical_strategy_summary": strategy
    }


# ==============================================================================
# SENTIMENT & POSITIONING DIAGNOSTIC
# ==============================================================================

def analyze_sentiment_and_positioning(fii_long_short: float = 0.45, pcr: float = 1.0,
                                      vix: float = 14.5) -> Dict[str, Any]:
    """
    Evaluates institutional derivative sentiment indicators:
    - FII Index Futures Long/Short ratio (Extreme < 0.20 or > 0.75)
    - Put-Call Ratio (PCR)
    - Volatility Index (VIX)
    """
    signals = []
    regime_bias = "Neutral / Equilibrium"
    contrarian_action = "Maintain disciplined trend-following allocations."

    # FII Positioning
    if fii_long_short <= 0.18:
        fii_status = f"Extreme Oversold ({fii_long_short*100:.1f}% Longs)"
        signals.append("FII short positioning is historically crowded. High probability of violent short squeeze within 2 to 5 trading sessions.")
        regime_bias = "Bullish Contrarian (Near-term Squeeze)"
        contrarian_action = "Front-run short covering: Allocate tactically to high-beta Banking and beaten-down Large-caps."
    elif fii_long_short >= 0.75:
        fii_status = f"Extreme Overbought ({fii_long_short*100:.1f}% Longs)"
        signals.append("FII long positioning is overcrowded. Vulnerable to sharp liquidation on minor negative news.")
        regime_bias = "Bearish Contrarian (Exhaustion Risk)"
        contrarian_action = "Trim cyclical beta; rotate profits into FMCG, Pharma, or Arbitrage funds."
    else:
        fii_status = f"Neutral / Healthy Range ({fii_long_short*100:.1f}% Longs)"

    # PCR
    if pcr <= 0.70:
        pcr_status = f"Complacent / Call-heavy ({pcr:.2f})"
        signals.append("Excessive retail call buying without downside put protection. Market vulnerable to surprise dip.")
    elif pcr >= 1.40:
        pcr_status = f"Panicked / Put-heavy ({pcr:.2f})"
        signals.append("Heavy put writing / panic hedging. Indicates strong near-term institutional support floor.")
        if regime_bias == "Neutral / Equilibrium":
            regime_bias = "Bullish Contrarian (Support Established)"
    else:
        pcr_status = f"Equilibrium ({pcr:.2f})"

    # VIX
    if vix < 12.0:
        vix_status = f"Extreme Complacency ({vix:.1f})"
        signals.append("Implied volatility is subdued; options are cheap. Ideal window to buy defensive put protection or rotate into low-beta.")
    elif vix > 20.0:
        vix_status = f"Elevated Stress ({vix:.1f})"
        signals.append("Market pricing in high uncertainty. Avoid illiquid small-caps; stay with liquid large-caps and defensives.")
    else:
        vix_status = f"Normal Trend Volatility ({vix:.1f})"

    return {
        "institutional_sentiment_bias": regime_bias,
        "fii_index_futures_status": fii_status,
        "put_call_ratio_status": pcr_status,
        "volatility_status": vix_status,
        "actionable_contrarian_recommendation": contrarian_action,
        "evidence_signals": signals
    }


# ==============================================================================
# VALUATION SPREAD & BREADTH DIAGNOSTIC
# ==============================================================================

def analyze_valuation_and_breadth(smallcap_largecap_pe_ratio: float = 1.05,
                                  stocks_above_50dma_pct: float = 55.0,
                                  yield_gap: float = 2.40) -> Dict[str, Any]:
    """
    Evaluates valuation spreads and market breadth:
    - Smallcap vs. Largecap PE multiple ratio (> 1.25 indicates danger/froth)
    - Breadth (% stocks above 50-DMA; divergence warning if benchmark makes ATH but breadth < 45%)
    - Yield Gap (10Y G-Sec yield minus Earnings Yield)
    """
    alerts = []
    style_tilt = "Neutral Core Allocation"

    if smallcap_largecap_pe_ratio > 1.25:
        alerts.append("CRITICAL FROTH: Smallcap PE exceeds Largecap PE by >25%. Historical precedent dictates multi-month underperformance.")
        style_tilt = "De-Froth: Trim Small-Caps by 25%-35% and rotate into Nifty 50 / Large-Cap Quality."
    elif smallcap_largecap_pe_ratio < 0.85:
        alerts.append("ATTRACTIVE VALUATION: Smallcaps trade at a healthy discount to Largecaps.")
        style_tilt = "Selective Small/Mid-Cap Accumulation in high-ROE businesses."

    if stocks_above_50dma_pct < 45.0:
        alerts.append("BREADTH DIVERGENCE: Less than 45% of stocks are above their 50-DMA. Rally is narrow and driven by mega-caps.")
    elif stocks_above_50dma_pct > 75.0:
        alerts.append("BROAD PARTICIPATION: Strong market breadth (>75% above 50-DMA). Healthy secular advance.")

    if yield_gap > 2.65:
        alerts.append(f"ELEVATED YIELD GAP ({yield_gap:.2f}%): Equities are expensive compared to risk-free sovereign debt. Tighten risk.")
    elif yield_gap < 1.80:
        alerts.append(f"ATTRACTIVE YIELD GAP ({yield_gap:.2f}%): Equities offer compelling equity risk premium over bonds.")

    return {
        "style_rotation_recommendation": style_tilt,
        "smallcap_to_largecap_pe_ratio": smallcap_largecap_pe_ratio,
        "stocks_above_50dma_percent": stocks_above_50dma_pct,
        "yield_gap_percent": yield_gap,
        "diagnostic_alerts": alerts
    }


# ==============================================================================
# FULL SECTOR ROTATION COMPOSITE SCORER
# ==============================================================================

def run_composite_rotation_analysis(growth: str = "accelerating",
                                    inflation: str = "falling",
                                    fii_long_short: float = 0.45,
                                    pcr: float = 1.0,
                                    vix: float = 14.5,
                                    small_large_pe: float = 1.05,
                                    breadth_50dma: float = 55.0,
                                    yield_gap: float = 2.40,
                                    market: str = "india") -> Dict[str, Any]:
    """Executes a 5-factor quantitative sector rotation synthesis."""
    macro = detect_macro_regime(growth, inflation)
    sentiment = analyze_sentiment_and_positioning(fii_long_short, pcr, vix)
    spread = analyze_valuation_and_breadth(small_large_pe, breadth_50dma, yield_gap)

    # Sector Composite Scoring (1 to 10 scale)
    if market.lower() in ["india", "bharat"]:
        sectors = {
            "Nifty Bank": {"score": 7.5, "tilt": "Neutral / Accumulate", "catalyst": "Credit growth 13-15%, stable asset quality, low NPA provisions."},
            "Nifty IT": {"score": 6.5, "tilt": "Neutral", "catalyst": "USD/INR tailwind offset by slow US discretionary spend."},
            "Nifty Auto": {"score": 8.0, "tilt": "Overweight (+5%)", "catalyst": "Strong premiumization, rural demand recovery, EV expansion."},
            "Nifty FMCG": {"score": 5.0, "tilt": "Underweight (-5%)", "catalyst": "High valuations; rotation into cyclicals during early/mid cycle."},
            "Nifty Pharma": {"score": 6.5, "tilt": "Neutral / Defensive Hedge", "catalyst": "US FDA approvals steady, domestic formulations growing 9-10%."},
            "Nifty Metal": {"score": 7.0, "tilt": "Tactical Overweight (+3%)", "catalyst": "China stimulus expectation and domestic infrastructure demand."},
            "Nifty Infra / Capital Goods": {"score": 8.5, "tilt": "Overweight (+7%)", "catalyst": "Multi-year private corporate capex cycle, capacity utilization > 75%."}
        }
        tax_wrapper_advice = "Execute sector rotations via Dynamic Asset Allocation or Multi-Asset Funds to bypass the 20% STCG / 12.5% LTCG friction."
    else:
        sectors = {
            "Global Technology / Nasdaq": {"score": 7.5, "tilt": "Overweight (+5%)", "catalyst": "AI infrastructure spend, rate cut cycle tailwind."},
            "UK Financials (FTSE)": {"score": 7.0, "tilt": "Neutral / Overweight", "catalyst": "Attractive dividend yields (5-6%) and low price-to-book valuations."},
            "Healthcare / Pharmaceuticals": {"score": 6.5, "tilt": "Neutral / Quality Core", "catalyst": "Defensive earnings floor during late-cycle volatility."},
            "Energy & Basic Materials": {"score": 6.0, "tilt": "Neutral", "catalyst": "Commodity price stabilization; robust free cash flow yields."},
            "Consumer Discretionary": {"score": 7.0, "tilt": "Tactical Overweight (+4%)", "catalyst": "Real wage growth recovery in UK and US."}
        }
        tax_wrapper_advice = "Execute all tactical rotations inside your £20k/year Stocks & Shares ISA to enjoy 100% tax-free capital gains and dividends."

    # Adjust scores based on contrarian sentiment & breadth
    if fii_long_short <= 0.20:
        if "Nifty Bank" in sectors:
            sectors["Nifty Bank"]["score"] += 1.5
            sectors["Nifty Bank"]["tilt"] = "Strong Overweight (+8%) [Short Squeeze Pre-Emption]"
    elif fii_long_short >= 0.75:
        if "Nifty FMCG" in sectors:
            sectors["Nifty FMCG"]["score"] += 1.5
            sectors["Nifty FMCG"]["tilt"] = "Defensive Safe Haven Overweight (+6%)"
        if "Nifty Bank" in sectors:
            sectors["Nifty Bank"]["tilt"] = "Trim / Take Profit (-5%)"

    if small_large_pe > 1.25:
        smallcap_alert = "MANDATORY ACTION: Trim Smallcap funds by 25%-35% into Largecap / Flexicap funds due to extreme valuation froth."
    else:
        smallcap_alert = "Smallcap valuation spread is within acceptable historical bounds."

    return {
        "market": market.upper(),
        "macro_regime": macro["macro_quadrant"],
        "sentiment_posture": sentiment["institutional_sentiment_bias"],
        "leading_rotation_triggers (3-5 days ahead)": [
            f"FII Index Futures Long/Short at {fii_long_short*100:.1f}% ({sentiment['fii_index_futures_status']})",
            f"Put-Call Ratio at {pcr:.2f} ({sentiment['put_call_ratio_status']})",
            f"Market Breadth: {breadth_50dma:.1f}% of constituent stocks above 50-DMA",
            f"Smallcap-to-Largecap PE ratio at {small_large_pe:.2f}"
        ],
        "sector_allocation_scorecard": sectors,
        "style_and_market_cap_tilt": smallcap_alert,
        "invalidation_criteria": [
            "RBI or US Federal Reserve delivers an unscheduled hawkish policy surprise.",
            "Crude oil spikes > $95/barrel, impairing Indian current account deficit.",
            "Market breadth drops below 35% with sustained FII institutional cash outflow > ₹3,000 Cr/day."
        ],
        "tax_smart_execution_strategy": tax_wrapper_advice
    }


# ==============================================================================
# MAIN CLI DISPATCHER
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Tactical Equity Rotation & Sentiment Engine")
    subparsers = parser.add_subparsers(dest="command", help="Rotations")

    # Analyze
    p_ana = subparsers.add_parser("analyze", help="Run full 5-factor composite equity rotation analysis")
    p_ana.add_argument("--market", type=str, default="india", choices=["india", "uk", "global"], help="Target market")
    p_ana.add_argument("--growth", type=str, default="accelerating", choices=["accelerating", "decelerating"], help="GDP / business growth trend")
    p_ana.add_argument("--inflation", type=str, default="falling", choices=["rising", "falling"], help="Inflation and interest rate trend")
    p_ana.add_argument("--fii-long-short", type=float, default=0.45, help="FII Index Futures Long/Short ratio (0.0 to 1.0)")
    p_ana.add_argument("--pcr", type=float, default=1.0, help="Options Put-Call Ratio (OI)")
    p_ana.add_argument("--vix", type=float, default=14.5, help="Volatility Index level")
    p_ana.add_argument("--small-large-pe", type=float, default=1.05, help="Smallcap to Largecap PE ratio")
    p_ana.add_argument("--breadth-50dma", type=float, default=55.0, help="Percent of stocks above 50-DMA")
    p_ana.add_argument("--yield-gap", type=float, default=2.40, help="10Y G-Sec yield minus Earnings Yield (percent)")

    # Regime
    p_reg = subparsers.add_parser("regime", help="Evaluate macroeconomic regime and sector tilts")
    p_reg.add_argument("--growth", type=str, default="accelerating", choices=["accelerating", "decelerating"])
    p_reg.add_argument("--inflation", type=str, default="falling", choices=["rising", "falling"])

    # Sentiment Check
    p_sent = subparsers.add_parser("sentiment-check", help="Evaluate contrarian smart money positioning")
    p_sent.add_argument("--fii-long-short", type=float, default=0.45, help="FII Long/Short ratio")
    p_sent.add_argument("--pcr", type=float, default=1.0, help="Put-Call Ratio")
    p_sent.add_argument("--vix", type=float, default=14.5, help="VIX level")

    # Spread Check
    p_spread = subparsers.add_parser("spread-check", help="Evaluate Smallcap froth and Yield Gap")
    p_spread.add_argument("--small-large-pe", type=float, default=1.05, help="Smallcap/Largecap PE ratio")
    p_spread.add_argument("--breadth-50dma", type=float, default=55.0, help="Percent stocks > 50-DMA")
    p_spread.add_argument("--yield-gap", type=float, default=2.40, help="Yield Gap")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "analyze":
        res = run_composite_rotation_analysis(
            growth=args.growth,
            inflation=args.inflation,
            fii_long_short=args.fii_long_short,
            pcr=args.pcr,
            vix=args.vix,
            small_large_pe=args.small_large_pe,
            breadth_50dma=args.breadth_50dma,
            yield_gap=args.yield_gap,
            market=args.market
        )
    elif args.command == "regime":
        res = detect_macro_regime(args.growth, args.inflation)
    elif args.command == "sentiment-check":
        res = analyze_sentiment_and_positioning(args.fii_long_short, args.pcr, args.vix)
    elif args.command == "spread-check":
        res = analyze_valuation_and_breadth(args.small_large_pe, args.breadth_50dma, args.yield_gap)

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
