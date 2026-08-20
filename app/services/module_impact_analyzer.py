class ModuleImpactAnalyzer:

    @staticmethod
    def analyze(dependency_graph):

        impact = {}

        # Initialize every module
        for module in dependency_graph:

            impact[module] = {
                "fan_in": 0,
                "fan_out": len(
                    dependency_graph[module]
                )
            }

        # Calculate fan-in
        for module, dependencies in dependency_graph.items():

            for dependency in dependencies:

                if dependency in impact:

                    impact[dependency]["fan_in"] += 1

        return impact