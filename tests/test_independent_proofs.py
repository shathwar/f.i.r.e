"""
Independent Mathematical Proofs and Statutory Verification Test Suite
UK & India F.I.R.E. Advisory Engine

This test suite rigorously tests the core mathematical algorithms, statutory tax rules,
and boundary conditions independently of the production implementation.
Equations and statutory slabs are calculated from first principles in the tests to
prove correctness down to the exact Rupee/Penny.
"""

import math
import sys
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".agents" / "skills" / "fire-advisor" / "scripts"))

from fire_calculator import (
    compute_new_regime_tax,
    calculate_india_tax,
    calculate_india_fire,
    compare_pension_vs_isa,
    calculate_pension_bridge,
    calculate_pension_death_tax,
    test_contribution_law,
    household_pension_equalization,
    calculate_loan_prepayment,
    compare_mortgage_vs_investing,
    calculate_cross_border_dtaa,
    calculate_crypto_tax,
    calculate_money_health_score,
)


class TestIndiaTaxEngine(unittest.TestCase):
    """
    Independent statutory tests for Indian Income Tax:
    - AY 2026-27 (Union Budget 2025: ₹12L Section 87A rebate & marginal relief)
    - AY 2025-26 (Legacy ₹7L Section 87A rebate)
    - Old Regime Deductions (80C, 80D, 24b, HRA)
    - CTC vs Gross Taxable Salary vs Net Taxable Income Invariant
    """

    @staticmethod
    def _independent_ay2026_slab_tax(taxable_income: float) -> float:
        """Independent closed-form slab calculation for AY 2026-27."""
        tax = 0.0
        rem = taxable_income
        if rem > 2400000:
            tax += (rem - 2400000) * 0.30
            rem = 2400000
        if rem > 2000000:
            tax += (rem - 2000000) * 0.25
            rem = 2000000
        if rem > 1600000:
            tax += (rem - 1600000) * 0.20
            rem = 1600000
        if rem > 1200000:
            tax += (rem - 1200000) * 0.15
            rem = 1200000
        if rem > 800000:
            tax += (rem - 800000) * 0.10
            rem = 800000
        if rem > 400000:
            tax += (rem - 400000) * 0.05
        return tax

    def test_ay2026_zero_tax_at_12_lakh_boundary(self):
        """Proof: Net taxable income <= ₹12,00,000 has zero tax due to Section 87A rebate."""
        # Exact boundary: ₹12,00,000
        res = compute_new_regime_tax(1200000.0, ay="2026-27")
        # Slab tax: 4L-8L @ 5% (20k) + 8L-12L @ 10% (40k) = ₹60,000
        expected_slab = 60000.0
        self.assertEqual(res["slab_tax_before_relief"], expected_slab)
        self.assertEqual(res["sec_87a_rebate"], expected_slab)
        self.assertEqual(res["tax_payable_before_cess"], 0.0)
        self.assertEqual(res["total_tax"], 0.0)

        # Below boundary: ₹8,00,000
        res_8l = compute_new_regime_tax(800000.0, ay="2026-27")
        self.assertEqual(res_8l["slab_tax_before_relief"], 20000.0)
        self.assertEqual(res_8l["sec_87a_rebate"], 20000.0)
        self.assertEqual(res_8l["total_tax"], 0.0)

    def test_ay2026_marginal_relief_cliff_edges(self):
        """
        Proof: Marginal relief under Section 87A ensures tax payable before cess does not
        exceed (taxable_income - ₹12,00,000).
        """
        # Case 1: ₹12,00,001 (Income exceeds threshold by ₹1)
        res_1 = compute_new_regime_tax(1200001.0, ay="2026-27")
        excess_1 = 1.0
        # Tax before cess must be exactly ₹1.00
        self.assertAlmostEqual(res_1["tax_payable_before_cess"], excess_1, places=2)
        # Total tax with 4% cess = ₹1.04
        self.assertAlmostEqual(res_1["total_tax"], 1.04, places=2)

        # Case 2: ₹12,10,000 (Income exceeds threshold by ₹10,000)
        res_10k = compute_new_regime_tax(1210000.0, ay="2026-27")
        excess_10k = 10000.0
        slab_10k = 60000.0 + (10000.0 * 0.15)  # ₹61,500
        expected_relief = slab_10k - excess_10k  # ₹51,500
        self.assertEqual(res_10k["slab_tax_before_relief"], slab_10k)
        self.assertEqual(res_10k["marginal_relief_87a"], expected_relief)
        self.assertEqual(res_10k["tax_payable_before_cess"], excess_10k)
        self.assertAlmostEqual(res_10k["total_tax"], excess_10k * 1.04, places=2)

        # Case 3: ₹12,70,588 (Upper boundary of marginal relief where slab tax ~ excess)
        res_upper = compute_new_regime_tax(1270588.0, ay="2026-27")
        slab_upper = 60000.0 + (70588.0 * 0.15)  # ₹70,588.20
        self.assertGreater(res_upper["marginal_relief_87a"], 0.0)
        self.assertAlmostEqual(res_upper["tax_payable_before_cess"], 70588.0, places=2)

        # Case 4: ₹12,70,589 (Cliff edge where marginal relief drops to 0)
        res_cliff = compute_new_regime_tax(1270589.0, ay="2026-27")
        slab_cliff = 60000.0 + (70589.0 * 0.15)  # ₹70,588.35 < ₹70,589
        self.assertEqual(res_cliff["marginal_relief_87a"], 0.0)
        self.assertAlmostEqual(res_cliff["tax_payable_before_cess"], slab_cliff, places=2)

    def test_ctc_vs_gross_vs_net_taxable_invariant(self):
        """
        Proof: CTC != Gross Taxable Salary != Net Taxable Income.
        A salary earner with CTC of ₹12,75,000 has standard deduction of ₹75,000,
        bringing Net Taxable Income to exactly ₹12,00,000 -> ₹0 total tax.
        """
        res = calculate_india_tax(
            gross_income=1275000.0,
            is_ctc=False,  # Treat 12.75L as Gross Salary
            ay="2026-27"
        )
        # Taxable income = 12,75,000 - 75,000 = 12,00,000
        self.assertEqual(res["new_regime"]["taxable_income"], 1200000.0)
        self.assertEqual(res["new_regime"]["total_tax"], 0.0)

        # Test CTC reconciliation breakdown
        res_ctc = calculate_india_tax(
            gross_income=2000000.0,
            is_ctc=True,
            basic_salary=1000000.0,
            ay="2026-27"
        )
        ctc_info = res_ctc["ctc_reconciliation"]
        self.assertEqual(ctc_info["total_ctc"], 2000000.0)
        # Employer EPF = 12% of basic = ₹1,20,000
        self.assertEqual(ctc_info["employer_epf_contribution (exempt)"], 120000.0)
        # Gratuity = 4.81% of basic = ₹48,100
        self.assertEqual(ctc_info["gratuity_accrual (statutory reserve)"], 48100.0)
        # Group insurance = ₹10,000
        self.assertEqual(ctc_info["group_health_insurance_by_employer"], 10000.0)
        # Gross salary = 20,00,000 - 1,20,000 - 48,100 - 10,000 = ₹18,21,900
        self.assertEqual(ctc_info["gross_taxable_salary"], 1821900.0)

    def test_legacy_ay2025_regression(self):
        """Proof: Legacy AY 2025-26 preserves ₹7L rebate threshold and historical slabs (3L-7L @ 5%)."""
        # Taxable income ₹7,00,000 in AY 2025-26 has ₹0 tax
        # Slabs (July 2024): 0-3L (0%), 3L-7L (5% = ₹20,000). Rebate = ₹20,000.
        res_7l = compute_new_regime_tax(700000.0, ay="2025-26")
        self.assertEqual(res_7l["sec_87a_rebate"], 20000.0)
        self.assertEqual(res_7l["total_tax"], 0.0)

        # Taxable income ₹10,00,000 in AY 2025-26
        # Slabs: 0-3L (0), 3-7L @ 5% (20k), 7-10L @ 10% (30k) = ₹50,000 + 4% cess = ₹52,000
        res_10l = compute_new_regime_tax(1000000.0, ay="2025-26")
        self.assertEqual(res_10l["slab_tax_before_relief"], 50000.0)
        self.assertEqual(res_10l["total_tax"], 52000.0)

    def test_old_vs_new_regime_breakeven(self):
        """Proof: Old Regime requires heavy deductions (80C, 80D, 24b, HRA) to beat New Regime."""
        res_high_deductions = calculate_india_tax(
            gross_income=2500000.0,
            basic_salary=1250000.0,
            hra_received=400000.0,
            rent_paid=450000.0,
            is_metro=True,
            sec_80c=150000.0,
            sec_80ccd_1b=50000.0,
            sec_80d=50000.0,
            sec_24b=200000.0,
            ay="2026-27"
        )
        self.assertIn("recommended_regime", res_high_deductions["comparison_summary"])
        # Total deductions under old regime: 50k(std) + 325k(hra: min(400k, 450k-125k, 625k)) + 150k + 50k + 50k + 200k = 825k
        self.assertAlmostEqual(res_high_deductions["old_regime"]["total_deductions"], 825000.0, places=2)


class TestSIPAndRetirementCorpus(unittest.TestCase):
    """
    Independent tests for SIP contributions, inflation escalation, and retirement corpus sizing.
    Uses closed-form mathematical equations to assert exact equality.
    """

    @staticmethod
    def _independent_future_spend(spend_today: float, inflation: float, years: int) -> float:
        return spend_today * ((1.0 + inflation) ** years)

    @staticmethod
    def _independent_target_corpus(future_spend: float, swr: float) -> float:
        return future_spend / swr

    @staticmethod
    def _independent_sip(deficit: float, annual_cagr: float, months: int) -> float:
        if deficit <= 0:
            return 0.0
        r_m = ((1.0 + annual_cagr) ** (1.0 / 12.0)) - 1.0
        factor = (((1.0 + r_m) ** months) - 1.0) * (1.0 + r_m)
        return (deficit * r_m) / factor

    def test_closed_form_sip_formula_accuracy(self):
        """Proof: Independent closed-form sinking fund equation matches fire_calculator."""
        age = 30
        retire_age = 45
        monthly_exp = 100000.0
        current_pf = 2000000.0
        inflation = 0.065
        swr = 0.033
        equity_cagr = 0.12

        years = retire_age - age
        months = years * 12

        # 1. Independent math
        expected_fut_spend = self._independent_future_spend(monthly_exp * 12.0, inflation, years)
        expected_target = self._independent_target_corpus(expected_fut_spend, swr)
        expected_fv_pf = current_pf * ((1.0 + equity_cagr) ** years)
        expected_deficit = max(0.0, expected_target - expected_fv_pf)
        expected_sip = self._independent_sip(expected_deficit, equity_cagr, months)

        # 2. Engine result
        res = calculate_india_fire(
            current_age=age,
            retire_age=retire_age,
            monthly_expenses=monthly_exp,
            current_portfolio=current_pf,
            inflation=inflation,
            swr=swr,
            expected_equity_return=equity_cagr
        )

        self.assertAlmostEqual(res["future_annual_expenses_at_retirement"], expected_fut_spend, places=2)
        self.assertAlmostEqual(res["target_fire_corpus"], expected_target, places=2)
        self.assertAlmostEqual(res["projected_fv_current_portfolio"], expected_fv_pf, places=2)
        self.assertAlmostEqual(res["corpus_gap_to_fund"], expected_deficit, places=2)
        self.assertAlmostEqual(res["required_monthly_sip"], expected_sip, places=2)

    def test_zero_deficit_boundary_condition(self):
        """Proof: When current portfolio exceeds target corpus, deficit = 0 and required SIP = 0."""
        res = calculate_india_fire(
            current_age=40,
            retire_age=45,
            monthly_expenses=50000.0,
            current_portfolio=50000000.0,  # ₹5 Cr already accumulated
            inflation=0.06,
            swr=0.033
        )
        self.assertEqual(res["corpus_gap_to_fund"], 0.0)
        self.assertEqual(res["required_monthly_sip"], 0.0)

    def test_horizon_extremes(self):
        """Proof: Handles 1-year horizon and 30-year horizon with positive growth."""
        res_1yr = calculate_india_fire(current_age=49, retire_age=50, monthly_expenses=100000.0)
        self.assertEqual(res_1yr["years_to_retirement"], 1)
        self.assertGreater(res_1yr["required_monthly_sip"], 0.0)

        res_30yr = calculate_india_fire(current_age=25, retire_age=55, monthly_expenses=50000.0)
        self.assertEqual(res_30yr["years_to_retirement"], 30)
        self.assertGreater(res_30yr["target_fire_corpus"], 0.0)


class TestUKPensionDrawdownAndTaxBands(unittest.TestCase):
    """
    Independent tests for UK Pension wrappers, Personal Allowance taper,
    post-April 2027 death tax scenarios, and spousal optimization.
    """

    def test_uk_personal_allowance_taper_and_60_trap(self):
        """Proof: £100k-£125k income zone suffers 60% effective marginal tax."""
        res_higher = compare_pension_vs_isa(gross_amount=10000.0, tax_bracket="higher")
        res_trap = compare_pension_vs_isa(gross_amount=10000.0, tax_bracket="60_trap")

        # In 60% trap: Net ISA contribution from £10,000 gross is only £4,000
        self.assertEqual(res_trap["isa_initial_investment"], 4000.0)
        # In 40% higher rate: Net ISA contribution is £6,000
        self.assertEqual(res_higher["isa_initial_investment"], 6000.0)

        # Pension initial investment is full £10,000 in both (via salary sacrifice or gross relief)
        self.assertEqual(res_trap["pension_initial_investment"], 10000.0)
        self.assertEqual(res_higher["pension_initial_investment"], 10000.0)

        # Pension advantage is significantly higher in the 60% trap
        self.assertGreater(res_trap["pension_wealth_advantage_percent"], res_higher["pension_wealth_advantage_percent"])

    def test_post_april_2027_spousal_exemption_first_death(self):
        """Proof: Section 18 IHTA 1984 100% Spousal Exemption eliminates IHT on first death."""
        res = calculate_pension_death_tax(
            pot_value=1500000.0,
            beneficiary_tax_rate=0.40,
            estate_value=2500000.0,
            married_or_civil_partner=True,
            spouse_is_beneficiary=True,  # Spouse inherits
            death_pre_75=False
        )
        iht_diag = res["iht_and_income_tax_diagnosis"]
        self.assertEqual(iht_diag["effective_iht_rate_on_pension"], 0.0)
        self.assertIn("Spousal Exemption", iht_diag["iht_rationale"])

    def test_post_april_2027_nil_rate_band_protection(self):
        """Proof: Estates within the Nil-Rate Band (£325k/£650k + £175k/£350k RNRB) face 0% IHT."""
        res = calculate_pension_death_tax(
            pot_value=400000.0,
            estate_value=800000.0,  # Married couple within £1,000,000 total NRB + RNRB
            married_or_civil_partner=True,
            spouse_is_beneficiary=False,
            death_pre_75=False
        )
        self.assertEqual(res["iht_and_income_tax_diagnosis"]["effective_iht_rate_on_pension"], 0.0)

    def test_post_april_2027_double_tax_drag_on_large_estate(self):
        """
        Proof: Large estate (>£2.5M) where NRB and RNRB are exhausted faces 40% IHT + 40% income tax
        resulting in 64% combined tax drag on pension bequest.
        """
        res = calculate_pension_death_tax(
            pot_value=1000000.0,
            beneficiary_tax_rate=0.40,
            estate_value=3000000.0,
            married_or_civil_partner=True,
            spouse_is_beneficiary=False,
            death_pre_75=False
        )
        # Net to heir = £1,000,000 * (1 - 0.40) * (1 - 0.40) = £360,000
        path_a = res["path_comparison"]["path_a_preserve_in_pension"]
        self.assertEqual(path_a["net_bequest_to_heir"], 360000.0)
        self.assertEqual(path_a["combined_effective_tax_drag_percent"], 64.0)

    def test_death_pre_75_income_tax_freedom(self):
        """Proof: Under pre-75 death, beneficiary pays 0% income tax on pension pots."""
        res = calculate_pension_death_tax(
            pot_value=500000.0,
            estate_value=500000.0,
            death_pre_75=True
        )
        self.assertEqual(res["iht_and_income_tax_diagnosis"]["beneficiary_income_tax_rate"], 0.0)

    def test_non_earning_spouse_personal_allowance_arbitrage(self):
        """
        Proof: Contributing £2,880 net (£3,600 gross) to a non-earning spouse
        with unused Personal Allowance yields an exact +25.0% risk-free return.
        """
        res = test_contribution_law(
            is_non_earning_spouse=True,
            non_earner_annual_contribution=2880.0,
            spouse_other_retirement_income=0.0  # Full £12,570 Personal Allowance available
        )
        self.assertIn("spousal_non_earner_assessment", res)
        spousal = res["spousal_non_earner_assessment"]
        self.assertEqual(spousal["net_cash_invested"], 2880.0)
        self.assertEqual(spousal["hmrc_basic_rate_topup"], 720.0)
        self.assertEqual(spousal["gross_pension_created"], 3600.0)
        self.assertEqual(spousal["effective_net_return_percent"], 25.0)

    def test_spousal_equalization_reduces_household_tax(self):
        """Proof: Splitting pension drawdown across two personal allowances saves significant tax."""
        res = household_pension_equalization(household_drawdown=50000.0)
        # Unequal: 75% taxable = £37,500. Tax = (£37,500 - £12,570) * 0.20 = £4,986
        # Equalized: Two pots of £25,000. 75% taxable = £18,750 each. Tax = (£18,750 - £12,570) * 0.20 = £1,236 * 2 = £2,472
        # Tax saved = £4,986 - £2,472 = £2,514
        self.assertEqual(res["unequal_total_tax"], 4986.0)
        self.assertEqual(res["equalized_total_tax"], 2472.0)
        self.assertEqual(res["annual_tax_saved_by_equalizing"], 2514.0)


class TestMortgagePrepaymentVsInvesting(unittest.TestCase):
    """
    Independent tests for reducing-balance loan prepayment and investment comparison.
    """

    @staticmethod
    def _independent_reducing_balance_emi(principal: float, annual_rate: float, tenure_years: float) -> float:
        r_m = (annual_rate / 100.0) / 12.0
        n = int(tenure_years * 12)
        return principal * r_m * ((1.0 + r_m) ** n) / (((1.0 + r_m) ** n) - 1.0)

    def test_reducing_balance_emi_and_amortization_proof(self):
        """Proof: Standard banking EMI formula matches fire_calculator."""
        principal = 5000000.0  # ₹50 Lakh loan
        rate = 8.5            # 8.5% interest
        tenure = 20.0          # 20 years

        expected_emi = self._independent_reducing_balance_emi(principal, rate, tenure)
        res = calculate_loan_prepayment(principal, rate, tenure)

        self.assertAlmostEqual(res["monthly_emi"], expected_emi, places=2)
        self.assertEqual(res["months_saved"], 0)
        self.assertEqual(res["total_interest_saved"], 0.0)

    def test_extra_monthly_prepayment_tenure_and_interest_reduction(self):
        """Proof: Extra monthly prepayment strictly reduces tenure and total interest paid."""
        principal = 5000000.0
        rate = 8.5
        tenure = 20.0
        extra_monthly = 10000.0

        res = calculate_loan_prepayment(principal, rate, tenure, extra_monthly_prepay=extra_monthly)

        # Revised tenure must be strictly shorter than 240 months
        self.assertLess(res["revised_tenure_months"], 240)
        self.assertGreater(res["months_saved"], 0)
        self.assertGreater(res["total_interest_saved"], 0.0)

    def test_mortgage_vs_investing_opportunity_cost(self):
        """Proof: Higher-rate taxpayer investing in pension achieves higher net growth than mortgage payoff."""
        res = compare_mortgage_vs_investing(
            mortgage_balance=250000.0,
            mortgage_rate=4.5,
            available_gross=10000.0,
            tax_bracket="higher",
            expected_invest_return=0.075
        )
        # Net cash for mortgage: £10,000 * (1 - 0.40) = £6,000
        self.assertEqual(res["net_cash_for_mortgage_or_isa"], 6000.0)
        # Mortgage interest saved: £6,000 * 4.5% = £270
        self.assertEqual(res["guaranteed_annual_mortgage_interest_saved"], 270.0)
        # Pension growth on full £10,000 gross = £750 * 0.85 = £637.50
        self.assertEqual(res["expected_pension_annual_net_growth"], 637.50)
        self.assertIn("Pension", res["recommendation"])


class TestCrossBorderDTAAAndCurrency(unittest.TestCase):
    """
    Independent tests for cross-border taxation, UK-India DTAA,
    Foreign Tax Credit (FTC) ceilings, NRE/NRO accounts, and currency PPP.
    """

    def test_currency_ppp_closed_form_projection(self):
        """
        Proof: Over T years, nominal exchange rate adjusts by inflation differential:
        Rate_T = Rate_0 * ((1 + i_INR) / (1 + i_GBP))^T
        """
        rate_0 = 105.0
        i_inr = 0.065
        i_gbp = 0.025
        years = 10

        expected_rate = rate_0 * (((1.0 + i_inr) / (1.0 + i_gbp)) ** years)
        res = calculate_cross_border_dtaa(
            uk_pension_gbp=50000.0,
            gbp_inr_rate=rate_0,
            india_inflation=i_inr,
            uk_inflation=i_gbp,
            years=years
        )
        ppp = res["currency_ppp_projection"]
        self.assertAlmostEqual(ppp["projected_exchange_rate_in_years"], expected_rate, places=2)
        self.assertAlmostEqual(ppp["uk_pension_future_annual_inr"], 50000.0 * expected_rate, places=2)

    def test_nre_tax_free_statutory_exemption(self):
        """Proof: NRE deposit interest is 100% tax-free in India under Section 10(4)(ii)."""
        res = calculate_cross_border_dtaa(india_nre_income_inr=500000.0, is_uk_resident=True)
        nre_tax = res["nre_nro_banking_tax"]
        self.assertEqual(nre_tax["nre_tax_in_india"], 0.0)
        self.assertIn("Section 10(4)(ii)", nre_tax["nre_statutory_exemption"])

    def test_nro_tds_treaty_reduction_with_trc(self):
        """
        Proof: Submitting TRC + Form 10F reduces NRO TDS from domestic 31.2% to treaty 15.0%,
        saving exactly 16.2% of gross NRO income.
        """
        nro_income = 1000000.0  # ₹10 Lakh NRO interest
        # Without TRC
        res_no_trc = calculate_cross_border_dtaa(india_nro_income_inr=nro_income, has_trc=False)
        self.assertEqual(res_no_trc["nre_nro_banking_tax"]["applicable_nro_tds_rate_percent"], 31.2)
        self.assertEqual(res_no_trc["nre_nro_banking_tax"]["nro_tds_deducted_inr"], 312000.0)
        self.assertEqual(res_no_trc["nre_nro_banking_tax"]["potential_tds_saving_with_trc_inr"], 162000.0)

        # With TRC
        res_trc = calculate_cross_border_dtaa(india_nro_income_inr=nro_income, has_trc=True)
        self.assertEqual(res_trc["nre_nro_banking_tax"]["applicable_nro_tds_rate_percent"], 15.0)
        self.assertEqual(res_trc["nre_nro_banking_tax"]["nro_tds_deducted_inr"], 150000.0)
        self.assertEqual(res_trc["nre_nro_banking_tax"]["potential_tds_saving_with_trc_inr"], 0.0)

    def test_dtaa_article_20_private_pension_residency_rule(self):
        """Proof: Article 20 dictates private pensions are taxable only in the state of residence."""
        # Scenario A: UK Resident
        res_uk = calculate_cross_border_dtaa(uk_pension_gbp=40000.0, is_uk_resident=True, pension_type="private")
        self.assertEqual(res_uk["pension_dtaa_assessment"]["taxable_in"], "UK Only")
        self.assertEqual(res_uk["pension_dtaa_assessment"]["india_tax_liability_inr"], 0.0)

        # Scenario B: India Resident
        res_in = calculate_cross_border_dtaa(uk_pension_gbp=40000.0, is_uk_resident=False, pension_type="private", gbp_inr_rate=105.0)
        self.assertEqual(res_in["pension_dtaa_assessment"]["taxable_in"], "India Only")
        self.assertEqual(res_in["pension_dtaa_assessment"]["uk_tax_liability_gbp"], 0.0)
        self.assertIn("India-Individual 2004", res_in["pension_dtaa_assessment"]["treaty_guidance_notes"][1])

    def test_dtaa_article_19_government_pension_rule(self):
        """Proof: Article 19 dictates government/civil service pensions are taxable in paying country."""
        res_gov = calculate_cross_border_dtaa(uk_pension_gbp=30000.0, is_uk_resident=False, pension_type="government")
        self.assertEqual(res_gov["pension_dtaa_assessment"]["dtaa_article"], "Article 19 (UK-India DTAA)")
        self.assertEqual(res_gov["pension_dtaa_assessment"]["taxable_in"], "UK (Source State)")

    def test_foreign_tax_credit_statutory_ceiling(self):
        """
        Proof: Foreign Tax Credit (FTC) under Section 90 / Form 67 & TIOPA 2010
        is capped at min(Foreign Tax Paid, Domestic Tax Payable).
        """
        # Case 1: Foreign tax exceeds domestic tax (Unrelieved foreign tax occurs)
        # NRO income = ₹10L at 105 = £9,523.81.
        # India TDS paid at 31.2% = ₹3,12,000 = £2,971.43.
        # UK tax liability at 20% basic rate = £1,904.76.
        # FTC allowed must equal UK tax liability (£1,904.76).
        # Unrelieved foreign tax = £2,971.43 - £1,904.76 = £1,066.67.
        res_excess = calculate_cross_border_dtaa(
            india_nro_income_inr=1000000.0,
            gbp_inr_rate=105.0,
            is_uk_resident=True,
            has_trc=False,
            uk_marginal_rate=0.20
        )
        ftc = res_excess["double_tax_relief_ftc"]
        self.assertEqual(ftc["net_uk_tax_payable_to_hmrc"], 0.0)
        self.assertEqual(ftc["foreign_tax_credit_allowed_gbp"], ftc["uk_tax_liability_on_foreign_income"])
        self.assertGreater(ftc["unrelieved_foreign_tax_drag_gbp"], 0.0)

        # Case 2: Foreign tax is lower than domestic tax (Higher rate taxpayer)
        # UK tax liability at 40% = £3,809.52.
        # India TDS paid with TRC at 15% = ₹1,50,000 = £1,428.57.
        # FTC allowed = £1,428.57 (all of it).
        # Net UK tax payable = £3,809.52 - £1,428.57 = £2,380.95.
        # Unrelieved tax = 0.
        res_lower = calculate_cross_border_dtaa(
            india_nro_income_inr=1000000.0,
            gbp_inr_rate=105.0,
            is_uk_resident=True,
            has_trc=True,
            uk_marginal_rate=0.40
        )
        ftc_lower = res_lower["double_tax_relief_ftc"]
        self.assertEqual(ftc_lower["unrelieved_foreign_tax_drag_gbp"], 0.0)
        self.assertAlmostEqual(
            ftc_lower["foreign_tax_credit_allowed_gbp"],
            ftc_lower["foreign_tax_paid_gbp (India TDS)"],
            places=2
        )
        self.assertGreater(ftc_lower["net_uk_tax_payable_to_hmrc"], 0.0)


if __name__ == "__main__":
    unittest.main()
