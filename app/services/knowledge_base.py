from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.schemas.common import UserProfile

OFFICES: dict[str, dict[str, Any]] = {
    "dds_south_dekalb": {
        "id": "dds_south_dekalb",
        "agency": "Georgia Department of Driver Services",
        "name": "South DeKalb DDS Customer Service Center",
        "address": {
            "street": "2801 Candler Rd",
            "city": "Decatur",
            "state": "GA",
            "postal_code": "30034",
        },
        "hours": "Monday-Friday 8:00 AM-5:00 PM",
        "appointment_url": "https://dds.georgia.gov/locations",
        "service_tags": ["drivers_license", "knowledge_test", "road_test"],
    },
    "dds_locator_generic": {
        "id": "dds_locator_generic",
        "agency": "Georgia Department of Driver Services",
        "name": "Georgia DDS Office Locator",
        "address": {
            "street": "Use the DDS locator for the nearest office.",
            "city": "Georgia",
            "state": "GA",
            "postal_code": "",
        },
        "hours": "Typically Monday-Friday 8:00 AM-5:00 PM",
        "appointment_url": "https://dds.georgia.gov/locations",
        "service_tags": ["drivers_license"],
    },
    "atlanta_passport_acceptance": {
        "id": "atlanta_passport_acceptance",
        "agency": "US Passport Acceptance Facility",
        "name": "Atlanta Main Post Office Passport Services",
        "address": {
            "street": "3900 Crown Rd SW",
            "city": "Atlanta",
            "state": "GA",
            "postal_code": "30304",
        },
        "hours": "Hours vary by facility appointment schedule",
        "appointment_url": "https://tools.usps.com/rcas.htm",
        "service_tags": ["passport_new"],
    },
}

FORMS: dict[str, dict[str, Any]] = {
    "ga_dds_online_portal": {
        "id": "ga_dds_online_portal",
        "name": "Georgia DDS Online Services Portal",
        "url": "https://dds.georgia.gov/",
        "channel": "online_portal",
    },
    "dds_scheduler": {
        "id": "dds_scheduler",
        "name": "DDS Appointment Scheduler",
        "url": "https://dds.georgia.gov/locations",
        "channel": "appointment",
    },
    "ds_11": {
        "id": "ds_11",
        "name": "Form DS-11",
        "number": "DS-11",
        "url": "https://travel.state.gov/content/travel/en/passports.html",
        "channel": "form",
    },
    "ds_82": {
        "id": "ds_82",
        "name": "Form DS-82",
        "number": "DS-82",
        "url": "https://travel.state.gov/content/travel/en/passports.html",
        "channel": "form",
    },
    "i_765": {
        "id": "i_765",
        "name": "Form I-765",
        "number": "I-765",
        "url": "https://www.uscis.gov/i-765",
        "channel": "form",
    },
    "i_130": {
        "id": "i_130",
        "name": "Form I-130",
        "number": "I-130",
        "url": "https://www.uscis.gov/i-130",
        "channel": "form",
    },
    "i_539": {
        "id": "i_539",
        "name": "Form I-539",
        "number": "I-539",
        "url": "https://www.uscis.gov/i-539",
        "channel": "form",
    },
}

FEES: dict[str, dict[str, Any]] = {
    "ga_class_c_license": {"id": "ga_class_c_license", "amount_usd": 32, "label": "Georgia Class C license fee"},
    "passport_new_book": {"id": "passport_new_book", "amount_usd": 165, "label": "New adult passport book"},
    "passport_execution": {"id": "passport_execution", "amount_usd": 30, "label": "Passport execution fee"},
    "passport_renewal_mail": {"id": "passport_renewal_mail", "amount_usd": 130, "label": "Passport renewal by mail"},
    "opt_i765": {"id": "opt_i765", "amount_usd": 410, "label": "Form I-765 filing fee"},
    "family_i130": {"id": "family_i130", "amount_usd": 535, "label": "Form I-130 filing fee"},
    "visa_extension_i539": {"id": "visa_extension_i539", "amount_usd": 370, "label": "Form I-539 filing fee"},
}

TIMELINES: dict[str, dict[str, Any]] = {
    "ga_card_delivery": {
        "id": "ga_card_delivery",
        "temporary_license": "Temporary paper license is issued the same day.",
        "hard_card_arrival": "Hard card typically arrives in 2-3 weeks by mail.",
    },
    "passport_new_processing": {
        "id": "passport_new_processing",
        "routine": "6-8 weeks",
        "expedited": "2-3 weeks",
        "urgent": "Urgent travel may require a special escalation or emergency appointment.",
    },
    "passport_renewal_processing": {
        "id": "passport_renewal_processing",
        "routine": "6-8 weeks",
    },
    "opt_processing": {
        "id": "opt_processing",
        "filing_window": "File about 90 days before graduation.",
        "processing": "USCIS processing is often 3-5 months.",
    },
}

DOCUMENT_SETS: dict[str, dict[str, Any]] = {
    "ga_new_immigrant_with_ssn": {
        "id": "ga_new_immigrant_with_ssn",
        "items": [
            "Passport",
            "Visa or immigration document",
            "I-94 arrival record",
            "Social Security card",
            "Two proofs of Georgia residency",
        ],
    },
    "ga_no_ssn_alternative": {
        "id": "ga_no_ssn_alternative",
        "items": [
            "Passport",
            "Visa or immigration document",
            "I-94 arrival record",
            "SSN denial letter or DDS-accepted alternative evidence",
            "Two proofs of Georgia residency",
        ],
    },
    "passport_new_required_documents": {
        "id": "passport_new_required_documents",
        "items": [
            "Birth certificate or naturalization certificate",
            "Government-issued photo ID",
            "Passport photo",
            "Photocopy of front and back of ID",
        ],
    },
    "passport_renewal_documents": {
        "id": "passport_renewal_documents",
        "items": [
            "Most recent passport",
            "Recent passport photo",
            "Completed DS-82",
            "Payment for renewal fee",
        ],
    },
}

TESTING_RULES: dict[str, dict[str, Any]] = {
    "ga_knowledge_test": {
        "id": "ga_knowledge_test",
        "summary": "Written exam based on the Georgia Driver's Manual plus standard vision screening.",
    },
    "ga_road_skills_test": {
        "id": "ga_road_skills_test",
        "summary": "In-car driving evaluation using a properly insured vehicle that meets DDS requirements.",
    },
}

FLOW_CONTEXT: dict[str, dict[str, Any]] = {
    "ga_drivers_license": {
        "id": "ga_drivers_license",
        "journey_type": "drivers_license",
        "portal_ids": ["ga_dds_online_portal", "dds_scheduler"],
        "document_set_id": "ga_new_immigrant_with_ssn",
        "fee_ids": ["ga_class_c_license"],
        "timeline_id": "ga_card_delivery",
        "testing_ids": ["ga_knowledge_test", "ga_road_skills_test"],
        "tip_ids": ["ga_two_residency_proofs"],
    },
    "passport_new": {
        "id": "passport_new",
        "journey_type": "passport",
        "form_ids": ["ds_11"],
        "document_set_id": "passport_new_required_documents",
        "fee_ids": ["passport_new_book", "passport_execution"],
        "timeline_id": "passport_new_processing",
        "office_id": "atlanta_passport_acceptance",
    },
    "passport_renewal": {
        "id": "passport_renewal",
        "journey_type": "passport",
        "form_ids": ["ds_82"],
        "document_set_id": "passport_renewal_documents",
        "fee_ids": ["passport_renewal_mail"],
        "timeline_id": "passport_renewal_processing",
    },
    "f1_opt": {
        "id": "f1_opt",
        "journey_type": "visa",
        "form_ids": ["i_765"],
        "fee_ids": ["opt_i765"],
        "rule_items": {
            "filing_window": "File about 90 days before graduation.",
            "processing_time": "USCIS processing is often 3-5 months.",
            "unemployment_limit": "Standard post-completion OPT allows up to 90 days of unemployment.",
            "stem_extension": "Eligible STEM graduates may qualify for a 24-month extension.",
            "h1b_note": "OPT can be a bridge toward H-1B planning for some students.",
        },
    },
    "family_green_card": {
        "id": "family_green_card",
        "journey_type": "visa",
        "form_ids": ["i_130"],
        "fee_ids": ["family_i130"],
        "rule_items": {
            "category_summary": {
                "immediate_relative": "Immediate relatives are not subject to annual visa-number caps.",
                "preference_category": "Preference categories can involve multi-year waits depending on relationship and country.",
            },
            "concurrent_filing": "I-485 may be filed concurrently when the priority date is current and eligibility rules are met.",
        },
    },
    "visa_extension": {
        "id": "visa_extension",
        "journey_type": "visa",
        "form_ids": ["i_539"],
        "fee_ids": ["visa_extension_i539"],
        "rule_items": {
            "deadline": "The extension must be filed before the current status expires.",
            "biometrics": "USCIS may schedule a biometrics appointment after filing.",
        },
    },
}

TIPS: dict[str, dict[str, Any]] = {
    "ga_two_residency_proofs": {
        "id": "ga_two_residency_proofs",
        "label": "Bring two proofs of residency",
        "detail": "Applicants are commonly turned away when they only bring one Georgia residency document.",
    }
}


class KnowledgeBaseService:
    def get_context_for_branch(self, branch_key: str, profile: UserProfile | dict[str, Any] | None) -> dict[str, Any]:
        normalized_profile = self._normalize_profile(profile)
        context_key = self._resolve_context_key(branch_key)
        if context_key == "ga_drivers_license":
            return self._ga_context(branch_key, normalized_profile)
        if context_key == "passport_new":
            return self._passport_new_context(branch_key, normalized_profile)
        if context_key == "passport_renewal":
            return self._passport_renewal_context(branch_key, normalized_profile)
        if context_key == "f1_opt":
            return self._visa_context(branch_key, normalized_profile, context_key)
        if context_key == "family_green_card":
            return self._visa_context(branch_key, normalized_profile, context_key)
        return self._visa_context(branch_key, normalized_profile, "visa_extension")

    def get_office(self, office_id: str) -> dict[str, Any]:
        return deepcopy(OFFICES[office_id])

    def get_form(self, form_id: str) -> dict[str, Any]:
        return deepcopy(FORMS[form_id])

    def _ga_context(self, branch_key: str, profile: dict[str, Any]) -> dict[str, Any]:
        flow = deepcopy(FLOW_CONTEXT["ga_drivers_license"])
        county_slug = self._county_slug(profile.get("county"))
        office_id = "dds_south_dekalb" if county_slug == "dekalb" else "dds_locator_generic"
        has_ssn = ".ssn.yes." in branch_key
        is_transfer = ".us_license.transfer." in branch_key
        is_reciprocity = ".foreign_license.reciprocity." in branch_key
        requires_joshuas_law = ".joshuas_law." in branch_key or ".age_under_18." in branch_key

        documents = self._document_set("ga_new_immigrant_with_ssn" if has_ssn else "ga_no_ssn_alternative")
        return {
            "context_id": flow["id"],
            "journey_type": flow["journey_type"],
            "branch_key": branch_key,
            "profile": normalized_profile_snapshot(profile),
            "documents": documents,
            "portals": [self.get_form(form_id) for form_id in flow["portal_ids"]],
            "office": self.get_office(office_id),
            "tests": [
                self._test_rule("ga_knowledge_test", waived=is_transfer or is_reciprocity),
                self._test_rule("ga_road_skills_test", waived=is_transfer or is_reciprocity),
            ],
            "fees": [deepcopy(FEES[fee_id]) for fee_id in flow["fee_ids"]],
            "timelines": deepcopy(TIMELINES[flow["timeline_id"]]),
            "tips": [deepcopy(TIPS[tip_id]) for tip_id in flow["tip_ids"]],
            "rules": {
                "is_transfer": is_transfer,
                "is_reciprocity": is_reciprocity,
                "requires_full_testing": ".full_testing." in branch_key,
                "requires_joshuas_law": requires_joshuas_law,
                "ssn_required_path": has_ssn,
            },
            "guidance": {
                "joshua_law": {
                    "applies": requires_joshuas_law,
                    "detail": "Under-18 applicants should complete Joshua's Law coursework and supervised driving logs.",
                },
                "ssn": {
                    "has_ssn": has_ssn,
                    "detail": (
                        "Use SSN-based document checklist."
                        if has_ssn
                        else "Use DDS alternative SSN evidence and ITIN-supporting identity records when available."
                    ),
                },
            },
        }

    def _passport_new_context(self, branch_key: str, profile: dict[str, Any]) -> dict[str, Any]:
        flow = deepcopy(FLOW_CONTEXT["passport_new"])
        return {
            "context_id": flow["id"],
            "journey_type": flow["journey_type"],
            "branch_key": branch_key,
            "profile": normalized_profile_snapshot(profile),
            "forms": [self.get_form(form_id) for form_id in flow["form_ids"]],
            "documents": self._document_set(flow["document_set_id"]),
            "fees": [deepcopy(FEES[fee_id]) for fee_id in flow["fee_ids"]],
            "timelines": deepcopy(TIMELINES[flow["timeline_id"]]),
            "office": self.get_office(flow["office_id"]),
        }

    def _passport_renewal_context(self, branch_key: str, profile: dict[str, Any]) -> dict[str, Any]:
        flow = deepcopy(FLOW_CONTEXT["passport_renewal"])
        return {
            "context_id": flow["id"],
            "journey_type": flow["journey_type"],
            "branch_key": branch_key,
            "profile": normalized_profile_snapshot(profile),
            "forms": [self.get_form(form_id) for form_id in flow["form_ids"]],
            "documents": self._document_set(flow["document_set_id"]),
            "fees": [deepcopy(FEES[fee_id]) for fee_id in flow["fee_ids"]],
            "timelines": deepcopy(TIMELINES[flow["timeline_id"]]),
        }

    def _visa_context(self, branch_key: str, profile: dict[str, Any], flow_key: str) -> dict[str, Any]:
        flow = deepcopy(FLOW_CONTEXT[flow_key])
        return {
            "context_id": flow["id"],
            "journey_type": flow["journey_type"],
            "branch_key": branch_key,
            "profile": normalized_profile_snapshot(profile),
            "forms": [self.get_form(form_id) for form_id in flow["form_ids"]],
            "fees": [deepcopy(FEES[fee_id]) for fee_id in flow["fee_ids"]],
            "rules": deepcopy(flow["rule_items"]),
            "timelines": deepcopy(TIMELINES.get("opt_processing", {})) if flow_key == "f1_opt" else {},
        }

    def _resolve_context_key(self, branch_key: str) -> str:
        if branch_key.startswith("ga_dl.") or branch_key.startswith("ga_license"):
            return "ga_drivers_license"
        if branch_key.startswith("passport.new.") or branch_key == "passport_first_time":
            return "passport_new"
        if branch_key.startswith("passport.renewal.") or branch_key == "passport_renewal":
            return "passport_renewal"
        if branch_key.startswith("visa.f1_opt.") or branch_key == "visa_opt":
            return "f1_opt"
        if branch_key.startswith("visa.family_green_card.") or branch_key == "visa_family_green_card":
            return "family_green_card"
        return "visa_extension"

    def _document_set(self, document_set_id: str) -> dict[str, Any]:
        return deepcopy(DOCUMENT_SETS[document_set_id])

    def _test_rule(self, rule_id: str, *, waived: bool) -> dict[str, Any]:
        payload = deepcopy(TESTING_RULES[rule_id])
        payload["waived"] = waived
        return payload

    def _normalize_profile(self, profile: UserProfile | dict[str, Any] | None) -> dict[str, Any]:
        if profile is None:
            return {}
        if isinstance(profile, UserProfile):
            return profile.model_dump()
        return dict(profile)

    def _county_slug(self, value: Any) -> str:
        raw = str(value or "").strip().lower()
        if not raw:
            return ""
        characters: list[str] = []
        previous_was_separator = False
        for char in raw:
            if char.isalnum():
                characters.append(char)
                previous_was_separator = False
            elif not previous_was_separator:
                characters.append("_")
                previous_was_separator = True
        return "".join(characters).strip("_")


def normalized_profile_snapshot(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "state": profile.get("state"),
        "county": profile.get("county"),
        "language": profile.get("language"),
        "goal": profile.get("goal"),
        "age": profile.get("age"),
        "has_ssn": profile.get("has_ssn"),
        "immigration_status": profile.get("immigration_status"),
    }
