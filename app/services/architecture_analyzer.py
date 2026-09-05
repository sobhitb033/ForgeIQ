class ArchitectureAnalyzer:

    @staticmethod
    def analyze(
        analysis,
        dependency_graph,
        module_impact
    ):

        architecture_type = ArchitectureAnalyzer.detect_architecture(analysis)
        entry_points = ArchitectureAnalyzer.detect_entry_points(analysis)
        core_modules = ArchitectureAnalyzer.detect_core_modules(module_impact)
        layers = ArchitectureAnalyzer.detect_layers(analysis)
        issues = ArchitectureAnalyzer.detect_issues(
            dependency_graph,
            module_impact
        )
        impact_hotspots = ArchitectureAnalyzer.detect_impact_hotspots(
            module_impact
        )

        return {
            "architecture_type": architecture_type,
            "entry_points": entry_points,
            "core_modules": core_modules,
            "layers": layers,
            "issues": issues,
            "impact_hotspots": impact_hotspots,
        }

    @staticmethod
    def detect_architecture(analysis):
        files = [
            file_data["file"].replace("\\", "/").lower()
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

        if has_presentation and has_application and has_domain:
            return "Layered Architecture"

        if has_domain or has_application:
            return "Modular Architecture"

        return "Unclassified"

    @staticmethod
    def detect_entry_points(analysis):
        entry_points = []
        entry_point_names = {
            "main.py", "app.py", "server.py", "run.py",
            "manage.py", "wsgi.py", "asgi.py"
        }

        for file_data in analysis:
            file_path = file_data["file"].replace("\\", "/")
            file_name = file_path.split("/")[-1]
            if file_name in entry_point_names:
                entry_points.append(file_data["file"])

        return entry_points

    @staticmethod
    def detect_core_modules(module_impact):
        core_modules = []

        for module, impact in module_impact.items():
            fan_in = impact.get("fan_in", 0)
            fan_out = impact.get("fan_out", 0)
            blast_radius = impact.get("blast_radius", 0)
            importance_score = (
                fan_in
                + fan_out
                + blast_radius
            )

            if importance_score >= 2:
                core_modules.append({
                    "module": module,
                    "fan_in": fan_in,
                    "fan_out": fan_out,
                    "blast_radius": blast_radius,
                    "importance_score": importance_score,
                })

        core_modules.sort(
            key=lambda item: (
                item["importance_score"],
                item["blast_radius"],
                item["fan_in"],
            ),
            reverse=True,
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
            file_path = file_data["file"].replace("\\", "/").lower()

            if (
                "/api/" in file_path
                or "/routes/" in file_path
                or "/controllers/" in file_path
                or file_path.startswith("api/")
                or file_path.startswith("routes/")
            ):
                layers["presentation"].append(file_data["file"])

            elif (
                "/services/" in file_path
                or "/usecases/" in file_path
                or "/application/" in file_path
                or file_path.startswith("services/")
            ):
                layers["application"].append(file_data["file"])

            elif (
                "/models/" in file_path
                or "/entities/" in file_path
                or "/domain/" in file_path
                or "/schemas/" in file_path
                or file_path.startswith("models/")
            ):
                layers["domain"].append(file_data["file"])

            elif (
                "/database/" in file_path
                or "/repositories/" in file_path
                or "/infrastructure/" in file_path
                or "/storage/" in file_path
                or file_path.startswith("database/")
            ):
                layers["infrastructure"].append(file_data["file"])

        return layers

    @staticmethod
    def detect_issues(dependency_graph, module_impact):
        issues = []

        for module, dependencies in dependency_graph.items():
            if len(dependencies) >= 5:
                issues.append({
                    "type": "High Coupling",
                    "severity": "Medium",
                    "module": module,
                    "message": (
                        f"Module '{module}' depends on "
                        f"{len(dependencies)} modules."
                    )
                })

        for module, impact in module_impact.items():
            fan_in = impact.get("fan_in", 0)
            if fan_in >= 5:
                issues.append({
                    "type": "High Dependency",
                    "severity": "Medium",
                    "module": module,
                    "message": (
                        f"Module '{module}' is depended on by "
                        f"{fan_in} modules."
                    )
                })

        for module, impact in module_impact.items():
            fan_in = impact.get("fan_in", 0)
            fan_out = impact.get("fan_out", 0)
            if fan_in == 0 and fan_out == 0:
                issues.append({
                    "type": "Orphan Module",
                    "severity": "Low",
                    "module": module,
                    "message": (
                        f"Module '{module}' has no internal "
                        "dependencies or dependents."
                    )
                })

        return issues

    @staticmethod
    def detect_impact_hotspots(module_impact):
        """Identify meaningful change-impact hotspots.

        A large transitive dependency count alone is not enough to call a
        module an architectural hotspot. Entry points, configuration modules,
        database primitives, and other low fan-in infrastructure can naturally
        sit on many dependency paths without being shared application
        boundaries. We therefore require meaningful fan-in before surfacing a
        module as an impact hotspot.
        """
        hotspots = []

        for module, impact in module_impact.items():
            fan_in = impact.get("fan_in", 0)
            fan_out = impact.get("fan_out", 0)
            blast_radius = impact.get("blast_radius", 0)
            impact_score = impact.get("impact_score", 0)

            # Fan-in represents the number of modules that directly depend on
            # this module. It is the strongest signal that changing this
            # module can affect other parts of the system.
            #
            # Do not label low fan-in modules as architectural hotspots merely
            # because a long dependency chain passes through them.
            if fan_in < 3:
                continue

            if fan_in >= 5 and blast_radius >= 8:
                severity = "Critical"
            elif fan_in >= 5 or (fan_in >= 3 and blast_radius >= 5):
                severity = "High"
            elif fan_in >= 3 and blast_radius >= 3:
                severity = "Medium"
            else:
                continue

            hotspots.append({
                "module": module,
                "severity": severity,
                "fan_in": fan_in,
                "fan_out": fan_out,
                "blast_radius": blast_radius,
                "dependency_reach": impact.get("dependency_reach", 0),
                "impact_score": impact_score,
                "affected_modules": impact.get(
                    "transitive_dependents", []
                ),
            })

        hotspots.sort(
            key=lambda item: (
                {"Critical": 1, "High": 2, "Medium": 3}.get(
                    item["severity"], 4
                ),
                -item["blast_radius"],
                -item["fan_in"],
                -item["impact_score"],
            )
        )

        return hotspots
