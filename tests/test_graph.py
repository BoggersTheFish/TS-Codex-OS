import json
import unittest

from ts_codex_os.graph import add_edge, add_node, create_project_graph, find_node, summarize_graph
from ts_codex_os.types import TSEdge, TSNode, to_jsonable


class GraphTests(unittest.TestCase):
    def test_node_edge_creation_and_summary(self):
        graph = create_project_graph("demo")
        add_node(graph, TSNode("repo", "repo", "demo", "observed", 0.7, {}))
        add_node(graph, TSNode("tests", "tests", "tests", "observed", 0.8, {}))
        add_edge(graph, TSEdge("tests", "repo", "verifies", 0.8, {}))
        self.assertEqual("demo", graph.project_name)
        self.assertIsNotNone(find_node(graph, "repo"))
        summary = summarize_graph(graph)
        self.assertEqual(2, summary["node_count"])
        self.assertEqual(1, summary["edge_count"])

    def test_json_serialization(self):
        graph = create_project_graph("demo")
        add_node(graph, TSNode("repo", "repo", "demo", "observed", 0.7, {"x": 1}))
        payload = to_jsonable(graph)
        encoded = json.dumps(payload, sort_keys=True)
        self.assertIn("demo", encoded)
        self.assertEqual("repo", payload["nodes"][0]["node_id"])


if __name__ == "__main__":
    unittest.main()

