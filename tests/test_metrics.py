import pytest
from pydantic import ValidationError

from app.models.metrics import ServiceMetrics
from app.tools.metrics import get_service_metrics


def test_get_orders_api_metrics() -> None:
    metrics = get_service_metrics("orders-api")

    assert metrics is not None
    assert metrics.memory_usage_percent == 91.0
    assert metrics.cpu_usage_percent == 34.0
    assert metrics.latency_ms == 840.0


def test_unknown_service_has_no_metrics() -> None:
    metrics = get_service_metrics("unknown-api")

    assert metrics is None


def test_service_metrics_reject_invalid_values() -> None:
    with pytest.raises(ValidationError):
        ServiceMetrics(
            memory_usage_percent=150.0,
            cpu_usage_percent=30.0,
            latency_ms=100.0,
        )