from __future__ import annotations

import unittest

from app.repositories.memory import InMemoryJourneyRepository
from app.rules.routing import route_onboarding
from app.schemas.common import GoalEnum, UserProfile
from app.services.journey_service import JourneyService


class JourneyServiceChecklistTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = JourneyService(InMemoryJourneyRepository())

    def test_ga_direct_transfer_builds_seven_step_checklist(self) -> None:
        profile = UserProfile(
            state="Georgia",
            county="Dekalb",
            goal=GoalEnum.GA_DRIVERS_LICENSE,
            age=29,
            has_ssn=True,
            has_foreign_license=True,
            foreign_license_country="Germany",
        )
        routing = route_onboarding(profile)

        checklist = self.service.build_checklist(
            journey_id="preview-ga-direct",
            profile=profile,
            routing=routing,
        )

        self.assertEqual(checklist.disclaimer, "This tool provides guidance, not legal advice.")
        self.assertEqual(checklist.progress, {"completed_steps": 0, "total_steps": 7, "percent": 0})
        self.assertEqual(len(checklist.steps), 7)
        self.assertEqual(checklist.steps[0].title, "Gather documents")
        self.assertEqual(checklist.steps[3].title, "Confirm reciprocity-based knowledge test waiver")
        self.assertEqual(checklist.steps[4].title, "Confirm road skills test waiver")

    def test_ga_under_18_without_ssn_includes_joshuas_law_and_itin_guidance(self) -> None:
        profile = UserProfile(
            state="Georgia",
            county="Gwinnett",
            goal=GoalEnum.GA_DRIVERS_LICENSE,
            age=17,
            has_ssn=False,
        )
        routing = route_onboarding(profile)

        checklist = self.service.build_checklist(
            journey_id="preview-ga-teen",
            profile=profile,
            routing=routing,
        )

        self.assertEqual(len(checklist.steps), 7)
        self.assertIn("Joshua's Law", checklist.steps[0].warning)
        self.assertIn("ITIN", checklist.steps[0].warning)
        self.assertEqual(checklist.steps[3].title, "Pass knowledge test")
        self.assertEqual(checklist.steps[4].title, "Pass road skills test")

    def test_passport_new_uses_clear_step_by_step_checklist(self) -> None:
        profile = UserProfile(
            state="Georgia",
            county="Fulton",
            goal=GoalEnum.PASSPORT_NEW,
        )
        routing = route_onboarding(profile)

        checklist = self.service.build_checklist(
            journey_id="preview-passport",
            profile=profile,
            routing=routing,
        )

        self.assertGreaterEqual(len(checklist.steps), 5)
        self.assertEqual(checklist.steps[1].form_number, "DS-11")
        self.assertIn("Fulton", checklist.steps[2].office_address)

    def test_visa_flow_adds_legal_caution_to_steps(self) -> None:
        profile = UserProfile(
            state="Georgia",
            county="Clayton",
            goal=GoalEnum.F1_OPT,
            immigration_status="F-1 student",
        )
        routing = route_onboarding(profile)

        checklist = self.service.build_checklist(
            journey_id="preview-opt",
            profile=profile,
            routing=routing,
        )

        self.assertGreaterEqual(len(checklist.steps), 5)
        self.assertIn("legal help", checklist.steps[0].warning)
        self.assertEqual(checklist.steps[2].form_number, "I-765")


if __name__ == "__main__":
    unittest.main()
