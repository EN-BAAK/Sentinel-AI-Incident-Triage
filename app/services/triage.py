from app.models.incident import IncidentReport, IncidentRequest


def triage_incident(incident: IncidentRequest) -> IncidentReport:
    description = incident.description.lower()

    hypotheses: list[str] = []
    recommended_steps: list[str] = []

    if "memory" in description and "restart" in description:
        hypotheses.append("Possible memory leak")
        recommended_steps.extend(
            [
                "Inspect memory usage over time",
                "Compare memory usage before and after restart",
            ]
        )

    return IncidentReport(
        summary=incident.description,
        evidence=[],
        hypotheses=hypotheses,
        recommended_steps=recommended_steps,
        confidence=0.4 if hypotheses else 0.0,
    )