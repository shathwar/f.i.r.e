#!/usr/bin/env python3
"""
UK & India F.I.R.E. Quantitative Calculation Engine
Senior Financial Advisory Tool for F.I.R.E. Modeling
Multi-Jurisdiction: UK & Bharat (India)
Supports:
  1. FIRE Target sizing (Lean/Standard/Fat/Coast)
  2. Retirement date & years-to-FI projection
  3. UK Tax Optimisation (Pensions, ISAs, 60% marginal tax trap)
  4. Mortgage overpayment vs. investing arbitrage
  5. Pension bridge sizing (Pre-57 funding)
  6. Stress testing (30% Year-1 market crash & SORR)
  7. Household / Spousal tax equalization
  8. April 2027 Inheritance Tax & effective death tax rate (pension vs ISA)
  9. The r > 0.75m pension contribution law
  10. First death & survivor financial shock modeling
  11. India Tax Optimization: Old vs New Regime (FY24-25 / FY25-26 slabs, HRA, 80C, 80D, 24b)
  12. India FIRE Planner: 6.5% inflation, 3.3% SWR, SIP gap & milestone targets
  13. Loan Prepayment Analyzer: Reducing balance EMI, tenure reduction & interest saved
  14. Money Health Score (MHS): 6-dimension weighted diagnostic (Emergency, Insurance, FOIR, Equity)
"""

import argparse
import json
import math
import os
from pathlib import Path
import sys
from typing import Dict, Any, Tuple, List, Optional


# ==============================================================================
# UK & GLOBAL FOUNDATIONS
# ==============================================================================

def calculate_fire_target(annual_spend: float, swr: float = 0.035, state_pension_annual: float = 0.0) -> Dict[str, Any]:
    """Calculate the FIRE target portfolio under various safe withdrawal rates."""
    target_full = annual_spend / swr
    adjusted_spend = max(0.0, annual_spend - state_pension_annual)
    target_with_state_pension = adjusted_spend / swr
    
    return {
        "annual_spend": annual_spend,
        "swr_percent": swr * 100,
        "fire_target": round(target_full, 2),
        "lean_fire_target (3.25% SWR)": round(annual_spend / 0.0325, 2),
        "standard_fire_target (3.5% SWR)": round(annual_spend / 0.035, 2),
        "flexible_fire_target (4.0% SWR)": round(annual_spend / 0.04, 2),
        "state_pension_offset": state_pension_annual,
        "fire_target_post_state_pension": round(target_with_state_pension, 2),
    }


def calculate_retirement_date(current_age: int, current_net_worth: float, annual_savings: float, 
                              annual_spend: float, swr: float = 0.035, real_return: float = 0.05) -> Dict[str, Any]:
    """Calculate years to FI and exact retirement age."""
    fire_target = annual_spend / swr
    if current_net_worth >= fire_target:
        return {
            "current_age": current_age,
            "retirement_age": current_age,
            "years_to_fi": 0.0,
            "fire_target": round(fire_target, 2),
            "status": "FI Already Achieved!"
        }
    
    nw = current_net_worth
    years = 0
    max_years = 60
    while nw < fire_target and years < max_years:
        nw = (nw * (1.0 + real_return)) + annual_savings
        years += 1
        
    projected_age = current_age + years
    return {
        "current_age": current_age,
        "projected_retirement_age": projected_age,
        "years_to_fi": years,
        "fire_target": round(fire_target, 2),
        "portfolio_at_fi": round(nw, 2),
        "assumed_real_return_percent": real_return * 100,
        "annual_savings": annual_savings,
    }


def calculate_pension_bridge(retire_age: int, nmpa: int = 57, annual_spend: float = 40000.0, 
                             cash_buffer_years: int = 2) -> Dict[str, Any]:
    """Sizes the required liquid bridge (ISAs/Cash) before pension access at NMPA."""
    bridge_years = max(0, nmpa - retire_age)
    if bridge_years == 0:
        return {
            "retire_age": retire_age,
            "nmpa": nmpa,
            "bridge_years": 0,
            "bridge_required": 0.0,
            "note": "Client has reached or passed NMPA (57). Full private pension access is available."
        }
    
    cash_buffer = min(bridge_years, cash_buffer_years) * annual_spend
    invested_bridge = max(0.0, (bridge_years - cash_buffer_years) * annual_spend)
    total_bridge = bridge_years * annual_spend
    
    return {
        "retire_age": retire_age,
        "nmpa": nmpa,
        "bridge_years": bridge_years,
        "annual_spend": annual_spend,
        "total_bridge_required": round(total_bridge, 2),
        "bucket_1_cash_buffer (0-2 yrs)": round(cash_buffer, 2),
        "bucket_2_isa_investments (3+ yrs)": round(invested_bridge, 2),
    }


def compare_pension_vs_isa(gross_amount: float, tax_bracket: str) -> Dict[str, Any]:
    """Compares terminal wealth of contributing to a Pension vs ISA for UK tax brackets."""
    brackets = {
        "basic": {"tax_rate": 0.20, "ni_rate": 0.08, "effective_relief": 0.20},
        "higher": {"tax_rate": 0.40, "ni_rate": 0.02, "effective_relief": 0.40},
        "60_trap": {"tax_rate": 0.60, "ni_rate": 0.02, "effective_relief": 0.60},
        "additional": {"tax_rate": 0.45, "ni_rate": 0.02, "effective_relief": 0.45},
    }
    
    info = brackets.get(tax_bracket.lower(), brackets["higher"])
    tax_rate = info["tax_rate"]
    
    isa_invested = gross_amount * (1.0 - tax_rate)
    pension_invested = gross_amount
    growth_multiplier = (1.05) ** 20
    isa_future_value = isa_invested * growth_multiplier
    pension_future_gross = pension_invested * growth_multiplier
    
    pension_net_withdrawal = (pension_future_gross * 0.25) + ((pension_future_gross * 0.75) * 0.80)
    pension_advantage_pct = ((pension_net_withdrawal - isa_future_value) / isa_future_value) * 100
    
    return {
        "gross_contribution": gross_amount,
        "tax_bracket": tax_bracket,
        "isa_initial_investment": round(isa_invested, 2),
        "pension_initial_investment": round(pension_invested, 2),
        "isa_value_after_20_years (tax_free)": round(isa_future_value, 2),
        "pension_net_value_after_20_years": round(pension_net_withdrawal, 2),
        "pension_wealth_advantage_percent": round(pension_advantage_pct, 1),
    }


def compare_mortgage_vs_investing(mortgage_balance: float, mortgage_rate: float,
                                  available_gross: float, tax_bracket: str = "higher",
                                  expected_invest_return: float = 0.075) -> Dict[str, Any]:
    """Compares paying down mortgage vs investing in ISA or Pension."""
    marginal_tax = 0.40 if tax_bracket == "higher" else (0.60 if tax_bracket == "60_trap" else 0.20)
    net_cash = available_gross * (1.0 - marginal_tax)
    annual_mortgage_saved = net_cash * (mortgage_rate / 100.0)
    annual_isa_growth = net_cash * expected_invest_return
    annual_pension_growth = available_gross * expected_invest_return
    annual_pension_net_yield = annual_pension_growth * 0.85
    
    return {
        "available_gross": available_gross,
        "net_cash_for_mortgage_or_isa": round(net_cash, 2),
        "mortgage_rate_percent": mortgage_rate,
        "guaranteed_annual_mortgage_interest_saved": round(annual_mortgage_saved, 2),
        "expected_isa_annual_growth": round(annual_isa_growth, 2),
        "expected_pension_annual_net_growth": round(annual_pension_net_yield, 2),
        "recommendation": "Pension strongly dominates" if tax_bracket in ["higher", "60_trap"] else (
            "Mortgage overpayment highly attractive" if mortgage_rate > 5.5 else "Invest in ISA/Pension"
        )
    }


def stress_test_crash(starting_portfolio: float, annual_withdrawal: float, 
                      crash_pct: float = 0.30, years: int = 5) -> Dict[str, Any]:
    """Stress-tests portfolio against a crash in Year 1 with vs without cash buffer."""
    val_a = starting_portfolio * (1.0 - crash_pct) - annual_withdrawal
    history_a = [round(val_a, 2)]
    for _ in range(years - 1):
        val_a = (val_a * 1.06) - annual_withdrawal
        history_a.append(round(val_a, 2))
        
    cash_buffer = annual_withdrawal * 2.0
    equities_b = (starting_portfolio - cash_buffer) * (1.0 - crash_pct)
    history_b = []
    
    cash_buffer -= annual_withdrawal
    history_b.append(round(equities_b + cash_buffer, 2))
    
    equities_b = equities_b * 1.06
    cash_buffer = 0.0
    history_b.append(round(equities_b, 2))
    
    val_b = equities_b
    for _ in range(years - 2):
        val_b = (val_b * 1.06) - annual_withdrawal
        history_b.append(round(val_b, 2))
        
    preservation_advantage = history_b[-1] - history_a[-1]
    
    return {
        "starting_portfolio": starting_portfolio,
        "crash_magnitude_percent": crash_pct * 100,
        "annual_withdrawal": annual_withdrawal,
        "policy_a_trajectory (no buffer)": history_a,
        "policy_b_trajectory (with 2yr buffer)": history_b,
        "portfolio_saved_by_cash_buffer_after_5_years": round(preservation_advantage, 2)
    }


def household_pension_equalization(household_drawdown: float) -> Dict[str, Any]:
    """Compares unequal vs equalized spousal pension pots."""
    taxable_1 = household_drawdown * 0.75
    tax_1 = max(0.0, (taxable_1 - 12570) * 0.20)
    
    half = household_drawdown / 2.0
    taxable_2 = half * 0.75
    tax_per_person = max(0.0, (taxable_2 - 12570) * 0.20)
    total_tax_2 = tax_per_person * 2.0
    
    tax_saved = total_tax_2 - tax_1
    return {
        "household_gross_drawdown": household_drawdown,
        "unequal_total_tax": round(tax_1, 2),
        "equalized_total_tax": round(total_tax_2, 2),
        "annual_tax_saved_by_equalizing": round(abs(tax_saved), 2),
        "percent_tax_reduction": round((abs(tax_saved) / tax_1) * 100, 1) if tax_1 > 0 else 0.0
    }


def calculate_pension_death_tax(pot_value: float, beneficiary_tax_rate: float = 0.40, 
                                iht_rate: float = 0.40, retiree_tax_rate_during_life: float = 0.20,
                                estate_value: Optional[float] = None, married_or_civil_partner: bool = True,
                                spouse_is_beneficiary: bool = False, death_pre_75: bool = False,
                                has_taxable_gias: bool = False) -> Dict[str, Any]:
    """
    Scenario-based decumulation and bequest evaluation post-April 2027.
    Evaluates whether accelerating pension drawdown vs preserving in pension is optimal,
    accounting for estate size, nil-rate bands, spousal exemption, beneficiary tax rates,
    and taxable GIA drag.
    """
    total_estate = estate_value if estate_value is not None else pot_value
    
    # 1. Determine Effective IHT Rate on Pension
    if spouse_is_beneficiary:
        # Spousal Exemption (Section 18 IHTA 1984): 100% exempt from IHT on first death
        effective_iht = 0.0
        iht_reason = "100% Spousal Exemption applies under Section 18 IHTA 1984. Zero IHT on transfer to spouse."
    else:
        # Check Nil-Rate Band (£325k single, £650k married) + RNRB (£175k single, £350k married)
        nrb = 650000.0 if married_or_civil_partner else 325000.0
        rnrb = 350000.0 if married_or_civil_partner else 175000.0
        # RNRB taper: reduces by £1 for every £2 estate exceeds £2m
        if total_estate > 2000000.0:
            excess_2m = total_estate - 2000000.0
            taper = excess_2m * 0.50
            rnrb = max(0.0, rnrb - taper)
        total_relief_band = nrb + rnrb
        
        if total_estate <= total_relief_band:
            effective_iht = 0.0
            iht_reason = f"Estate (£{total_estate:,.0f}) is fully within Nil-Rate Bands (£{total_relief_band:,.0f}). 0% IHT payable."
        else:
            effective_iht = iht_rate
            iht_reason = f"Estate (£{total_estate:,.0f}) exceeds Nil-Rate Bands (£{total_relief_band:,.0f}). Marginal {round(iht_rate*100)}% IHT applies."

    # 2. Beneficiary Income Tax (Post-75 vs Pre-75)
    if death_pre_75:
        beneficiary_effective_income_tax = 0.0
        income_tax_reason = "Death occurs before age 75: Beneficiary draws pension 100% income-tax-free (under LSDBA)."
    else:
        beneficiary_effective_income_tax = beneficiary_tax_rate
        income_tax_reason = f"Death occurs post age 75: Beneficiary pays income tax at their marginal rate ({round(beneficiary_tax_rate * 100)}%)."

    # 3. Path A: Retain in Pension Until Death
    iht_paid_pension = pot_value * effective_iht
    pot_after_iht = pot_value - iht_paid_pension
    income_tax_paid_pension = pot_after_iht * beneficiary_effective_income_tax
    net_pension_to_heir = pot_after_iht - income_tax_paid_pension
    combined_pension_death_drag = (pot_value - net_pension_to_heir) / pot_value if pot_value > 0 else 0.0

    # 4. Path B: Drawdown During Life at retiree_tax_rate_during_life and Recycle to ISA/Gift
    cash_in_hand = pot_value * (1.0 - retiree_tax_rate_during_life)
    isa_iht_paid = cash_in_hand * effective_iht
    net_isa_recycled_to_heir = cash_in_hand - isa_iht_paid
    combined_isa_drag = (pot_value - net_isa_recycled_to_heir) / pot_value if pot_value > 0 else 0.0

    # 5. Formulate Scenario-Based Nuanced Recommendation & Exceptions
    recommendations = []
    exceptions = []
    
    if spouse_is_beneficiary:
        optimal_strategy = "PRESERVE PENSION (Spouse Beneficiary Exception)"
        recommendations.append("Do NOT accelerate pension drawdown. The pot transfers to your spouse completely free of IHT under Section 18 IHTA 1984.")
        exceptions.append("100% Spousal Exemption: Drawing pension early creates immediate 20%-40% income tax drag with zero IHT savings.")
    elif total_estate <= (650000.0 if married_or_civil_partner else 325000.0):
        optimal_strategy = "PRESERVE PENSION (Nil-Rate Band Exemption)"
        recommendations.append("Do NOT accelerate pension drawdown. Your estate is within the Nil-Rate Band, so IHT is 0%.")
        exceptions.append("Zero IHT Estate: Draining the pension destroys wealth by incurring unnecessary income tax during life.")
    elif retiree_tax_rate_during_life >= 0.40:
        optimal_strategy = "CAUTION: HIGH INCOME TAX DRAG"
        recommendations.append("Do NOT accelerate pension drawdown if it incurs 40% or 60% marginal income tax today.")
        exceptions.append("Tax Inversion Trap: Paying 40% income tax today to save a potential 40% future IHT yields no net benefit and loses tax-free compounding.")
    elif has_taxable_gias:
        optimal_strategy = "DRAIN TAXABLE GIAS FIRST"
        recommendations.append("Exhaust General Investment Accounts (GIAs) before accelerating pension withdrawals to eliminate ongoing dividend and CGT drag.")
        exceptions.append("Taxable Wrapper Drag: GIAs suffer ongoing annual tax, whereas pensions compound tax-free.")
    elif effective_iht > 0 and retiree_tax_rate_during_life <= 0.20 and beneficiary_effective_income_tax >= 0.40:
        optimal_strategy = "PENSION RECYCLING ACCREDITED"
        recommendations.append("Draw pension within 20% basic rate band and recycle surplus into ISAs or inter-vivos gifting.")
        exceptions.append("High-Tax Beneficiary + 40% Estate: Taking income at 20% beats leaving a 64% combined IHT + Higher Rate income tax burden.")
    else:
        optimal_strategy = "BALANCED MULTI-WRAPPER DRAWDOWN"
        recommendations.append("Balance pension drawdown to cover essential spending up to the Personal Allowance / Basic Rate ceiling, preserving tax-sheltered compounding.")

    return {
        "scenario_inputs": {
            "pot_value": pot_value,
            "total_estate_value": total_estate,
            "married_or_civil_partner": married_or_civil_partner,
            "spouse_is_beneficiary": spouse_is_beneficiary,
            "death_pre_75": death_pre_75,
            "retiree_income_tax_rate_during_life": retiree_tax_rate_during_life,
            "beneficiary_tax_rate_post75": beneficiary_tax_rate,
            "has_taxable_gias": has_taxable_gias
        },
        "iht_and_income_tax_diagnosis": {
            "effective_iht_rate_on_pension": round(effective_iht * 100, 1),
            "iht_rationale": iht_reason,
            "beneficiary_income_tax_rate": round(beneficiary_effective_income_tax * 100, 1),
            "income_tax_rationale": income_tax_reason
        },
        "path_comparison": {
            "path_a_preserve_in_pension": {
                "net_bequest_to_heir": round(net_pension_to_heir, 2),
                "combined_effective_tax_drag_percent": round(combined_pension_death_drag * 100, 1)
            },
            "path_b_draw_during_life_and_recycle": {
                "cash_drawn_post_income_tax": round(cash_in_hand, 2),
                "net_bequest_if_in_estate": round(net_isa_recycled_to_heir, 2),
                "combined_effective_tax_drag_percent": round(combined_isa_drag * 100, 1)
            }
        },
        "optimal_strategy": optimal_strategy,
        "recommendations": recommendations,
        "explicit_exceptions": exceptions
    }


def test_contribution_law(relief_rate: float = 0.20, retirement_marginal_rate: float = 0.20, 
                          pcls_available: bool = True, is_non_earning_spouse: bool = False,
                          non_earner_annual_contribution: float = 2880.0,
                          spouse_other_retirement_income: float = 0.0,
                          partner_pension_pot: float = 0.0) -> Dict[str, Any]:
    """
    Evaluates pension contribution efficiency and the r > 0.75m theorem.
    Explicitly models non-earning spouse scenarios (£2,880 net / £3,600 gross),
    Personal Allowance arbitrage, and spousal pot equalization exceptions.
    """
    cost = 1.0 - relief_rate
    if pcls_available:
        payout = 0.25 + (0.75 * (1.0 - retirement_marginal_rate))
        breakeven_m = relief_rate / 0.75
    else:
        payout = 1.0 - retirement_marginal_rate
        breakeven_m = relief_rate
        
    net_return_percent = ((payout - cost) / cost) * 100
    formula_favorable = relief_rate > (0.75 * retirement_marginal_rate if pcls_available else retirement_marginal_rate)

    spousal_analysis = None
    explicit_exceptions = []
    recommendation = "Contribute (Value accretive)" if formula_favorable else "Exercise Caution / Evaluate Alternatives"

    if is_non_earning_spouse:
        net_paid = non_earner_annual_contribution
        basic_relief = net_paid * 0.25  # £2,880 * 0.25 = £720 relief -> £3,600 gross pot
        gross_pot = net_paid + basic_relief
        
        # Test if spouse draws within Personal Allowance (£12,570)
        pa_remaining = max(0.0, 12570.0 - spouse_other_retirement_income)
        if pa_remaining >= (gross_pot * 0.75):
            actual_spousal_return_pct = (basic_relief / net_paid) * 100  # +25.0% instant return
            spousal_verdict = "STRONGLY ACCRETIVE (+25% Return via Personal Allowance Arbitrage)"
            explicit_exceptions.append(
                "Personal Allowance Arbitrage: The non-earning spouse has unused Personal Allowance (£12,570). "
                "Drawdown is taxed at 0%, yielding an immediate 25% risk-free return on the £2,880 net contribution."
            )
        elif retirement_marginal_rate <= 0.20:
            actual_spousal_return_pct = 6.25  # 25% tax-free + 75% taxed at 20%
            spousal_verdict = "ACCRETIVE (+6.25% Net Return in Basic Rate Band)"
            explicit_exceptions.append(
                "Basic Rate Parity: Even with basic rate tax on exit, 25% tax-free PCLS delivers a net positive +6.25% return."
            )
        else:
            actual_spousal_return_pct = -12.5  # 25% tax free + 75% taxed at 40% = 0.70 payout vs 0.80 cost
            spousal_verdict = "MARGINALLY DILUTIVE ON PAPER (-12.5% if entire drawdown hits 40% band)"
            explicit_exceptions.append(
                "Higher-Rate Exit Condition: Only value-dilutive if the non-earner ALREADY has substantial other guaranteed income "
                "(e.g. large DB pension or rent) that fully exhausts their Personal Allowance and Basic Rate band."
            )
            explicit_exceptions.append(
                "Spousal Equalization Exception: If the higher-earning partner is approaching lifetime limits or higher-rate drawdown, "
                "building the non-earner pot equalizes retirement income, utilizing two Personal Allowances and Basic Rate bands."
            )
            explicit_exceptions.append(
                "Alternative Recommendation: If higher-rate exit is genuinely unavoidable, direct the £2,880 into an ISA for tax-free compounding."
            )

        if partner_pension_pot > 500000.0:
            explicit_exceptions.append(
                "Pot Equalization Alpha: Equalizing pots allows the household to extract up to £25,140 tax-free annually across both Personal Allowances."
            )

        spousal_analysis = {
            "net_cash_invested": net_paid,
            "hmrc_basic_rate_topup": basic_relief,
            "gross_pension_created": gross_pot,
            "unused_personal_allowance_headroom": pa_remaining,
            "effective_net_return_percent": actual_spousal_return_pct,
            "spousal_verdict": spousal_verdict
        }

    return {
        "relief_going_in_percent": relief_rate * 100,
        "retirement_marginal_rate_percent": retirement_marginal_rate * 100,
        "pcls_available": pcls_available,
        "cash_cost_per_pound_gross": round(cost, 3),
        "net_payout_per_pound_gross": round(payout, 3),
        "immediate_net_return_percent": round(net_return_percent, 2),
        "breakeven_marginal_rate_percent": round(breakeven_m * 100, 1),
        "general_verdict": recommendation,
        "spousal_non_earner_assessment": spousal_analysis,
        "explicit_exceptions_and_context": explicit_exceptions
    }


def calculate_survivor_shock(household_spend: float, p1_state_pension: float = 11500.0,
                             p2_state_pension: float = 11500.0, p1_db_pension: float = 0.0,
                             db_survivor_fraction: float = 0.50) -> Dict[str, Any]:
    """Models the First Death & Survivor Shock."""
    total_sp_couple = p1_state_pension + p2_state_pension
    total_db_couple = p1_db_pension
    
    survivor_spend = household_spend * 0.85
    survivor_sp = p2_state_pension
    survivor_db = p1_db_pension * db_survivor_fraction
    lost_pa_tax_drag = 12570.0 * 0.20
    
    drawdown_couple = max(0.0, household_spend - total_sp_couple - total_db_couple)
    drawdown_survivor = max(0.0, survivor_spend - survivor_sp - survivor_db + lost_pa_tax_drag)
    drawdown_increase = drawdown_survivor - drawdown_couple
    
    return {
        "couple_annual_spend": household_spend,
        "survivor_annual_spend (85% baseline)": round(survivor_spend, 2),
        "lost_state_pension_annual": p1_state_pension,
        "lost_db_pension_annual": round(p1_db_pension * (1.0 - db_survivor_fraction), 2),
        "lost_personal_allowance_tax_penalty": round(lost_pa_tax_drag, 2),
        "required_portfolio_drawdown_couple": round(drawdown_couple, 2),
        "required_portfolio_drawdown_survivor": round(drawdown_survivor, 2),
        "net_drawdown_change_for_survivor": round(drawdown_increase, 2),
        "survivor_warning": "Warning: Survivor requires higher private portfolio drawdown despite spending less!" if drawdown_increase > 0 else "Sustainable"
    }


# ==============================================================================
# INDIA (BHARAT) FINANCIAL & TAX MODULES (ARTHMITRA BORROWINGS)
# ==============================================================================

def compute_new_regime_tax(taxable_income: float, ay: str = "2026-27") -> Dict[str, Any]:
    """
    Computes tax under the New Tax Regime according to the specified Assessment Year.
    Supports AY 2026-27 (Union Budget 2025: ₹12L rebate + marginal relief + revised slabs)
    and AY 2025-26 (Legacy: ₹7L rebate + slabs up to ₹15L).
    """
    taxable = max(0.0, taxable_income)
    
    if ay == "2026-27":
        # AY 2026-27 Slabs (Budget 2025):
        # 0 - 4L: Nil
        # 4L - 8L: 5% (max 20,000)
        # 8L - 12L: 10% (max 40,000) -> cumulative 60,000 at 12L
        # 12L - 16L: 15% (max 60,000)
        # 16L - 20L: 20% (max 80,000)
        # 20L - 24L: 25% (max 1,00,000)
        # Above 24L: 30%
        slab_tax = 0.0
        rem = taxable
        if rem > 2400000:
            slab_tax += (rem - 2400000) * 0.30
            rem = 2400000
        if rem > 2000000:
            slab_tax += (rem - 2000000) * 0.25
            rem = 2000000
        if rem > 1600000:
            slab_tax += (rem - 1600000) * 0.20
            rem = 1600000
        if rem > 1200000:
            slab_tax += (rem - 1200000) * 0.15
            rem = 1200000
        if rem > 800000:
            slab_tax += (rem - 800000) * 0.10
            rem = 800000
        if rem > 400000:
            slab_tax += (rem - 400000) * 0.05
        
        rebate_87a = 0.0
        marginal_relief = 0.0
        tax_after_relief = slab_tax
        
        if taxable <= 1200000:
            rebate_87a = slab_tax
            tax_after_relief = 0.0
        else:
            # Section 87A Marginal Relief:
            # Tax payable cannot exceed excess of taxable income over ₹12,00,000
            excess_income = taxable - 1200000.0
            if slab_tax > excess_income:
                marginal_relief = slab_tax - excess_income
                tax_after_relief = excess_income
        
        cess = tax_after_relief * 0.04
        total_tax = tax_after_relief + cess
        
        return {
            "assessment_year": "AY 2026-27 (FY 2025-26)",
            "taxable_income": round(taxable, 2),
            "slab_tax_before_relief": round(slab_tax, 2),
            "sec_87a_rebate": round(rebate_87a, 2),
            "marginal_relief_87a": round(marginal_relief, 2),
            "tax_payable_before_cess": round(tax_after_relief, 2),
            "cess_4_percent": round(cess, 2),
            "total_tax": round(total_tax, 2),
            "effective_tax_rate_pct": round((total_tax / taxable * 100) if taxable > 0 else 0.0, 2),
            "rebate_threshold": "₹12,00,000 Taxable Income (0 tax up to ₹12.75L Gross Salary with Standard Deduction)"
        }
    else:
        # AY 2025-26 (Legacy FY 2024-25 / FY 2025-26):
        # 0 - 3L: Nil | 3L - 7L: 5% | 7L - 10L: 10% | 10L - 12L: 15% | 12L - 15L: 20% | > 15L: 30%
        slab_tax = 0.0
        rem = taxable
        if rem > 1500000:
            slab_tax += (rem - 1500000) * 0.30
            rem = 1500000
        if rem > 1200000:
            slab_tax += (rem - 1200000) * 0.20
            rem = 1200000
        if rem > 1000000:
            slab_tax += (rem - 1000000) * 0.15
            rem = 1000000
        if rem > 700000:
            slab_tax += (rem - 700000) * 0.10
            rem = 700000
        if rem > 300000:
            slab_tax += (rem - 300000) * 0.05
        
        rebate_87a = 0.0
        marginal_relief = 0.0
        tax_after_relief = slab_tax
        if taxable <= 700000:
            rebate_87a = slab_tax
            tax_after_relief = 0.0
        else:
            excess_income = taxable - 700000.0
            if slab_tax > excess_income:
                marginal_relief = slab_tax - excess_income
                tax_after_relief = excess_income
        
        cess = tax_after_relief * 0.04
        total_tax = tax_after_relief + cess
        return {
            "assessment_year": "AY 2025-26 (FY 2024-25)",
            "taxable_income": round(taxable, 2),
            "slab_tax_before_relief": round(slab_tax, 2),
            "sec_87a_rebate": round(rebate_87a, 2),
            "marginal_relief_87a": round(marginal_relief, 2),
            "tax_payable_before_cess": round(tax_after_relief, 2),
            "cess_4_percent": round(cess, 2),
            "total_tax": round(total_tax, 2),
            "effective_tax_rate_pct": round((total_tax / taxable * 100) if taxable > 0 else 0.0, 2),
            "rebate_threshold": "₹7,00,000 Taxable Income (0 tax up to ₹7.75L Gross Salary with Standard Deduction)"
        }


def calculate_india_tax(gross_income: float, basic_salary: float = 0.0, hra_received: float = 0.0,
                        rent_paid: float = 0.0, is_metro: bool = True, sec_80c: float = 0.0,
                        sec_80ccd_1b: float = 0.0, sec_80d: float = 0.0, sec_24b: float = 0.0,
                        ay: str = "2026-27", is_ctc: bool = False, employer_pf: float = 0.0,
                        employer_nps_80ccd2: float = 0.0) -> Dict[str, Any]:
    """
    Compares Old vs New Tax Regime for Indian residents under versioned statutory rules.
    Accurately distinguishes CTC, Gross Taxable Salary, and Net Taxable Income.
    
    Supports:
    - AY 2026-27 (Default, Union Budget 2025): ₹12L Sec 87A rebate threshold, revised slabs, marginal relief.
    - AY 2025-26 (Legacy): ₹7L Sec 87A rebate threshold.
    """
    # 0. CTC vs Gross Taxable Salary Reconciliation
    ctc_breakdown = None
    if is_ctc:
        ctc_amount = gross_income
        basic = basic_salary if basic_salary > 0 else (ctc_amount * 0.40)
        emp_pf = employer_pf if employer_pf > 0 else (basic * 0.12)
        gratuity = basic * 0.0481
        group_insurance = 10000.0 if ctc_amount >= 500000 else 0.0
        
        gross_salary = max(0.0, ctc_amount - emp_pf - gratuity - group_insurance)
        ctc_breakdown = {
            "total_ctc": round(ctc_amount, 2),
            "employer_epf_contribution (exempt)": round(emp_pf, 2),
            "gratuity_accrual (statutory reserve)": round(gratuity, 2),
            "group_health_insurance_by_employer": round(group_insurance, 2),
            "gross_taxable_salary": round(gross_salary, 2),
            "distinction_note": "CTC represents total company cost. Gross Taxable Salary excludes employer EPF, gratuity accrual, and group insurance."
        }
    else:
        gross_salary = gross_income
        basic = basic_salary if basic_salary > 0 else (gross_salary * 0.50)

    # 1. New Tax Regime
    std_ded_new = 75000.0
    taxable_new = max(0.0, gross_salary - std_ded_new - employer_nps_80ccd2)
    new_regime_res = compute_new_regime_tax(taxable_new, ay=ay)

    # 2. Old Tax Regime
    std_ded_old = 50000.0
    hra_exemption = 0.0
    if hra_received > 0 and rent_paid > 0 and basic > 0:
        excess_rent = max(0.0, rent_paid - (0.10 * basic))
        salary_pct = (0.50 if is_metro else 0.40) * basic
        hra_exemption = min(hra_received, excess_rent, salary_pct)

    c_80c = min(150000.0, sec_80c)
    c_80ccd = min(50000.0, sec_80ccd_1b)
    c_80d = min(75000.0, sec_80d)
    c_24b = min(200000.0, sec_24b)

    total_deductions_old = std_ded_old + hra_exemption + c_80c + c_80ccd + c_80d + c_24b + employer_nps_80ccd2
    taxable_old = max(0.0, gross_salary - total_deductions_old)

    # Old Regime Slabs: 0-2.5L (0%), 2.5L-5L (5%), 5L-10L (20%), >10L (30%)
    tax_old = 0.0
    rem_old = taxable_old
    if rem_old > 1000000:
        tax_old += (rem_old - 1000000) * 0.30
        rem_old = 1000000
    if rem_old > 500000:
        tax_old += (rem_old - 500000) * 0.20
        rem_old = 500000
    if rem_old > 250000:
        tax_old += (rem_old - 250000) * 0.05

    rebate_87a_old = 0.0
    if taxable_old <= 500000:
        rebate_87a_old = tax_old
        tax_old = 0.0

    cess_old = tax_old * 0.04
    total_tax_old = tax_old + cess_old

    total_tax_new = new_regime_res["total_tax"]
    tax_diff = total_tax_old - total_tax_new
    recommendation = "New Regime" if total_tax_new <= total_tax_old else "Old Regime"
    savings = abs(tax_diff)

    return {
        "assessment_year": ay,
        "income_inputs": {
            "provided_amount": gross_income,
            "input_type": "Cost to Company (CTC)" if is_ctc else "Gross Taxable Salary",
            "gross_taxable_salary": round(gross_salary, 2)
        },
        "ctc_reconciliation": ctc_breakdown,
        "new_regime": {
            "standard_deduction": std_ded_new,
            "employer_nps_80ccd2": round(employer_nps_80ccd2, 2),
            "taxable_income": round(taxable_new, 2),
            "slab_tax_before_relief": new_regime_res["slab_tax_before_relief"],
            "sec_87a_rebate": new_regime_res["sec_87a_rebate"],
            "marginal_relief_87a": new_regime_res["marginal_relief_87a"],
            "tax_payable_before_cess": new_regime_res["tax_payable_before_cess"],
            "cess_4_percent": new_regime_res["cess_4_percent"],
            "total_tax": round(total_tax_new, 2),
            "effective_tax_rate_pct": new_regime_res["effective_tax_rate_pct"],
            "notes": new_regime_res["rebate_threshold"]
        },
        "old_regime": {
            "standard_deduction": std_ded_old,
            "hra_exemption": round(hra_exemption, 2),
            "sec_80c": round(c_80c, 2),
            "sec_80ccd_1b": round(c_80ccd, 2),
            "sec_80d": round(c_80d, 2),
            "sec_24b_home_loan": round(c_24b, 2),
            "employer_nps_80ccd2": round(employer_nps_80ccd2, 2),
            "total_deductions": round(total_deductions_old, 2),
            "taxable_income": round(taxable_old, 2),
            "base_tax_before_rebate": round(tax_old + rebate_87a_old, 2),
            "sec_87a_rebate": round(rebate_87a_old, 2),
            "cess_4_percent": round(cess_old, 2),
            "total_tax": round(total_tax_old, 2),
            "effective_tax_rate_pct": round((total_tax_old / taxable_old * 100) if taxable_old > 0 else 0.0, 2)
        },
        "comparison_summary": {
            "recommended_regime": recommendation,
            "annual_tax_saving": round(savings, 2),
            "taxable_income_distinction_clarification": (
                "CRITICAL: CTC != Gross Salary != Taxable Income. "
                "The Section 87A rebate applies on Net Taxable Income (after deductions), not CTC."
            )
        }
    }


def calculate_india_fire(current_age: int, retire_age: int, monthly_expenses: float,
                         current_portfolio: float = 0.0, inflation: float = 0.065,
                         swr: float = 0.033, expected_equity_return: float = 0.12) -> Dict[str, Any]:
    """Calculates India FIRE corpus with 6.5% inflation, 3.3% SWR, and monthly SIP gap."""
    years = max(1, retire_age - current_age)
    months = years * 12
    annual_spend_today = monthly_expenses * 12.0
    future_annual_spend = annual_spend_today * ((1.0 + inflation) ** years)
    future_monthly_spend = future_annual_spend / 12.0
    
    target_corpus = future_annual_spend / swr
    fv_current_nw = current_portfolio * ((1.0 + expected_equity_return) ** years)
    deficit_corpus = max(0.0, target_corpus - fv_current_nw)
    
    monthly_r = ((1.0 + expected_equity_return) ** (1.0 / 12.0)) - 1.0
    if deficit_corpus > 0 and monthly_r > 0:
        factor = (((1.0 + monthly_r) ** months) - 1.0) * (1.0 + monthly_r)
        required_monthly_sip = (deficit_corpus * monthly_r) / factor
    else:
        required_monthly_sip = 0.0
        
    return {
        "current_age": current_age,
        "target_retirement_age": retire_age,
        "years_to_retirement": years,
        "current_monthly_expenses": monthly_expenses,
        "assumed_inflation_percent": inflation * 100,
        "future_monthly_expenses_at_retirement": round(future_monthly_spend, 2),
        "future_annual_expenses_at_retirement": round(future_annual_spend, 2),
        "swr_percent": swr * 100,
        "target_fire_corpus": round(target_corpus, 2),
        "current_portfolio": current_portfolio,
        "projected_fv_current_portfolio": round(fv_current_nw, 2),
        "corpus_gap_to_fund": round(deficit_corpus, 2),
        "required_monthly_sip": round(required_monthly_sip, 2),
        "assumed_equity_cagr_percent": expected_equity_return * 100,
        "corpus_in_crores": f"₹{target_corpus / 1e7:.2f} Cr"
    }


def calculate_loan_prepayment(principal: float, annual_rate: float, tenure_years: float,
                              extra_monthly_prepay: float = 0.0, lump_sum_prepay: float = 0.0) -> Dict[str, Any]:
    """Reducing-balance EMI and loan prepayment interest savings simulator."""
    monthly_r = (annual_rate / 100.0) / 12.0
    total_months = int(tenure_years * 12)
    
    emi = principal * monthly_r * ((1.0 + monthly_r) ** total_months) / (((1.0 + monthly_r) ** total_months) - 1.0)
    
    balance_base = principal
    total_interest_base = 0.0
    for _ in range(total_months):
        interest = balance_base * monthly_r
        principal_paid = emi - interest
        total_interest_base += interest
        balance_base -= principal_paid
        if balance_base <= 0:
            break
            
    balance_prep = principal - lump_sum_prepay
    total_interest_prep = 0.0
    months_taken = 0
    while balance_prep > 0 and months_taken < total_months * 2:
        interest = balance_prep * monthly_r
        principal_paid = (emi + extra_monthly_prepay) - interest
        total_interest_prep += interest
        balance_prep -= principal_paid
        months_taken += 1
        if balance_prep <= 0:
            break
            
    interest_saved = max(0.0, total_interest_base - total_interest_prep)
    months_saved = max(0, total_months - months_taken)
    
    return {
        "loan_principal": principal,
        "interest_rate_percent": annual_rate,
        "original_tenure_years": tenure_years,
        "monthly_emi": round(emi, 2),
        "baseline_total_interest": round(total_interest_base, 2),
        "extra_monthly_prepayment": extra_monthly_prepay,
        "lump_sum_prepayment": lump_sum_prepay,
        "revised_tenure_months": months_taken,
        "revised_tenure_years": round(months_taken / 12.0, 1),
        "months_saved": months_saved,
        "years_saved": round(months_saved / 12.0, 1),
        "total_interest_saved": round(interest_saved, 2)
    }


def calculate_money_health_score(monthly_income: float, monthly_expenses: float, monthly_emi: float,
                                 liquid_fund: float, term_insurance_cover: float,
                                 has_health_insurance: bool = True, age: int = 30,
                                 equity_percent: float = 70.0, has_credit_card_debt: bool = False) -> Dict[str, Any]:
    """Calculates the ArthMitra 6-dimension Money Health Score (0-100)."""
    monthly_obligation = monthly_expenses + monthly_emi
    months_covered = liquid_fund / monthly_obligation if monthly_obligation > 0 else 6.0
    emergency_score = min(100.0, (months_covered / 6.0) * 100.0)
    
    annual_income = monthly_income * 12.0
    target_term = annual_income * 15.0
    term_ratio = term_insurance_cover / target_term if target_term > 0 else 1.0
    life_score = min(100.0, term_ratio * 100.0)
    health_score = 100.0 if has_health_insurance else 20.0
    insurance_score = (life_score * 0.65) + (health_score * 0.35)
    
    foir = monthly_emi / monthly_income if monthly_income > 0 else 0.0
    if foir <= 0.30:
        debt_score = 100.0
    elif foir <= 0.45:
        debt_score = 70.0
    elif foir <= 0.60:
        debt_score = 40.0
    else:
        debt_score = 15.0
    if has_credit_card_debt:
        debt_score = max(0.0, debt_score - 50.0)
        
    target_equity = max(20.0, min(90.0, 100.0 - age))
    equity_dev = abs(equity_percent - target_equity)
    invest_score = max(0.0, 100.0 - (equity_dev * 2.0))
    
    savings_rate = (monthly_income - monthly_obligation) / monthly_income if monthly_income > 0 else 0.0
    discipline_score = min(100.0, (savings_rate / 0.30) * 100.0)
    
    total_mhs = (emergency_score * 0.20) + (insurance_score * 0.25) + (debt_score * 0.15) + (invest_score * 0.20) + (discipline_score * 0.20)
    total_mhs = round(total_mhs, 1)
    
    if total_mhs >= 85:
        rating = "Good (Resilient, Ready for aggressive compounding)"
    elif total_mhs >= 70:
        rating = "Fair (Sound baseline, minor vulnerabilities)"
    elif total_mhs >= 50:
        rating = "Poor (Vulnerable to income disruption or debt drag)"
    else:
        rating = "Critical (Immediate restructuring required)"
        
    return {
        "total_mhs_score": total_mhs,
        "rating": rating,
        "dimension_scores": {
            "emergency_shield (20%)": round(emergency_score, 1),
            "protection_insurance (25%)": round(insurance_score, 1),
            "debt_health_foir (15%)": round(debt_score, 1),
            "investment_allocation (20%)": round(invest_score, 1),
            "savings_discipline (20%)": round(discipline_score, 1)
        },
        "diagnostics": {
            "months_emergency_covered": round(months_covered, 1),
            "foir_percent": round(foir * 100, 1),
            "term_cover_multiple": round(term_insurance_cover / annual_income, 1) if annual_income > 0 else 0.0,
            "savings_rate_percent": round(savings_rate * 100, 1)
        }
    }


def calculate_india_asset_returns(tax_bracket: str = "30", inflation: float = 0.065) -> Dict[str, Any]:
    """Compares post-tax nominal and real returns across core Indian asset classes."""
    slab_rates = {
        "30": 0.312,
        "25": 0.260,
        "20": 0.208,
        "15": 0.156,
        "10": 0.104,
        "5": 0.052,
        "0": 0.0
    }
    marginal_tax = slab_rates.get(str(tax_bracket), 0.312)

    assets = [
        {
            "asset": "Bank Fixed Deposit (1-3 Year)",
            "nominal_cagr_pct": 7.25,
            "tax_treatment": f"Taxed at slab ({round(marginal_tax*100, 1)} percent)",
            "post_tax_cagr_pct": round(7.25 * (1.0 - marginal_tax), 2),
            "role_in_fire": "Emergency buffer only (0-2 yrs). Wealth destroyer vs inflation."
        },
        {
            "asset": "Arbitrage Mutual Fund",
            "nominal_cagr_pct": 7.00,
            "tax_treatment": "12.5 percent LTCG after 12 months",
            "post_tax_cagr_pct": round(7.00 * (1.0 - 0.125), 2),
            "role_in_fire": "Superior cash/parking alternative to FDs for high-earning investors."
        },
        {
            "asset": "Equity Mutual Funds (Nifty / Flexicap)",
            "nominal_cagr_pct": 12.00,
            "tax_treatment": "12.5 percent LTCG above ₹1.25L exemption",
            "post_tax_cagr_pct": round(12.00 * (1.0 - 0.125), 2),
            "role_in_fire": "Core growth engine (50-70 percent allocation)."
        },
        {
            "asset": "Sovereign Gold Bond (SGB - RBI Maturity)",
            "nominal_cagr_pct": 10.00,
            "tax_treatment": "Capital gains 100 percent tax-free at 8y maturity; 2.5 percent coupon taxed at slab",
            "post_tax_cagr_pct": round(7.50 + (2.50 * (1.0 - marginal_tax)), 2),
            "role_in_fire": "Currency depreciation hedge (5-10 percent allocation)."
        },
        {
            "asset": "Gold ETF / Physical Bullion",
            "nominal_cagr_pct": 9.50,
            "tax_treatment": "12.5 percent LTCG after 24 months (Post-Budget 2024)",
            "post_tax_cagr_pct": round(9.50 * (1.0 - 0.125), 2),
            "role_in_fire": "Liquid precious metals hedge without SGB lock-in."
        },
        {
            "asset": "Silver ETF",
            "nominal_cagr_pct": 11.00,
            "tax_treatment": "12.5 percent LTCG after 24 months (Post-Budget 2024)",
            "post_tax_cagr_pct": round(11.00 * (1.0 - 0.125), 2),
            "role_in_fire": "High-beta industrial commodity hedge (2-5 percent allocation)."
        },
        {
            "asset": "Residential Real Estate (Rental)",
            "nominal_cagr_pct": 7.30,
            "tax_treatment": "Net rent taxed at slab; 12.5 percent LTCG on exit (post-July 2024)",
            "post_tax_cagr_pct": round((1.8 * (1.0 - marginal_tax)) + (5.5 * (1.0 - 0.125)), 2),
            "role_in_fire": "Low net yield (1.8-2.2 percent). Sub-optimal for cash flow retirement."
        },
        {
            "asset": "Listed REITs (Commercial / Retail)",
            "nominal_cagr_pct": 10.50,
            "tax_treatment": "Blended distribution tax (~20 percent effective) + 12.5 percent LTCG on units",
            "post_tax_cagr_pct": round((7.2 * 0.80) + (3.3 * (1.0 - 0.125)), 2),
            "role_in_fire": "Fractional liquid commercial real estate income stream."
        },
        {
            "asset": "Digital Currencies / Bitcoin (Satellite)",
            "nominal_cagr_pct": 20.00,
            "tax_treatment": "Flat 31.2 percent tax (Sec 115BBH) with ZERO loss set-off",
            "post_tax_cagr_pct": round(20.00 * (1.0 - 0.312), 2),
            "role_in_fire": "High volatility asymmetric satellite (1-5 percent max). NEVER in emergency fund."
        }
    ]

    for a in assets:
        post_tax = a["post_tax_cagr_pct"] / 100.0
        real_ret = ((1.0 + post_tax) / (1.0 + inflation)) - 1.0
        a["real_return_pct"] = round(real_ret * 100.0, 2)
        a["net_annual_alpha_vs_inflation_pct"] = round((post_tax - inflation) * 100.0, 2)

    return {
        "investor_tax_bracket": tax_bracket,
        "assumed_inflation_pct": round(inflation * 100.0, 2),
        "asset_comparison": assets,
        "key_takeaways": [
            "Fixed Deposits guarantee a NEGATIVE real return (-1.5 percent) in high tax brackets; use Arbitrage Funds instead for cash buffers.",
            "Gold SGB delivers the highest post-tax risk-adjusted return among debt/hedges due to 100 percent tax-free capital gains on maturity.",
            "Residential real estate rental yield (1.8-2.2 percent net) locks up ~50 percent more capital than an equity/REIT financial independence portfolio.",
            "Crypto is taxed at flat 31.2 percent in India with zero loss set-off, making it suitable only as a disciplined 1-5 percent satellite."
        ]
    }


def calculate_buy_vs_rent_real_estate(property_price: float, monthly_rent: float,
                                      loan_rate: float = 0.0875, tenure_years: int = 20,
                                      equity_cagr: float = 0.12, prop_cagr: float = 0.06,
                                      rent_inflation: float = 0.05) -> Dict[str, Any]:
    """Evaluates the financial outcome of buying a property vs renting and investing the difference."""
    down_payment = property_price * 0.20
    stamp_duty = property_price * 0.07
    total_upfront = down_payment + stamp_duty
    loan_amount = property_price * 0.80

    r_m = loan_rate / 12.0
    n = tenure_years * 12
    if r_m > 0:
        emi = loan_amount * (r_m * (1.0 + r_m)**n) / ((1.0 + r_m)**n - 1.0)
    else:
        emi = loan_amount / n

    monthly_maintenance = (property_price * 0.005) / 12.0
    initial_ownership_cost = emi + monthly_maintenance

    future_property_value = property_price * ((1.0 + prop_cagr) ** tenure_years)
    fv_upfront = total_upfront * ((1.0 + equity_cagr) ** tenure_years)

    monthly_equity_r = (1.0 + equity_cagr) ** (1.0 / 12.0) - 1.0
    current_rent = monthly_rent
    accumulated_sip_wealth = 0.0

    total_rent_paid = 0.0
    total_emi_paid = emi * n

    for month in range(1, n + 1):
        if month > 1 and month % 12 == 1:
            current_rent *= (1.0 + rent_inflation)
        total_rent_paid += current_rent
        surplus = initial_ownership_cost - current_rent
        if surplus > 0:
            accumulated_sip_wealth = (accumulated_sip_wealth + surplus) * (1.0 + monthly_equity_r)
        else:
            accumulated_sip_wealth = accumulated_sip_wealth * (1.0 + monthly_equity_r)

    total_renter_wealth = fv_upfront + accumulated_sip_wealth
    renter_advantage = total_renter_wealth - future_property_value

    capital_needed_real_estate = (100000.0 * 12.0) / 0.022
    capital_needed_fire_portfolio = (100000.0 * 12.0) / 0.033

    return {
        "property_price": property_price,
        "monthly_rent": monthly_rent,
        "loan_parameters": {
            "loan_amount": round(loan_amount, 2),
            "interest_rate_percent": loan_rate * 100,
            "tenure_years": tenure_years,
            "monthly_emi": round(emi, 2),
            "upfront_cash_required (down payment and stamp duty)": round(total_upfront, 2),
            "total_emi_paid": round(total_emi_paid, 2)
        },
        "scenario_buyer": {
            "property_value_after_tenure": round(future_property_value, 2),
            "total_outflow (upfront and emi and maintenance)": round(total_upfront + total_emi_paid + (monthly_maintenance * n), 2),
            "net_equity_value": round(future_property_value, 2)
        },
        "scenario_renter_investor": {
            "upfront_capital_invested_fv": round(fv_upfront, 2),
            "monthly_surplus_sip_accumulated": round(accumulated_sip_wealth, 2),
            "total_financial_portfolio": round(total_renter_wealth, 2),
            "total_rent_paid": round(total_rent_paid, 2)
        },
        "comparison_result": {
            "renter_financial_advantage": round(renter_advantage, 2),
            "verdict": "Renting and investing surplus generates substantial alpha" if renter_advantage > 0 else "Buying beats renting under these parameters"
        },
        "retirement_income_capital_efficiency (for 1L/month cash flow)": {
            "capital_needed_via_real_estate_rental (2.2 percent net yield)": round(capital_needed_real_estate, 2),
            "capital_needed_via_fire_portfolio (3.3 percent SWR)": round(capital_needed_fire_portfolio, 2),
            "excess_capital_locked_in_property": round(capital_needed_real_estate - capital_needed_fire_portfolio, 2)
        }
    }


def calculate_crypto_tax(jurisdiction: str, gain: float, loss: float = 0.0,
                         transfer_value: float = 0.0, tax_bracket: str = "higher") -> Dict[str, Any]:
    """Computes statutory crypto / Virtual Digital Asset tax for UK or India."""
    jurisdiction = jurisdiction.lower().strip()
    if transfer_value <= 0:
        transfer_value = gain

    if jurisdiction in ["india", "in", "bharat"]:
        gross_taxable_gain = max(0.0, gain)
        statutory_tax = gross_taxable_gain * 0.312
        net_economic_profit = gain - loss
        tds_194s = transfer_value * 0.01 if transfer_value >= 50000.0 else 0.0
        effective_tax = (statutory_tax / net_economic_profit * 100.0) if net_economic_profit > 0 else "N/A (Loss or breakeven, but tax is strictly owed on gross gains!)"

        return {
            "jurisdiction": "India (Section 115BBH & Section 194S)",
            "gross_crypto_gains": round(gain, 2),
            "reported_crypto_losses": round(loss, 2),
            "net_economic_profit": round(net_economic_profit, 2),
            "statutory_tax_rate": "Flat 30 percent + 4 percent Cess = 31.2 percent",
            "statutory_tax_owed": round(statutory_tax, 2),
            "tds_deducted_at_source_sec_194s (1 percent)": round(tds_194s, 2),
            "net_post_tax_in_hand": round(net_economic_profit - statutory_tax, 2),
            "effective_tax_rate_on_real_profit_pct": round(effective_tax, 1) if isinstance(effective_tax, float) else effective_tax,
            "critical_statutory_rules": [
                "Section 115BBH(2)(b): Losses in one token/coin CANNOT be set off against gains in another token.",
                "Zero loss carry forward: Unabsorbed VDA losses expire at the end of the financial year.",
                "Zero business deductions: No deduction permitted for electricity, exchange fees, trading software, or internet.",
                "Section 194S: 1 percent TDS applies on all transfers > ₹50,000/year to establish an unbroken PAN audit trail."
            ],
            "fiduciary_fire_verdict": "Due to 31.2 percent flat tax without loss set-off, crypto is severely tax-penalized in India. Limit to 1-3 percent max satellite allocation."
        }
    else:
        cgt_rate = 0.18 if tax_bracket.lower() in ["basic", "standard"] else 0.24
        net_gain = gain - loss
        annual_exemption = 3000.0
        taxable_gain = max(0.0, net_gain - annual_exemption)
        cgt_owed = taxable_gain * cgt_rate
        unabsorbed_loss = max(0.0, loss - gain)

        return {
            "jurisdiction": "United Kingdom (HMRC Cryptoassets Manual)",
            "gross_crypto_gains": round(gain, 2),
            "crypto_losses_offset": round(min(gain, loss), 2),
            "net_capital_gain": round(net_gain, 2),
            "cgt_annual_exempt_amount": annual_exemption,
            "taxable_gain": round(taxable_gain, 2),
            "marginal_cgt_rate_percent": cgt_rate * 100,
            "cgt_tax_owed": round(cgt_owed, 2),
            "net_post_tax_in_hand": round(net_gain - cgt_owed, 2),
            "unabsorbed_loss_carried_forward": round(unabsorbed_loss, 2),
            "critical_statutory_rules": [
                "HMRC Pooling Rules: Same-day rule, 30-day 'Bed & Breakfast' rule, and Section 104 blended cost pool apply.",
                "Loss offset allowed: Crypto losses offset other capital gains and carry forward indefinitely if reported within 4 years.",
                "No ISA/SIPP wrapping: Direct crypto cannot be held inside tax-sheltered ISA or SIPP wrappers.",
                "Staking & mining: Taxed as Miscellaneous Income (20 percent/40 percent/45 percent) upon receipt, then CGT on disposal."
            ],
            "fiduciary_fire_verdict": "Unlike India, UK allows full loss offsetting and £3,000 exemption, but lack of ISA shielding limits crypto to a 1-5 percent satellite asset."
        }


# ==============================================================================
# LOCAL PROFILE STORAGE & ASSET MANAGEMENT
# ==============================================================================

def get_default_profiles_dir() -> Path:
    """Returns the default directory for local profiles if none specified."""
    env_dir = os.environ.get("FIRE_PROFILES_DIR")
    if env_dir:
        return Path(env_dir)
    config_file = Path(".fire_advisor_config.json")
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                cfg = json.load(f)
                if "profiles_directory" in cfg:
                    return Path(cfg["profiles_directory"])
        except Exception:
            pass
    return Path("./profiles")


def generate_profile_template(jurisdiction: str = "india", output_path: Optional[str] = None) -> Dict[str, Any]:
    """Generates a blank client profile template for local storage."""
    jurisdiction = jurisdiction.lower().strip()
    if jurisdiction in ["uk", "gb", "britain"]:
        template = {
            "profile_name": "New_UK_Client",
            "jurisdiction": "UK",
            "client_info": {
                "age": 35,
                "target_retirement_age": 55,
                "annual_spend": 40000.0,
                "gross_annual_income": 85000.0,
                "tax_bracket": "higher"
            },
            "assets": {
                "cash_and_emergency": [
                    {
                        "name": "Emergency Cash Account",
                        "amount": 20000.0,
                        "source": "Marcus by Goldman Sachs",
                        "account_id": "MC-8849201",
                        "portal_url": "https://www.marcus.co.uk"
                    }
                ],
                "isas": [
                    {
                        "name": "Stocks and Shares ISA",
                        "amount": 100000.0,
                        "source": "Vanguard Investor UK",
                        "account_id": "VG-100984",
                        "isin": "GB00BD3RZ582",
                        "portal_url": "https://www.vanguardinvestor.co.uk"
                    }
                ],
                "pensions": [
                    {
                        "name": "SIPP",
                        "amount": 150000.0,
                        "source": "Interactive Investor (ii)",
                        "account_id": "SIPP-ii-94821",
                        "portal_url": "https://www.ii.co.uk"
                    },
                    {
                        "name": "Workplace DC Pension",
                        "amount": 75000.0,
                        "source": "Aviva MyWorkplace",
                        "policy_id": "AV-489201",
                        "portal_url": "https://www.aviva.co.uk/workplace"
                    }
                ],
                "gias": [
                    {
                        "name": "General Investment Account",
                        "amount": 25000.0,
                        "source": "Hargreaves Lansdown",
                        "account_id": "HL-GIA-3910",
                        "portal_url": "https://www.hl.co.uk"
                    }
                ],
                "digital_assets": [
                    {
                        "name": "Bitcoin",
                        "amount": 5000.0,
                        "source": "Trezor Safe 3 Hardware Wallet",
                        "tracking_label": "Vault 1"
                    }
                ],
                "real_estate": [
                    {
                        "name": "Primary Residence",
                        "amount": 450000.0,
                        "is_primary": True,
                        "source": "HM Land Registry Title Deed",
                        "title_number": "NGL849210"
                    }
                ]
            },
            "liabilities": [
                {
                    "name": "Residential Mortgage",
                    "principal_outstanding": 220000.0,
                    "interest_rate": 0.045,
                    "monthly_emi": 1250.0,
                    "source": "NatWest Mortgage Services",
                    "mortgage_account_id": "NW-MTG-88912",
                    "portal_url": "https://www.natwest.com"
                }
            ],
            "protection": {
                "term_insurance_cover": 1000000.0,
                "has_health_insurance": True,
                "has_revolving_credit_card_debt": False,
                "term_insurance_source": "Legal & General Life (Policy #LG-489201)",
                "health_insurance_source": "Bupa Corporate Scheme"
            }
        }
    else:
        template = {
            "profile_name": "New_India_Client",
            "jurisdiction": "India",
            "client_info": {
                "age": 32,
                "target_retirement_age": 47,
                "monthly_expenses": 75000.0,
                "annual_income": 2400000.0,
                "tax_bracket": "30",
                "tax_regime": "New"
            },
            "assets": {
                "cash_and_emergency": [
                    {
                        "name": "Bank Fixed Deposit",
                        "amount": 500000.0,
                        "rate": 0.0725,
                        "source": "State Bank of India (SBI YONO)",
                        "account_id": "FD-984729184",
                        "portal_url": "https://retail.onlinesbi.sbi"
                    },
                    {
                        "name": "Arbitrage Mutual Fund",
                        "amount": 300000.0,
                        "rate": 0.07,
                        "source": "Zerodha Coin / CAMS",
                        "folio_number": "1849204/92",
                        "portal_url": "https://coin.zerodha.com"
                    }
                ],
                "equities": [
                    {
                        "name": "Nifty 50 Index Fund",
                        "amount": 2000000.0,
                        "expected_cagr": 0.12,
                        "source": "Kuvera / CAMS",
                        "folio_number": "UTI-8924719",
                        "isin": "INF209K01167"
                    },
                    {
                        "name": "Flexi Cap Fund",
                        "amount": 1000000.0,
                        "expected_cagr": 0.12,
                        "source": "Groww / KFintech",
                        "folio_number": "PPFAS-559102",
                        "isin": "INF879O01019"
                    }
                ],
                "pensions_and_retirement": [
                    {
                        "name": "EPF Balance",
                        "amount": 1000000.0,
                        "rate": 0.0825,
                        "source": "EPFO Member Portal",
                        "uan": "100984721940",
                        "portal_url": "https://unifiedportal-mem.epfindia.gov.in"
                    },
                    {
                        "name": "PPF",
                        "amount": 400000.0,
                        "rate": 0.071,
                        "source": "SBI Koramangala Branch",
                        "account_id": "PPF-309482109",
                        "portal_url": "https://retail.onlinesbi.sbi"
                    },
                    {
                        "name": "NPS Tier 1",
                        "amount": 250000.0,
                        "source": "Protean CRA (NSDL)",
                        "pran": "110098472109",
                        "portal_url": "https://cra-nsdl.com"
                    }
                ],
                "precious_metals": [
                    {
                        "name": "Sovereign Gold Bonds (SGB)",
                        "amount": 350000.0,
                        "source": "RBI Retail Direct / Zerodha Demat",
                        "isin_or_certificate": "IN0020200270 (SGB 2028 Series)",
                        "portal_url": "https://rbiretaildirect.org.in"
                    },
                    {
                        "name": "Silver ETF",
                        "amount": 75000.0,
                        "source": "Zerodha Kite",
                        "ticker": "SILVERBEES.NS"
                    }
                ],
                "real_estate": [
                    {
                        "name": "Self-occupied Apartment",
                        "amount": 12000000.0,
                        "is_primary": True,
                        "source": "Sub-Registrar Office Indiranagar / Title Deed",
                        "property_id": "BBMP Khata #8921/42A"
                    },
                    {
                        "name": "Listed REIT Units",
                        "amount": 250000.0,
                        "distribution_yield": 0.072,
                        "source": "Zerodha Demat",
                        "ticker": "NXST.NS"
                    }
                ],
                "digital_assets": [
                    {
                        "name": "Bitcoin (Cold Storage)",
                        "amount": 200000.0,
                        "cost_basis": 120000.0,
                        "source": "Ledger Nano X Hardware Wallet (Cold Storage)",
                        "tracking_label": "HODL Vault 1"
                    }
                ]
            },
            "liabilities": [
                {
                    "name": "Home Loan",
                    "principal_outstanding": 4000000.0,
                    "interest_rate": 0.0875,
                    "remaining_tenure_years": 18,
                    "monthly_emi": 36500.0,
                    "source": "State Bank of India Home Finance",
                    "loan_account_id": "HL-9982341209",
                    "portal_url": "https://homeloans.sbi"
                }
            ],
            "protection": {
                "term_insurance_cover": 25000000.0,
                "has_health_insurance": True,
                "has_revolving_credit_card_debt": False,
                "term_insurance_source": "HDFC Life Click2Protect (Policy #9847120)",
                "health_insurance_source": "Care Health Supreme (Policy #CH-389102)"
            }
        }

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2)
        return {
            "status": "success",
            "message": f"Profile template saved to {out.resolve()}",
            "file_path": str(out.resolve()),
            "template": template
        }
    return template


def load_profile(file_path: str) -> Dict[str, Any]:
    """Loads a client profile from a specified local file path."""
    p = Path(file_path)
    if not p.exists():
        return {"error": f"Profile file not found at {file_path}"}
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            data["_file_path"] = str(p.resolve())
            return data
    except Exception as e:
        return {"error": f"Failed to parse profile JSON: {str(e)}"}


def list_profiles(directory_path: Optional[str] = None) -> Dict[str, Any]:
    """Lists all local client profiles in the user-specified directory."""
    target_dir = Path(directory_path) if directory_path else get_default_profiles_dir()
    if not target_dir.exists():
        return {
            "directory": str(target_dir.resolve()),
            "profiles_found": 0,
            "profiles": [],
            "note": "Directory does not exist. Use profile-template to create one."
        }

    profiles = []
    for f in target_dir.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as pf:
                d = json.load(pf)
                profiles.append({
                    "file_name": f.name,
                    "full_path": str(f.resolve()),
                    "profile_name": d.get("profile_name", f.stem),
                    "jurisdiction": d.get("jurisdiction", "Unknown"),
                    "age": d.get("client_info", {}).get("age", "N/A"),
                    "last_modified": os.path.getmtime(f)
                })
        except Exception:
            continue

    return {
        "directory": str(target_dir.resolve()),
        "profiles_found": len(profiles),
        "profiles": profiles
    }


def evaluate_profile(file_path: str, inflation: float = 0.065, swr: float = 0.033) -> Dict[str, Any]:
    """Evaluates a stored client profile across FIRE readiness, allocation, and Money Health."""
    profile = load_profile(file_path)
    if "error" in profile:
        return profile

    jurisdiction = profile.get("jurisdiction", "India").lower()
    client_info = profile.get("client_info", {})
    assets = profile.get("assets", {})
    liabilities = profile.get("liabilities", [])
    protection = profile.get("protection", {})

    def sum_category(cat_name):
        items = assets.get(cat_name, [])
        return sum(item.get("amount", item.get("market_value", 0.0)) for item in items)

    cash_total = sum_category("cash_and_emergency")
    equities_total = sum_category("equities")
    isas_total = sum_category("isas")
    pensions_total = sum_category("pensions") + sum_category("pensions_and_retirement")
    gias_total = sum_category("gias")
    precious_metals_total = sum_category("precious_metals")
    digital_assets_total = sum_category("digital_assets")

    re_items = assets.get("real_estate", [])
    primary_residence_val = 0.0
    investment_re_val = 0.0
    for re_item in re_items:
        val = re_item.get("amount", re_item.get("market_value", 0.0))
        if re_item.get("is_primary", False):
            primary_residence_val += val
        else:
            investment_re_val += val

    financial_portfolio = (cash_total + equities_total + isas_total + pensions_total +
                           gias_total + precious_metals_total + digital_assets_total + investment_re_val)

    total_gross_assets = financial_portfolio + primary_residence_val
    total_debt = sum(l.get("principal_outstanding", 0.0) for l in liabilities)
    total_monthly_emi = sum(l.get("monthly_emi", l.get("monthly_payment", 0.0)) for l in liabilities)

    total_net_worth = total_gross_assets - total_debt

    allocation_pct = {}
    if financial_portfolio > 0:
        allocation_pct = {
            "cash_pct": round((cash_total / financial_portfolio) * 100.0, 1),
            "equities_pct": round(((equities_total + isas_total + gias_total) / financial_portfolio) * 100.0, 1),
            "pensions_pct": round((pensions_total / financial_portfolio) * 100.0, 1),
            "precious_metals_pct": round((precious_metals_total / financial_portfolio) * 100.0, 1),
            "crypto_pct": round((digital_assets_total / financial_portfolio) * 100.0, 1),
            "investment_real_estate_pct": round((investment_re_val / financial_portfolio) * 100.0, 1)
        }

    current_age = client_info.get("age", 35)
    target_retire_age = client_info.get("target_retirement_age", 50)
    years_to_retire = max(0, target_retire_age - current_age)

    if "monthly_expenses" in client_info:
        current_monthly_spend = client_info["monthly_expenses"]
        current_annual_spend = current_monthly_spend * 12.0
    else:
        current_annual_spend = client_info.get("annual_spend", 40000.0)
        current_monthly_spend = current_annual_spend / 12.0

    calibrated_inflation = 0.025 if jurisdiction in ["uk", "gb"] else inflation
    calibrated_swr = 0.035 if jurisdiction in ["uk", "gb"] else swr

    future_annual_spend = current_annual_spend * ((1.0 + calibrated_inflation) ** years_to_retire)
    fire_target = future_annual_spend / calibrated_swr

    growth_rate = 0.07 if jurisdiction in ["uk", "gb"] else 0.10
    portfolio_at_retirement = financial_portfolio * ((1.0 + growth_rate) ** years_to_retire)
    corpus_gap = max(0.0, fire_target - portfolio_at_retirement)

    monthly_r = (1.0 + growth_rate) ** (1.0 / 12.0) - 1.0
    n_months = years_to_retire * 12
    if corpus_gap > 0 and n_months > 0:
        required_monthly_sip = (corpus_gap * monthly_r) / ((1.0 + monthly_r) * ((1.0 + monthly_r)**n_months - 1.0))
    else:
        required_monthly_sip = 0.0

    annual_income = client_info.get("annual_income", client_info.get("gross_annual_income", current_annual_spend * 2.0))
    monthly_income = annual_income / 12.0
    term_cover = protection.get("term_insurance_cover", 0.0)
    has_health = protection.get("has_health_insurance", True)
    has_cc_debt = protection.get("has_revolving_credit_card_debt", False)
    equity_pct_val = allocation_pct.get("equities_pct", 60.0)

    mhs_result = calculate_money_health_score(
        monthly_income=monthly_income,
        monthly_expenses=current_monthly_spend,
        monthly_emi=total_monthly_emi,
        liquid_fund=cash_total,
        term_insurance_cover=term_cover,
        has_health_insurance=has_health,
        age=current_age,
        equity_percent=equity_pct_val,
        has_credit_card_debt=has_cc_debt
    )

    currency_sym = "£" if jurisdiction in ["uk", "gb"] else "₹"

    # Build Asset Tracking & Source Ledger
    tracking_ledger = []
    for cat_name, cat_items in assets.items():
        if not isinstance(cat_items, list):
            continue
        for itm in cat_items:
            ident = (
                itm.get("account_id") or itm.get("folio_number") or itm.get("isin") or
                itm.get("isin_or_certificate") or itm.get("ticker") or itm.get("property_id") or
                itm.get("title_number") or itm.get("policy_id") or itm.get("uan") or
                itm.get("pran") or itm.get("public_address") or itm.get("tracking_label") or "N/A"
            )
            tracking_ledger.append({
                "category": cat_name,
                "asset_name": itm.get("name", "Unnamed Asset"),
                f"value_{currency_sym}": itm.get("amount", itm.get("market_value", 0.0)),
                "source": itm.get("source", "Not Specified"),
                "account_or_identifier": ident,
                "portal_url": itm.get("portal_url", "N/A"),
                "notes": itm.get("type") or itm.get("notes") or ""
            })

    for l in liabilities:
        l_ident = (
            l.get("loan_account_id") or l.get("loan_account_number") or
            l.get("mortgage_account_id") or l.get("account_id") or "N/A"
        )
        rate_val = l.get('interest_rate_pct')
        if rate_val is None and 'interest_rate' in l:
            rate_val = round(l['interest_rate'] * 100, 2)
        tracking_ledger.append({
            "category": "liabilities",
            "asset_name": l.get("name", "Liability"),
            f"value_{currency_sym}": -abs(l.get("principal_outstanding", 0.0)),
            "source": l.get("lender") or l.get("source", "Not Specified"),
            "account_or_identifier": l_ident,
            "portal_url": l.get("portal_url", "N/A"),
            "notes": f"Rate: {rate_val}%, EMI: {currency_sym}{l.get('monthly_emi', l.get('monthly_payment', 0))}"
        })

    return {
        "profile_metadata": {
            "profile_name": profile.get("profile_name", Path(file_path).stem),
            "file_source": str(Path(file_path).resolve()),
            "jurisdiction": jurisdiction.upper(),
            "client_age": current_age,
            "target_retirement_age": target_retire_age,
            "years_to_fire": years_to_retire
        },
        "balance_sheet_summary": {
            f"liquid_financial_portfolio ({currency_sym})": round(financial_portfolio, 2),
            f"primary_residence_value (illiquid {currency_sym})": round(primary_residence_val, 2),
            f"gross_total_assets ({currency_sym})": round(total_gross_assets, 2),
            f"total_debt_liabilities ({currency_sym})": round(total_debt, 2),
            f"total_net_worth ({currency_sym})": round(total_net_worth, 2)
        },
        "asset_allocation_breakdown": allocation_pct,
        "fire_target_and_gap_analysis": {
            f"current_annual_spend ({currency_sym})": round(current_annual_spend, 2),
            f"future_annual_spend_at_retirement ({currency_sym})": round(future_annual_spend, 2),
            f"fire_target_corpus ({currency_sym})": round(fire_target, 2),
            f"projected_portfolio_at_retirement ({currency_sym})": round(portfolio_at_retirement, 2),
            f"corpus_gap ({currency_sym})": round(corpus_gap, 2),
            f"required_monthly_savings ({currency_sym})": round(required_monthly_sip, 2),
            "status": "FI on track!" if corpus_gap == 0 else f"Requires additional {currency_sym}{round(required_monthly_sip):,}/month savings"
        },
        "asset_tracking_source_ledger": {
            "total_tracked_assets_and_liabilities": len(tracking_ledger),
            "ledger": tracking_ledger,
            "protection_policies": {
                "term_life_source": protection.get("term_insurance_source", "N/A"),
                "health_insurance_source": protection.get("health_insurance_source", "N/A")
            }
        },
        "money_health_diagnostic": mhs_result
    }


def calculate_cross_border_dtaa(uk_pension_gbp: float = 0.0,
                                india_nro_income_inr: float = 0.0,
                                india_nre_income_inr: float = 0.0,
                                uk_tax_paid_gbp: float = 0.0,
                                india_tax_paid_inr: float = 0.0,
                                gbp_inr_rate: float = 105.0,
                                india_inflation: float = 0.065,
                                uk_inflation: float = 0.025,
                                years: int = 10,
                                is_uk_resident: bool = True,
                                has_trc: bool = False,
                                pension_type: str = "private",
                                uk_marginal_rate: float = 0.20,
                                india_marginal_rate: float = 0.30) -> Dict[str, Any]:
    """
    Evaluates cross-border taxation, statutory DTAA relief, NRE/NRO accounts, and currency PPP.
    - UK-India Double Tax Avoidance Agreement (DTAA):
        * Article 20: Private/occupational pensions are taxable ONLY in the country of residence.
        * Article 19: Government/civil service pensions are taxable in paying country.
        * Article 12: Interest income taxed at domestic 30% + cess (31.2%) or DTAA 15% with TRC + Form 10F.
    - Foreign Tax Credit (FTC): Under Section 90 / Form 67 (India) and TIOPA 2010 (UK):
        Relief = min(Foreign Tax Paid, Domestic Tax Payable on that income).
    - Purchasing Power Parity (PPP): Projected exchange rate over time T:
        Rate_T = Rate_0 * ((1 + i_INR) / (1 + i_GBP))^T
    """
    # 1. Currency Purchasing Power Parity (PPP) Projection
    inflation_ratio = (1.0 + india_inflation) / (1.0 + uk_inflation)
    projected_rate = gbp_inr_rate * (inflation_ratio ** years)
    annual_depreciation_pct = (inflation_ratio - 1.0) * 100.0

    current_pension_inr = uk_pension_gbp * gbp_inr_rate
    projected_pension_inr = uk_pension_gbp * projected_rate

    # 2. NRE Interest (Section 10(4)(ii) of Indian Income Tax Act)
    nre_india_tax = 0.0
    nre_gbp = india_nre_income_inr / gbp_inr_rate if gbp_inr_rate > 0 else 0.0
    nre_uk_tax = nre_gbp * uk_marginal_rate if is_uk_resident else 0.0

    # 3. NRO Interest TDS (Domestic Sec 195 vs DTAA Article 12)
    # Domestic: 30% + 4% cess = 31.2%
    # DTAA Article 12: 15% with valid TRC (Tax Residency Certificate) + Form 10F
    tds_rate = 0.15 if has_trc else 0.312
    nro_tds_deducted_inr = india_nro_income_inr * tds_rate
    nro_tds_deducted_gbp = nro_tds_deducted_inr / gbp_inr_rate if gbp_inr_rate > 0 else 0.0
    potential_tds_saving_inr = india_nro_income_inr * (0.312 - 0.15) if not has_trc else 0.0

    # 4. Pension DTAA Evaluation (Article 19 vs Article 20)
    pension_classification = pension_type.lower()
    pension_notes = []
    if pension_classification == "private":
        article_cited = "Article 20 (UK-India DTAA)"
        if is_uk_resident:
            pension_taxable_in = "UK Only"
            pension_uk_tax_liability = uk_pension_gbp * uk_marginal_rate
            pension_india_tax_liability = 0.0
            pension_notes.append("Under DTAA Article 20, UK private/occupational pensions are taxable ONLY in the UK for UK residents. Zero Indian tax.")
        else:
            pension_taxable_in = "India Only"
            pension_uk_tax_liability = 0.0
            pension_india_tax_liability = current_pension_inr * india_marginal_rate
            pension_notes.append("Under DTAA Article 20, UK private/occupational pensions are taxable ONLY in the state of residence (India).")
            pension_notes.append("ACTION: File HMRC Form 'India-Individual 2004' to claim treaty relief and obtain an 'NT' (No Tax) PAYE code in the UK to prevent UK tax withholding.")
    else:
        article_cited = "Article 19 (UK-India DTAA)"
        pension_taxable_in = "UK (Source State)"
        pension_uk_tax_liability = uk_pension_gbp * uk_marginal_rate
        if is_uk_resident:
            pension_india_tax_liability = 0.0
            pension_notes.append("Under DTAA Article 19, UK Government/Civil Service pensions are taxable in the UK. No Indian tax as UK resident.")
        else:
            pension_india_tax_liability = current_pension_inr * india_marginal_rate
            pension_notes.append("Under DTAA Article 19, UK Government pensions are taxable in the UK. When taxed in India on worldwide income, Foreign Tax Credit (FTC) under Section 90 / Form 67 applies.")

    # 5. Foreign Tax Credit (FTC) / Double Taxation Relief Calculation
    ftc_summary = {}
    recommendations = []

    if is_uk_resident:
        nro_gbp = india_nro_income_inr / gbp_inr_rate if gbp_inr_rate > 0 else 0.0
        uk_tax_on_nro = nro_gbp * uk_marginal_rate
        actual_india_tax_paid_inr = india_tax_paid_inr if india_tax_paid_inr > 0 else nro_tds_deducted_inr
        actual_india_tax_paid_gbp = actual_india_tax_paid_inr / gbp_inr_rate if gbp_inr_rate > 0 else 0.0

        uk_ftc_allowed = min(actual_india_tax_paid_gbp, uk_tax_on_nro)
        uk_net_tax_payable = max(0.0, uk_tax_on_nro - uk_ftc_allowed)
        unrelieved_foreign_tax_gbp = max(0.0, actual_india_tax_paid_gbp - uk_ftc_allowed)

        ftc_summary = {
            "residence_jurisdiction": "UK (HMRC)",
            "foreign_income_gbp": round(nro_gbp, 2),
            "uk_tax_liability_on_foreign_income": round(uk_tax_on_nro, 2),
            "foreign_tax_paid_gbp (India TDS)": round(actual_india_tax_paid_gbp, 2),
            "foreign_tax_credit_allowed_gbp": round(uk_ftc_allowed, 2),
            "net_uk_tax_payable_to_hmrc": round(uk_net_tax_payable, 2),
            "unrelieved_foreign_tax_drag_gbp": round(unrelieved_foreign_tax_gbp, 2),
            "double_tax_relief_mechanism": "Section 790 TIOPA 2010 / UK Double Taxation Relief"
        }

        if not has_trc and india_nro_income_inr > 0:
            recommendations.append(
                f"Obtain HMRC Certificate of Residence and file Form 10F online with Indian bank. "
                f"This caps NRO TDS at 15% instead of 31.2%, saving ₹{potential_tds_saving_inr:,.0f} and avoiding uncreditable foreign tax drag."
            )
        if india_nre_income_inr > 0:
            recommendations.append(
                f"India NRE interest (₹{india_nre_income_inr:,.0f}) is 100% tax-free in India under Sec 10(4)(ii), "
                f"but reportable in UK under worldwide income rules (£{round(nre_gbp, 2):,})."
            )

    else:
        uk_income_inr = current_pension_inr
        india_tax_on_uk_income = pension_india_tax_liability
        actual_uk_tax_paid_gbp = uk_tax_paid_gbp if uk_tax_paid_gbp > 0 else pension_uk_tax_liability
        actual_uk_tax_paid_inr = actual_uk_tax_paid_gbp * gbp_inr_rate

        india_ftc_allowed = min(actual_uk_tax_paid_inr, india_tax_on_uk_income)
        india_net_tax_payable = max(0.0, india_tax_on_uk_income - india_ftc_allowed)
        unrelieved_foreign_tax_inr = max(0.0, actual_uk_tax_paid_inr - india_ftc_allowed)

        ftc_summary = {
            "residence_jurisdiction": "India (Income Tax Department)",
            "foreign_income_inr": round(uk_income_inr, 2),
            "india_tax_liability_on_foreign_income": round(india_tax_on_uk_income, 2),
            "foreign_tax_paid_inr (UK HMRC)": round(actual_uk_tax_paid_inr, 2),
            "foreign_tax_credit_allowed_inr": round(india_ftc_allowed, 2),
            "net_india_tax_payable": round(india_net_tax_payable, 2),
            "unrelieved_foreign_tax_drag_inr": round(unrelieved_foreign_tax_inr, 2),
            "double_tax_relief_mechanism": "Section 90 of Income Tax Act 1961 read with Rule 128 (Mandatory Form 67 filing)"
        }

        if actual_uk_tax_paid_inr > 0:
            recommendations.append(
                "MANDATORY: Submit Form 67 online before filing Indian Income Tax Return (ITR) to claim Foreign Tax Credit under Section 90. Failure to submit Form 67 before the due date can result in FTC denial."
            )
        if pension_classification == "private":
            recommendations.append(
                "Submit HMRC Form 'India-Individual 2004' to claim DTAA Article 20 exemption in the UK so HMRC issues an NT (No Tax) PAYE code, avoiding unnecessary UK withholding."
            )

    return {
        "currency_ppp_projection": {
            "base_rate_gbp_inr": round(gbp_inr_rate, 2),
            "projection_years": years,
            "india_inflation_percent": round(india_inflation * 100, 2),
            "uk_inflation_percent": round(uk_inflation * 100, 2),
            "annual_inr_depreciation_percent": round(annual_depreciation_pct, 2),
            "projected_exchange_rate_in_years": round(projected_rate, 2),
            "uk_pension_current_annual_inr": round(current_pension_inr, 2),
            "uk_pension_future_annual_inr": round(projected_pension_inr, 2),
            "ppp_insight": f"Due to the {round((india_inflation - uk_inflation) * 100, 1)}% inflation differential, GBP/INR is projected to reach ₹{round(projected_rate, 1)} in {years} years. A fixed £{uk_pension_gbp:,.0f} pension grows in nominal INR terms from ₹{current_pension_inr/1e5:.1f}L to ₹{projected_pension_inr/1e5:.1f}L."
        },
        "nre_nro_banking_tax": {
            "nre_interest_inr": round(india_nre_income_inr, 2),
            "nre_tax_in_india": 0.0,
            "nre_statutory_exemption": "Section 10(4)(ii) of Indian Income Tax Act (100% Tax-Free in India)",
            "nre_taxable_in_uk": round(nre_uk_tax, 2) if is_uk_resident else 0.0,
            "nro_interest_inr": round(india_nro_income_inr, 2),
            "has_valid_trc_and_form_10f": has_trc,
            "applicable_nro_tds_rate_percent": round(tds_rate * 100, 1),
            "nro_tds_deducted_inr": round(nro_tds_deducted_inr, 2),
            "nro_tds_deducted_gbp": round(nro_tds_deducted_gbp, 2),
            "potential_tds_saving_with_trc_inr": round(potential_tds_saving_inr, 2)
        },
        "pension_dtaa_assessment": {
            "pension_type": pension_type,
            "dtaa_article": article_cited,
            "taxable_in": pension_taxable_in,
            "uk_tax_liability_gbp": round(pension_uk_tax_liability, 2),
            "india_tax_liability_inr": round(pension_india_tax_liability, 2),
            "treaty_guidance_notes": pension_notes
        },
        "double_tax_relief_ftc": ftc_summary,
        "actionable_compliance_steps": recommendations
    }


# ==============================================================================
# MAIN CLI DISPATCHER
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="UK & India F.I.R.E. Advisory Calculation Engine")
    subparsers = parser.add_subparsers(dest="command", help="Calculations")

    # Target
    p_target = subparsers.add_parser("target", help="Calculate FIRE target")
    p_target.add_argument("--spend", type=float, required=True, help="Desired annual spending")
    p_target.add_argument("--swr", type=float, default=0.035, help="Safe withdrawal rate (default 0.035)")
    p_target.add_argument("--state-pension", type=float, default=0.0, help="Expected annual state pension")

    # Date
    p_date = subparsers.add_parser("date", help="Calculate retirement age / years to FI")
    p_date.add_argument("--age", type=int, required=True, help="Current age")
    p_date.add_argument("--nw", type=float, required=True, help="Current net worth")
    p_date.add_argument("--savings", type=float, required=True, help="Annual savings")
    p_date.add_argument("--spend", type=float, required=True, help="Annual retirement spending")
    p_date.add_argument("--swr", type=float, default=0.035, help="Safe withdrawal rate")

    # Bridge
    p_bridge = subparsers.add_parser("bridge", help="Size the pre-57 pension bridge")
    p_bridge.add_argument("--retire-age", type=int, required=True, help="Target retirement age")
    p_bridge.add_argument("--spend", type=float, required=True, help="Annual spending")
    p_bridge.add_argument("--nmpa", type=int, default=57, help="NMPA age (default 57)")

    # Tax (UK)
    p_tax = subparsers.add_parser("tax", help="Compare Pension vs ISA (UK)")
    p_tax.add_argument("--gross", type=float, required=True, help="Gross amount (£)")
    p_tax.add_argument("--bracket", type=str, default="higher", choices=["basic", "higher", "60_trap", "additional"])

    # Mortgage
    p_mortgage = subparsers.add_parser("mortgage", help="Compare mortgage overpayment vs investing")
    p_mortgage.add_argument("--rate", type=float, required=True, help="Mortgage interest rate (percent)")
    p_mortgage.add_argument("--gross", type=float, required=True, help="Available gross funds")
    p_mortgage.add_argument("--bracket", type=str, default="higher")

    # Stress
    p_stress = subparsers.add_parser("stress", help="Simulate 30 percent Year 1 crash")
    p_stress.add_argument("--portfolio", type=float, required=True, help="Starting portfolio")
    p_stress.add_argument("--spend", type=float, required=True, help="Annual withdrawal")

    # Household (UK)
    p_house = subparsers.add_parser("household", help="Spousal pension equalization check (UK)")
    p_house.add_argument("--drawdown", type=float, required=True, help="Annual household pension drawdown")

    # Death Tax (Post-April 2027)
    p_deathtax = subparsers.add_parser("death-tax", help="Calculate effective death tax on pension vs ISA post-April 2027")
    p_deathtax.add_argument("--pot", type=float, required=True, help="Pension pot value")
    p_deathtax.add_argument("--beneficiary-rate", type=float, default=0.40, help="Beneficiary marginal rate (default 0.40)")
    p_deathtax.add_argument("--iht-rate", type=float, default=0.40, help="IHT rate (default 0.40)")
    p_deathtax.add_argument("--retiree-rate", type=float, default=0.20, help="Retiree income tax rate if drawn during life (default 0.20)")
    p_deathtax.add_argument("--estate", type=float, default=None, help="Total estate value including property and pension")
    p_deathtax.add_argument("--single", action="store_true", help="Set if single/unmarried (defaults to married/civil partner)")
    p_deathtax.add_argument("--spouse-beneficiary", action="store_true", help="Set if spouse/civil partner is the beneficiary (100 percent IHT exempt)")
    p_deathtax.add_argument("--death-pre-75", action="store_true", help="Set if modeling death before age 75 (income tax free to heir)")
    p_deathtax.add_argument("--has-gias", action="store_true", help="Set if household holds taxable GIAs")

    # Contrib Test (r > 0.75m & Non-Earner)
    p_contrib = subparsers.add_parser("contrib-test", help="Test pension contribution efficiency and non-earning spouse rules")
    p_contrib.add_argument("--relief", type=float, default=0.20, help="Tax relief going in (default 0.20)")
    p_contrib.add_argument("--marginal-out", type=float, default=0.20, help="Marginal rate in drawdown (default 0.20)")
    p_contrib.add_argument("--no-pcls", action="store_true", help="Set if PCLS is unavailable")
    p_contrib.add_argument("--non-earner", action="store_true", help="Model non-earning spouse (£2,880 net / £3,600 gross)")
    p_contrib.add_argument("--spouse-other-income", type=float, default=0.0, help="Non-earning spouse's other retirement income (£)")
    p_contrib.add_argument("--partner-pot", type=float, default=0.0, help="Higher-earning partner's pension pot")

    # Survivor Shock
    p_survivor = subparsers.add_parser("survivor", help="Model first death survivor shock")
    p_survivor.add_argument("--spend", type=float, required=True, help="Couple annual spending")
    p_survivor.add_argument("--sp1", type=float, default=11500.0, help="Partner 1 State Pension")
    p_survivor.add_argument("--sp2", type=float, default=11500.0, help="Partner 2 State Pension")
    p_survivor.add_argument("--db", type=float, default=0.0, help="Partner 1 DB Pension")

    # India Tax
    p_ind_tax = subparsers.add_parser("india-tax", help="Compare Old vs New Tax Regime for India (₹)")
    p_ind_tax.add_argument("--gross", type=float, required=True, help="Gross annual salary or CTC (₹)")
    p_ind_tax.add_argument("--basic", type=float, default=0.0, help="Basic annual salary for HRA (₹)")
    p_ind_tax.add_argument("--hra", type=float, default=0.0, help="Actual HRA received (₹)")
    p_ind_tax.add_argument("--rent", type=float, default=0.0, help="Actual annual rent paid (₹)")
    p_ind_tax.add_argument("--metro", action="store_true", help="Set if renting in a Metro city (Delhi/Mumbai/Kolkata/Chennai)")
    p_ind_tax.add_argument("--sec-80c", type=float, default=0.0, help="Section 80C investments (₹)")
    p_ind_tax.add_argument("--sec-80ccd", type=float, default=0.0, help="NPS Section 80CCD(1B) (₹)")
    p_ind_tax.add_argument("--sec-80d", type=float, default=0.0, help="Health insurance Section 80D (₹)")
    p_ind_tax.add_argument("--sec-24b", type=float, default=0.0, help="Home loan interest Section 24(b) (₹)")
    p_ind_tax.add_argument("--ay", type=str, default="2026-27", choices=["2026-27", "2025-26"], help="Assessment Year (default: 2026-27 / FY 2025-26)")
    p_ind_tax.add_argument("--is-ctc", action="store_true", help="Set if --gross represents Cost to Company (CTC) rather than Gross Taxable Salary")
    p_ind_tax.add_argument("--employer-pf", type=float, default=0.0, help="Employer EPF contribution in CTC (₹)")
    p_ind_tax.add_argument("--employer-nps", type=float, default=0.0, help="Employer NPS Section 80CCD(2) contribution (₹)")

    # India FIRE
    p_ind_fire = subparsers.add_parser("india-fire", help="Calculate India FIRE target & SIP gap (₹)")
    p_ind_fire.add_argument("--age", type=int, required=True, help="Current age")
    p_ind_fire.add_argument("--retire-age", type=int, required=True, help="Target retirement age")
    p_ind_fire.add_argument("--monthly-spend", type=float, required=True, help="Current monthly expenses (₹)")
    p_ind_fire.add_argument("--portfolio", type=float, default=0.0, help="Current portfolio value (₹)")
    p_ind_fire.add_argument("--inflation", type=float, default=0.065, help="Assumed inflation (default 0.065)")
    p_ind_fire.add_argument("--swr", type=float, default=0.033, help="Safe withdrawal rate (default 0.033)")

    # Loan Prepayment Analyzer
    p_loan = subparsers.add_parser("loan-prepay", help="Analyze reducing-balance loan prepayment savings")
    p_loan.add_argument("--principal", type=float, required=True, help="Outstanding loan principal")
    p_loan.add_argument("--rate", type=float, required=True, help="Annual interest rate (percent)")
    p_loan.add_argument("--tenure", type=float, required=True, help="Remaining tenure in years")
    p_loan.add_argument("--extra-monthly", type=float, default=0.0, help="Extra monthly prepayment")
    p_loan.add_argument("--lump-sum", type=float, default=0.0, help="Lump-sum prepayment today")

    # Money Health Score
    p_mhs = subparsers.add_parser("mhs", help="Calculate Money Health Score (0-100)")
    p_mhs.add_argument("--income", type=float, required=True, help="Monthly in-hand income")
    p_mhs.add_argument("--expenses", type=float, required=True, help="Monthly living expenses")
    p_mhs.add_argument("--emi", type=float, default=0.0, help="Monthly loan EMIs")
    p_mhs.add_argument("--liquid", type=float, required=True, help="Liquid savings / emergency fund")
    p_mhs.add_argument("--term-cover", type=float, default=0.0, help="Term life insurance cover amount")
    p_mhs.add_argument("--no-health-insurance", action="store_true", help="Set if no private health insurance")
    p_mhs.add_argument("--age", type=int, default=30, help="Current age")
    p_mhs.add_argument("--equity-pct", type=float, default=70.0, help="Current portfolio equity percent")
    p_mhs.add_argument("--credit-card-debt", action="store_true", help="Set if revolving unpaid credit card debt")

    # India Asset Compare
    p_asset = subparsers.add_parser("asset-compare", help="Compare post-tax real returns across Indian asset classes")
    p_asset.add_argument("--tax-bracket", type=str, default="30", choices=["30", "25", "20", "15", "10", "5", "0"], help="Marginal tax slab (percent)")
    p_asset.add_argument("--inflation", type=float, default=0.065, help="Assumed inflation (default 0.065)")

    # Real Estate Buy vs Rent Evaluator
    p_re = subparsers.add_parser("real-estate-eval", help="Evaluate Buy vs Rent and capital efficiency of Real Estate")
    p_re.add_argument("--price", type=float, required=True, help="Property purchase price (₹)")
    p_re.add_argument("--rent", type=float, required=True, help="Monthly rent for equivalent property (₹)")
    p_re.add_argument("--loan-rate", type=float, default=0.0875, help="Home loan interest rate (default 0.0875)")
    p_re.add_argument("--tenure", type=int, default=20, help="Loan tenure in years (default 20)")
    p_re.add_argument("--equity-cagr", type=float, default=0.12, help="Expected equity CAGR (default 0.12)")
    p_re.add_argument("--prop-cagr", type=float, default=0.06, help="Expected property appreciation (default 0.06)")

    # Crypto Tax Calculator (UK & India)
    p_crypto = subparsers.add_parser("crypto-tax", help="Calculate crypto/VDA statutory tax for UK or India")
    p_crypto.add_argument("--jurisdiction", type=str, required=True, choices=["uk", "india", "in", "bharat"], help="Tax jurisdiction")
    p_crypto.add_argument("--gain", type=float, required=True, help="Gross capital gains on profitable tokens")
    p_crypto.add_argument("--loss", type=float, default=0.0, help="Losses incurred on losing tokens")
    p_crypto.add_argument("--transfer-value", type=float, default=0.0, help="Total transaction / sale value for TDS")
    p_crypto.add_argument("--bracket", type=str, default="higher", choices=["basic", "higher"], help="UK tax bracket")

    # Profile Management Subparsers
    p_pro_temp = subparsers.add_parser("profile-template", help="Generate a blank profile template in your chosen local path")
    p_pro_temp.add_argument("--jurisdiction", type=str, default="india", choices=["india", "uk"], help="Tax jurisdiction template")
    p_pro_temp.add_argument("--output", type=str, help="Local file path to save the template (e.g. /path/to/profile.json)")

    p_pro_list = subparsers.add_parser("profile-list", help="List all local profiles in the user-specified directory")
    p_pro_list.add_argument("--dir", type=str, help="Local directory containing profiles (default: ./profiles or FIRE_PROFILES_DIR)")

    p_pro_show = subparsers.add_parser("profile-show", help="Load and view a local client profile JSON")
    p_pro_show.add_argument("--file", type=str, required=True, help="Local file path to client profile JSON")

    p_pro_eval = subparsers.add_parser("profile-eval", help="Evaluate a local client profile for FIRE readiness, allocation & MHS")
    p_pro_eval.add_argument("--file", type=str, required=True, help="Local file path to client profile JSON")
    p_pro_eval.add_argument("--inflation", type=float, default=0.065, help="Assumed inflation (default 0.065 for India)")
    p_pro_eval.add_argument("--swr", type=float, default=0.033, help="Safe withdrawal rate (default 0.033 for India)")

    # Cross-Border DTAA & Currency PPP
    p_cb = subparsers.add_parser("cross-border", help="Analyze cross-border DTAA, FTC, NRE/NRO taxation and currency PPP")
    p_cb.add_argument("--uk-pension", type=float, default=0.0, help="Annual UK pension in GBP")
    p_cb.add_argument("--india-nro", type=float, default=0.0, help="Annual India NRO interest/income in INR")
    p_cb.add_argument("--india-nre", type=float, default=0.0, help="Annual India NRE interest in INR")
    p_cb.add_argument("--uk-tax-paid", type=float, default=0.0, help="UK tax paid in GBP")
    p_cb.add_argument("--india-tax-paid", type=float, default=0.0, help="India tax paid in INR")
    p_cb.add_argument("--rate", type=float, default=105.0, help="GBP/INR exchange rate (default 105.0)")
    p_cb.add_argument("--india-inflation", type=float, default=0.065, help="Assumed India inflation (default 0.065)")
    p_cb.add_argument("--uk-inflation", type=float, default=0.025, help="Assumed UK inflation (default 0.025)")
    p_cb.add_argument("--years", type=int, default=10, help="PPP projection horizon in years (default 10)")
    p_cb.add_argument("--india-resident", action="store_true", help="Set if tax resident in India (default: UK resident)")
    p_cb.add_argument("--has-trc", action="store_true", help="Set if HMRC Tax Residency Certificate and Form 10F provided")
    p_cb.add_argument("--pension-type", type=str, default="private", choices=["private", "government"], help="Pension classification under DTAA")
    p_cb.add_argument("--uk-bracket", type=str, default="basic", choices=["basic", "higher", "additional"], help="UK marginal tax bracket")
    p_cb.add_argument("--india-bracket", type=float, default=0.30, help="India marginal tax rate (e.g. 0.30)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    import json
    if args.command == "target":
        res = calculate_fire_target(args.spend, args.swr, args.state_pension)
    elif args.command == "date":
        res = calculate_retirement_date(args.age, args.nw, args.savings, args.spend, args.swr)
    elif args.command == "bridge":
        res = calculate_pension_bridge(args.retire_age, args.nmpa, args.spend)
    elif args.command == "tax":
        res = compare_pension_vs_isa(args.gross, args.bracket)
    elif args.command == "mortgage":
        res = compare_mortgage_vs_investing(0.0, args.rate, args.gross, args.bracket)
    elif args.command == "stress":
        res = stress_test_crash(args.portfolio, args.spend)
    elif args.command == "household":
        res = household_pension_equalization(args.drawdown)
    elif args.command == "death-tax":
        res = calculate_pension_death_tax(args.pot, beneficiary_tax_rate=args.beneficiary_rate,
                                          iht_rate=args.iht_rate, retiree_tax_rate_during_life=args.retiree_rate,
                                          estate_value=args.estate, married_or_civil_partner=not args.single,
                                          spouse_is_beneficiary=args.spouse_beneficiary,
                                          death_pre_75=args.death_pre_75, has_taxable_gias=args.has_gias)
    elif args.command == "contrib-test":
        res = test_contribution_law(args.relief, args.marginal_out, pcls_available=not args.no_pcls,
                                    is_non_earning_spouse=args.non_earner,
                                    spouse_other_retirement_income=args.spouse_other_income,
                                    partner_pension_pot=args.partner_pot)
    elif args.command == "survivor":
        res = calculate_survivor_shock(args.spend, args.sp1, args.sp2, args.db)
    elif args.command == "india-tax":
        res = calculate_india_tax(args.gross, args.basic, args.hra, args.rent, args.metro,
                                  args.sec_80c, args.sec_80ccd, args.sec_80d, args.sec_24b,
                                  ay=args.ay, is_ctc=args.is_ctc, employer_pf=args.employer_pf,
                                  employer_nps_80ccd2=args.employer_nps)
    elif args.command == "india-fire":
        res = calculate_india_fire(args.age, args.retire_age, args.monthly_spend, args.portfolio,
                                   args.inflation, args.swr)
    elif args.command == "loan-prepay":
        res = calculate_loan_prepayment(args.principal, args.rate, args.tenure, args.extra_monthly, args.lump_sum)
    elif args.command == "mhs":
        res = calculate_money_health_score(args.income, args.expenses, args.emi, args.liquid,
                                           args.term_cover, not args.no_health_insurance,
                                           args.age, args.equity_pct, args.credit_card_debt)
    elif args.command == "asset-compare":
        res = calculate_india_asset_returns(args.tax_bracket, args.inflation)
    elif args.command == "real-estate-eval":
        res = calculate_buy_vs_rent_real_estate(args.price, args.rent, args.loan_rate, args.tenure,
                                                args.equity_cagr, args.prop_cagr)
    elif args.command == "crypto-tax":
        res = calculate_crypto_tax(args.jurisdiction, args.gain, args.loss, args.transfer_value, args.bracket)
    elif args.command == "profile-template":
        res = generate_profile_template(args.jurisdiction, args.output)
    elif args.command == "profile-list":
        res = list_profiles(args.dir)
    elif args.command == "profile-show":
        res = load_profile(args.file)
    elif args.command == "profile-eval":
        res = evaluate_profile(args.file, args.inflation, args.swr)
    elif args.command == "cross-border":
        uk_rates = {"basic": 0.20, "higher": 0.40, "additional": 0.45}
        uk_marginal = uk_rates.get(args.uk_bracket, 0.20)
        res = calculate_cross_border_dtaa(
            uk_pension_gbp=args.uk_pension,
            india_nro_income_inr=args.india_nro,
            india_nre_income_inr=args.india_nre,
            uk_tax_paid_gbp=args.uk_tax_paid,
            india_tax_paid_inr=args.india_tax_paid,
            gbp_inr_rate=args.rate,
            india_inflation=args.india_inflation,
            uk_inflation=args.uk_inflation,
            years=args.years,
            is_uk_resident=not args.india_resident,
            has_trc=args.has_trc,
            pension_type=args.pension_type,
            uk_marginal_rate=uk_marginal,
            india_marginal_rate=args.india_bracket
        )

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
