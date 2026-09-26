from app.models.incident import IncidentReport, IncidentRequest
from app.tools.logs import get_service_logs
from app.tools.metrics import get_service_metrics


def triage_incident(incident: IncidentRequest) -> IncidentReport:
    description = incident.description.lower()

    metrics = get_service_metrics(incident.service)
    logs = get_service_logs(incident.service)

    evidence: list[str] = []
    hypotheses: list[str] = []
    recommended_steps: list[str] = []
    limitations: list[str] = []

    high_memory = False
    low_cpu = False
    high_latency = False

    memory_growth_log = False
    memory_stabilized_log = False
    normal_deployment_restart_log = False
    provider_timeout_log = False

    if metrics is None:
        limitations.append(
            f"Metrics are unavailable for service '{incident.service}'."
        )
    else:
        high_memory = metrics.memory_usage_percent >= 85
        low_cpu = metrics.cpu_usage_percent < 50
        high_latency = metrics.latency_ms >= 500

        if high_memory:
            evidence.append(
                f"Memory usage is high at "
                f"{metrics.memory_usage_percent}%."
            )

        if high_latency:
            evidence.append(
                f"Service latency is high at "
                f"{metrics.latency_ms} ms."
            )

    if logs is None:
        limitations.append(
            f"Logs are unavailable for service '{incident.service}'."
        )
    else:
        for log in logs:
            message = log.message.lower()

            if "memory" in message and "increase" in message:
                memory_growth_log = True
                evidence.append(
                    f"Log evidence: {log.message}"
                )

            if "provider" in message and "timed out" in message:
                provider_timeout_log = True
                evidence.append(
                    f"Log evidence: {log.message}"
                )

            if "restart" in message and "normal deployment" in message:
                normal_deployment_restart_log = True
                evidence.append(
                    f"Log evidence: {log.message}"
                )

            if "memory" in message and "stabilized" in message:
                memory_stabilized_log = True
                evidence.append(
                    f"Log evidence: {log.message}"
            )

    if (
        high_memory
        and low_cpu
        and memory_growth_log
        and not memory_stabilized_log
        and not normal_deployment_restart_log
        and "restart" in description
    ):
        hypotheses.append("Possible memory leak")
        recommended_steps.extend(
            [
                "Inspect memory usage over time",
                "Compare memory usage before and after restart",
                "Inspect heap or object allocation growth",
            ]
        )

    if provider_timeout_log:
        hypotheses.append("Possible upstream provider timeout")
        recommended_steps.extend(
        [
            "Inspect upstream provider latency and error rates",
            "Check recent provider incidents or status changes",
            "Review timeout configuration and failed requests",
        ]
    )

    return IncidentReport(
        summary=incident.description,
        evidence=evidence,
        hypotheses=hypotheses,
        recommended_steps=recommended_steps,
        limitations=limitations,
        confidence=0.8 if hypotheses else 0.0,
    )