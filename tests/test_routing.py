from __future__ import annotations

import unittest

from app.rules.routing import route_onboarding
from app.schemas.common import GoalEnum, JourneyTypeEnum, UserProfile


class RouteOnboardingTests(unittest.TestCase):
    def test_ga_direct_transfer_branch_is_readable_and_deterministic(self) -> None:
        routing = route_onboarding(
            UserProfile(
                state="Georgia",
                county="Dekalb",
                goal=GoalEnum.GA_DRIVERS_LICENSE,
                age=29,
                has_ssn=True,
                has_us_license=False,
                has_foreign_license=True,
                foreign_license_country="Germany",
            )
        )

        self.assertEqual(routing.journey_type, JourneyTypeEnum.DRIVERS_LICENSE)
        self.assertEqual(routing.template_key, "ga_license_direct_transfer")
        self.assertEqual(
            routing.branch_key,
            "ga_dl.foreign_license.reciprocity.ssn.yes.age_18_plus.dekalb",
        )
        self.assertTrue(routing.derived_flags["is_direct_transfer"])
        self.assertFalse(routing.derived_flags["requires_full_testing"])

    def test_ga_full_testing_without_ssn_sets_guidance_flags(self) -> None:
        routing = route_onboarding(
            UserProfile(
                state="Georgia",
                county="Fulton",
                goal=GoalEnum.GA_DRIVERS_LICENSE,
                age=24,
                has_ssn=False,
                has_us_license=False,
                has_foreign_license=True,
                foreign_license_country="Brazil",
            )
        )

        self.assertEqual(routing.template_key, "ga_license_full_testing")
        self.assertEqual(
            routing.branch_key,
            "ga_dl.foreign_license.full_testing.ssn.no.age_18_plus.fulton",
        )
        self.assertTrue(routing.derived_flags["requires_full_testing"])
        self.assertTrue(routing.derived_flags["needs_itin_guidance"])
        self.assertEqual(routing.branch_summary["ssn_status"], "no")

    def test_ga_under_18_prioritizes_joshuas_law(self) -> None:
        routing = route_onboarding(
            UserProfile(
                state="Georgia",
                county="Gwinnett",
                goal=GoalEnum.GA_DRIVERS_LICENSE,
                age=17,
                has_ssn=False,
                has_us_license=True,
            )
        )

        self.assertEqual(routing.template_key, "ga_license_under18")
        self.assertEqual(
            routing.branch_key,
            "ga_dl.joshuas_law.ssn.no.age_under_18.gwinnett",
        )
        self.assertTrue(routing.derived_flags["requires_joshuas_law"])

    def test_goal_mappings_for_passport_and_visa_flows(self) -> None:
        cases = [
            (
                GoalEnum.PASSPORT_NEW,
                JourneyTypeEnum.PASSPORT,
                "passport_first_time",
                "passport.new.clayton",
            ),
            (
                GoalEnum.PASSPORT_RENEWAL,
                JourneyTypeEnum.PASSPORT,
                "passport_renewal",
                "passport.renewal.clayton",
            ),
            (
                GoalEnum.F1_OPT,
                JourneyTypeEnum.VISA,
                "visa_opt",
                "visa.f1_opt.clayton",
            ),
            (
                GoalEnum.FAMILY_GREEN_CARD,
                JourneyTypeEnum.VISA,
                "visa_family_green_card",
                "visa.family_green_card.clayton",
            ),
            (
                GoalEnum.VISA_EXTENSION,
                JourneyTypeEnum.VISA,
                "visa_extension",
                "visa.extension.clayton",
            ),
        ]

        for goal, journey_type, template_key, branch_key in cases:
            with self.subTest(goal=goal):
                routing = route_onboarding(
                    UserProfile(
                        state="Georgia",
                        county="Clayton",
                        goal=goal,
                        immigration_status="F-1 student",
                    )
                )

                self.assertEqual(routing.journey_type, journey_type)
                self.assertEqual(routing.template_key, template_key)
                self.assertEqual(routing.branch_key, branch_key)


if __name__ == "__main__":
    unittest.main()
