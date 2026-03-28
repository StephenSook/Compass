from __future__ import annotations

import unittest

from app.schemas.common import GoalEnum, UserProfile
from app.services.knowledge_base import KnowledgeBaseService


class KnowledgeBaseServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = KnowledgeBaseService()

    def test_ga_dekalb_context_returns_reusable_office_and_ssn_docs(self) -> None:
        profile = UserProfile(
            state="Georgia",
            county="Dekalb",
            goal=GoalEnum.GA_DRIVERS_LICENSE,
            has_ssn=True,
        )

        context = self.service.get_context_for_branch(
            "ga_dl.foreign_license.reciprocity.ssn.yes.age_18_plus.dekalb",
            profile,
        )

        self.assertEqual(context["journey_type"], "drivers_license")
        self.assertEqual(context["office"]["id"], "dds_south_dekalb")
        self.assertEqual(context["fees"][0]["amount_usd"], 32)
        self.assertTrue(context["tests"][0]["waived"])
        self.assertIn("Two proofs of Georgia residency", context["documents"]["items"])

    def test_passport_new_context_contains_ds11_fee_breakdown_and_atlanta_office(self) -> None:
        context = self.service.get_context_for_branch(
            "passport.new.fulton",
            {"state": "Georgia", "county": "Fulton", "goal": "passport_new"},
        )

        self.assertEqual(context["forms"][0]["number"], "DS-11")
        self.assertEqual([fee["amount_usd"] for fee in context["fees"]], [165, 30])
        self.assertEqual(context["timelines"]["routine"], "6-8 weeks")
        self.assertEqual(context["office"]["id"], "atlanta_passport_acceptance")

    def test_passport_renewal_context_contains_ds82_and_mail_fee(self) -> None:
        context = self.service.get_context_for_branch(
            "passport.renewal.fulton",
            {"state": "Georgia", "county": "Fulton", "goal": "passport_renewal"},
        )

        self.assertEqual(context["forms"][0]["number"], "DS-82")
        self.assertEqual(context["fees"][0]["amount_usd"], 130)
        self.assertEqual(context["timelines"]["routine"], "6-8 weeks")

    def test_opt_context_contains_key_rules(self) -> None:
        context = self.service.get_context_for_branch(
            "visa.f1_opt.clayton",
            {"state": "Georgia", "county": "Clayton", "goal": "f1_opt"},
        )

        self.assertEqual(context["forms"][0]["number"], "I-765")
        self.assertEqual(context["fees"][0]["amount_usd"], 410)
        self.assertIn("90 days before graduation", context["rules"]["filing_window"])
        self.assertIn("90 days of unemployment", context["rules"]["unemployment_limit"])

    def test_family_green_card_and_extension_contexts_are_structured(self) -> None:
        green_card = self.service.get_context_for_branch(
            "visa.family_green_card.clayton",
            {"state": "Georgia", "county": "Clayton", "goal": "family_green_card"},
        )
        extension = self.service.get_context_for_branch(
            "visa.extension.clayton",
            {"state": "Georgia", "county": "Clayton", "goal": "visa_extension"},
        )

        self.assertEqual(green_card["forms"][0]["number"], "I-130")
        self.assertEqual(green_card["fees"][0]["amount_usd"], 535)
        self.assertIn("concurrently", green_card["rules"]["concurrent_filing"])

        self.assertEqual(extension["forms"][0]["number"], "I-539")
        self.assertEqual(extension["fees"][0]["amount_usd"], 370)
        self.assertIn("before the current status expires", extension["rules"]["deadline"])
        self.assertIn("biometrics", extension["rules"]["biometrics"].lower())


if __name__ == "__main__":
    unittest.main()
