class ArchitectureAnalyzer:

    @staticmethod
    def analyze(
        analysis,
        dependency_graph,
        module_impact
    ):

        architecture_type = (
            ArchitectureAnalyzer.detect_architecture(
                analysis
            )
        )

        entry_points = (
            ArchitectureAnalyzer.detect_entry_points(
                analysis
            )
        )

        core_modules = (
            ArchitectureAnalyzer.detect_core_modules(
                module_impact
            )
        )

        layers = (
            ArchitectureAnalyzer.detect_layers(
                analysis
            )
        )

        issues = (
            ArchitectureAnalyzer.detect_issues(
                dependency_graph,
                module_impact
            )
        )

        return {
            "architecture_type": architecture_type,
            "entry_points": entry_points,
            "core_modules": core_modules,
            "layers": layers,
            "issues": issues
        }

    @staticmethod
    def detect_architecture(analysis):

        files = [
            file_data["file"]
            .replace("\\", "/")
            .lower()
            for file_data in analysis
        ]

        has_presentation = any(
            "/api/" in file
            or "/routes/" in file
            or "/controllers/" in file
            for file in files
        )

        has_application = any(
            "/services/" in file
            or "/usecases/" in file
            for file in files
        )

        has_domain = any(
            "/models/" in file
            or "/entities/" in file
            or "/domain/" in file
            for file in files
        )

        has_infrastructure = any(
            "/database/" in file
            or "/repositories/" in file
            or "/infrastructure/" in file
            for file in files
        )

        # Layered Architecture
        if (
            has_presentation
            and has_application
            and has_domain
        ):
            return "Layered Architecture"

        # Modular Architecture
        if has_domain or has_application:
            return "Modular Architecture"

        return "Unclassified"

    @staticmethod
    def detect_entry_points(analysis):

        entry_points = []

        entry_point_names = {
            "main.py",
            "app.py",
            "server.py",
            "run.py",
            "manage.py",
            "wsgi.py",
            "asgi.py"
        }

        for file_data in analysis:

            file_path = (
                file_data["file"]
                .replace("\\", "/")
            )

            file_name = file_path.split("/")[-1]

            if file_name in entry_point_names:

                entry_points.append(
                    file_data["file"]
                )

        return entry_points

    @staticmethod
    def detect_core_modules(module_impact):

        core_modules = []

        for module, impact in module_impact.items():

            fan_in = impact.get(
                "fan_in",
                0
            )

            fan_out = impact.get(
                "fan_out",
                0
            )

            importance_score = fan_in + fan_out

            # Module must have some meaningful
            # connection to the project
            if importance_score >= 2:

                core_modules.append(
                    {
                        "module": module,
                        "fan_in": fan_in,
                        "fan_out": fan_out,
                        "importance_score": importance_score
                    }
                )

        core_modules.sort(
            key=lambda item: (
                item["importance_score"],
                item["fan_in"]
            ),
            reverse=True
        )

        return core_modules

    @staticmethod
    def detect_layers(analysis):

        layers = {
            "presentation": [],
            "application": [],
            "domain": [],
            "infrastructure": []
        }

        for file_data in analysis:

            file_path = (
                file_data["file"]
                .replace("\\", "/")
                .lower()
            )

            # Presentation Layer
            if (
                "/api/" in file_path
                or "/routes/" in file_path
                or "/controllers/" in file_path
                or file_path.startswith("api/")
                or file_path.startswith("routes/")
            ):

                layers["presentation"].append(
                    file_data["file"]
                )

            # Application Layer
            elif (
                "/services/" in file_path
                or "/usecases/" in file_path
                or "/application/" in file_path
                or file_path.startswith("services/")
            ):

                layers["application"].append(
                    file_data["file"]
                )

            # Domain Layer
            elif (
                "/models/" in file_path
                or "/entities/" in file_path
                or "/domain/" in file_path
                or "/schemas/" in file_path
                or file_path.startswith("models/")
            ):

                layers["domain"].append(
                    file_data["file"]
                )

            # Infrastructure Layer
            elif (
                "/database/" in file_path
                or "/repositories/" in file_path
                or "/infrastructure/" in file_path
                or "/storage/" in file_path
                or file_path.startswith("database/")
            ):

                layers["infrastructure"].append(
                    file_data["file"]
                )

        return layers

    @staticmethod
    def detect_issues(
        dependency_graph,
        module_impact
    ):

        issues = []

        for module, dependencies in dependency_graph.items():

            if len(dependencies) >= 5:

                issues.append(
                    {
                        "type": "High Coupling",
                        "severity": "Medium",
                        "module": module,
                        "message": (
                            f"Module '{module}' depends on "
                            f"{len(dependencies)} modules."
                        )
                    }
                )

        for module, impact in module_impact.items():

            fan_in = impact.get(
                "fan_in",
                0
            )

            if fan_in >= 5:

                issues.append(
                    {
                        "type": "High Dependency",
                        "severity": "Medium",
                        "module": module,
                        "message": (
                            f"Module '{module}' is depended on "
                            f"by {fan_in} modules."
                        )
                    }
                )

        for module, impact in module_impact.items():

            fan_in = impact.get(
                "fan_in",
                0
            )

            fan_out = impact.get(
                "fan_out",
                0
            )

            if fan_in == 0 and fan_out == 0:

                issues.append(
                    {
                        "type": "Orphan Module",
                        "severity": "Low",
                        "module": module,
                        "message": (
                            f"Module '{module}' has no "
                            "internal dependencies or dependents."
                        )
                    }
                )

        return issues