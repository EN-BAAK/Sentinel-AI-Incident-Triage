from app.models.incident import IncidentRequest
from app.services.triage import triage_incident


def test_triage_detects_possible_memory_leak() -> None:
    incident = IncidentRequest(
        title="API latency increasing",
        description=(
            "Latency keeps increasing and restarting "
            "the service temporarily fixes the issue."
        ),
        service="orders-api",
    )

    report = triage_incident(incident)

    assert "Memory usage is high at 91.0%." in report.evidence
    assert "Service latency is high at 840.0 ms." in report.evidence
    assert "Possible memory leak" in report.hypotheses
    assert report.confidence == 0.6

def test_triage_handles_missing_metrics() -> None:
    incident = IncidentRequest(
        title="Unknown service problem",
        description="The service has been behaving strangely after restart.",
        service="unknown-api",
    )

    report = triage_incident(incident)

    assert report.evidence == []
    assert report.hypotheses == []
    assert report.confidence == 0.0
    assert report.limitations == [
        "Metrics are unavailable for service 'unknown-api'."
    ]