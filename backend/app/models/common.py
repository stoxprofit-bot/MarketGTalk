from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def object_id_str(value) -> str | None:
    if value is None:
        return None
    return str(value)
