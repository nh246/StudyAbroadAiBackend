# Profile Service - Manages user profile storage and retrieval

from typing import Optional
from core.cache import profile_cache
from schemas.profile import UserInfoCreate


def save_user_profile(profile: UserInfoCreate) -> int:
    """
    Save a user profile to cache and return the user_id
    
    Args:
        profile: UserInfoCreate schema with all profile data
        
    Returns:
        user_id: Unique identifier for this profile
    """
    profile_data = profile.dict()
    user_id = profile_cache.save_profile(profile_data)
    return user_id


def get_user_profile(user_id: int) -> Optional[dict]:
    """
    Retrieve a user profile by ID
    
    Args:
        user_id: The unique identifier
        
    Returns:
        Profile data dictionary or None if not found
    """
    return profile_cache.get_profile(user_id)


def format_profile_for_ai(profile: dict) -> str:
    """
    Format user profile data for AI consumption
    
    Args:
        profile: Profile dictionary
        
    Returns:
        Formatted string with profile context
    """
    education_info = ""
    if profile.get('education'):
        edu = profile['education'][0] if isinstance(profile['education'], list) else profile['education']
        education_info = f"""
- Education Level: {edu.get('level', 'N/A')}
- Field of Study: {edu.get('field', 'N/A')}
- Institution: {edu.get('institution', 'N/A')}
- GPA/CGPA: {edu.get('gpa', 'N/A')}
- Year: {edu.get('year_completed', 'N/A')}"""
    
    budget_info = ""
    if profile.get('budget_min_bdt') or profile.get('budget_max_bdt'):
        min_budget = profile.get('budget_min_bdt', 0)
        max_budget = profile.get('budget_max_bdt', 0)
        budget_info = f"\n- Budget Range: {min_budget:,} - {max_budget:,} BDT/year"
    
    profile_context = f"""
Student Profile:
- Name: {profile.get('full_name', 'Student')}
- Email: {profile.get('email', 'N/A')}
- Nationality: {', '.join(profile.get('nationality', ['N/A']))}
- Currently Living: {', '.join(profile.get('current_living_country', ['N/A']))}
{education_info}
{budget_info}
- Preferred Study Destinations: {', '.join(profile.get('preferred_countries', ['N/A']))}
- Preferred Intake: {profile.get('preferred_intake', 'Flexible')}

Resume Context:
{profile.get('resume_text', 'No resume provided.')}
"""
    return profile_context.strip()
