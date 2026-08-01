from app.services.graph_utils import GraphUtils

from app.services.cycle_detector import CycleDetector

class GraphAnalyzer:

    @staticmethod
    def analyze(graph: dict):

        incoming = GraphUtils.get_incoming_edges(graph)

        # Most connected module
        most_connected = max(
            graph,
            key=lambda module: len(graph[module]),
            default=None,
        )

        # Orphan modules
        orphan_modules = []

        for module in graph:

            if len(graph[module]) == 0 and incoming[module] == 0:
                orphan_modules.append(module)

        return {
            "most_connected_module": most_connected,
            "max_dependencies": len(graph.get(most_connected, [])),
            "orphan_modules": orphan_modules,
            "circular_dependencies": CycleDetector.find_cycles(graph)
        }