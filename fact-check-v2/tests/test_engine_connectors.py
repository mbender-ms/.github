import tempfile
import unittest
from pathlib import Path

from fact_check_v2.engine import run_gap_analysis
from fact_check_v2.models import FactInput, Verdict


class EngineConnectorTests(unittest.TestCase):
    def test_unverifiable_when_missing_and_no_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            article = root / "article.md"
            article.write_text("No matching content here.", encoding="utf-8")

            facts = [FactInput(id="F-1", text="A unique unmatched statement", service="test")]
            analysis = run_gap_analysis(facts, [article], cache=None, source_roots=[root])

            self.assertEqual(len(analysis.results), 1)
            self.assertEqual(analysis.results[0].verdict, Verdict.UNVERIFIABLE)


if __name__ == "__main__":
    unittest.main()
