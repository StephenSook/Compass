from __future__ import annotations

from copy import deepcopy


DIRECT_TRANSFER_COUNTRIES = {"south korea", "germany", "france", "taiwan"}


JOURNEY_LIBRARY: dict[str, dict[str, object]] = {
    "ga_license_transfer_us": {
        "title": "Georgia Driver's License Transfer",
        "journey_type": "drivers_license",
        "summary": (
            "A shorter Georgia DDS path for people transferring an active license from another "
            "US state."
        ),
        "steps": [
            {
                "title": "Gather identity and residency documents",
                "description": "Collect identity, lawful presence, and two proofs of Georgia residency.",
                "documents": [
                    "Current out-of-state license",
                    "Passport or immigration document",
                    "Social Security card or SSN denial letter if applicable",
                    "Two proofs of Georgia residency",
                ],
                "fee": "$32 for an 8-year Class C license",
                "timeline": "Same-day temporary paper license; hard card in 2-3 weeks by mail.",
                "tip": "Bring two separate residency proofs because applicants are often turned away with only one.",
            },
            {
                "title": "Complete the DDS online application",
                "description": "Pre-fill the Georgia DDS application to save time at the field office.",
                "forms": [{"name": "Georgia DDS Online Application", "url": "https://dds.georgia.gov/"}],
                "timeline": "Usually 10-15 minutes online.",
                "tip": "Save or screenshot the confirmation page in case the DDS clerk asks for it.",
            },
            {
                "title": "Book a DDS appointment",
                "description": "Reserve an appointment at the nearest DDS location serving your county.",
                "forms": [{"name": "DDS Appointment Scheduler", "url": "https://dds.georgia.gov/"}],
                "office": {
                    "name": "Georgia Department of Driver Services",
                    "address": "Find the office closest to your county using the DDS locator.",
                    "hours": "Typically Monday-Friday, 8:00 AM-5:00 PM",
                    "appointment_url": "https://dds.georgia.gov/locations",
                },
                "tip": "Appointments are usually faster than walk-ins, especially in Metro Atlanta.",
            },
            {
                "title": "Visit DDS for vision screening and payment",
                "description": "Bring your documents, complete any required vision check, and pay the fee.",
                "fee": "$32",
                "timeline": "Expect 30-90 minutes at the office depending on wait times.",
                "tip": "Double-check the license expiration date from your prior state because Georgia may ask for it.",
            },
            {
                "title": "Receive your temporary license",
                "description": "Keep the temporary paper license until the physical card arrives by mail.",
                "timeline": "Temporary paper issued the same day; plastic card arrives in 2-3 weeks.",
                "tip": "Make sure your mailing address matches your residency proof to avoid delivery issues.",
            },
        ],
    },
    "ga_license_direct_transfer": {
        "title": "Georgia Driver's License Direct Transfer",
        "journey_type": "drivers_license",
        "summary": (
            "A Georgia DDS transfer path for select foreign licenses that may qualify for direct conversion."
        ),
        "steps": [
            {
                "title": "Confirm your license qualifies for direct transfer",
                "description": "Georgia recognizes direct transfer arrangements for a limited set of countries.",
                "documents": ["Foreign driver's license", "Certified translation if the license is not in English"],
                "timeline": "Verify before paying or booking travel to the DDS office.",
                "tip": "Bring extra identity documents because DDS officers may still verify lawful presence and residency.",
            },
            {
                "title": "Gather required Georgia DDS documents",
                "description": "Prepare identity, lawful presence, SSN evidence, and Georgia residency documents.",
                "documents": [
                    "Passport",
                    "Visa or immigration record",
                    "Social Security card or denial letter",
                    "Two proofs of Georgia residency",
                ],
                "fee": "$32 for an 8-year Class C license",
                "tip": "Translations should be legible and professionally prepared if any document is not in English.",
            },
            {
                "title": "Complete the online application and schedule DDS visit",
                "description": "Finish the online intake and reserve an appointment at a local DDS office.",
                "forms": [{"name": "Georgia DDS Online Application", "url": "https://dds.georgia.gov/"}],
                "office": {
                    "name": "Georgia Department of Driver Services",
                    "address": "Use the DDS office finder for the nearest location.",
                    "hours": "Typically Monday-Friday, 8:00 AM-5:00 PM",
                    "appointment_url": "https://dds.georgia.gov/locations",
                },
                "tip": "Take your original license to the appointment because copies are usually not enough.",
            },
            {
                "title": "Complete in-person verification and pay fee",
                "description": "DDS verifies your documents, runs screening checks, and processes the transfer.",
                "fee": "$32",
                "timeline": "Temporary paper license may be issued the same day if no extra review is needed.",
                "tip": "If DDS says your license does not qualify, ask which test path applies before leaving.",
            },
            {
                "title": "Receive Georgia license by mail",
                "description": "Track the card delivery while using the temporary paper license if provided.",
                "timeline": "2-3 weeks by mail in typical cases.",
                "tip": "Use a stable mailing address where you can receive state mail safely.",
            },
        ],
    },
    "ga_license_under18": {
        "title": "Georgia Teen Driver's License Path",
        "journey_type": "drivers_license",
        "summary": "A Georgia license path for drivers under 18, including Joshua's Law requirements.",
        "steps": [
            {
                "title": "Complete Joshua's Law education requirements",
                "description": "Finish the approved driver education and supervised driving hours required for teens.",
                "documents": ["Joshua's Law completion certificate", "Driving log signed by parent or guardian"],
                "timeline": "Timing varies based on course and practice completion.",
                "tip": "Keep a clean driving log because missing hours can delay the application.",
            },
            {
                "title": "Gather identity, residency, and school compliance documents",
                "description": "Collect documents proving identity, lawful presence, Georgia residency, and school status.",
                "documents": [
                    "Passport or birth certificate",
                    "Social Security card or denial letter",
                    "Two proofs of Georgia residency",
                    "Certificate of school enrollment if required",
                ],
                "tip": "Have a parent or guardian review the packet before the appointment.",
            },
            {
                "title": "Complete the online application and schedule DDS",
                "description": "Prepare the application and choose a DDS location with road test availability.",
                "forms": [{"name": "Georgia DDS Online Application", "url": "https://dds.georgia.gov/"}],
                "office": {
                    "name": "Georgia Department of Driver Services",
                    "address": "Select the DDS office that handles teen road tests in your area.",
                    "hours": "Typically Monday-Friday, 8:00 AM-5:00 PM",
                    "appointment_url": "https://dds.georgia.gov/locations",
                },
                "tip": "Road test slots can fill quickly, so book early.",
            },
            {
                "title": "Pass the knowledge and road skills tests",
                "description": "Take the tests required for your permit or license stage.",
                "fee": "$32",
                "timeline": "Testing is usually completed during the DDS visit if all documents are accepted.",
                "tip": "Check the vehicle requirements before the road test so the car is not rejected.",
            },
            {
                "title": "Receive temporary license and wait for card",
                "description": "Georgia issues temporary credentials while the physical license is mailed.",
                "timeline": "Same-day temporary credential; hard card usually arrives in 2-3 weeks.",
                "tip": "Carry the temporary credential anytime you drive.",
            },
        ],
    },
    "ga_license_full_testing": {
        "title": "Georgia Driver's License Full Testing Path",
        "journey_type": "drivers_license",
        "summary": (
            "A complete DDS journey for applicants who must pass the Georgia knowledge and road tests."
        ),
        "steps": [
            {
                "title": "Gather identity and residency documents",
                "description": "Collect passport, lawful presence evidence, SSN documentation, and residency proofs.",
                "documents": [
                    "Passport",
                    "Visa and I-94 record if applicable",
                    "Social Security card or denial letter",
                    "Two proofs of Georgia residency",
                ],
                "fee": "$32 for license issuance",
                "tip": "Bring printed residency proofs because mobile phone screenshots may not be accepted.",
            },
            {
                "title": "Complete the online application",
                "description": "Fill out the DDS application before your visit to reduce counter time.",
                "forms": [{"name": "Georgia DDS Online Application", "url": "https://dds.georgia.gov/"}],
                "timeline": "About 10-15 minutes online.",
                "tip": "Use your legal name exactly as it appears on immigration or identity documents.",
            },
            {
                "title": "Book DDS appointment and prepare for the knowledge test",
                "description": "Choose a DDS location and review the Georgia Driver's Manual.",
                "forms": [{"name": "DDS Appointment Scheduler", "url": "https://dds.georgia.gov/"}],
                "office": {
                    "name": "Georgia Department of Driver Services",
                    "address": "Choose the nearest DDS center from the state office locator.",
                    "hours": "Typically Monday-Friday, 8:00 AM-5:00 PM",
                    "appointment_url": "https://dds.georgia.gov/locations",
                },
                "tip": "Some offices allow retests on later dates only, so arrive prepared.",
            },
            {
                "title": "Pass the knowledge test and vision screening",
                "description": "Complete the written exam and vision screening at DDS.",
                "timeline": "Usually same-day during the appointment.",
                "tip": "If you need language support, confirm available options before test day.",
            },
            {
                "title": "Pass the road skills test",
                "description": "Schedule or complete the road test depending on DDS office procedures.",
                "timeline": "Often same day or on a follow-up appointment.",
                "tip": "Bring a properly insured vehicle and check the brake lights before arriving.",
            },
            {
                "title": "Pay fee and receive temporary license",
                "description": "After passing required tests, pay the issuance fee and keep the temporary paper license.",
                "fee": "$32",
                "timeline": "Temporary paper license issued the same day; hard card arrives in 2-3 weeks.",
                "tip": "Keep your receipt until the physical card arrives.",
            },
        ],
    },
    "passport_first_time": {
        "title": "US Passport First-Time Application",
        "journey_type": "passport",
        "summary": "A first-time adult US passport application journey for applicants in Metro Atlanta.",
        "steps": [
            {
                "title": "Gather citizenship and identity documents",
                "description": "Collect your citizenship proof, photo ID, photocopies, and passport photo.",
                "documents": [
                    "Birth certificate or naturalization certificate",
                    "Government-issued photo ID",
                    "Passport photo",
                    "Photocopies of front and back of ID",
                ],
                "tip": "Make photocopies before your appointment because not every acceptance facility offers them.",
            },
            {
                "title": "Complete Form DS-11",
                "description": "Fill out the first-time passport application but do not sign until instructed.",
                "forms": [{"name": "Form DS-11", "url": "https://travel.state.gov/content/travel/en/passports.html"}],
                "fee": "$165 passport book fee plus $30 execution fee",
                "tip": "Do not sign DS-11 early because it must usually be signed in front of the acceptance agent.",
            },
            {
                "title": "Book a passport acceptance facility appointment",
                "description": "Schedule an appointment at a post office, clerk of court, or other local facility.",
                "office": {
                    "name": "Metro Atlanta Passport Acceptance Facility",
                    "address": "Choose a USPS or county office near Atlanta that processes DS-11 applications.",
                    "hours": "Varies by facility",
                },
                "tip": "Ask whether the site also takes passport photos if you still need one.",
            },
            {
                "title": "Submit the application and pay fees",
                "description": "Bring your unsigned DS-11, supporting documents, and payment to the appointment.",
                "fee": "$195 total for a first-time adult passport book and execution fee",
                "timeline": "Routine processing is about 6-8 weeks; expedited is about 2-3 weeks plus $60.",
                "tip": "If travel is urgent, check emergency appointment rules before relying on expedited mail service.",
            },
            {
                "title": "Track application and receive passport",
                "description": "Monitor the case status online until the passport book arrives.",
                "timeline": "Routine 6-8 weeks; expedited 2-3 weeks plus mailing time.",
                "tip": "Keep copies of your documents until the original citizenship proof is mailed back.",
            },
        ],
    },
    "passport_renewal": {
        "title": "US Passport Renewal by Mail",
        "journey_type": "passport",
        "summary": "A renewal flow for eligible applicants using Form DS-82.",
        "steps": [
            {
                "title": "Confirm you are eligible to renew by mail",
                "description": "Make sure your prior passport qualifies for DS-82 renewal rules.",
                "documents": ["Most recent passport book", "Recent compliant passport photo"],
                "tip": "If your passport is too old or heavily damaged, you may need the first-time DS-11 route instead.",
            },
            {
                "title": "Complete Form DS-82",
                "description": "Fill out the passport renewal form carefully and print it for mailing.",
                "forms": [{"name": "Form DS-82", "url": "https://travel.state.gov/content/travel/en/passports.html"}],
                "fee": "$130 renewal fee",
                "tip": "Use the same legal name as your prior passport unless you are also submitting a name-change document.",
            },
            {
                "title": "Assemble renewal packet",
                "description": "Prepare the old passport, photo, payment, and any supporting name-change evidence.",
                "documents": ["Completed DS-82", "Old passport", "Passport photo", "Payment check or money order"],
                "tip": "Use trackable mail to reduce the risk of losing your documents.",
            },
            {
                "title": "Mail the renewal application",
                "description": "Send the packet to the correct State Department mailing address for your service level.",
                "timeline": "Routine 6-8 weeks; expedited about 2-3 weeks plus $60.",
                "tip": "Double-check the mailing address because it can vary by state and service choice.",
            },
            {
                "title": "Track status and receive new passport",
                "description": "Monitor the renewal online until the new book and supporting documents arrive.",
                "timeline": "Expect the new passport first and returned documents later in separate mailings.",
                "tip": "Renew well before international travel because processing times can change.",
            },
        ],
    },
    "visa_opt": {
        "title": "F-1 OPT Application Journey",
        "journey_type": "visa",
        "summary": "A post-completion OPT path for F-1 students preparing an I-765 filing.",
        "steps": [
            {
                "title": "Confirm OPT eligibility and timeline",
                "description": "Review graduation timing and make sure you are filing within the allowed OPT window.",
                "timeline": "Students often file around 90 days before graduation.",
                "tip": "Late filing can cost work authorization time or invalidate the application.",
            },
            {
                "title": "Coordinate with your DSO",
                "description": "Request an OPT recommendation and an updated I-20 from your school's international office.",
                "documents": ["Updated Form I-20 with OPT recommendation"],
                "tip": "USCIS expects the I-765 to match the recommendation details from your school.",
            },
            {
                "title": "Prepare Form I-765 filing package",
                "description": "Assemble your I-765, identity documents, passport photo, and payment.",
                "forms": [{"name": "Form I-765", "url": "https://www.uscis.gov/i-765"}],
                "documents": ["Passport", "Visa", "I-94", "OPT I-20", "Passport-style photos"],
                "fee": "$410 filing fee",
                "tip": "Keep complete digital copies of the packet before submitting it.",
            },
            {
                "title": "Submit the application before status expires",
                "description": "File the application on time and track receipt notices from USCIS.",
                "timeline": "USCIS processing is often around 3-5 months, though it can vary.",
                "tip": "You cannot work until your OPT start date and EAD approval rules are satisfied.",
            },
            {
                "title": "Track approval and unemployment limits",
                "description": "Monitor your case and plan carefully once employment begins.",
                "timeline": "Standard OPT allows up to 90 days of unemployment.",
                "tip": "STEM students may qualify for a 24-month extension if their employer and degree meet the rules.",
            },
        ],
    },
    "visa_family_green_card": {
        "title": "Family-Based Green Card Sponsorship",
        "journey_type": "visa",
        "summary": "A family-based immigration starting point focused on I-130 and priority date awareness.",
        "steps": [
            {
                "title": "Identify the family relationship and category",
                "description": "Determine whether the beneficiary is an immediate relative or falls into a preference category.",
                "timeline": "Immediate relatives usually have no visa-number cap; preference cases can wait years.",
                "tip": "Country of origin and relationship category can dramatically change wait times.",
            },
            {
                "title": "Prepare Form I-130 and evidence",
                "description": "Gather relationship evidence, identity documents, and filing details for the petition.",
                "forms": [{"name": "Form I-130", "url": "https://www.uscis.gov/i-130"}],
                "documents": ["Marriage or birth certificate", "Petitioner proof of status", "Supporting relationship evidence"],
                "fee": "$535 filing fee",
                "tip": "Strong evidence up front can reduce requests for evidence later.",
            },
            {
                "title": "Check whether concurrent filing is available",
                "description": "If the priority date is current and the applicant is eligible, I-485 may be filed together.",
                "timeline": "Concurrent filing depends on category and visa bulletin timing.",
                "tip": "Do not assume concurrent filing is allowed without verifying the current visa bulletin rules.",
            },
            {
                "title": "Track petition processing and next stage",
                "description": "Monitor USCIS processing and prepare for adjustment of status or consular processing.",
                "timeline": "Some preference categories can take 2-20+ years depending on demand and country caps.",
                "tip": "Save every receipt notice and keep addresses updated with USCIS.",
            },
        ],
    },
    "visa_extension": {
        "title": "Visa Renewal or Extension",
        "journey_type": "visa",
        "summary": "A general extension journey for nonimmigrant status holders preparing to file before expiration.",
        "steps": [
            {
                "title": "Review your current status expiration date",
                "description": "Check your I-94 and supporting documents to identify the filing deadline.",
                "timeline": "You should file before your current status expires.",
                "tip": "Waiting too long can lead to unlawful presence or lost eligibility.",
            },
            {
                "title": "Prepare Form I-539 and evidence",
                "description": "Collect status documents, supporting evidence, and filing payment.",
                "forms": [{"name": "Form I-539", "url": "https://www.uscis.gov/i-539"}],
                "documents": ["Passport", "I-94 record", "Current visa documents", "Financial or supporting evidence"],
                "fee": "$370 filing fee",
                "tip": "Make sure every date is consistent across your forms and supporting documents.",
            },
            {
                "title": "Submit the extension application",
                "description": "File the application and keep your receipt notice in a safe place.",
                "timeline": "Processing varies widely by category and service center.",
                "tip": "Mailing with tracking or filing online can make follow-up much easier.",
            },
            {
                "title": "Complete biometrics if required",
                "description": "Attend the biometrics appointment after USCIS sends the notice.",
                "timeline": "Biometrics notices usually arrive after filing.",
                "tip": "Missing the biometrics appointment can delay or derail the case.",
            },
            {
                "title": "Track decision and maintain compliance",
                "description": "Monitor the case status and follow any USCIS requests for evidence.",
                "tip": "If anything is uncertain, get qualified immigration advice rather than guessing.",
            },
        ],
    },
}


def get_journey_template(branch_key: str) -> dict[str, object]:
    try:
        return deepcopy(JOURNEY_LIBRARY[branch_key])
    except KeyError as exc:
        raise ValueError(f"Unknown branch key: {branch_key}") from exc
