from pydantic import BaseModel, Field
from typing import List, Optional
from typing_extensions import Literal

COUNTRIES = [
    "Bangladesh", "India", "Pakistan", "Nepal", "Sri Lanka", "Malaysia", "Germany",
    "Canada", "Australia", "United Kingdom", "United States", "Turkey", "Italy",
    "Poland", "Sweden", "Finland", "Netherlands", "France", "Saudi Arabia", "UAE",
    "Qatar", "Other"
]

PHONE_COUNTRY_CODES = [
    "+880", "+91", "+92", "+977", "+94", "+60", "+49", "+1", "+61", "+44",
    "+966", "+971", "+974", "+90", "+39", "+48", "+46", "+358", "+31", "+33"
]

CURRENCY_CHOICES = Literal["BDT", "USD", "INR", "EUR", "MYR", "AUD", "CAD", "GBP"]

class EducationEntry(BaseModel):
    level: str = Field(..., description="Education level", example="HSC")
    institution: Optional[str] = Field(None, description="School or university name", example="Notre Dame College")
    field: Optional[str] = Field(None, description="Field of study", example="Science")
    gpa: Optional[float] = Field(None, description="GPA/CGPA", example=5.0)
    year_completed: Optional[int] = Field(None, description="Year completed or expected", example=2024)

class UserInfoBase(BaseModel):
    # Personal Details
    full_name: str = Field(..., description="Full name as in passport", example="Md. Abdullah Al Mamun")
    father_name: Optional[str] = Field(None, description="Father's name", example="Mr. XYZ")
    mother_name: Optional[str] = Field(None, description="Mother's name", example="Mrs. ABC")

    # Contact
    email: str = Field(..., description="Email address", example="student@gmail.com")
    phone_country_code: Optional[str] = Field("+880", description="Phone country code", example="+880")
    phone_number: Optional[str] = Field(None, description="Phone number", example="1712345678")
    full_phone: Optional[str] = Field(None, description="Combined phone number", example="+8801712345678")

    # Background
    nationality: List[str] = Field(default=["Bangladesh"], description="Nationality", example=["Bangladesh"])
    current_living_country: List[str] = Field(default=["Bangladesh"], description="Current residence", example=["Bangladesh"])

    # Education
    education: List[EducationEntry] = Field(default=[], description="Education history")

    # Preferences
    preferred_countries: List[str] = Field(..., description="Preferred study destinations", example=["Germany", "Malaysia"])
    budget_min_bdt: Optional[int] = Field(None, description="Minimum budget per year in BDT", example=500000)
    budget_max_bdt: Optional[int] = Field(None, description="Maximum budget per year in BDT", example=2500000)
    preferred_currency: CURRENCY_CHOICES = Field("BDT", description="Preferred currency")
    preferred_intake: Optional[str] = Field(None, description="Preferred intake", example="Fall 2026")

    # Optional
    resume_filename: Optional[str] = Field(None, description="Uploaded resume filename")
    resume_text: Optional[str] = Field(None, description="Extracted text from resume")

class UserInfoCreate(UserInfoBase):
    pass

class UserInfoResponse(UserInfoBase):
    id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[str] = None
    message: Optional[str] = None

    class Config:
        from_attributes = True