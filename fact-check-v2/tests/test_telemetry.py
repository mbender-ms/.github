import json
import tempfile
import unittest
from pathlib import Path

from fact_check_v2.telemetry import ToolCallTracer


class TelemetryTests(unittest.TestCase):
    def test_emits_jsonl_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tool_calls.jsonl"
            tracer = ToolCallTracer(path)
            tracer.emit("fact-checker", "run", "ok", 12, "allowed")

            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            payload = json.loads(lines[0])
            self.assertEqual(payload["tool_name"], "fact-checker")
            self.assertEqual(payload["status"], "ok")
            self.assertIn("correlation_id", payload)


if __name__ == "__main__":
    unittest.main()
