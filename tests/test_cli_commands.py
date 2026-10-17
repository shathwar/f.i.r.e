"""
Automated CLI Command Verification & Advisory Output Audit Test Suite
Verifies that every advertised CLI command exists, executes cleanly,
and returns the exact JSON fields required by the advisor.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIRE_CALC = ROOT / ".agents" / "skills" / "fire-advisor" / "scripts" / "fire_calculator.py"
ROT_ENGINE = ROOT / ".agents" / "skills" / "equity-rotator" / "scripts" / "rotation_engine.py"


class TestCLICommandsAudit(unittest.TestCase):
    """Verifies that each advertised CLI command exists and its output is complete."""

    def _run_cmd(self, script_path: Path, args: list) -> dict:
        cmd = [sys.executable, str(script_path)] + args
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(
            proc.returncode, 0,
            f"Command failed with code {proc.returncode}:\n{' '.join(cmd)}\nSTDERR: {proc.stderr}"
        )
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError:
            self.fail(f"Command did not return valid JSON:\n{' '.join(cmd)}\nSTDOUT: {proc.stdout}")

    # =========================================================================
    # FIRE ADVISOR CLI COMMANDS (All 22 advertised subcommands)
    # =========================================================================

    def test_cmd_target(self):
        res = self._run_cmd(FIRE_CALC, ["target", "--spend", "40000", "--swr", "0.035"])
        self.assertIn("fire_target", res)
        self.assertIn("fire_target_post_state_pension", res)
        self.assertGreater(res["fire_target"], 0)

    def test_cmd_date(self):
        res = self._run_cmd(FIRE_CALC, ["date", "--age", "32", "--nw", "150000", "--savings", "30000", "--spend", "40000"])
        self.assertIn("years_to_fi", res)
        self.assertIn("projected_retirement_age", res)
        self.assertIn("portfolio_at_fi", res)

    def test_cmd_bridge(self):
        res = self._run_cmd(FIRE_CALC, ["bridge", "--retire-age", "50", "--spend", "40000", "--nmpa", "57"])
        self.assertIn("bridge_years", res)
        self.assertIn("bucket_1_cash_buffer (0-2 yrs)", res)
        self.assertIn("bucket_2_isa_investments (3+ yrs)", res)

    def test_cmd_tax(self):
        res = self._run_cmd(FIRE_CALC, ["tax", "--gross", "10000", "--bracket", "higher"])
        self.assertIn("isa_value_after_20_years (tax_free)", res)
        self.assertIn("pension_net_value_after_20_years", res)
        self.assertIn("pension_wealth_advantage_percent", res)

    def test_cmd_mortgage(self):
        res = self._run_cmd(FIRE_CALC, ["mortgage", "--rate", "4.5", "--gross", "10000", "--bracket", "higher"])
        self.assertIn("guaranteed_annual_mortgage_interest_saved", res)
        self.assertIn("expected_pension_annual_net_growth", res)
        self.assertIn("recommendation", res)

    def test_cmd_stress(self):
        res = self._run_cmd(FIRE_CALC, ["stress", "--portfolio", "1000000", "--spend", "40000"])
        self.assertIn("portfolio_saved_by_cash_buffer_after_5_years", res)
        self.assertIn("policy_a_trajectory (no buffer)", res)
        self.assertIn("policy_b_trajectory (with 2yr buffer)", res)

    def test_cmd_household(self):
        res = self._run_cmd(FIRE_CALC, ["household", "--drawdown", "50000"])
        self.assertIn("unequal_total_tax", res)
        self.assertIn("equalized_total_tax", res)
        self.assertIn("annual_tax_saved_by_equalizing", res)

    def test_cmd_death_tax(self):
        res = self._run_cmd(FIRE_CALC, ["death-tax", "--pot", "500000", "--estate", "1200000"])
        self.assertIn("iht_and_income_tax_diagnosis", res)
        self.assertIn("path_comparison", res)
        self.assertIn("optimal_strategy", res)

    def test_cmd_contrib_test(self):
        res = self._run_cmd(FIRE_CALC, ["contrib-test", "--relief", "0.20", "--marginal-out", "0.20", "--non-earner"])
        self.assertIn("spousal_non_earner_assessment", res)
        self.assertIn("general_verdict", res)
        self.assertEqual(res["spousal_non_earner_assessment"]["effective_net_return_percent"], 25.0)

    def test_cmd_survivor(self):
        res = self._run_cmd(FIRE_CALC, ["survivor", "--spend", "50000", "--sp1", "11500", "--sp2", "11500"])
        self.assertIn("survivor_annual_spend (85% baseline)", res)
        self.assertIn("lost_state_pension_annual", res)
        self.assertIn("net_drawdown_change_for_survivor", res)

    def test_cmd_india_tax(self):
        res = self._run_cmd(FIRE_CALC, [
            "india-tax", "--gross", "2200000", "--rent", "420000", "--basic", "1100000",
            "--metro", "--sec-80c", "150000", "--ay", "2026-27"
        ])
        self.assertIn("comparison_summary", res)
        self.assertIn("new_regime", res)
        self.assertIn("old_regime", res)
        self.assertIn("recommended_regime", res["comparison_summary"])

    def test_cmd_india_fire(self):
        res = self._run_cmd(FIRE_CALC, [
            "india-fire", "--age", "32", "--retire-age", "47",
            "--monthly-spend", "75000", "--portfolio", "2500000"
        ])
        self.assertIn("future_annual_expenses_at_retirement", res)
        self.assertIn("target_fire_corpus", res)
        self.assertIn("corpus_in_crores", res)
        self.assertIn("required_monthly_sip", res)

    def test_cmd_loan_prepay(self):
        res = self._run_cmd(FIRE_CALC, [
            "loan-prepay", "--principal", "5000000", "--rate", "8.75",
            "--tenure", "20", "--extra-monthly", "10000"
        ])
        self.assertIn("monthly_emi", res)
        self.assertIn("revised_tenure_years", res)
        self.assertIn("months_saved", res)
        self.assertIn("total_interest_saved", res)

    def test_cmd_mhs(self):
        res = self._run_cmd(FIRE_CALC, [
            "mhs", "--income", "150000", "--expenses", "60000", "--emi", "35000",
            "--liquid", "600000", "--term-cover", "27000000"
        ])
        self.assertIn("total_mhs_score", res)
        self.assertIn("rating", res)
        self.assertIn("dimension_scores", res)
        self.assertIn("diagnostics", res)

    def test_cmd_asset_compare(self):
        res = self._run_cmd(FIRE_CALC, ["asset-compare", "--tax-bracket", "30"])
        self.assertIn("asset_comparison", res)
        self.assertIn("investor_tax_bracket", res)
        self.assertIn("key_takeaways", res)

    def test_cmd_real_estate_eval(self):
        res = self._run_cmd(FIRE_CALC, ["real-estate-eval", "--price", "15000000", "--rent", "35000"])
        self.assertIn("comparison_result", res)
        self.assertIn("scenario_buyer", res)
        self.assertIn("scenario_renter_investor", res)
        self.assertIn("retirement_income_capital_efficiency (for 1L/month cash flow)", res)

    def test_cmd_crypto_tax_india(self):
        res = self._run_cmd(FIRE_CALC, [
            "crypto-tax", "--jurisdiction", "india",
            "--gain", "1000000", "--loss", "400000", "--transfer-value", "1000000"
        ])
        self.assertIn("statutory_tax_owed", res)
        self.assertIn("gross_crypto_gains", res)
        self.assertIn("tds_deducted_at_source_sec_194s (1 percent)", res)

    def test_cmd_crypto_tax_uk(self):
        res = self._run_cmd(FIRE_CALC, [
            "crypto-tax", "--jurisdiction", "uk",
            "--gain", "15000", "--loss", "4000", "--bracket", "higher"
        ])
        self.assertIn("taxable_gain", res)
        self.assertIn("cgt_tax_owed", res)
        self.assertIn("cgt_annual_exempt_amount", res)

    def test_cmd_cross_border(self):
        res = self._run_cmd(FIRE_CALC, [
            "cross-border", "--uk-pension", "40000", "--india-nro", "500000",
            "--rate", "105", "--has-trc"
        ])
        self.assertIn("currency_ppp_projection", res)
        self.assertIn("nre_nro_banking_tax", res)
        self.assertIn("pension_dtaa_assessment", res)
        self.assertIn("double_tax_relief_ftc", res)

    def test_cmd_profile_management(self):
        tmp_output = ROOT / "tests" / "scratch_template.json"
        try:
            # 1. profile-template
            res_temp = self._run_cmd(FIRE_CALC, [
                "profile-template", "--jurisdiction", "india", "--output", str(tmp_output)
            ])
            self.assertIn("file_path", res_temp)
            self.assertEqual(res_temp["status"], "success")
            self.assertTrue(tmp_output.exists())

            # 2. profile-list
            res_list = self._run_cmd(FIRE_CALC, ["profile-list", "--dir", str(ROOT / "profiles")])
            self.assertIn("profiles_found", res_list)
            self.assertGreater(res_list["profiles_found"], 0)

            # 3. profile-show
            test_prof = ROOT / "profiles" / "test_india_client.json"
            res_show = self._run_cmd(FIRE_CALC, ["profile-show", "--file", str(test_prof)])
            self.assertIn("profile_name", res_show)
            self.assertIn("assets", res_show)

            # 4. profile-eval
            res_eval = self._run_cmd(FIRE_CALC, ["profile-eval", "--file", str(test_prof)])
            self.assertIn("balance_sheet_summary", res_eval)
            self.assertIn("fire_target_and_gap_analysis", res_eval)
            self.assertIn("asset_tracking_source_ledger", res_eval)
            self.assertIn("money_health_diagnostic", res_eval)
        finally:
            if tmp_output.exists():
                tmp_output.unlink()

    # =========================================================================
    # EQUITY ROTATOR CLI COMMANDS (All 4 advertised subcommands)
    # =========================================================================

    def test_cmd_rotator_analyze(self):
        res = self._run_cmd(ROT_ENGINE, [
            "analyze", "--market", "india", "--growth", "accelerating",
            "--inflation", "falling", "--fii-long-short", "0.16", "--pcr", "1.10"
        ])
        self.assertIn("macro_regime", res)
        self.assertIn("sentiment_posture", res)
        self.assertIn("sector_allocation_scorecard", res)

    def test_cmd_rotator_regime(self):
        res = self._run_cmd(ROT_ENGINE, ["regime", "--growth", "accelerating", "--inflation", "falling"])
        self.assertIn("macro_quadrant", res)
        self.assertIn("india_sector_recommendations", res)
        self.assertIn("global_sector_recommendations", res)

    def test_cmd_rotator_sentiment_check(self):
        res = self._run_cmd(ROT_ENGINE, [
            "sentiment-check", "--fii-long-short", "0.15", "--pcr", "1.45", "--vix", "16.2"
        ])
        self.assertIn("fii_index_futures_status", res)
        self.assertIn("put_call_ratio_status", res)
        self.assertIn("institutional_sentiment_bias", res)

    def test_cmd_rotator_spread_check(self):
        res = self._run_cmd(ROT_ENGINE, [
            "spread-check", "--small-large-pe", "1.28", "--breadth-50dma", "42.0", "--yield-gap", "2.70"
        ])
        self.assertIn("style_rotation_recommendation", res)
        self.assertIn("smallcap_to_largecap_pe_ratio", res)
        self.assertIn("diagnostic_alerts", res)


if __name__ == "__main__":
    unittest.main()
