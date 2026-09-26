from dataclasses import dataclass

from app.models.incident import IncidentRequest


@dataclass
class EvalCase:
    name: str
    incident: IncidentRequest
    expected_hypotheses: list[str]
    forbidden_hypotheses: list[str]

EVAL_CASES = [
    EvalCase(
        name="memory_leak_orders_api",
        incident=IncidentRequest(
            title="Increasing latency and memory",
            description=(
                "Latency keeps increasing and restarting "
                "the service temporarily fixes the issue."
            ),
            service="orders-api",
        ),
        expected_hypotheses=[
            "Possible memory leak",
        ],
        forbidden_hypotheses=[
            "Possible upstream provider timeout",
        ],
    ),
    EvalCase(
        name="payments_provider_timeout",
        incident=IncidentRequest(
            title="Payments failing",
            description="Some payment requests have started failing.",
            service="payments-api",
        ),
        expected_hypotheses=[
            "Possible upstream provider timeout",
        ],
        forbidden_hypotheses=[
            "Possible memory leak",
        ],
    ),
    EvalCase(
        name="unknown_service",
        incident=IncidentRequest(
            title="Unknown service issue",
            description="The service appears unstable after restart.",
            service="unknown-api",
        ),
        expected_hypotheses=[],
        forbidden_hypotheses=[
            "Possible memory leak",
            "Possible upstream provider timeout",
        ],
    ),
    EvalCase(
        name="cache_warmup_not_memory_leak",
        incident=IncidentRequest(
            title="High memory during startup",
            description=(
                "Memory is elevated during startup. "
                "The service was restarted during a normal deployment."
            ),
            service="reports-api",
        ),
        expected_hypotheses=[],
        forbidden_hypotheses=[
            "Possible memory leak",
        ],
),
]