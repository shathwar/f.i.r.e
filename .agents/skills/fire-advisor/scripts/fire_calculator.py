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
import math
import sys
from typing import Dict, Any, Tuple


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
                                iht_rate: float = 0.40) -> Dict[str, Any]:
    """Computes effective death tax on inherited pension vs inherited ISA post-April 2027."""
    iht_paid_pension = pot_value * iht_rate
    post_iht_pension = pot_value - iht_paid_pension
    income_tax_paid = post_iht_pension * beneficiary_tax_rate
    net_pension_to_heir = post_iht_pension - income_tax_paid
    effective_pension_tax_rate = (pot_value - net_pension_to_heir) / pot_value
    
    iht_paid_isa = pot_value * iht_rate
    net_isa_to_heir = pot_value - iht_paid_isa
    effective_isa_tax_rate = iht_rate
    
    advantage_of_isa = net_isa_to_heir - net_pension_to_heir
    pct_more_wealth = ((net_isa_to_heir - net_pension_to_heir) / net_pension_to_heir) * 100
    
    return {
        "pot_value": pot_value,
        "beneficiary_tax_rate_percent": beneficiary_tax_rate * 100,
        "iht_rate_percent": iht_rate * 100,
        "pension_net_to_heir": round(net_pension_to_heir, 2),
        "effective_pension_death_tax_percent": round(effective_pension_tax_rate * 100, 1),
        "isa_net_to_heir": round(net_isa_to_heir, 2),
        "effective_isa_death_tax_percent": round(effective_isa_tax_rate * 100, 1),
        "isa_bequest_advantage_pounds": round(advantage_of_isa, 2),
        "isa_bequest_advantage_percent": round(pct_more_wealth, 1),
        "decision_rule": "Draw pension during life at 20% basic rate and recycle into ISA to avoid the 64% combined death tax!"
    }


def test_contribution_law(relief_rate: float, retirement_marginal_rate: float, 
                          pcls_available: bool = True) -> Dict[str, Any]:
    """Evaluates the r > 0.75m contribution law."""
    cost = 1.0 - relief_rate
    if pcls_available:
        payout = 0.25 + (0.75 * (1.0 - retirement_marginal_rate))
        breakeven_m = relief_rate / 0.75
    else:
        payout = 1.0 - retirement_marginal_rate
        breakeven_m = relief_rate
        
    net_return_percent = ((payout - cost) / cost) * 100
    is_favorable = relief_rate > (0.75 * retirement_marginal_rate if pcls_available else retirement_marginal_rate)
    
    return {
        "relief_going_in_percent": relief_rate * 100,
        "retirement_marginal_rate_percent": retirement_marginal_rate * 100,
        "pcls_available": pcls_available,
        "cash_cost_per_pound_gross": round(cost, 3),
        "net_payout_per_pound_gross": round(payout, 3),
        "immediate_net_return_percent": round(net_return_percent, 2),
        "breakeven_marginal_rate_percent": round(breakeven_m * 100, 1),
        "verdict": "Contribute (Value accretive)" if is_favorable else "DO NOT Contribute (Value destructive)"
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

def calculate_india_tax(gross_income: float, basic_salary: float = 0.0, hra_received: float = 0.0,
                        rent_paid: float = 0.0, is_metro: bool = True, sec_80c: float = 0.0,
                        sec_80ccd_1b: float = 0.0, sec_80d: float = 0.0, sec_24b: float = 0.0) -> Dict[str, Any]:
    """
    Compares Old vs New Tax Regime for Indian residents (FY24-25 / FY25-26).
    Includes ₹75k standard deduction (New) vs ₹50k (Old), Section 87A rebate, and HRA min formula.
    """
    # 1. New Tax Regime (Default)
    std_ded_new = 75000.0
    taxable_new = max(0.0, gross_income - std_ded_new)
    
    # Slabs: 0-3L (0%), 3L-7L (5%), 7L-10L (10%), 10L-12L (15%), 12L-15L (20%), >15L (30%)
    tax_new = 0.0
    if taxable_new > 1500000:
        tax_new += (taxable_new - 1500000) * 0.30 + 300000 * 0.20 + 200000 * 0.15 + 300000 * 0.10 + 400000 * 0.05
    elif taxable_new > 1200000:
        tax_new += (taxable_new - 1200000) * 0.20 + 200000 * 0.15 + 300000 * 0.10 + 400000 * 0.05
    elif taxable_new > 1000000:
        tax_new += (taxable_new - 1000000) * 0.15 + 300000 * 0.10 + 400000 * 0.05
    elif taxable_new > 700000:
        tax_new += (taxable_new - 700000) * 0.10 + 400000 * 0.05
    elif taxable_new > 300000:
        tax_new += (taxable_new - 300000) * 0.05

    # Section 87A rebate up to ₹7,00,000 taxable income
    if taxable_new <= 700000:
        tax_new = 0.0

    cess_new = tax_new * 0.04
    total_tax_new = tax_new + cess_new

    # 2. Old Tax Regime
    std_ded_old = 50000.0
    hra_exemption = 0.0
    if hra_received > 0 and rent_paid > 0 and basic_salary > 0:
        excess_rent = max(0.0, rent_paid - (0.10 * basic_salary))
        salary_pct = (0.50 if is_metro else 0.40) * basic_salary
        hra_exemption = min(hra_received, excess_rent, salary_pct)

    c_80c = min(150000.0, sec_80c)
    c_80ccd = min(50000.0, sec_80ccd_1b)
    c_80d = min(75000.0, sec_80d)
    c_24b = min(200000.0, sec_24b)

    total_deductions_old = std_ded_old + hra_exemption + c_80c + c_80ccd + c_80d + c_24b
    taxable_old = max(0.0, gross_income - total_deductions_old)

    # Slabs: 0-2.5L (0%), 2.5L-5L (5%), 5L-10L (20%), >10L (30%)
    tax_old = 0.0
    if taxable_old > 1000000:
        tax_old += (taxable_old - 1000000) * 0.30 + 500000 * 0.20 + 250000 * 0.05
    elif taxable_old > 500000:
        tax_old += (taxable_old - 500000) * 0.20 + 250000 * 0.05
    elif taxable_old > 250000:
        tax_old += (taxable_old - 250000) * 0.05

    if taxable_old <= 500000:
        tax_old = 0.0

    cess_old = tax_old * 0.04
    total_tax_old = tax_old + cess_old

    tax_diff = total_tax_old - total_tax_new
    recommendation = "New Regime" if total_tax_new <= total_tax_old else "Old Regime"
    savings = abs(tax_diff)

    return {
        "gross_income": gross_income,
        "new_regime": {
            "standard_deduction": std_ded_new,
            "taxable_income": round(taxable_new, 2),
            "base_tax": round(tax_new, 2),
            "cess_4_percent": round(cess_new, 2),
            "total_tax": round(total_tax_new, 2),
        },
        "old_regime": {
            "total_deductions": round(total_deductions_old, 2),
            "hra_exemption": round(hra_exemption, 2),
            "sec_80c": round(c_80c, 2),
            "sec_80ccd_1b": round(c_80ccd, 2),
            "sec_80d": round(c_80d, 2),
            "sec_24b_home_loan": round(c_24b, 2),
            "taxable_income": round(taxable_old, 2),
            "base_tax": round(tax_old, 2),
            "cess_4_percent": round(cess_old, 2),
            "total_tax": round(total_tax_old, 2),
        },
        "recommended_regime": recommendation,
        "annual_tax_saving": round(savings, 2)
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
            "Residential real estate rental yield (1.8-2.2 percent net) locks up ~50 percent more capital than an equity/REIT financial independence portfolio."
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

    # Contrib Test (r > 0.75m)
    p_contrib = subparsers.add_parser("contrib-test", help="Test r > 0.75m contribution law")
    p_contrib.add_argument("--relief", type=float, required=True, help="Tax relief going in (e.g. 0.20 or 0.40)")
    p_contrib.add_argument("--marginal-out", type=float, required=True, help="Marginal rate in drawdown (e.g. 0.20 or 0.40)")
    p_contrib.add_argument("--no-pcls", action="store_true", help="Set if PCLS is unavailable")

    # Survivor Shock
    p_survivor = subparsers.add_parser("survivor", help="Model first death survivor shock")
    p_survivor.add_argument("--spend", type=float, required=True, help="Couple annual spending")
    p_survivor.add_argument("--sp1", type=float, default=11500.0, help="Partner 1 State Pension")
    p_survivor.add_argument("--sp2", type=float, default=11500.0, help="Partner 2 State Pension")
    p_survivor.add_argument("--db", type=float, default=0.0, help="Partner 1 DB Pension")

    # India Tax
    p_ind_tax = subparsers.add_parser("india-tax", help="Compare Old vs New Tax Regime for India (₹)")
    p_ind_tax.add_argument("--gross", type=float, required=True, help="Gross annual CTC / income (₹)")
    p_ind_tax.add_argument("--basic", type=float, default=0.0, help="Basic annual salary for HRA (₹)")
    p_ind_tax.add_argument("--hra", type=float, default=0.0, help="Actual HRA received (₹)")
    p_ind_tax.add_argument("--rent", type=float, default=0.0, help="Actual annual rent paid (₹)")
    p_ind_tax.add_argument("--metro", action="store_true", help="Set if renting in a Metro city (Delhi/Mumbai/Kolkata/Chennai)")
    p_ind_tax.add_argument("--sec-80c", type=float, default=0.0, help="Section 80C investments (₹)")
    p_ind_tax.add_argument("--sec-80ccd", type=float, default=0.0, help="NPS Section 80CCD(1B) (₹)")
    p_ind_tax.add_argument("--sec-80d", type=float, default=0.0, help="Health insurance Section 80D (₹)")
    p_ind_tax.add_argument("--sec-24b", type=float, default=0.0, help="Home loan interest Section 24(b) (₹)")

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
    p_asset.add_argument("--tax-bracket", type=str, default="30", choices=["30", "20", "15", "10", "5", "0"], help="Marginal tax slab (percent)")
    p_asset.add_argument("--inflation", type=float, default=0.065, help="Assumed inflation (default 0.065)")

    # Real Estate Buy vs Rent Evaluator
    p_re = subparsers.add_parser("real-estate-eval", help="Evaluate Buy vs Rent and capital efficiency of Real Estate")
    p_re.add_argument("--price", type=float, required=True, help="Property purchase price (₹)")
    p_re.add_argument("--rent", type=float, required=True, help="Monthly rent for equivalent property (₹)")
    p_re.add_argument("--loan-rate", type=float, default=0.0875, help="Home loan interest rate (default 0.0875)")
    p_re.add_argument("--tenure", type=int, default=20, help="Loan tenure in years (default 20)")
    p_re.add_argument("--equity-cagr", type=float, default=0.12, help="Expected equity CAGR (default 0.12)")
    p_re.add_argument("--prop-cagr", type=float, default=0.06, help="Expected property appreciation (default 0.06)")

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
        res = calculate_pension_death_tax(args.pot, args.beneficiary_rate, args.iht_rate)
    elif args.command == "contrib-test":
        res = test_contribution_law(args.relief, args.marginal_out, not args.no_pcls)
    elif args.command == "survivor":
        res = calculate_survivor_shock(args.spend, args.sp1, args.sp2, args.db)
    elif args.command == "india-tax":
        res = calculate_india_tax(args.gross, args.basic, args.hra, args.rent, args.metro,
                                  args.sec_80c, args.sec_80ccd, args.sec_80d, args.sec_24b)
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

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
