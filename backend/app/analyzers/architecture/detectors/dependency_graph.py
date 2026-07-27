"""Dependency graph generation and architecture rule validation."""

import os

from app.analyzers.architecture.models import (
    DependencyEdgeResult,
    DependencyGraphData,
    DependencyNodeResult,
    ViolationResult,
)
from app.analyzers.shared.models import FileAnalysisResult


class DependencyGraphBuilder:
    """Generates module dependency graph and validates architectural dependency rules."""

    @classmethod
    def build_graph(  # noqa: C901
        cls,
        file_results: list[FileAnalysisResult],
    ) -> tuple[DependencyGraphData, list[ViolationResult], dict[str, float]]:
        """Generate dependency graph, detect violations, and calculate architecture scores."""
        nodes_dict: dict[str, DependencyNodeResult] = {}
        edges_list: list[DependencyEdgeResult] = []
        violations: list[ViolationResult] = []

        path_to_node: dict[str, str] = {}

        # 1. Build Internal Nodes
        for f in file_results:
            node_id = f.path
            path_to_node[f.path] = node_id

            # Determine Layer
            layer_name = "Domain"
            p_lower = f.path.lower()
            if any(
                k in p_lower
                for k in ("controllers", "routes", "api", "endpoints", "views", "pages")
            ):
                layer_name = "Presentation"
            elif any(
                k in p_lower for k in ("services", "use_cases", "commands", "queries")
            ):
                layer_name = "Application"
            elif any(
                k in p_lower
                for k in ("infrastructure", "repositories", "database", "external")
            ):
                layer_name = "Infrastructure"
            elif any(k in p_lower for k in ("utils", "helpers", "shared", "common")):
                layer_name = "Utilities"

            nodes_dict[node_id] = DependencyNodeResult(
                node_id=node_id,
                name=os.path.basename(f.path),
                node_type="internal",
                layer_name=layer_name,
                path=f.path,
            )

        # Track imports for circular dependency detection
        adjacency: dict[str, set[str]] = {n_id: set() for n_id in nodes_dict}

        # 2. Build Edges and External Nodes
        for f in file_results:
            source_id = f.path
            source_node = nodes_dict[source_id]

            for imp in f.imports:
                target_path = cls._resolve_import(imp, file_results)
                if target_path:
                    target_id = target_path
                    edges_list.append(
                        DependencyEdgeResult(
                            source_id=source_id,
                            target_id=target_id,
                            import_type="internal",
                        )
                    )
                    adjacency[source_id].add(target_id)

                    target_node = nodes_dict[target_id]

                    # Validate Dependency Direction Rules
                    if (
                        source_node.layer_name == "Presentation"
                        and target_node.layer_name == "Infrastructure"
                    ):
                        violations.append(
                            ViolationResult(
                                violation_type="Cross-Layer Violation",
                                severity="HIGH",
                                source_path=source_id,
                                target_path=target_id,
                                description="Presentation layer directly imports Infrastructure layer without going through Application layer.",
                            )
                        )
                    elif (
                        source_node.layer_name == "Infrastructure"
                        and target_node.layer_name == "Presentation"
                    ):
                        violations.append(
                            ViolationResult(
                                violation_type="Improper Dependency Direction",
                                severity="HIGH",
                                source_path=source_id,
                                target_path=target_id,
                                description="Infrastructure layer depends on Presentation layer (Architecture Inversion).",
                            )
                        )
                else:
                    # External Dependency
                    ext_id = f"ext:{imp}"
                    if ext_id not in nodes_dict:
                        nodes_dict[ext_id] = DependencyNodeResult(
                            node_id=ext_id,
                            name=imp,
                            node_type="external",
                            layer_name="External",
                        )
                    edges_list.append(
                        DependencyEdgeResult(
                            source_id=source_id,
                            target_id=ext_id,
                            import_type="external",
                        )
                    )

        # 3. Detect Circular Dependencies
        circular_pairs = cls._find_circular_dependencies(adjacency)
        for src, tgt in circular_pairs:
            violations.append(
                ViolationResult(
                    violation_type="Circular Dependency",
                    severity="CRITICAL",
                    source_path=src,
                    target_path=tgt,
                    description=f"Circular import loop detected between '{src}' and '{tgt}'.",
                )
            )

        # 4. Calculate Raw Scores
        num_violations = len(violations)
        layer_sep_score = max(50.0, 100.0 - (num_violations * 10.0))
        dep_dir_score = max(50.0, 100.0 - (len(circular_pairs) * 15.0))
        coupling_score = max(
            40.0, 90.0 - (len(edges_list) / max(1, len(file_results)) * 2.0)
        )
        modularity_score = round(
            (layer_sep_score + dep_dir_score + coupling_score) / 3.0, 2
        )

        scores = {
            "layer_separation_score": round(layer_sep_score, 2),
            "dependency_direction_score": round(dep_dir_score, 2),
            "coupling_score": round(coupling_score, 2),
            "modularity_score": modularity_score,
            "project_organization_score": 85.0,
            "pattern_confidence": 80.0,
        }

        graph_data = DependencyGraphData(
            nodes=list(nodes_dict.values()),
            edges=edges_list,
        )

        return graph_data, violations, scores

    @staticmethod
    def _resolve_import(
        imp_name: str, file_results: list[FileAnalysisResult]
    ) -> str | None:
        clean_imp = imp_name.replace(".", "/").lower()
        for f in file_results:
            p_lower = f.path.lower()
            if (
                clean_imp in p_lower
                or p_lower.endswith(clean_imp + ".py")
                or p_lower.endswith(clean_imp + ".ts")
            ):
                return f.path
        return None

    @staticmethod
    def _find_circular_dependencies(adj: dict[str, set[str]]) -> list[tuple[str, str]]:
        circular: list[tuple[str, str]] = []
        visited: set[tuple[str, str]] = set()

        for u, neighbors in adj.items():
            for v in neighbors:
                if u in adj.get(v, set()):
                    pair = (min(u, v), max(u, v))
                    if pair not in visited:
                        visited.add(pair)
                        circular.append((u, v))
        return circular
