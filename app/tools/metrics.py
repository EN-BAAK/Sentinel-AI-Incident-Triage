from app.models.metrics import ServiceMetrics


def get_service_metrics(service: str) -> ServiceMetrics | None:
    simulated_metrics = {
        "orders-api": ServiceMetrics(
            memory_usage_percent=91.0,
            cpu_usage_percent=34.0,
            latency_ms=840.0,
        ),
        "payments-api": ServiceMetrics(
            memory_usage_percent=52.0,
            cpu_usage_percent=76.0,
            latency_ms=240.0,
        ),
        "reports-api": ServiceMetrics(
            memory_usage_percent=92.0,
            cpu_usage_percent=25.0,
            latency_ms=650.0,
        ),
    }

    return simulated_metrics.get(service)