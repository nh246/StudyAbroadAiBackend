from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from typing import List, Optional
from schemas.profile import UserInfoCreate, UserInfoResponse, COUNTRIES, PHONE_COUNTRY_CODES
from services.profile_service import save_user_profile, get_user_profile
import json

router = APIRouter(prefix="/profile", tags=["User Profile"])

def format_name(name: Optional[str]) -> Optional[str]:
    if not name:
        return name
    name = name.strip().lower()
    prefixes = ["md.", "mr.", "mrs.", "dr.", "prof."]
    for prefix in prefixes:
        name = name.replace(prefix.replace(".", ""), prefix)
    name = name.title()
    name = name.replace("Md.", "Md. ").replace("Mr.", "Mr. ").replace("Mrs.", "Mrs. ")
    return name.strip()

def normalize_country_input(value: str) -> List[str]:
    """Handle comma-separated or single country input"""
    if not value:
        return []
    items = [item.strip().title() for item in value.split(",") if item.strip()]
    return items

@router.post(
    "/submit",
    response_model=UserInfoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit User Profile Form",
    description="Accepts profile data. Country fields support comma-separated values for testing (e.g., 'Germany,Canada')"
)
async def submit_profile(
    full_name_raw: str = Form(..., description="Full name as typed by user"),
    father_name_raw: Optional[str] = Form(None, description="Father's name"),
    mother_name_raw: Optional[str] = Form(None, description="Mother's name"),
    email: str = Form(..., description="Email address"),
    phone_country_code: Optional[str] = Form("+880", description="Phone country code"),
    phone_number: Optional[str] = Form(None, description="Phone number without country code"),
    nationality: str = Form("Bangladesh", description="Nationality (comma-separated for testing)"),
    current_living_country: str = Form("Bangladesh", description="Current residence (comma-separated)"),
    education_json: str = Form("[]", description="JSON string of education entries"),
    preferred_countries: str = Form(..., description="Preferred study destinations (comma-separated, required)"),
    budget_min_bdt: Optional[int] = Form(None),
    budget_max_bdt: Optional[int] = Form(None),
    preferred_currency: str = Form("BDT"),
    preferred_intake: Optional[str] = Form(None),
    resume: Optional[UploadFile] = File(None)
):
    # Name formatting
    full_name = format_name(full_name_raw)
    father_name = format_name(father_name_raw)
    mother_name = format_name(mother_name_raw)

    # Normalize countries
    nationality = normalize_country_input(nationality) or ["Bangladesh"]
    current_living_country = normalize_country_input(current_living_country) or ["Bangladesh"]
    preferred_countries = normalize_country_input(preferred_countries)
    if not preferred_countries:
        raise HTTPException(status_code=400, detail="At least one preferred country is required")

    # Validation
    all_countries = nationality + current_living_country + preferred_countries
    invalid = [c for c in all_countries if c not in COUNTRIES]
    if invalid:
        raise HTTPException(status_code=400, detail=f"Invalid countries: {', '.join(invalid)}")

    if phone_country_code and phone_country_code not in PHONE_COUNTRY_CODES:
        raise HTTPException(status_code=400, detail="Invalid phone country code")

    # Education
    try:
        education = json.loads(education_json) if education_json.strip() else []
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid education JSON")

    # Resume
    resume_filename = resume.filename if resume else None

    # Full phone
    full_phone = f"{phone_country_code}{phone_number.strip()}" if phone_country_code and phone_number else None

    # Create profile
    profile = UserInfoCreate(
        full_name=full_name,
        father_name=father_name,
        mother_name=mother_name,
        email=email.lower().strip(),
        phone_country_code=phone_country_code,
        phone_number=phone_number.strip() if phone_number else None,
        full_phone=full_phone,
        nationality=nationality,
        current_living_country=current_living_country,
        education=education,
        preferred_countries=preferred_countries,
        budget_min_bdt=budget_min_bdt,
        budget_max_bdt=budget_max_bdt,
        preferred_currency=preferred_currency,
        preferred_intake=preferred_intake,
        resume_filename=resume_filename
    )
    
    # Save to cache and get user_id
    user_id = save_user_profile(profile)

    return UserInfoResponse(
        **profile.dict(),
        id=user_id,
        user_id=user_id,
        status="success",
        message=f"Profile submitted successfully! Your user_id is {user_id}. Use this ID for chat requests."
    )


@router.get(
    "/get/{user_id}",
    summary="Get User Profile",
    description="Retrieve a user profile by ID"
)
async def get_profile(user_id: int):
    """Retrieve user profile by ID"""
    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile not found for user_id: {user_id}")
    return {"user_id": user_id, "profile": profile}
