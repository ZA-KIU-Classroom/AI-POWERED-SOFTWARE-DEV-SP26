from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="User input to send to the model")
    system: str | None = Field(None, description="Optional system prompt override")
    model:  str | None = Field(None, description="Optional model override — defaults to DEFAULT_MODEL in .env")

    model_config = {"json_schema_extra": {"example": {
        "prompt": "Summarise the following text in three sentences: ...",
        "system": "You are a concise summarisation assistant.",
    }}}


class GenerateResponse(BaseModel):
    content:       str
    model:         str
    input_tokens:  int
    output_tokens: int
    latency_ms:    int
    cost_usd:      float
