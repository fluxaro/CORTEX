"""Architecture Intelligence service layer."""

import math
import uuid
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analyzers.architecture.engine import ArchitectureIntelligenceEngine
from app.exceptions.custom_exceptions import RepositoryNotFoundError
from app.models.analysis import AnalysisRun
from app.models.architecture import (
    ArchitectureAnalysis,
    ArchitectureLayer,
    ArchitectureViolation,
    DependencyEdge,
    DependencyGraph,
    DependencyNode,
    DetectedPattern,
    FrameworkDetection,
    TechnologyStack,
)
from app.models.repository import Repository


class ArchitectureService:
    """Service handling Architecture Intelligence analysis and queries."""

    @staticmethod
    async def trigger_architecture_analysis(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> ArchitectureAnalysis:
        """Trigger or run synchronous Architecture Intelligence analysis for a repository."""
        repo_res = await db.execute(
            select(Repository).where(Repository.id == repository_id)
        )
        repo = repo_res.scalar_one_or_none()
        if not repo or not repo.local_path:
            raise RepositoryNotFoundError(identifier=str(repository_id))

        run_res = await db.execute(
            select(AnalysisRun)
            .where(AnalysisRun.repository_id == repository_id)
            .order_by(AnalysisRun.created_at.desc())
            .limit(1)
        )
        latest_run = run_res.scalar_one_or_none()
        if latest_run:
            run_id = latest_run.id
        else:
            new_run = AnalysisRun(repository_id=repository_id, status="COMPLETED")
            db.add(new_run)
            await db.commit()
            run_id = new_run.id

        engine = ArchitectureIntelligenceEngine(target_path=repo.local_path)
        report = engine.run()

        arch_record = ArchitectureAnalysis(
            repository_id=repository_id,
            analysis_run_id=run_id,
            arch_style=report.arch_style,
            confidence_score=report.confidence_score,
            layer_separation_score=report.layer_separation_score,
            dependency_direction_score=report.dependency_direction_score,
            pattern_confidence=report.pattern_confidence,
            project_organization_score=report.project_organization_score,
            coupling_score=report.coupling_score,
            modularity_score=report.modularity_score,
        )
        db.add(arch_record)
        await db.flush()

        for layer_res in report.layers:
            db.add(
                ArchitectureLayer(
                    architecture_analysis_id=arch_record.id,
                    repository_id=repository_id,
                    name=layer_res.name,
                    category=layer_res.category,
                    file_paths=layer_res.file_paths,
                    description=layer_res.description,
                )
            )

        for v_res in report.violations:
            db.add(
                ArchitectureViolation(
                    architecture_analysis_id=arch_record.id,
                    repository_id=repository_id,
                    violation_type=v_res.violation_type,
                    severity=v_res.severity,
                    source_path=v_res.source_path,
                    target_path=v_res.target_path,
                    description=v_res.description,
                )
            )

        for p_res in report.patterns:
            db.add(
                DetectedPattern(
                    architecture_analysis_id=arch_record.id,
                    repository_id=repository_id,
                    pattern_name=p_res.pattern_name,
                    category=p_res.category,
                    confidence_score=p_res.confidence_score,
                    location=p_res.location,
                    description=p_res.description,
                )
            )

        for fw_res in report.frameworks:
            db.add(
                FrameworkDetection(
                    architecture_analysis_id=arch_record.id,
                    repository_id=repository_id,
                    name=fw_res.name,
                    category=fw_res.category,
                    detected_version=fw_res.detected_version,
                    is_convention_compliant=fw_res.is_convention_compliant,
                    convention_findings=fw_res.convention_findings,
                )
            )

        dep_graph = DependencyGraph(
            architecture_analysis_id=arch_record.id,
            repository_id=repository_id,
            total_nodes=len(report.graph_data.nodes),
            total_edges=len(report.graph_data.edges),
        )
        db.add(dep_graph)
        await db.flush()

        for n_res in report.graph_data.nodes:
            db.add(
                DependencyNode(
                    dependency_graph_id=dep_graph.id,
                    node_identifier=n_res.node_id,
                    name=n_res.name,
                    node_type=n_res.node_type,
                    layer_name=n_res.layer_name,
                    path=n_res.path,
                )
            )

        for e_res in report.graph_data.edges:
            db.add(
                DependencyEdge(
                    dependency_graph_id=dep_graph.id,
                    source_node_id=e_res.source_id,
                    target_node_id=e_res.target_id,
                    import_type=e_res.import_type,
                    weight=e_res.weight,
                )
            )

        tech = report.tech_stack
        db.add(
            TechnologyStack(
                architecture_analysis_id=arch_record.id,
                repository_id=repository_id,
                languages=tech.languages,
                frameworks=tech.frameworks,
                orms=tech.orms,
                databases=tech.databases,
                cloud=tech.cloud,
                ci_cd=tech.ci_cd,
                package_managers=tech.package_managers,
                build_tools=tech.build_tools,
                testing_frameworks=tech.testing_frameworks,
                formatters=tech.formatters,
                linters=tech.linters,
                containers=tech.containers,
                caching=tech.caching,
                auth=tech.auth,
                api_surfaces=tech.api_surfaces,
            )
        )

        await db.commit()
        return await ArchitectureService.get_latest_architecture(db, repository_id)

    @staticmethod
    async def get_latest_architecture(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> ArchitectureAnalysis:
        """Get latest architecture intelligence report for repository."""
        query = (
            select(ArchitectureAnalysis)
            .options(
                selectinload(ArchitectureAnalysis.layers),
                selectinload(ArchitectureAnalysis.violations),
                selectinload(ArchitectureAnalysis.patterns),
                selectinload(ArchitectureAnalysis.frameworks),
                selectinload(ArchitectureAnalysis.dependency_graph),
                selectinload(ArchitectureAnalysis.technology_stack),
            )
            .where(ArchitectureAnalysis.repository_id == repository_id)
            .order_by(ArchitectureAnalysis.created_at.desc())
            .limit(1)
        )
        result = await db.execute(query)
        arch = result.scalar_one_or_none()
        if not arch:
            raise RepositoryNotFoundError(
                identifier=f"Architecture for repository {repository_id}"
            )
        return arch

    @staticmethod
    async def list_patterns(
        db: AsyncSession,
        repository_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        category: str | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        """List paginated design patterns."""
        latest_arch = await ArchitectureService.get_latest_architecture(
            db, repository_id
        )
        query = select(DetectedPattern).where(
            DetectedPattern.architecture_analysis_id == latest_arch.id
        )

        if category:
            query = query.where(
                func.lower(DetectedPattern.category) == category.lower()
            )
        if name:
            query = query.where(DetectedPattern.pattern_name.ilike(f"%{name}%"))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar_one()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        items = list((await db.execute(query)).scalars().all())

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }

    @staticmethod
    async def list_layers(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> list[ArchitectureLayer]:
        """Get architectural layers."""
        latest_arch = await ArchitectureService.get_latest_architecture(
            db, repository_id
        )
        return latest_arch.layers

    @staticmethod
    async def get_dependency_graph(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> DependencyGraph:
        """Get full module dependency graph."""
        latest_arch = await ArchitectureService.get_latest_architecture(
            db, repository_id
        )
        if not latest_arch.dependency_graph:
            raise RepositoryNotFoundError(
                identifier=f"Dependency graph for repository {repository_id}"
            )
        return latest_arch.dependency_graph

    @staticmethod
    async def list_frameworks(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> list[FrameworkDetection]:
        """List detected frameworks and convention findings."""
        latest_arch = await ArchitectureService.get_latest_architecture(
            db, repository_id
        )
        return latest_arch.frameworks

    @staticmethod
    async def get_technology_stack(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> TechnologyStack:
        """Get extracted technology stack metadata."""
        latest_arch = await ArchitectureService.get_latest_architecture(
            db, repository_id
        )
        if not latest_arch.technology_stack:
            raise RepositoryNotFoundError(
                identifier=f"Technology stack for repository {repository_id}"
            )
        return latest_arch.technology_stack
