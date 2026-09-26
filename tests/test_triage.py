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

    assert any(
        "memory usage continues to increase" in evidence.lower()
        for evidence in report.evidence
    )

    assert "Possible memory leak" in report.hypotheses
    assert report.confidence == 0.8


def test_triage_handles_missing_data() -> None:
    incident = IncidentRequest(
        title="Unknown service problem",
        description="The service behaves strangely after restart.",
        service="unknown-api",
    )

    report = triage_incident(incident)

    assert report.evidence == []
    assert report.hypotheses == []
    assert report.confidence == 0.0

    assert report.limitations == [
        "Metrics are unavailable for service 'unknown-api'.",
        "Logs are unavailable for service 'unknown-api'.",
    ]

def test_triage_detects_upstream_provider_timeout() -> None:
    incident = IncidentRequest(
        title="Payments failing",
        description="Some payment requests have started failing.",
        service="payments-api",
    )

    report = triage_incident(incident)

    assert any(
        "payment provider request timed out" in evidence.lower()
        for evidence in report.evidence
    )

    assert (
        "Possible upstream provider timeout"
        in report.hypotheses
    )

def test_triage_does_not_flag_cache_warmup_as_memory_leak() -> None:
    incident = IncidentRequest(
        title="High memory during startup",
        description=(
            "Memory is elevated during startup. "
            "The service was restarted during a normal deployment."
        ),
        service="reports-api",
    )

    report = triage_incident(incident)

    assert "Possible memory leak" not in report.hypotheses
    assert report.confidence == 0.0