import unittest

from fact_check_v2.policy import ToolPolicy
from fact_check_v2.tool_executor import ToolExecutor


class ToolExecutorTests(unittest.TestCase):
    def test_blocks_disallowed_tool(self) -> None:
        executor = ToolExecutor(policy=ToolPolicy(strict=True))
        with self.assertRaises(PermissionError):
            executor.invoke("web.fetch", "url=https://example.com", lambda: "ok")

    def test_allows_fact_checker_prefix(self) -> None:
        executor = ToolExecutor(policy=ToolPolicy(strict=True))
        result = executor.invoke("fact-checker.local-source.search", "fact=F-1", lambda: "ok")
        self.assertEqual(result, "ok")


if __name__ == "__main__":
    unittest.main()
