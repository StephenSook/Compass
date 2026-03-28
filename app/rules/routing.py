from __future__ import annotations

from app.rules.knowledge_base import DIRECT_TRANSFER_COUNTRIES
from app.schemas.common import GoalEnum, UserProfile


def determine_branch(profile: UserProfile) -> str:
    if profile.goal == GoalEnum.GA_DRIVERS_LICENSE:
        return _driver_license_branch(profile)
    if profile.goal == GoalEnum.PASSPORT_NEW:
        return "passport_first_time"
    if profile.goal == GoalEnum.PASSPORT_RENEWAL:
        return "passport_renewal"
    if profile.goal == GoalEnum.F1_OPT:
        return "visa_opt"
    if profile.goal == GoalEnum.FAMILY_GREEN_CARD:
        return "visa_family_green_card"
    return "visa_extension"


def build_session_title(profile: UserProfile, branch_key: str) -> str:
    if branch_key.startswith("ga_license"):
        county = profile.county or "your area"
        return f"Georgia license help for {county}"
    if branch_key.startswith("passport"):
        return "US passport help session"
    return "Visa and immigration help session"


def _driver_license_branch(profile: UserProfile) -> str:
    if profile.age is not None and profile.age < 18:
        return "ga_license_under18"

    if profile.has_us_license:
        return "ga_license_transfer_us"

    foreign_country = (profile.foreign_license_country or "").strip().lower()
    if profile.has_foreign_license and foreign_country in DIRECT_TRANSFER_COUNTRIES:
        return "ga_license_direct_transfer"

    return "ga_license_full_testing"
