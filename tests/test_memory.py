import tempfile
import unittest
from pathlib import Path

from ts_codex_os.cli import main
from ts_codex_os.graph import add_node, create_project_graph
from ts_codex_os.memory import append_event, read_events, read_graph, write_graph
from ts_codex_os.types import TSNode


class MemoryTests(unittest.TestCase):
    def test_append_and_read_events(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            append_event(path, {"kind": "demo", "value": 1})
            append_event(path, {"kind": "demo", "value": 2})
            events = read_events(path)
            self.assertEqual(2, len(events))
            self.assertEqual(2, events[-1]["value"])

    def test_write_and_read_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            graph = create_project_graph("demo")
            add_node(graph, TSNode("repo", "repo", "demo", "observed", 0.7, {}))
            path = write_graph(Path(tmp) / "graph.json", graph)
            payload = read_graph(path)
            self.assertEqual("demo", payload["project_name"])

    def test_cli_status_runs_on_tiny_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Tiny repo.\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "tests").mkdir()
            result = main(["status", "--project-path", str(root)])
            self.assertEqual(0, result)
            self.assertTrue((root / "artifacts" / "ts_status.md").exists())
            self.assertTrue((root / "artifacts" / "project_graph.json").exists())
            self.assertTrue((root / "artifacts" / "next_actions.md").exists())


if __name__ == "__main__":
    unittest.main()

