# Chat Service - Multi-Agent Orchestration

from typing import Dict
# Using GitHub Models (o4-mini)
from core.config import settings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from services.profile_service import get_user_profile, format_profile_for_ai
from services.search_service import search_web, format_search_results

# Initialize GitHub Model
try:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.github_token,
        base_url="https://models.inference.ai.azure.com",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
except Exception as e:
    print(f"Warning: GitHub Model initialization failed: {e}")
    llm = None


def generate_ai_response(prompt: str, system_instruction: str = None, max_tokens: int = 1000) -> str:
    """
    Call GitHub Model (o4-mini) for text generation
    """
    if not llm:
        return "Error: GitHub Token not configured. Please add GITHUB_TOKEN to your .env file."

    try:
        messages = []
        if system_instruction:
            messages.append(SystemMessage(content=system_instruction))
        
        messages.append(HumanMessage(content=prompt))
        
        response = llm.invoke(messages)
        return response.content

    except Exception as e:
        return f"Error generating response: {str(e)}"


def chat_with_multi_agent(user_id: int, question: str) -> Dict:
    """
    Multi-Agent Chat Orchestration
    """
    
    # AGENT 1: Profile Agent - Get user context
    profile = get_user_profile(user_id)
    if not profile:
        return {
            "error": f"Profile not found for user_id: {user_id}. Please submit your profile first.",
            "response": None,
            "profile_used": None,
            "search_results": None
        }
    
    profile_context = format_profile_for_ai(profile)
    
    # AGENT 2: Search Agent - Web search for current information
    search_query = f"study abroad {question} {' '.join(profile.get('preferred_countries', []))}"
    search_data = search_web(search_query, max_results=5)
    search_context = format_search_results(search_data)
    
    # AGENT 3: Response Agent - Build "Perfect Prompt"
    system_prompt = """You are an elite Study Abroad Consultant and Career Strategist. Your goal is to provide highly personalized, data-driven, and actionable advice to students aspiring to study overseas. 

You have access to the student's full academic profile, financial constraints, and resume details. You also have real-time web search results to supplement your knowledge.

**Guidelines for Excellence:**
1.  **Deep Personalization**: Never give generic advice. Always reference the student's specific GPA, budget, background, and resume highlights.
2.  **Strategic Insight**: Go beyond surface-level answers. Analyze *why* a country or university is a good fit. Discuss long-term career ROI (Return on Investment).
3.  **Financial Realism**: Be brutally honest about costs. If their budget is low, suggest specific scholarships, part-time work options, or alternative affordable destinations designated in their preferences.
4.  **Resume Integration**: If a resume is provided, analyze it. Suggest how they can improve their profile for better admission chances.
5.  **Actionable Roadmap**: Every response must end with a clear set of next steps (e.g., "Draft your SOP," "Research these 3 universities").
6.  **Tone**: Professional, encouraging, authoritative, and structured.

**Format your response using Markdown:**
- Use **Bold** for emphasis.
- Use lists for readability.
- Use headers to structure the advice.
"""

    user_prompt = f"""
Student Profile Context:
{profile_context}

Latest Web Search Intelligence:
{search_context}

Student's Inquiry:
{question}

Based on the above, provide your expert consultation.
"""
    
    # Generate AI response
    ai_response = generate_ai_response(user_prompt, system_instruction=system_prompt, max_tokens=1000)
    
    return {
        "response": ai_response,
        "profile_used": {
            "name": profile.get("full_name"),
            "preferred_countries": profile.get("preferred_countries"),
            "budget_range": f"{profile.get('budget_min_bdt', 0):,} - {profile.get('budget_max_bdt', 0):,} BDT"
        },
        "search_results": {
            "query": search_query,
            "answer": search_data.get("answer", ""),
            "sources_count": len(search_data.get("sources", []))
        }
    }
