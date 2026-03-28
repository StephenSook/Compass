from __future__ import annotations

import unittest

from app.core.dependencies import ServiceContainer
from app.schemas.onboarding import OnboardRequest


class MockCompassAIServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.container = ServiceContainer()

    def test_residency_alternatives_response_is_specific_and_grounded(self) -> None:
        journey, session = self._onboard(
            state="GA",
            county="DeKalb",
            city="Atlanta",
            goal="ga_drivers_license",
            age=23,
            has_ssn=True,
            has_foreign_license=True,
            foreign_license_country="France",
        )

        response = self.container.ai_service.generate_response(
            journey=journey,
            session=session,
            question="What if I do not have a utility bill for proof of residency?",
        )

        self.assertIn("bank statement", response["answer"])
        self.assertIn("lease", response["answer"])
        self.assertIn("manual verification", response["answer"])
        self.assertEqual(response["recommended_next_step"], "Gather documents")
        self.assertEqual(response["citations"][0]["source_key"], "ga_dds_residency_docs")
        self.assertFalse(response["legal_warning"])

    def test_foreign_license_response_mentions_transfer_path(self) -> None:
        journey, session = self._onboard(
            state="GA",
            county="DeKalb",
            goal="ga_drivers_license",
            age=23,
            has_ssn=True,
            has_foreign_license=True,
            foreign_license_country="France",
        )

        response = self.container.ai_service.generate_response(
            journey=journey,
            session=session,
            question="Can I use my foreign license?",
        )

        self.assertIn("France", response["answer"])
        self.assertIn("manual verification", response["answer"])
        self.assertTrue(any(citation["source_key"] == "ga_dds_foreign_license_rules" for citation in response["citations"]))
        self.assertFalse(response["legal_warning"])

    def test_i765_timing_uses_prior_chat_context_and_sets_legal_warning(self) -> None:
        journey, session = self._onboard(
            state="GA",
            county="Clayton",
            goal="f1_opt",
            immigration_status="F-1 student",
        )
        self.container.session_service.append_conversation(
            journey.id,
            "I am trying to understand Form I-765 for OPT.",
            "Form I-765 is the work authorization filing step for OPT.",
        )
        session = self.container.session_service.get_session(journey.id)

        response = self.container.ai_service.generate_response(
            journey=journey,
            session=session,
            question="How long does it usually take?",
        )

        self.assertIn("3-5 months", response["answer"])
        self.assertIn("manual verification", response["answer"])
        self.assertTrue(response["legal_warning"])
        self.assertTrue(any(citation["source_key"] == "uscis_i765_processing_time" for citation in response["citations"]))

    def test_fee_and_location_answers_are_contextual(self) -> None:
        journey, session = self._onboard(
            state="GA",
            county="DeKalb",
            goal="ga_drivers_license",
            age=23,
            has_ssn=True,
        )

        fee_response = self.container.ai_service.generate_response(
            journey=journey,
            session=session,
            question="What fee do I pay?",
        )
        location_response = self.container.ai_service.generate_response(
            journey=journey,
            session=session,
            question="Where do I go?",
        )

        self.assertIn("$32", fee_response["answer"])
        self.assertIn("South DeKalb DDS", location_response["answer"])
        self.assertIn("2801 Candler Rd", location_response["answer"])
        self.assertEqual(location_response["recommended_next_step"], "Book DDS appointment")

    def test_no_ssn_answer_gives_alternative_docs(self) -> None:
        journey, session = self._onboard(
            state="GA",
            county="Gwinnett",
            goal="ga_drivers_license",
            age=17,
            has_ssn=False,
        )

        response = self.container.ai_service.generate_response(
            journey=journey,
            session=session,
            question="What if I do not have an SSN?",
        )

        self.assertIn("SSN denial letter", response["answer"])
        self.assertIn("ITIN", response["answer"])
        self.assertIn("manual verification", response["answer"])
        self.assertEqual(response["recommended_next_step"], "Gather documents")

    def _onboard(self, **payload):
        journey = self.container.onboarding_service.onboard(OnboardRequest(**payload))
        session = self.container.session_service.get_session(journey.id)
        return journey, session


if __name__ == "__main__":
    unittest.main()
