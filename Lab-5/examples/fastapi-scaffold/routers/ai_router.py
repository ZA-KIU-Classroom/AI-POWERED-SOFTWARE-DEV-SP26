from fastapi import APIRouter, HTTPException
from models.request_models import GenerateRequest, GenerateResponse
from services import llm_service

router = APIRouter()


@router.post("/ai/generate", response_model=GenerateResponse)
def generate(body: GenerateRequest):
    """
    Primary AI endpoint. Replace this with your capstone-specific logic.
    """
    try:
        result = llm_service.generate(
            prompt  = body.prompt,
            system  = body.system or "You are a helpful assistant.",
            model   = body.model,
            purpose = "api_generate",
        )
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
