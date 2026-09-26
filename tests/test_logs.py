from app.tools.logs import get_service_logs


def test_get_orders_api_logs() -> None:
    logs = get_service_logs("orders-api")

    assert logs is not None
    assert len(logs) == 3

    assert logs[0].level == "WARNING"
    assert "memory" in logs[0].message.lower()


def test_unknown_service_has_no_logs() -> None:
    logs = get_service_logs("unknown-api")

    assert logs is None