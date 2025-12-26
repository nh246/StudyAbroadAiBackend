from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
from services.chat_service import chat_with_multi_agent

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    user_id: int = Field(..., description="User ID from profile submission", example=1)
    question: str = Field(..., description="User's question about studying abroad", example="What are the best universities in Germany for Computer Science?")


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI-generated personalized response")
    profile_used: Optional[Dict] = Field(None, description="Summary of user profile used")
    search_results: Optional[Dict] = Field(None, description="Web search results summary")
    error: Optional[str] = Field(None, description="Error message if any")


@router.post(
    "/ask",
    response_model=ChatResponse,
    summary="Ask the AI Study Abroad Advisor",
    description="Send a question to the multi-agent chatbot. Requires user_id from profile submission."
)
async def chat_with_ai(request: ChatRequest):
    """
    Multi-Agent Chat Endpoint:
    1. Retrieves user profile context
    2. Searches web for current information (Tavily)
    3. Generates personalized answer (HuggingFace model)
    
    Returns comprehensive response with AI answer and metadata
    """
    
    # Validate inputs
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Call multi-agent orchestrator
    result = chat_with_multi_agent(
        user_id=request.user_id,
        question=request.question.strip()
    )
    
    # Check for errors
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    
    return ChatResponse(
        response=result["response"],
        profile_used=result.get("profile_used"),
        search_results=result.get("search_results")
    )


@router.get(
    "/",
    summary="Chat API Info",
    description="Get information about the chat API"
)
async def chat_info():
    """Information about the chat endpoint"""
    return {
        "message": "Multi-Agent Study Abroad Chat API",
        "agents": [
            "Profile Agent - Retrieves user context",
            "Search Agent - Tavily web search",
            "Response Agent - HuggingFace AI model"
        ],
        "usage": {
            "step_1": "Submit profile at /profile/submit to get user_id",
            "step_2": "Send questions to /chat/ask with user_id"
        },
        "model": "millat/study-abroad-guidance-ai (HuggingFace)"
    }