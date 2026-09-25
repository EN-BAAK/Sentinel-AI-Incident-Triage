from pydantic import BaseModel, Field


class IncidentRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)
    service: str = Field(min_length=1, max_length=100)


class IncidentReport(BaseModel):
    summary: str
    evidence: list[str]
    hypotheses: list[str]
    recommended_steps: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
