class DependencyGraphBuilder:

    @staticmethod
    def build(file_analysis: list[dict]):

        graph = {}

        for file in file_analysis:

            path = file["file"].replace("\\", "/")

            if path.startswith("Sample/"):
                path = path[len("Sample/"):]

            module = path.replace("/", ".").replace(".py", "")

            graph[module] = file["dependencies"]["internal"]

        return graph