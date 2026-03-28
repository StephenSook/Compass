from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.core.dependencies import get_container
from app.main import app


class ApiRoutesTests(unittest.TestCase):
    def setUp(self) -> None:
        get_container.cache_clear()
        self.client = TestClient(app)

    def test_health_returns_ok(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_onboard_and_journey_endpoints_work_together(self) -> None:
        onboard_response = self.client.post(
            "/api/v1/onboard",
            json={
                "state": "Georgia",
                "county": "Dekalb",
                "goal": "ga_drivers_license",
                "age": 24,
                "has_ssn": False,
                "has_foreign_license": True,
                "foreign_license_country": "Brazil",
            },
        )

        self.assertEqual(onboard_response.status_code, 201)
        onboard_payload = onboard_response.json()
        self.assertEqual(onboard_payload["next_action"], "generate_journey")
        self.assertEqual(onboard_payload["journey_type"], "drivers_license")
        self.assertIn("branch_key", onboard_payload["branch_summary"])

        journey_id = onboard_payload["journey_id"]

        journey_response = self.client.get(f"/api/v1/journeys/{journey_id}")
        self.assertEqual(journey_response.status_code, 200)
        journey_payload = journey_response.json()
        self.assertEqual(journey_payload["progress"], {"completed_steps": 0, "total_steps": 7, "percent": 0})
        self.assertEqual(journey_payload["disclaimer"], "This tool provides guidance, not legal advice.")

        first_step_id = journey_payload["steps"][0]["step_id"]

        ask_response = self.client.post(
            f"/api/v1/journeys/{journey_id}/ask",
            json={"question": "What if I do not have an SSN but I have an ITIN?"},
        )
        self.assertEqual(ask_response.status_code, 200)
        ask_payload = ask_response.json()
        self.assertIn("SSN", ask_payload["answer"])

        progress_response = self.client.patch(
            f"/api/v1/journeys/{journey_id}/progress",
            json={"step_id": first_step_id, "completed": True},
        )
        self.assertEqual(progress_response.status_code, 200)
        progress_payload = progress_response.json()
        self.assertEqual(progress_payload["progress"]["completed_steps"], 1)

        session_response = self.client.get(f"/api/v1/sessions/{journey_id}")
        self.assertEqual(session_response.status_code, 200)
        session_payload = session_response.json()
        self.assertEqual(session_payload["journey"]["journey_id"], journey_id)
        self.assertGreaterEqual(len(session_payload["chat_history"]), 3)

    def test_missing_journey_returns_404(self) -> None:
        missing_id = "11111111-1111-1111-1111-111111111111"

        journey_response = self.client.get(f"/api/v1/journeys/{missing_id}")
        ask_response = self.client.post(
            f"/api/v1/journeys/{missing_id}/ask",
            json={"question": "What should I do next?"},
        )
        progress_response = self.client.patch(
            f"/api/v1/journeys/{missing_id}/progress",
            json={"step_id": missing_id, "completed": True},
        )
        session_response = self.client.get(f"/api/v1/sessions/{missing_id}")

        self.assertEqual(journey_response.status_code, 404)
        self.assertEqual(ask_response.status_code, 404)
        self.assertEqual(progress_response.status_code, 404)
        self.assertEqual(session_response.status_code, 404)

    def test_openapi_examples_are_exposed_for_core_endpoints(self) -> None:
        response = self.client.get("/openapi.json")

        self.assertEqual(response.status_code, 200)
        schema = response.json()
        paths = schema["paths"]

        onboard_post = paths["/api/v1/onboard"]["post"]
        onboard_request_example = onboard_post["requestBody"]["content"]["application/json"]["examples"][
            "ga_foreign_license_transfer"
        ]["value"]
        onboard_response_example = onboard_post["responses"]["201"]["content"]["application/json"]["example"]
        self.assertEqual(onboard_request_example["state"], "GA")
        self.assertEqual(onboard_request_example["foreign_license_country"], "France")
        self.assertEqual(onboard_response_example["journey_type"], "ga_drivers_license")
        self.assertEqual(onboard_response_example["branch_summary"]["license_path"], "foreign_reciprocity_transfer")

        journey_get = paths["/api/v1/journeys/{journey_id}"]["get"]
        journey_response_example = journey_get["responses"]["200"]["content"]["application/json"]["example"]
        self.assertEqual(journey_response_example["title"], "Georgia Driver’s License")
        self.assertEqual(journey_response_example["progress"]["percent"], 29)

        ask_post = paths["/api/v1/journeys/{journey_id}/ask"]["post"]
        ask_request_example = ask_post["requestBody"]["content"]["application/json"]["examples"][
            "residency_proof_question"
        ]["value"]
        ask_response_example = ask_post["responses"]["200"]["content"]["application/json"]["example"]
        self.assertEqual(
            ask_request_example["question"],
            "What if I don’t have a utility bill for proof of residency?",
        )
        self.assertEqual(ask_response_example["citations"][0]["source_key"], "ga_dds_residency_docs")

        progress_patch = paths["/api/v1/journeys/{journey_id}/progress"]["patch"]
        progress_request_example = progress_patch["requestBody"]["content"]["application/json"]["examples"][
            "complete_first_step"
        ]["value"]
        progress_response_example = progress_patch["responses"]["200"]["content"]["application/json"]["example"]
        self.assertEqual(progress_request_example, {"step_id": "step_1", "completed": True})
        self.assertEqual(progress_response_example["steps"][0]["completed"], True)

        session_get = paths["/api/v1/sessions/{journey_id}"]["get"]
        session_response_example = session_get["responses"]["200"]["content"]["application/json"]["example"]
        self.assertEqual(session_response_example["journey_id"], "jrny_123")
        self.assertEqual(session_response_example["profile_summary"]["state"], "GA")
        self.assertEqual(session_response_example["chat_history"][0]["role"], "user")


if __name__ == "__main__":
    unittest.main()
