from __future__ import annotations

from uuid import UUID

from app.core.exceptions import InvalidProgressUpdateError, JourneyNotFoundError
from app.core.utils import new_uuid, utc_now
from app.repositories.base import JourneyRepository
from app.rules.knowledge_base import get_journey_template
from app.rules.models import RoutingDecision
from app.schemas.common import (
    FormInfo,
    JourneyRecord,
    JourneyStatusEnum,
    JourneyStep,
    OfficeInfo,
    UserProfile,
)
from app.schemas.journey import JourneyOut, JourneyStepOut
from app.schemas.journey import ProgressUpdateRequest
from app.services.journey_builder import build_progress_summary, determine_journey_status


class JourneyService:
    def __init__(self, journey_repository: JourneyRepository) -> None:
        self.journey_repository = journey_repository

    def create_journey(
        self,
        *,
        user_id,
        profile_id,
        session_id,
        profile: UserProfile,
        routing: RoutingDecision,
    ) -> JourneyRecord:
        template = get_journey_template(routing.template_key)
        step_specs = self._build_step_specs(profile=profile, routing=routing, template=template)
        steps = self._build_journey_steps(step_specs)
        timestamp = utc_now()
        journey = JourneyRecord(
            id=new_uuid(),
            user_id=user_id,
            profile_id=profile_id,
            session_id=session_id,
            title=template["title"],
            journey_type=routing.journey_type,
            branch_key=routing.branch_key,
            summary=template["summary"],
            branch_summary=routing.branch_summary,
            derived_flags=routing.derived_flags,
            status=determine_journey_status(steps),
            state=profile.state,
            language=profile.language,
            user_profile=profile,
            steps=steps,
            progress=build_progress_summary(steps),
            created_at=timestamp,
            updated_at=timestamp,
        )
        return self.journey_repository.create(journey)

    def build_checklist(
        self,
        *,
        journey_id: str,
        profile: UserProfile,
        routing: RoutingDecision,
    ) -> JourneyOut:
        template = get_journey_template(routing.template_key)
        step_specs = self._build_step_specs(profile=profile, routing=routing, template=template)
        total_steps = len(step_specs)
        return JourneyOut(
            journey_id=journey_id,
            journey_type=routing.journey_type,
            title=template["title"],
            status=JourneyStatusEnum.IN_PROGRESS if total_steps else JourneyStatusEnum.NOT_STARTED,
            progress={
                "completed_steps": 0,
                "total_steps": total_steps,
                "percent": 0,
            },
            steps=[
                JourneyStepOut(
                    step_id=f"step-{index + 1}",
                    order_index=index,
                    title=spec["title"],
                    action=spec["description"],
                    documents=list(spec.get("documents", [])),
                    form_number=self._extract_form_number(spec),
                    form_url=self._extract_form_url(spec),
                    fee_usd=self._extract_fee(spec.get("fee")),
                    office_name=self._extract_office_value(spec, "name"),
                    office_address=self._extract_office_value(spec, "address"),
                    office_hours=self._extract_office_value(spec, "hours"),
                    estimated_time=spec.get("timeline"),
                    tip=spec.get("tip"),
                    warning=spec.get("warning"),
                    completed=False,
                )
                for index, spec in enumerate(step_specs)
            ],
            disclaimer="This tool provides guidance, not legal advice.",
        )

    def get_journey(self, journey_id: UUID) -> JourneyRecord:
        journey = self.journey_repository.get(journey_id)
        if journey is None:
            raise JourneyNotFoundError(f"Journey '{journey_id}' was not found.")
        return journey

    def update_progress(self, journey_id: UUID, payload: ProgressUpdateRequest) -> JourneyRecord:
        journey = self.get_journey(journey_id)
        try:
            target_step_id = UUID(payload.step_id)
        except ValueError as exc:
            raise InvalidProgressUpdateError("step_id must be a valid UUID string.") from exc

        updated_steps = []
        step_found = False
        for step in journey.steps:
            if step.id == target_step_id:
                step_found = True
                status = JourneyStatusEnum.COMPLETED if payload.completed else JourneyStatusEnum.NOT_STARTED
                updated_steps.append(step.model_copy(update={"status": status}))
            else:
                updated_steps.append(step)

        if not step_found:
            raise InvalidProgressUpdateError(f"Unknown step id for this journey: {payload.step_id}.")

        if updated_steps and not all(step.status == JourneyStatusEnum.COMPLETED for step in updated_steps):
            updated_steps = [
                step.model_copy(update={"status": JourneyStatusEnum.NOT_STARTED})
                if step.status == JourneyStatusEnum.IN_PROGRESS
                else step
                for step in updated_steps
            ]
            for index, step in enumerate(updated_steps):
                if step.status != JourneyStatusEnum.COMPLETED:
                    updated_steps[index] = step.model_copy(update={"status": JourneyStatusEnum.IN_PROGRESS})
                    break

        updated_journey = journey.model_copy(
            update={
                "steps": updated_steps,
                "progress": build_progress_summary(updated_steps),
                "status": determine_journey_status(updated_steps),
            }
        )
        return self.journey_repository.update(updated_journey)

    def _build_step_specs(
        self,
        *,
        profile: UserProfile,
        routing: RoutingDecision,
        template: dict[str, object],
    ) -> list[dict[str, object]]:
        if routing.template_key.startswith("ga_license"):
            return self._ga_license_step_specs(profile, routing)
        return self._enrich_template_steps(profile=profile, routing=routing, template=template)

    def _build_journey_steps(self, step_specs: list[dict[str, object]]) -> list[JourneyStep]:
        steps = [
            JourneyStep(
                id=new_uuid(),
                title=spec["title"],
                description=spec["description"],
                documents=list(spec.get("documents", [])),
                forms=[FormInfo(**form) for form in spec.get("forms", [])],
                fee=spec.get("fee"),
                office=OfficeInfo(**spec["office"]) if spec.get("office") else None,
                timeline=spec.get("timeline"),
                tip=spec.get("tip"),
                warning=spec.get("warning"),
            )
            for spec in step_specs
        ]
        if steps:
            steps[0] = steps[0].model_copy(update={"status": JourneyStatusEnum.IN_PROGRESS})
        return steps

    def _ga_license_step_specs(
        self,
        profile: UserProfile,
        routing: RoutingDecision,
    ) -> list[dict[str, object]]:
        county = profile.county or "your county"
        office = {
            "name": "Georgia Department of Driver Services",
            "address": f"Use the DDS locator for the nearest office serving {county}.",
            "hours": "Typically Monday-Friday, 8:00 AM-5:00 PM",
            "appointment_url": "https://dds.georgia.gov/locations",
        }
        base_documents = self._ga_license_documents(profile, routing)
        ssn_warning = (
            "If you do not have an SSN, bring DDS-accepted alternative evidence such as an SSN denial letter "
            "and keep ITIN-related identity records available."
            if routing.derived_flags.get("needs_ssn_alternative_docs")
            else None
        )
        joshuas_warning = (
            "Joshua's Law applies because the applicant is under 18. Bring course completion and supervised driving records."
            if routing.derived_flags.get("requires_joshuas_law")
            else None
        )
        knowledge_title, knowledge_description, knowledge_warning = self._ga_knowledge_step(routing)
        road_title, road_description, road_warning = self._ga_road_step(routing)

        return [
            {
                "title": "Gather documents",
                "description": "Collect identity, lawful presence, residency, and license-transfer documents before starting the DDS process.",
                "documents": base_documents,
                "timeline": "Do this before booking the appointment.",
                "tip": "Bring two printed Georgia residency proofs because applicants are often turned away with only one.",
                "warning": self._combine_warnings(ssn_warning, joshuas_warning),
            },
            {
                "title": "Complete online application",
                "description": "Finish the Georgia DDS online application using your legal name exactly as it appears on identity records.",
                "forms": [{"name": "Georgia DDS Online Application", "url": "https://dds.georgia.gov/"}],
                "timeline": "Usually 10-15 minutes online.",
                "tip": "Save the confirmation page or screenshot after submitting the online form.",
            },
            {
                "title": "Book DDS appointment",
                "description": "Reserve a DDS appointment and choose an office convenient to your county.",
                "forms": [{"name": "DDS Appointment Scheduler", "url": "https://dds.georgia.gov/"}],
                "office": office,
                "timeline": "Appointments are usually faster than walk-ins in Metro Atlanta.",
                "tip": "Choose a location that handles the type of testing or transfer review you may need.",
            },
            {
                "title": knowledge_title,
                "description": knowledge_description,
                "timeline": "Usually reviewed during the DDS visit.",
                "tip": "Study the Georgia Driver's Manual unless DDS confirms your transfer path waives the written test.",
                "warning": self._combine_warnings(knowledge_warning, joshuas_warning),
            },
            {
                "title": road_title,
                "description": road_description,
                "timeline": "Same-day or follow-up scheduling depends on the office and path.",
                "tip": "Bring a properly insured vehicle if a road skills test may still apply.",
                "warning": road_warning,
            },
            {
                "title": "Pay fee",
                "description": "Pay the Georgia Class C license fee after completing the required transfer review or testing steps.",
                "fee": "$32",
                "timeline": "Payment is typically made during the DDS visit.",
                "tip": "Keep the receipt until the physical card arrives by mail.",
                "warning": ssn_warning,
            },
            {
                "title": "Receive license",
                "description": "Use the temporary paper credential after your visit and wait for the hard card to arrive by mail.",
                "timeline": "Temporary paper license the same day; hard card usually arrives in 2-3 weeks.",
                "tip": "Make sure your mailing address matches your residency proofs to avoid delivery issues.",
            },
        ]

    def _enrich_template_steps(
        self,
        *,
        profile: UserProfile,
        routing: RoutingDecision,
        template: dict[str, object],
    ) -> list[dict[str, object]]:
        steps: list[dict[str, object]] = []
        for index, raw_step in enumerate(template["steps"]):
            step = dict(raw_step)
            if routing.journey_type == "visa":
                legal_warning = (
                    "Immigration eligibility and deadlines can change based on individual facts. Review official instructions and get legal help if anything is unclear."
                )
                step["warning"] = self._combine_warnings(step.get("warning"), legal_warning)
            if routing.template_key == "passport_first_time" and index == 2:
                office = dict(step.get("office") or {})
                office["address"] = (
                    f"Choose a USPS or county acceptance facility convenient to {profile.county or 'your area'}."
                )
                step["office"] = office
            steps.append(step)
        return steps

    def _ga_license_documents(
        self,
        profile: UserProfile,
        routing: RoutingDecision,
    ) -> list[str]:
        documents = [
            "Passport or birth certificate",
            "Visa and I-94 record if applicable",
            "Two proofs of Georgia residency",
        ]
        if routing.derived_flags.get("has_us_license"):
            documents.insert(0, "Current out-of-state driver's license")
        elif routing.derived_flags.get("has_foreign_license"):
            documents.insert(0, "Foreign driver's license")
            if profile.foreign_license_country:
                documents.insert(1, f"License from {profile.foreign_license_country}")
            if routing.derived_flags.get("is_direct_transfer_country"):
                documents.append("Certified translation if the license is not in English")
        if routing.derived_flags.get("needs_ssn_alternative_docs"):
            documents.append("SSN denial letter or DDS-accepted alternative evidence")
            documents.append("ITIN letter or tax identity record if available")
        else:
            documents.append("Social Security card")
        if routing.derived_flags.get("requires_joshuas_law"):
            documents.append("Joshua's Law completion certificate")
            documents.append("Driving log signed by parent or guardian")
        return documents

    def _ga_knowledge_step(self, routing: RoutingDecision) -> tuple[str, str, str | None]:
        if routing.derived_flags.get("is_us_transfer"):
            return (
                "Confirm knowledge test waiver",
                "Bring your active out-of-state license and ask DDS to confirm whether the transfer path waives the Georgia knowledge test.",
                "Even transfer applicants may be asked for extra verification if records or immigration documents do not match.",
            )
        if routing.derived_flags.get("is_direct_transfer"):
            return (
                "Confirm reciprocity-based knowledge test waiver",
                "Ask DDS whether your qualifying foreign license allows you to skip the Georgia knowledge test under the direct-transfer path.",
                "Reciprocity is limited to specific countries and DDS may still require additional checks.",
            )
        if routing.derived_flags.get("requires_joshuas_law"):
            return (
                "Pass knowledge test",
                "Prepare for the Georgia knowledge test and teen-driver rules after completing Joshua's Law requirements.",
                "Teen applicants can be turned away if Joshua's Law or school compliance documents are missing.",
            )
        return (
            "Pass knowledge test",
            "Study the Georgia Driver's Manual and pass the written knowledge test at DDS.",
            None,
        )

    def _ga_road_step(self, routing: RoutingDecision) -> tuple[str, str, str | None]:
        if routing.derived_flags.get("is_us_transfer"):
            return (
                "Confirm road skills test waiver",
                "Verify whether your transfer path allows you to skip the Georgia road skills test after DDS reviews your current US license.",
                "If DDS does not waive the road test, you may need to return with a qualified vehicle.",
            )
        if routing.derived_flags.get("is_direct_transfer"):
            return (
                "Confirm road skills test waiver",
                "Ask DDS whether your direct-transfer foreign license path waives the road skills test or requires a follow-up appointment.",
                "Do not assume the test is waived until DDS confirms your exact case.",
            )
        if routing.derived_flags.get("requires_joshuas_law"):
            return (
                "Pass road skills test",
                "Schedule or complete the teen road skills test using a properly insured vehicle that meets DDS requirements.",
                "Bring the parent or guardian documents required for under-18 applicants.",
            )
        return (
            "Pass road skills test",
            "Complete the Georgia road skills test after passing the written test and vision screening.",
            None,
        )

    def _combine_warnings(self, *warnings: str | None) -> str | None:
        values = [warning for warning in warnings if warning]
        if not values:
            return None
        return " ".join(values)

    def _extract_form_number(self, spec: dict[str, object]) -> str | None:
        forms = spec.get("forms", [])
        if not forms:
            return None
        name = forms[0]["name"]
        upper_name = name.upper()
        for token in upper_name.replace("(", " ").replace(")", " ").split():
            if "-" in token and any(char.isdigit() for char in token):
                return token.strip(".,")
        return None

    def _extract_form_url(self, spec: dict[str, object]) -> str | None:
        forms = spec.get("forms", [])
        if not forms:
            return None
        return forms[0].get("url")

    def _extract_fee(self, value: object) -> float | None:
        if not isinstance(value, str):
            return None
        digits = []
        seen_number = False
        for char in value:
            if char.isdigit() or (char == "." and seen_number):
                digits.append(char)
                seen_number = True
                continue
            if seen_number:
                break
        if not digits:
            return None
        return float("".join(digits))

    def _extract_office_value(self, spec: dict[str, object], key: str) -> str | None:
        office = spec.get("office")
        if not office:
            return None
        return office.get(key)
