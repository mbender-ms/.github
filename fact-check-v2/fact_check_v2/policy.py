from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ToolPolicy:
    allowed_exact: set[str] = field(default_factory=lambda: {"fact-checker"})
    allowed_prefixes: tuple[str, ...] = ("mcp.", "fact-checker.")
    strict: bool = True

    def is_allowed(self, tool_name: str) -> bool:
        if tool_name in self.allowed_exact:
            return True
        return any(tool_name.startswith(prefix) for prefix in self.allowed_prefixes)
