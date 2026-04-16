from __future__ import annotations

import time
from typing import Callable, TypeVar

from .policy import ToolPolicy
from .telemetry import ToolCallTracer

T = TypeVar("T")


class ToolExecutor:
    def __init__(self, policy: ToolPolicy | None = None, tracer: ToolCallTracer | None = None) -> None:
        self.policy = policy
        self.tracer = tracer

    def invoke(self, tool_name: str, args_summary: str, func: Callable[[], T]) -> T:
        start = time.perf_counter()
        allowed = self.policy.is_allowed(tool_name) if self.policy else True
        if not allowed:
            latency = int((time.perf_counter() - start) * 1000)
            if self.tracer:
                self.tracer.emit(tool_name, args_summary, "blocked", latency, "blocked by policy")
            raise PermissionError(f"Tool call blocked by policy: {tool_name}")

        try:
            result = func()
            latency = int((time.perf_counter() - start) * 1000)
            if self.tracer:
                self.tracer.emit(tool_name, args_summary, "ok", latency, "allowed by policy")
            return result
        except Exception as exc:
            latency = int((time.perf_counter() - start) * 1000)
            if self.tracer:
                self.tracer.emit(tool_name, args_summary, "error", latency, str(exc))
            raise
