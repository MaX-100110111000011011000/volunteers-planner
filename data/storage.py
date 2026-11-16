import json
from pathlib import Path

DATA_FILE = Path.home() / "VolunteersPlanner" / "events.json"


def load_events() -> list:
    if not DATA_FILE.exists():
        return []
    try:
        content = DATA_FILE.read_text(encoding="utf-8").strip()
        if not content:
            return []
        data = json.loads(content)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_events(events: list) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(events, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] Сохранено мероприятий: {len(events)} -> {DATA_FILE}")
