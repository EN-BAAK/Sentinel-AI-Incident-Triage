from app.models.incident import IncidentRequest
from app.services.triage import triage_incident


def test_triage_detects_possible_memory_leak() -> None:
    incident = IncidentRequest(
        title="API latency increasing",
        description=(
            "Memory usage keeps growing and restarting "
            "the service temporarily fixes the issue."
        ),
        service="orders-api",
    )

    report = triage_incident(incident)

    assert "Possible memory leak" in report.hypotheses
    assert report.confidence == 0.4