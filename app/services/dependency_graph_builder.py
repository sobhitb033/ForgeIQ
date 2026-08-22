class DependencyGraphBuilder:

    @staticmethod
    def build(file_analysis: list[dict]):

        graph = {}

        for file in file_analysis:

            path = file["file"].replace("\\", "/")

            # Remove .py extension
            if path.endswith(".py"):
                path = path[:-3]

            # Convert file path to Python module format
            module = path.replace("/", ".")

            graph[module] = file["dependencies"]["internal"]

        return graph