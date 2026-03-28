from __future__ import annotations

from app.rules.knowledge_base import DIRECT_TRANSFER_COUNTRIES
from app.rules.models import RoutingDecision
from app.schemas.common import GoalEnum, JourneyTypeEnum, UserProfile

"""
Deterministic routing helpers for onboarding.

Unit-style examples:
    >>> route_onboarding(
    ...     UserProfile(
    ...         state="Georgia",
    ...         county="Dekalb",
    ...         goal=GoalEnum.GA_DRIVERS_LICENSE,
    ...         age=29,
    ...         has_ssn=True,
    ...         has_us_license=False,
    ...         has_foreign_license=True,
    ...         foreign_license_country="Germany",
    ...     )
    ... ).branch_key
    'ga_dl.foreign_license.reciprocity.ssn.yes.age_18_plus.dekalb'

    >>> route_onboarding(
    ...     UserProfile(
    ...         state="Georgia",
    ...         county="Fulton",
    ...         goal=GoalEnum.GA_DRIVERS_LICENSE,
    ...         age=17,
    ...         has_ssn=False,
    ...     )
    ... ).template_key
    'ga_license_under18'
"""


def route_onboarding(profile: UserProfile) -> RoutingDecision:
    if profile.goal == GoalEnum.GA_DRIVERS_LICENSE:
        return _route_driver_license(profile)
    if profile.goal == GoalEnum.PASSPORT_NEW:
        return _simple_route(
            profile=profile,
            journey_type=JourneyTypeEnum.PASSPORT,
            template_key="passport_first_time",
            branch_key=f"passport.new.{_county_slug(profile.county)}",
            branch_summary={
                "goal": GoalEnum.PASSPORT_NEW.value,
                "path": "passport_new",
                "template_key": "passport_first_time",
                "county": profile.county,
                "county_slug": _county_slug(profile.county),
                "office_routing": "passport_locator",
            },
            derived_flags={
                "is_drivers_license_flow": False,
                "is_passport_flow": True,
                "is_visa_flow": False,
                "is_passport_new": True,
                "is_passport_renewal": False,
                "requires_acceptance_facility": True,
            },
        )
    if profile.goal == GoalEnum.PASSPORT_RENEWAL:
        return _simple_route(
            profile=profile,
            journey_type=JourneyTypeEnum.PASSPORT,
            template_key="passport_renewal",
            branch_key=f"passport.renewal.{_county_slug(profile.county)}",
            branch_summary={
                "goal": GoalEnum.PASSPORT_RENEWAL.value,
                "path": "passport_renewal",
                "template_key": "passport_renewal",
                "county": profile.county,
                "county_slug": _county_slug(profile.county),
                "office_routing": "passport_locator",
            },
            derived_flags={
                "is_drivers_license_flow": False,
                "is_passport_flow": True,
                "is_visa_flow": False,
                "is_passport_new": False,
                "is_passport_renewal": True,
                "may_be_eligible_for_mail_renewal": True,
            },
        )
    if profile.goal == GoalEnum.F1_OPT:
        return _simple_route(
            profile=profile,
            journey_type=JourneyTypeEnum.VISA,
            template_key="visa_opt",
            branch_key=f"visa.f1_opt.{_county_slug(profile.county)}",
            branch_summary={
                "goal": GoalEnum.F1_OPT.value,
                "path": "f1_opt",
                "template_key": "visa_opt",
                "county": profile.county,
                "county_slug": _county_slug(profile.county),
                "immigration_status": profile.immigration_status,
            },
            derived_flags={
                "is_drivers_license_flow": False,
                "is_passport_flow": False,
                "is_visa_flow": True,
                "is_f1_opt": True,
                "is_family_green_card": False,
                "is_visa_extension": False,
            },
        )
    if profile.goal == GoalEnum.FAMILY_GREEN_CARD:
        return _simple_route(
            profile=profile,
            journey_type=JourneyTypeEnum.VISA,
            template_key="visa_family_green_card",
            branch_key=f"visa.family_green_card.{_county_slug(profile.county)}",
            branch_summary={
                "goal": GoalEnum.FAMILY_GREEN_CARD.value,
                "path": "family_green_card",
                "template_key": "visa_family_green_card",
                "county": profile.county,
                "county_slug": _county_slug(profile.county),
                "immigration_status": profile.immigration_status,
            },
            derived_flags={
                "is_drivers_license_flow": False,
                "is_passport_flow": False,
                "is_visa_flow": True,
                "is_f1_opt": False,
                "is_family_green_card": True,
                "is_visa_extension": False,
            },
        )
    return _simple_route(
        profile=profile,
        journey_type=JourneyTypeEnum.VISA,
        template_key="visa_extension",
        branch_key=f"visa.extension.{_county_slug(profile.county)}",
        branch_summary={
            "goal": GoalEnum.VISA_EXTENSION.value,
            "path": "visa_extension",
            "template_key": "visa_extension",
            "county": profile.county,
            "county_slug": _county_slug(profile.county),
            "immigration_status": profile.immigration_status,
        },
        derived_flags={
            "is_drivers_license_flow": False,
            "is_passport_flow": False,
            "is_visa_flow": True,
            "is_f1_opt": False,
            "is_family_green_card": False,
            "is_visa_extension": True,
        },
    )


def determine_branch(profile: UserProfile) -> str:
    return route_onboarding(profile).template_key


def build_session_title(profile: UserProfile, branch_key: str) -> str:
    if branch_key.startswith(("ga_dl.", "ga_license")):
        county = profile.county or "your area"
        return f"Georgia license help for {county}"
    if branch_key.startswith("passport."):
        return "US passport help session"
    return "Visa and immigration help session"


def _route_driver_license(profile: UserProfile) -> RoutingDecision:
    county_slug = _county_slug(profile.county)
    ssn_token = _bool_token(profile.has_ssn)
    age_bucket = _age_bucket(profile.age)
    foreign_country = _normalize_text(profile.foreign_license_country)
    is_direct_transfer_country = bool(
        profile.has_foreign_license and foreign_country in DIRECT_TRANSFER_COUNTRIES
    )
    needs_itin_guidance = profile.has_ssn is False

    if profile.age is not None and profile.age < 18:
        template_key = "ga_license_under18"
        branch_key = f"ga_dl.joshuas_law.ssn.{ssn_token}.{age_bucket}.{county_slug}"
        path = "joshuas_law"
        license_origin = "under_18"
        is_us_transfer = False
        is_direct_transfer = False
        requires_full_testing = True
    elif profile.has_us_license:
        template_key = "ga_license_transfer_us"
        branch_key = f"ga_dl.us_license.transfer.ssn.{ssn_token}.{age_bucket}.{county_slug}"
        path = "transfer"
        license_origin = "us"
        is_us_transfer = True
        is_direct_transfer = False
        requires_full_testing = False
    elif is_direct_transfer_country:
        template_key = "ga_license_direct_transfer"
        branch_key = f"ga_dl.foreign_license.reciprocity.ssn.{ssn_token}.{age_bucket}.{county_slug}"
        path = "direct_transfer"
        license_origin = "foreign"
        is_us_transfer = False
        is_direct_transfer = True
        requires_full_testing = False
    else:
        template_key = "ga_license_full_testing"
        origin_token = "foreign_license" if profile.has_foreign_license else "no_license"
        branch_key = f"ga_dl.{origin_token}.full_testing.ssn.{ssn_token}.{age_bucket}.{county_slug}"
        path = "full_testing"
        license_origin = "foreign" if profile.has_foreign_license else "none_or_unknown"
        is_us_transfer = False
        is_direct_transfer = False
        requires_full_testing = True

    return RoutingDecision(
        journey_type=JourneyTypeEnum.DRIVERS_LICENSE,
        template_key=template_key,
        branch_key=branch_key,
        branch_summary={
            "goal": GoalEnum.GA_DRIVERS_LICENSE.value,
            "path": path,
            "template_key": template_key,
            "license_origin": license_origin,
            "foreign_license_country": profile.foreign_license_country,
            "foreign_license_country_slug": _slugify(profile.foreign_license_country, "unknown_country"),
            "county": profile.county,
            "county_slug": county_slug,
            "age": profile.age,
            "age_bucket": age_bucket,
            "ssn_status": ssn_token,
            "office_routing": "dds_locator",
        },
        derived_flags={
            "is_drivers_license_flow": True,
            "is_passport_flow": False,
            "is_visa_flow": False,
            "is_us_transfer": is_us_transfer,
            "is_direct_transfer": is_direct_transfer,
            "requires_full_testing": requires_full_testing,
            "requires_joshuas_law": profile.age is not None and profile.age < 18,
            "has_ssn": profile.has_ssn is True,
            "needs_ssn_alternative_docs": profile.has_ssn is False,
            "needs_itin_guidance": needs_itin_guidance,
            "has_us_license": profile.has_us_license is True,
            "has_foreign_license": profile.has_foreign_license is True,
            "is_direct_transfer_country": is_direct_transfer_country,
        },
    )


def _simple_route(
    *,
    profile: UserProfile,
    journey_type: JourneyTypeEnum,
    template_key: str,
    branch_key: str,
    branch_summary: dict[str, object],
    derived_flags: dict[str, object],
) -> RoutingDecision:
    return RoutingDecision(
        journey_type=journey_type,
        template_key=template_key,
        branch_key=branch_key,
        branch_summary=branch_summary,
        derived_flags=derived_flags,
    )


def _bool_token(value: bool | None) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "unknown"


def _age_bucket(age: int | None) -> str:
    if age is None:
        return "age_unknown"
    if age < 18:
        return "age_under_18"
    return "age_18_plus"


def _county_slug(county: str | None) -> str:
    return _slugify(county, "unknown_county")


def _normalize_text(value: str | None) -> str:
    return (value or "").strip().lower()


def _slugify(value: str | None, fallback: str) -> str:
    cleaned = _normalize_text(value)
    if not cleaned:
        return fallback
    characters: list[str] = []
    previous_was_separator = False
    for char in cleaned:
        if char.isalnum():
            characters.append(char)
            previous_was_separator = False
            continue
        if not previous_was_separator:
            characters.append("_")
            previous_was_separator = True
    slug = "".join(characters).strip("_")
    return slug or fallback
