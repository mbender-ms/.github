from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .models import ToolCallEvent


class ToolCallTracer:
    def __init__(self, output_path: Path | None = None) -> None:
        self.output_path = output_path
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, tool_name: str, args_summary: str, status: str, latency_ms: int, message: str = "") -> ToolCallEvent:
        event = ToolCallEvent(
            timestamp=datetime.now(timezone.utc),
            correlation_id=str(uuid.uuid4()),
            tool_name=tool_name,
            args_summary=args_summary,
            status=status,
            latency_ms=latency_ms,
            message=message,
        )
        payload = event.model_dump(mode="json")
        line = json.dumps(payload)
        print(line)
        if self.output_path:
            with self.output_path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
        return event
