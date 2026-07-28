"""Celery background task for running Architecture Intelligence analysis."""

import asyncio
import logging
import uuid

from sqlalchemy import select

from app.analyzers.architecture.engine import ArchitectureIntelligenceEngine
from app.database.session import AsyncSessionLocal
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
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


async def _async_run_architecture_analysis(  # noqa: C901
    repository_id_str: str, analysis_run_id_str: str | None = None
) -> None:
    """Async execution of Architecture Intelligence Analysis."""
    repo_uuid = uuid.UUID(repository_id_str)

    async with AsyncSessionLocal() as session:
        repo_res = await session.execute(
            select(Repository).where(Repository.id == repo_uuid)
        )
        repo = repo_res.scalar_one_or_none()

        if not repo or not repo.local_path:
            logger.error(
                f"Task error: Repository {repository_id_str} not found or local storage missing."
            )
            return

        run_uuid = uuid.UUID(analysis_run_id_str) if analysis_run_id_str else None
        if not run_uuid:
            run_res = await session.execute(
                select(AnalysisRun)
                .where(AnalysisRun.repository_id == repo_uuid)
                .order_by(AnalysisRun.created_at.desc())
                .limit(1)
            )
            latest_run = run_res.scalar_one_or_none()
            if latest_run:
                run_uuid = latest_run.id
            else:
                new_run = AnalysisRun(repository_id=repo_uuid, status="COMPLETED")
                session.add(new_run)
                await session.commit()
                run_uuid = new_run.id

        logger.info(
            f"Architecture analysis started for repository {repo.full_name} (Run ID: {run_uuid})"
        )

        try:
            logger.info("Load Static Analysis")
            engine = ArchitectureIntelligenceEngine(target_path=repo.local_path)

            logger.info("Detect Architecture")
            logger.info("Detect Frameworks")
            logger.info("Detect Patterns")
            logger.info("Build Dependency Graph")

            report = engine.run()

            # Delete pre-existing architecture analysis for this run if any
            existing_arch = await session.execute(
                select(ArchitectureAnalysis).where(
                    ArchitectureAnalysis.analysis_run_id == run_uuid
                )
            )
            old_arch = existing_arch.scalar_one_or_none()
            if old_arch:
                await session.delete(old_arch)
                await session.flush()

            logger.info("Store Results")
            arch_record = ArchitectureAnalysis(
                repository_id=repo.id,
                analysis_run_id=run_uuid,
                arch_style=report.arch_style,
                confidence_score=report.confidence_score,
                layer_separation_score=report.layer_separation_score,
                dependency_direction_score=report.dependency_direction_score,
                pattern_confidence=report.pattern_confidence,
                project_organization_score=report.project_organization_score,
                coupling_score=report.coupling_score,
                modularity_score=report.modularity_score,
            )
            session.add(arch_record)
            await session.flush()

            # Store Layers
            for layer_res in report.layers:
                session.add(
                    ArchitectureLayer(
                        architecture_analysis_id=arch_record.id,
                        repository_id=repo.id,
                        name=layer_res.name,
                        category=layer_res.category,
                        file_paths=layer_res.file_paths,
                        description=layer_res.description,
                    )
                )

            # Store Violations
            for v_res in report.violations:
                session.add(
                    ArchitectureViolation(
                        architecture_analysis_id=arch_record.id,
                        repository_id=repo.id,
                        violation_type=v_res.violation_type,
                        severity=v_res.severity,
                        source_path=v_res.source_path,
                        target_path=v_res.target_path,
                        description=v_res.description,
                    )
                )

            # Store Patterns
            for p_res in report.patterns:
                session.add(
                    DetectedPattern(
                        architecture_analysis_id=arch_record.id,
                        repository_id=repo.id,
                        pattern_name=p_res.pattern_name,
                        category=p_res.category,
                        confidence_score=p_res.confidence_score,
                        location=p_res.location,
                        description=p_res.description,
                    )
                )

            # Store Frameworks
            for fw_res in report.frameworks:
                session.add(
                    FrameworkDetection(
                        architecture_analysis_id=arch_record.id,
                        repository_id=repo.id,
                        name=fw_res.name,
                        category=fw_res.category,
                        detected_version=fw_res.detected_version,
                        is_convention_compliant=fw_res.is_convention_compliant,
                        convention_findings=fw_res.convention_findings,
                    )
                )

            # Store Dependency Graph
            dep_graph = DependencyGraph(
                architecture_analysis_id=arch_record.id,
                repository_id=repo.id,
                total_nodes=len(report.graph_data.nodes),
                total_edges=len(report.graph_data.edges),
            )
            session.add(dep_graph)
            await session.flush()

            for n_res in report.graph_data.nodes:
                session.add(
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
                session.add(
                    DependencyEdge(
                        dependency_graph_id=dep_graph.id,
                        source_node_id=e_res.source_id,
                        target_node_id=e_res.target_id,
                        import_type=e_res.import_type,
                        weight=e_res.weight,
                    )
                )

            # Store Tech Stack
            tech = report.tech_stack
            session.add(
                TechnologyStack(
                    architecture_analysis_id=arch_record.id,
                    repository_id=repo.id,
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

            await session.commit()
            logger.info("Persistence complete")
            logger.info(f"Patterns detected: {len(report.patterns)}")
            logger.info(f"Framework detected: {[f.name for f in report.frameworks]}")
            logger.info(f"Architecture identified: {report.arch_style}")
            logger.info(f"Violations detected: {len(report.violations)}")
            logger.info(
                f"Dependency graph created with {len(report.graph_data.nodes)} nodes and {len(report.graph_data.edges)} edges"
            )
            logger.info(f"Analysis finished for repository {repo.full_name}")

            from app.tasks.security_tasks import security_analysis_task

            try:
                security_analysis_task.delay(str(repo.id), str(run_uuid))
            except Exception:
                pass

        except Exception as exc:
            logger.exception(
                f"Architecture analysis failed for repository {repo.full_name}: {exc}"
            )


@celery_app.task(name="app.tasks.architecture_tasks.architecture_analysis_task")
def architecture_analysis_task(
    repository_id: str, analysis_run_id: str | None = None
) -> None:
    """Celery background task for running Architecture Intelligence Engine."""
    asyncio.run(_async_run_architecture_analysis(repository_id, analysis_run_id))
