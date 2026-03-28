from __future__ import annotations

from app.schemas.common import JourneyRecord, JourneyStatusEnum, SessionRecord


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
    DDS_KEYWORDS = {"dds", "license", "road test", "knowledge test", "transfer", "joshua", "ssn"}
    PASSPORT_KEYWORDS = {"passport", "ds-11", "ds-82", "photo", "expedite", "renewal", "mail"}

    def answer_question(
        self,
        *,
        journey: JourneyRecord,
        session: SessionRecord,
        question: str,
    ) -> str:
        next_step = self._get_next_step(journey)
        step_titles = ", ".join(step.title for step in journey.steps[:3])
        county = journey.user_profile.county or "the relevant county"
        next_step_title = next_step.title if next_step else "review your journey details"
        focus = self._focus_hint(journey, question)
        answer = (
            f"Based on your {journey.title.lower()} journey, the most relevant next move is "
            f"'{next_step_title}'. The checklist already covers key details like {step_titles}. "
            f"{focus} Start by reviewing the documents, fees, and timeline listed on that step, "
            f"and use the office or form links in the journey before taking action. "
            f"This session currently has {len(session.turns)} prior message(s), so the advice stays tied to your case profile in {county}, {journey.user_profile.state}."
        )

        if self.needs_legal_caution(journey, question):
            answer += (
                " Because immigration consequences can be serious and facts matter, treat this as general guidance "
                "only and get qualified legal advice or accredited nonprofit help if anything is uncertain."
            )

        return answer

    def _get_next_step(self, journey: JourneyRecord):
        for step in journey.steps:
            if step.status != JourneyStatusEnum.COMPLETED:
                return step
        return journey.steps[-1] if journey.steps else None

    def needs_legal_caution(self, journey: JourneyRecord, question: str) -> bool:
        haystack = f"{journey.title} {journey.summary} {question}".lower()
        return any(keyword in haystack for keyword in self.IMMIGRATION_KEYWORDS)

    def recommended_next_step(self, journey: JourneyRecord) -> str | None:
        next_step = self._get_next_step(journey)
        return next_step.title if next_step else None

    def build_citations(self, journey: JourneyRecord) -> list[dict[str, str]]:
        citations: list[dict[str, str]] = []
        for step in journey.steps[:3]:
            if step.forms:
                first_form = step.forms[0]
                citations.append(
                    {
                        "title": step.title,
                        "source_type": "form",
                        "label": first_form.name,
                        "url": first_form.url or "",
                    }
                )
            elif step.office:
                citations.append(
                    {
                        "title": step.title,
                        "source_type": "office",
                        "label": step.office.name,
                        "url": step.office.appointment_url or "",
                    }
                )
            else:
                citations.append(
                    {
                        "title": step.title,
                        "source_type": "journey_step",
                        "label": step.title,
                        "url": "",
                    }
                )
        return citations

    def _focus_hint(self, journey: JourneyRecord, question: str) -> str:
        haystack = question.lower()
        if journey.journey_type == "drivers_license":
            if any(keyword in haystack for keyword in {"road", "drive", "skills"}):
                return "Your question sounds focused on the road skills part of the DDS process."
            if any(keyword in haystack for keyword in {"written", "knowledge", "manual", "test"}):
                return "Your question sounds focused on the written knowledge-test part of the DDS process."
            if any(keyword in haystack for keyword in {"ssn", "social security", "itin"}):
                return "Your question sounds focused on the SSN and identity-document portion of the DDS process."
            if any(keyword in haystack for keyword in self.DDS_KEYWORDS):
                return "Your question lines up with the current Georgia DDS checklist."
        if journey.journey_type == "passport":
            if any(keyword in haystack for keyword in {"renew", "renewal", "mail", "ds-82"}):
                return "Your question is pointing to the passport renewal requirements and mailing rules."
            if any(keyword in haystack for keyword in {"new", "first", "ds-11", "acceptance"}):
                return "Your question is pointing to the first-time passport application and acceptance-facility steps."
            if any(keyword in haystack for keyword in self.PASSPORT_KEYWORDS):
                return "Your question matches the passport forms, fees, and appointment details in your checklist."
        if journey.journey_type == "visa":
            if "opt" in haystack or "i-765" in haystack:
                return "Your question is centered on OPT timing, filing, or work-authorization details."
            if "i-130" in haystack or "green card" in haystack or "family" in haystack:
                return "Your question is centered on the family-based petition path and supporting evidence."
            if "i-539" in haystack or "extend" in haystack or "extension" in haystack:
                return "Your question is centered on extension timing and staying in status before expiration."
            if any(keyword in haystack for keyword in self.IMMIGRATION_KEYWORDS):
                return "Your question matches the immigration filing and deadline details in your checklist."
        return "Your question fits the current checklist context."
