"""Main Architecture Intelligence Engine orchestrator."""

import os

from app.analyzers.architecture.detectors.arch_detector import ArchDetector
from app.analyzers.architecture.detectors.config_tech_detector import ConfigTechDetector
from app.analyzers.architecture.detectors.dependency_graph import DependencyGraphBuilder
from app.analyzers.architecture.detectors.framework_detector import FrameworkDetector
from app.analyzers.architecture.detectors.layer_detector import LayerDetector
from app.analyzers.architecture.detectors.pattern_detector import PatternDetector
from app.analyzers.architecture.models import ArchitectureAnalysisResult
from app.analyzers.base.engine import StaticAnalysisEngine
from app.analyzers.detector import RepositoryFileDetector


class ArchitectureIntelligenceEngine:
    """Orchestrates architecture, framework, pattern, and dependency analysis for a repository."""

    def __init__(self, target_path: str) -> None:
        self.target_path = os.path.abspath(target_path)

    def run(self) -> ArchitectureAnalysisResult:
        """Run complete Architecture Intelligence analysis pipeline."""
        if not os.path.exists(self.target_path) or not os.path.isdir(self.target_path):
            raise ValueError(
                f"Target repository path '{self.target_path}' does not exist or is not a directory."
            )

        # 1. Discover files & run static code analysis
        discovered = RepositoryFileDetector.discover(self.target_path)
        static_engine = StaticAnalysisEngine(target_path=self.target_path)
        static_report = static_engine.run()

        # 2. Layer Detection
        layers = LayerDetector.detect_layers(discovered.all_files)

        # 3. Architecture Style Detection
        arch_style, confidence = ArchDetector.detect_architecture_style(
            layers=layers, all_file_paths=discovered.all_files
        )

        # 4. Pattern Detection
        patterns = PatternDetector.detect_patterns(static_report.file_results)

        # 5. Framework Detection & Conventions
        frameworks = FrameworkDetector.detect_frameworks(static_report.file_results)

        # 6. Dependency Graph & Rule Violations & Architectural Scores
        graph_data, violations, scores = DependencyGraphBuilder.build_graph(
            static_report.file_results
        )

        # 7. Technology Stack & API Surface Extraction
        tech_stack = ConfigTechDetector.analyze_tech_stack(
            all_file_paths=discovered.all_files,
            file_results=static_report.file_results,
        )

        return ArchitectureAnalysisResult(
            arch_style=arch_style,
            confidence_score=confidence,
            layer_separation_score=scores["layer_separation_score"],
            dependency_direction_score=scores["dependency_direction_score"],
            pattern_confidence=scores["pattern_confidence"],
            project_organization_score=scores["project_organization_score"],
            coupling_score=scores["coupling_score"],
            modularity_score=scores["modularity_score"],
            layers=layers,
            patterns=patterns,
            frameworks=frameworks,
            violations=violations,
            tech_stack=tech_stack,
            graph_data=graph_data,
        )
