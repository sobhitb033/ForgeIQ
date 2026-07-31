class GraphUtils:

    @staticmethod
    def get_all_nodes(graph: dict):

        nodes = set()

        for module, dependencies in graph.items():

            nodes.add(module)

            for dependency in dependencies:
                nodes.add(dependency)

        return nodes

    @staticmethod
    def get_incoming_edges(graph: dict):

        incoming = {}

        for node in GraphUtils.get_all_nodes(graph):
            incoming[node] = 0

        for dependencies in graph.values():

            for dependency in dependencies:

                if dependency in incoming:
                    incoming[dependency] += 1

        return incoming