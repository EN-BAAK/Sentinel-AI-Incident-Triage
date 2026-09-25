from fastapi import FastAPI

from app.models.incident import IncidentReport, IncidentRequest

app = FastAPI(
    title="Sentinel",
    description="AI Incident Triage System",
    version="0.1.0",
)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/incidents", response_model=IncidentReport)
async def create_incident(incident: IncidentRequest) -> IncidentReport:
    return IncidentReport(
        summary=incident.description,
        evidence=[],
        hypotheses=[],
        recommended_steps=[],
        confidence=0.0,
    )