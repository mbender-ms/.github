import unittest

from fact_check_v2.policy import ToolPolicy


class ToolPolicyTests(unittest.TestCase):
    def test_allows_fact_checker(self) -> None:
        policy = ToolPolicy()
        self.assertTrue(policy.is_allowed("fact-checker"))

    def test_allows_mcp_prefix(self) -> None:
        policy = ToolPolicy()
        self.assertTrue(policy.is_allowed("mcp.learn.search"))

    def test_blocks_non_allowlisted(self) -> None:
        policy = ToolPolicy()
        self.assertFalse(policy.is_allowed("web.fetch"))


if __name__ == "__main__":
    unittest.main()
