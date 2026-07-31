class GraphAnalyzer:

    @staticmethod
    def analyze(graph: dict):

        incoming = {}

        for module in graph:
            incoming[module] = 0

        # Count incoming dependencies
        for module, dependencies in graph.items():

            for dependency in dependencies:

                if dependency in incoming:
                    incoming[dependency] += 1

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
            "circular_dependencies": []
        }