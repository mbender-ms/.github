from pathlib import Path
import unittest

from fact_check_v2.chunking import chunk_files


class ChunkingTests(unittest.TestCase):
    def test_chunk_size_constraints(self) -> None:
        files = [Path(f"f{i}.md") for i in range(20)]
        with self.assertRaises(ValueError):
            chunk_files(files, chunk_size=7)
        with self.assertRaises(ValueError):
            chunk_files(files, chunk_size=11)

    def test_chunking_works(self) -> None:
        files = [Path(f"f{i}.md") for i in range(20)]
        chunks = chunk_files(files, chunk_size=10)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(len(chunks[0]), 10)
        self.assertEqual(len(chunks[1]), 10)


if __name__ == "__main__":
    unittest.main()
