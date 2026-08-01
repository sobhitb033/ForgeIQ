class CycleDetector:

    @staticmethod
    def find_cycles(graph: dict):

        visited = set()
        stack = []
        cycles = []

        def dfs(node):

            if node in stack:

                cycle = stack[stack.index(node):] + [node]

                if cycle not in cycles:
                    cycles.append(cycle)

                return

            if node in visited:
                return

            visited.add(node)
            stack.append(node)

            for neighbor in graph.get(node, []):

                if neighbor in graph:
                    dfs(neighbor)

            stack.pop()

        for node in graph:

            if node not in visited:
                dfs(node)

        return cycles