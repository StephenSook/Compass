from __future__ import annotations

from app.rules.knowledge_base import DIRECT_TRANSFER_COUNTRIES
from app.schemas.common import UserProfile


def determine_branch(profile: UserProfile) -> str:
    goal_text = profile.goal.strip().lower()

    if "driver" in goal_text or "license" in goal_text:
        return _driver_license_branch(profile)

    if "passport" in goal_text:
        application_type = (profile.passport_application_type or "").strip().lower()
        if "renew" in application_type:
            return "passport_renewal"
        return "passport_first_time"

    visa_goal = (profile.visa_goal or "").strip().lower()
    immigration_status = (profile.immigration_status or "").strip().lower()
    combined = f"{goal_text} {visa_goal} {immigration_status}"

    if "opt" in combined or "f-1" in combined:
        return "visa_opt"
    if "family" in combined or "green card" in combined or "sponsor" in combined:
        return "visa_family_green_card"
    return "visa_extension"


def build_session_title(profile: UserProfile, branch_key: str) -> str:
    if branch_key.startswith("ga_license"):
        return f"Georgia license help for {profile.county} County"
    if branch_key.startswith("passport"):
        return "US passport help session"
    return "Visa and immigration help session"


def _driver_license_branch(profile: UserProfile) -> str:
    if profile.age is not None and profile.age < 18:
        return "ga_license_under18"

    if profile.has_us_license:
        return "ga_license_transfer_us"

    foreign_country = (profile.foreign_license_country or "").strip().lower()
    if foreign_country in DIRECT_TRANSFER_COUNTRIES:
        return "ga_license_direct_transfer"

    return "ga_license_full_testing"
