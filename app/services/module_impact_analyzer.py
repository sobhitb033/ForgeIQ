class ModuleImpactAnalyzer:

    @staticmethod
    def analyze(dependency_graph):

        impact = {}

        # Initialize every module
        for module in dependency_graph:
            impact[module] = {
                "fan_in": 0,
                "fan_out": 0
            }

        # Calculate fan-in and fan-out
        for module, dependencies in dependency_graph.items():

            # fan_out = number of modules this module depends on
            impact[module]["fan_out"] = len(dependencies)

            # fan_in = number of modules depending on another module
            for dependency in dependencies:

                if dependency not in impact:
                    impact[dependency] = {
                        "fan_in": 0,
                        "fan_out": 0
                    }

                impact[dependency]["fan_in"] += 1

        return impact