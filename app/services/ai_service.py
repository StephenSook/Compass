from __future__ import annotations

from app.schemas.common import JourneyRecord, SessionRecord


class MockCompassAIService:
    """Grounded answer generator shaped like a future Gemini integration."""

    IMMIGRATION_KEYWORDS = {
        "visa",
        "uscis",
        "immigration",
        "green card",
        "opt",
        "i-130",
        "i-539",
        "i-765",
    }

    def answer_question(
        self,
        *,
        journey: JourneyRecord,
        session: SessionRecord,
        question: str,
    ) -> str:
        next_step = self._get_next_step(journey)
        step_titles = ", ".join(step.title for step in journey.steps[:3])
        answer = (
            f"Based on your {journey.title.lower()} journey, the most relevant next move is "
            f"'{next_step.title}'. The checklist already covers key details like {step_titles}. "
            f"For your question, start by reviewing the documents, fees, and timeline listed on that step, "
            f"and use the office or form links in the journey before taking action. "
            f"This session currently has {len(session.turns)} prior message(s), so the advice stays tied to your case profile in {journey.user_profile.county} County, {journey.user_profile.state}."
        )

        if self._needs_legal_caution(journey, question):
            answer += (
                " Because immigration consequences can be serious and facts matter, treat this as general guidance "
                "only and get qualified legal advice or accredited nonprofit help if anything is uncertain."
            )

        return answer

    def _get_next_step(self, journey: JourneyRecord):
        for step in journey.steps:
            if step.status != "completed":
                return step
        return journey.steps[-1]

    def _needs_legal_caution(self, journey: JourneyRecord, question: str) -> bool:
        haystack = f"{journey.title} {journey.summary} {question}".lower()
        return any(keyword in haystack for keyword in self.IMMIGRATION_KEYWORDS)
