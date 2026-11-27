"""Privacy-conscious activity log. Never record paths, keys, passphrases or content."""
import json
from datetime import datetime, timezone
from pathlib import Path


def write_event(event: str, status: str, details: str = "") -> None:
    from .key_manager import app_data_dir
    log = app_data_dir() / "activity.jsonl"
    allowed = {"key_profile_created", "public_key_imported", "file_encrypted", "file_decrypted", "profile_deleted"}
    if event not in allowed:
        return
    record = {"time_utc": datetime.now(timezone.utc).isoformat(), "event": event, "status": status, "details": details[:120]}
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
