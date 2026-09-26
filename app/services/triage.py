from app.models.incident import IncidentReport, IncidentRequest
from app.tools.metrics import get_service_metrics


def triage_incident(incident: IncidentRequest) -> IncidentReport:
    description = incident.description.lower()

    metrics = get_service_metrics(incident.service)

    evidence: list[str] = []
    hypotheses: list[str] = []
    recommended_steps: list[str] = []
    limitations: list[str] = []

    if metrics is None:
        limitations.append(
            f"Metrics are unavailable for service '{incident.service}'."
        )
    else:
        memory_usage = metrics.memory_usage_percent
        cpu_usage = metrics.cpu_usage_percent
        latency = metrics.latency_ms

        if memory_usage >= 85:
            evidence.append(
                f"Memory usage is high at {memory_usage}%."
            )

        if latency >= 500:
            evidence.append(
                f"Service latency is high at {latency} ms."
            )

        if (
            memory_usage >= 85
            and cpu_usage < 50
            and "restart" in description
        ):
            hypotheses.append("Possible memory leak")
            recommended_steps.extend(
                [
                    "Inspect memory usage over time",
                    "Compare memory usage before and after restart",
                ]
            )

    return IncidentReport(
        summary=incident.description,
        evidence=evidence,
        hypotheses=hypotheses,
        recommended_steps=recommended_steps,
        limitations=limitations,
        confidence=0.6 if hypotheses else 0.0,
    )