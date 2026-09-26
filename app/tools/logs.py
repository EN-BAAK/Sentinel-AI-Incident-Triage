from app.models.logs import LogEntry


def get_service_logs(service: str) -> list[LogEntry] | None:
    simulated_logs = {
        "orders-api": [
            LogEntry(
                level="WARNING",
                message="Worker memory usage continues to increase.",
            ),
            LogEntry(
                level="INFO",
                message="Service restarted successfully.",
            ),
            LogEntry(
                level="WARNING",
                message="Request latency exceeded expected threshold.",
            ),
        ],
        "payments-api": [
            LogEntry(
                level="ERROR",
                message="Payment provider request timed out.",
            ),
        ],

        "reports-api": [
            LogEntry(
                level="INFO",
                message=(
                    "Memory usage increase observed during cache warmup; "
                    "usage stabilized after initialization."
                ),
            ),
            LogEntry(
                level="INFO",
                message="Service restarted as part of a normal deployment.",
            ),
        ],
    }

    return simulated_logs.get(service)