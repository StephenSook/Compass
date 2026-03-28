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


if __name__ == "__main__":
    unittest.main()
