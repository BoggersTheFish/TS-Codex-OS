import unittest

from ts_codex_os.graph import add_node, create_project_graph
from ts_codex_os.planner import propose_next_actions
from ts_codex_os.types import TSNode, TSTension


class PlannerTests(unittest.TestCase):
    def test_missing_tests_action_is_proposed(self):
        graph = create_project_graph("demo")
        add_node(graph, TSNode("repo", "repo", "demo", "observed", 0.7, {}))
        graph.tensions.append(
            TSTension(
                "tension:1:missing_tests",
                "repo",
                "missing_tests",
                0.75,
                "No tests.",
                ["tests/ not found"],
                "Add focused unittest coverage.",
            )
        )
        actions = propose_next_actions(graph)
        self.assertTrue(any("unittest" in action.title.lower() for action in actions))


if __name__ == "__main__":
    unittest.main()

