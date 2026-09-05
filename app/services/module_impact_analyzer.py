from collections import deque


class ModuleImpactAnalyzer:
    """Calculate direct and transitive architectural impact for each module."""

    @staticmethod
    def analyze(dependency_graph):
        """Return fan-in/out plus downstream/upstream reachability.

        The dependency graph is directed as:
            module -> modules it depends on

        Therefore a module's *dependents* are the modules that may be
        affected when the module changes.  We call that its downstream
        impact because the change propagates through incoming edges.
        """
        nodes = set(dependency_graph.keys())
        for dependencies in dependency_graph.values():
            nodes.update(dependencies)

        graph = {
            node: list(dependency_graph.get(node, []))
            for node in nodes
        }

        reverse_graph = {node: [] for node in nodes}
        for module, dependencies in graph.items():
            for dependency in dependencies:
                reverse_graph.setdefault(dependency, []).append(module)

        impact = {}

        for module in sorted(nodes):
            direct_dependencies = sorted(set(graph.get(module, [])))
            direct_dependents = sorted(set(reverse_graph.get(module, [])))

            transitive_dependencies = ModuleImpactAnalyzer._reachable(
                graph,
                module,
            )
            transitive_dependents = ModuleImpactAnalyzer._reachable(
                reverse_graph,
                module,
            )

            # The direct counts remain the familiar fan-in/fan-out metrics.
            fan_out = len(direct_dependencies)
            fan_in = len(direct_dependents)
            blast_radius = len(transitive_dependents)
            dependency_reach = len(transitive_dependencies)

            # A weighted score gives architectural impact a single comparable
            # number while retaining the underlying evidence.
            impact_score = (
                fan_in * 2
                + blast_radius * 3
                + fan_out
                + dependency_reach
            )

            impact[module] = {
                "fan_in": fan_in,
                "fan_out": fan_out,
                "direct_dependents": direct_dependents,
                "direct_dependencies": direct_dependencies,
                "transitive_dependents": sorted(transitive_dependents),
                "transitive_dependencies": sorted(transitive_dependencies),
                "blast_radius": blast_radius,
                "dependency_reach": dependency_reach,
                "impact_score": impact_score,
            }

        return impact

    @staticmethod
    def _reachable(graph, start):
        visited = set()
        queue = deque(graph.get(start, []))

        while queue:
            node = queue.popleft()
            if node == start or node in visited:
                continue

            visited.add(node)
            queue.extend(graph.get(node, []))

        return visited
