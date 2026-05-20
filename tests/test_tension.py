import tempfile
import unittest
from pathlib import Path

from ts_codex_os.ingest import ingest_repo
from ts_codex_os.tension import score_project_tension


class TensionTests(unittest.TestCase):
    def test_missing_readme_license_tests_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            graph = score_project_tension(ingest_repo(tmp))
            kinds = {tension.kind for tension in graph.tensions}
            self.assertIn("missing_readme", kinds)
            self.assertIn("missing_license", kinds)
            self.assertIn("missing_tests", kinds)

    def test_overclaiming_language_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("This proves general reasoning and is guaranteed.\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "tests").mkdir()
            graph = score_project_tension(ingest_repo(tmp))
            self.assertIn("overclaiming_language", {tension.kind for tension in graph.tensions})


if __name__ == "__main__":
    unittest.main()

