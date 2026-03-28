from __future__ import annotations

from typing import Any

from app.schemas.common import JourneyRecord, JourneyStatusEnum, JourneyTypeEnum, SessionRecord
from app.services.knowledge_base import KnowledgeBaseService


class MockCompassAIService:
    """Simple rule-based assistant for demo-quality contextual guidance."""

    IMMIGRATION_KEYWORDS = {
        "visa",
        "uscis",
        "immigration",
        "green card",
        "opt",
        "i-130",
        "i-539",
        "i-765",
        "status",
        "employment authorization",
        "ead",
        "work authorization",
    }

    def __init__(self, knowledge_base_service: KnowledgeBaseService | None = None) -> None:
        self.knowledge_base_service = knowledge_base_service or KnowledgeBaseService()

    def generate_response(
        self,
        *,
        journey: JourneyRecord,
        session: SessionRecord,
        question: str,
    ) -> dict[str, Any]:
        knowledge_context = self.knowledge_base_service.get_context_for_branch(
            journey.branch_key,
            journey.user_profile,
        )
        intent = self._detect_intent(journey, session, question)

        if intent == "residency_alternatives":
            response = self._answer_residency_alternatives(journey, knowledge_context)
        elif intent == "foreign_license":
            response = self._answer_foreign_license(journey, knowledge_context)
        elif intent == "i765_timing":
            response = self._answer_i765_timing(journey, knowledge_context)
        elif intent == "fee":
            response = self._answer_fee(journey, knowledge_context)
        elif intent == "location":
            response = self._answer_location(journey, knowledge_context)
        elif intent == "no_ssn":
            response = self._answer_no_ssn(journey, knowledge_context)
        else:
            response = self._answer_general_guidance(journey, knowledge_context, question)

        legal_warning = self._needs_legal_warning(journey, question, intent)
        answer = response["answer"]
        if legal_warning:
            answer += (
                " Because immigration timing, eligibility, and status consequences can depend on individual facts, "
                "treat this as general guidance and get qualified legal help if anything is unclear."
            )

        return {
            "answer": answer,
            "citations": response["citations"],
            "legal_warning": legal_warning,
            "recommended_next_step": response["recommended_next_step"],
        }

    def answer_question(
        self,
        *,
        journey: JourneyRecord,
        session: SessionRecord,
        question: str,
    ) -> str:
        return self.generate_response(journey=journey, session=session, question=question)["answer"]

    def build_citations(
        self,
        journey: JourneyRecord,
        *,
        session: SessionRecord | None = None,
        question: str | None = None,
    ) -> list[dict[str, Any]]:
        if session is not None and question is not None:
            return self.generate_response(journey=journey, session=session, question=question)["citations"]
        return self._default_citations(journey)

    def needs_legal_caution(
        self,
        journey: JourneyRecord,
        question: str,
        *,
        session: SessionRecord | None = None,
    ) -> bool:
        if session is not None:
            intent = self._detect_intent(journey, session, question)
            return self._needs_legal_warning(journey, question, intent)
        return self._needs_legal_warning(journey, question, "general")

    def recommended_next_step(
        self,
        journey: JourneyRecord,
        *,
        session: SessionRecord | None = None,
        question: str | None = None,
    ) -> str | None:
        if session is not None and question is not None:
            return self.generate_response(journey=journey, session=session, question=question)["recommended_next_step"]
        next_step = self._get_next_step(journey)
        return next_step.title if next_step else None

    def _answer_residency_alternatives(
        self,
        journey: JourneyRecord,
        knowledge_context: dict[str, Any],
    ) -> dict[str, Any]:
        relevant_step = self._find_step(
            journey,
            title_keywords=("gather documents",),
            text_keywords=("residency", "utility bill", "bank statement", "lease"),
        )
        county = journey.user_profile.county or "your county"
        answer = (
            f"If you do not have a utility bill, you may still be able to use other Georgia residency documents such "
            f"as a bank statement, signed lease, or official mail that shows your current address in {county}. "
            "Bring two different residency proofs because one document is often not enough. "
            "Accepted document types can change by office and current DDS rules, so this needs manual verification before your appointment."
        )
        return {
            "answer": answer,
            "citations": [
                self._citation("knowledge_base", "ga_dds_residency_docs"),
                self._citation("knowledge_base", "ga_two_residency_proofs_tip"),
                self._office_citation(knowledge_context.get("office")),
            ],
            "recommended_next_step": relevant_step.title if relevant_step else "Gather documents",
        }

    def _answer_foreign_license(
        self,
        journey: JourneyRecord,
        knowledge_context: dict[str, Any],
    ) -> dict[str, Any]:
        profile = journey.user_profile
        country = profile.foreign_license_country or "your country"
        is_direct_transfer = bool(journey.derived_flags.get("is_direct_transfer"))
        relevant_step = self._find_step(
            journey,
            title_keywords=("confirm", "gather documents"),
            text_keywords=("foreign", "transfer", "reciprocity"),
        )

        if not profile.has_foreign_license:
            answer = (
                "Your current profile does not show a foreign license, so the checklist is not treating this as a "
                "foreign-license transfer case. If that profile detail is wrong, update it first so the journey can route correctly."
            )
        elif is_direct_transfer:
            answer = (
                f"Yes, your current journey treats the {country} license as a possible reciprocity or direct-transfer path. "
                "That usually means DDS may review the foreign license and may waive some testing, but you should not assume the waiver is automatic. "
                "Bring the original license, identity documents, and a certified translation if the license is not in English. "
                "This still needs manual verification by DDS at the appointment."
            )
        else:
            answer = (
                f"You can still bring your foreign license from {country}, but this journey does not currently place you on a direct-transfer waiver path. "
                "In that situation, the license is usually supporting evidence rather than a guarantee that Georgia will skip testing. "
                "Bring it anyway with the rest of your identity and residency documents, and manually verify your exact DDS testing requirements."
            )

        return {
            "answer": answer,
            "citations": [
                self._citation("knowledge_base", "ga_dds_foreign_license_rules"),
                self._citation(
                    "knowledge_base",
                    "ga_dds_foreign_license_reciprocity" if is_direct_transfer else "ga_dds_testing_rules",
                ),
                self._office_citation(knowledge_context.get("office")),
            ],
            "recommended_next_step": relevant_step.title if relevant_step else self._title_for_next_step(journey),
        }

    def _answer_i765_timing(
        self,
        journey: JourneyRecord,
        knowledge_context: dict[str, Any],
    ) -> dict[str, Any]:
        timelines = knowledge_context.get("timelines", {})
        rules = knowledge_context.get("rules", {})
        filing_window = rules.get("filing_window") or timelines.get("filing_window") or "File as early as your rules allow."
        processing = rules.get("processing_time") or timelines.get("processing") or "Processing times vary."
        relevant_step = self._find_step(
            journey,
            title_keywords=("file", "submit", "prepare"),
            text_keywords=("i-765", "uscis", "opt"),
        )
        answer = (
            f"For this immigration flow, the current guidance says: {filing_window} "
            f"USCIS processing for Form I-765 is often around {processing.lower().rstrip('.')}. "
            "That timing can move up or down based on USCIS workload and your filing details, so if your work start date is important, it needs manual verification against current USCIS processing information."
        )
        return {
            "answer": answer,
            "citations": [
                self._form_citation(knowledge_context),
                self._citation("knowledge_base", "uscis_i765_processing_time"),
            ],
            "recommended_next_step": relevant_step.title if relevant_step else self._title_for_next_step(journey),
        }

    def _answer_fee(
        self,
        journey: JourneyRecord,
        knowledge_context: dict[str, Any],
    ) -> dict[str, Any]:
        fees = knowledge_context.get("fees", [])
        relevant_step = self._find_step(
            journey,
            title_keywords=("pay fee", "pay"),
            text_keywords=("fee", "payment", "cost"),
        )

        if not fees:
            answer = (
                "I do not see a fee amount in the current knowledge-base context for this journey, so you should check the official form or agency page. "
                "That amount needs manual verification before you pay."
            )
            citations = self._default_citations(journey)
        elif len(fees) == 1:
            fee = fees[0]
            answer = (
                f"The current fee in your journey context is ${fee['amount_usd']} for {fee['label']}. "
                "Bring payment at the step shown in your checklist and verify the latest fee schedule before the appointment or filing, in case the agency changed it."
            )
            citations = [self._citation("knowledge_base", fee["id"], label=fee["label"])]
        else:
            fee_parts = [f"${fee['amount_usd']} for {fee['label']}" for fee in fees]
            answer = (
                f"The current fee breakdown in your journey is {', '.join(fee_parts)}. "
                "Use the checklist step for payment timing, and verify the latest official fee page before you submit anything."
            )
            citations = [self._citation("knowledge_base", fee["id"], label=fee["label"]) for fee in fees]

        return {
            "answer": answer,
            "citations": citations,
            "recommended_next_step": relevant_step.title if relevant_step else self._title_for_next_step(journey),
        }

    def _answer_location(
        self,
        journey: JourneyRecord,
        knowledge_context: dict[str, Any],
    ) -> dict[str, Any]:
        office = knowledge_context.get("office")
        relevant_step = self._find_step(
            journey,
            title_keywords=("book", "appointment", "office"),
            text_keywords=("office", "location", "appointment"),
        )

        if office:
            address = office.get("address", {})
            address_text = ", ".join(
                value for value in [address.get("street"), address.get("city"), address.get("state"), address.get("postal_code")] if value
            )
            answer = (
                f"Based on your current journey, the best office reference is {office['name']}"
                f"{f' at {address_text}' if address_text else ''}. "
                f"{office.get('hours', 'Check current office hours before going.')} "
                "Appointment availability and walk-in rules can change, so manually verify the location and hours before you go."
            )
            citations = [self._office_citation(office)]
        else:
            answer = (
                "I do not see a specific office in the current context, so use the official office or facility locator linked in your journey before you travel. "
                "That location needs manual verification."
            )
            citations = self._default_citations(journey)

        return {
            "answer": answer,
            "citations": citations,
            "recommended_next_step": relevant_step.title if relevant_step else self._title_for_next_step(journey),
        }

    def _answer_no_ssn(
        self,
        journey: JourneyRecord,
        knowledge_context: dict[str, Any],
    ) -> dict[str, Any]:
        profile = journey.user_profile
        relevant_step = self._find_step(
            journey,
            title_keywords=("gather documents",),
            text_keywords=("ssn", "itin", "social security"),
        )

        if journey.journey_type != JourneyTypeEnum.DRIVERS_LICENSE:
            answer = (
                "Your question mentions an SSN, but the current journey is not a Georgia DDS license flow. "
                "For this process, follow the document checklist and verify whether the agency specifically requires an SSN or only identity and status records."
            )
        elif profile.has_ssn:
            answer = (
                "Your current profile says you have an SSN, so the DDS path expects you to bring the Social Security card along with identity, lawful presence, and Georgia residency documents."
            )
        else:
            answer = (
                "If you do not have an SSN, the current Georgia DDS path usually shifts you to alternative SSN evidence, such as an SSN denial letter, plus your passport, immigration documents, and any ITIN-related identity records you have. "
                "Bring those with two Georgia residency proofs. "
                "DDS document acceptance can vary by case, so this needs manual verification before the appointment."
            )

        return {
            "answer": answer,
            "citations": [
                self._citation("knowledge_base", "ga_dds_ssn_alternative_docs"),
                self._citation("knowledge_base", "ga_dds_identity_and_residency_docs"),
            ],
            "recommended_next_step": relevant_step.title if relevant_step else "Gather documents",
        }

    def _answer_general_guidance(
        self,
        journey: JourneyRecord,
        knowledge_context: dict[str, Any],
        question: str,
    ) -> dict[str, Any]:
        next_step = self._get_next_step(journey)
        next_step_title = next_step.title if next_step else "review your checklist"
        county = journey.user_profile.county or "your county"
        first_open_steps = [step.title for step in journey.steps if step.status != JourneyStatusEnum.COMPLETED][:3]
        answer = (
            f"For your {journey.title.lower()} journey in {county}, the clearest next move is to focus on '{next_step_title}'. "
            f"The checklist already covers the most relevant items, including {', '.join(first_open_steps) if first_open_steps else 'your completed steps'}. "
            f"If your question is more specific, ask about documents, fees, office location, timing, or SSN requirements and I will answer from the current journey context."
        )
        if self._question_is_uncertain(question):
            answer += " If the issue depends on current agency practice or your exact documents, it needs manual verification."
        return {
            "answer": answer,
            "citations": self._default_citations(journey, knowledge_context=knowledge_context),
            "recommended_next_step": next_step_title if next_step else None,
        }

    def _detect_intent(self, journey: JourneyRecord, session: SessionRecord, question: str) -> str:
        haystack = self._conversation_haystack(session, question)
        if self._matches_any(haystack, "utility bill", "proof of residency", "residency", "bank statement", "lease"):
            return "residency_alternatives"
        if self._matches_any(haystack, "foreign license", "foreign licence", "reciprocity", "transfer my license"):
            return "foreign_license"
        if self._matches_any(haystack, "i-765", "uscis", "employment authorization", "ead") and self._matches_any(
            haystack,
            "how long",
            "processing",
            "process",
            "take",
            "timeline",
            "wait",
        ):
            return "i765_timing"
        if self._matches_any(haystack, "fee", "cost", "how much", "payment", "pay"):
            return "fee"
        if self._matches_any(haystack, "where do i go", "where should i go", "where do i file", "office", "location", "address"):
            return "location"
        if self._matches_any(haystack, "no ssn", "don't have an ssn", "do not have an ssn", "social security", "itin", "ssn"):
            return "no_ssn"
        if journey.journey_type == JourneyTypeEnum.VISA and self._matches_any(haystack, "how long does it take", "processing time"):
            return "i765_timing"
        return "general"

    def _needs_legal_warning(self, journey: JourneyRecord, question: str, intent: str) -> bool:
        haystack = f"{journey.title} {journey.summary} {question}".lower()
        if journey.journey_type != JourneyTypeEnum.VISA:
            return False
        if intent in {"i765_timing", "general"}:
            return True
        return any(keyword in haystack for keyword in self.IMMIGRATION_KEYWORDS)

    def _get_next_step(self, journey: JourneyRecord):
        for step in journey.steps:
            if step.status != JourneyStatusEnum.COMPLETED:
                return step
        return journey.steps[-1] if journey.steps else None

    def _title_for_next_step(self, journey: JourneyRecord) -> str | None:
        next_step = self._get_next_step(journey)
        return next_step.title if next_step else None

    def _find_step(
        self,
        journey: JourneyRecord,
        *,
        title_keywords: tuple[str, ...] = (),
        text_keywords: tuple[str, ...] = (),
    ):
        for step in journey.steps:
            title = step.title.lower()
            description = step.description.lower()
            if title_keywords and any(keyword in title for keyword in title_keywords):
                return step
            if text_keywords and any(keyword in description for keyword in text_keywords):
                return step
        return self._get_next_step(journey)

    def _default_citations(
        self,
        journey: JourneyRecord,
        *,
        knowledge_context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        context = knowledge_context or self.knowledge_base_service.get_context_for_branch(
            journey.branch_key,
            journey.user_profile,
        )
        citations: list[dict[str, Any]] = []
        form_citation = self._form_citation(context)
        if form_citation:
            citations.append(form_citation)
        office_citation = self._office_citation(context.get("office"))
        if office_citation:
            citations.append(office_citation)
        if not citations:
            next_step = self._get_next_step(journey)
            if next_step:
                citations.append(
                    {
                        "source_type": "journey_step",
                        "source_key": next_step.title.lower().replace(" ", "_"),
                        "label": next_step.title,
                    }
                )
        return citations

    def _form_citation(self, knowledge_context: dict[str, Any]) -> dict[str, Any] | None:
        forms = knowledge_context.get("forms") or knowledge_context.get("portals") or []
        if not forms:
            return None
        form = forms[0]
        return {
            "source_type": "form",
            "source_key": form.get("id", form.get("name", "form")),
            "label": form.get("name"),
            "url": form.get("url"),
        }

    def _office_citation(self, office: dict[str, Any] | None) -> dict[str, Any] | None:
        if not office:
            return None
        return {
            "source_type": "office",
            "source_key": office.get("id", "office"),
            "label": office.get("name"),
            "url": office.get("appointment_url"),
        }

    def _citation(
        self,
        source_type: str,
        source_key: str,
        *,
        label: str | None = None,
        url: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "source_type": source_type,
            "source_key": source_key,
        }
        if label:
            payload["label"] = label
        if url:
            payload["url"] = url
        return payload

    def _conversation_haystack(self, session: SessionRecord, question: str) -> str:
        recent_messages = " ".join(turn.message for turn in session.turns[-4:])
        normalized = f"{recent_messages} {question}".lower()
        return normalized.replace("’", "'")

    def _question_is_uncertain(self, question: str) -> bool:
        haystack = question.lower()
        return any(token in haystack for token in {"maybe", "not sure", "unclear", "depends", "can i"})

    def _matches_any(self, haystack: str, *keywords: str) -> bool:
        return any(keyword in haystack for keyword in keywords)
