# Database Schema Reference

ProjectIQ uses **PostgreSQL 15** with **SQLAlchemy 2.x** async ORM and **Alembic** for migrations.

The database schema spans 8 migration files (001–007) and contains **44+ tables** organized across 6 functional areas.

---

## Schema Areas

### 1. Repository Acquisition (Migration 001)
| Table | Purpose |
| :--- | :--- |
| `repositories` | Core repository metadata, URL, provider, clone path, status |
| `repository_file_indices` | File tree index with language tags, size, and line counts |
| `analysis_runs` | Individual analysis execution records with status and timestamps |

### 2. Static Analysis (Migration 002)
| Table | Purpose |
| :--- | :--- |
| `repository_metrics` | Aggregated LOC, complexity, maintainability, duplication |
| `file_metrics` | Per-file complexity, MI score, comment ratio |
| `function_metrics` | Per-function cyclomatic complexity and parameter count |
| `class_metrics` | Per-class method count, inheritance depth |
| `duplicate_groups` | Cross-file code duplication groups |
| `duplicate_files` | Files participating in duplication groups |
| `code_smells` | Detected code quality issues with severity |

### 3. Architecture Intelligence (Migration 003)
| Table | Purpose |
| :--- | :--- |
| `architecture_analyses` | Overall architecture style, score, modularity |
| `architecture_layers` | Detected architectural layers and their files |
| `architecture_violations` | Layer boundary violations and cross-cutting issues |
| `detected_patterns` | Design patterns found with confidence scores and locations |
| `dependency_graphs` | Repository-level dependency graph metadata |
| `dependency_nodes` | Module nodes with coupling metrics |
| `dependency_edges` | Module-to-module dependency relationships |
| `framework_detections` | Detected frameworks and convention compliance |
| `technology_stacks` | Languages, databases, ORMs, CI/CD tools |

### 4. Security Intelligence (Migration 004)
| Table | Purpose |
| :--- | :--- |
| `security_analyses` | Overall SAST scan metadata and score |
| `security_findings` | Individual SAST findings with severity and file locations |
| `secret_findings` | Committed secrets with type, entropy, and masked values |
| `dependency_findings` | Vulnerable dependencies with CVE IDs and CVSS scores |
| `configuration_findings` | Insecure infrastructure config findings |
| `authentication_findings` | Auth mechanism weaknesses |
| `authorization_findings` | Missing RBAC/authz coverage findings |
| `security_rules` | Library of static security detection rules |
| `security_references` | CVE and OWASP reference links |
| `security_summaries` | Aggregated security posture summary |

### 5. Maintainability Intelligence (Migration 005)
| Table | Purpose |
| :--- | :--- |
| `documentation_analyses` | README completeness and section scores |
| `documentation_sections` | Individual documentation section details |
| `readme_analyses` | Parsed README badges, examples, screenshots |
| `testing_analyses` | Test runner detection, test count, test type breakdown |
| `git_history_analyses` | Commit count, contributor count, velocity |
| `commit_analyses` | Conventional Commit %, quality score |
| `release_analyses` | Release count, SemVer compliance |
| `community_analyses` | CONTRIBUTING, CODE_OF_CONDUCT, SECURITY presence |
| `ci_analyses` | CI providers, jobs breakdown by category |
| `license_analyses` | License type, OSI approval, CHANGELOG |
| `maintainability_metrics` | Aggregated documentation, testing, CI, Git scores |
| `repository_healths` | Repository health composite score |

### 6. Repository IQ & AI (Migration 006)
| Table | Purpose |
| :--- | :--- |
| `repository_iqs` | Overall IQ score, maturity level, subsystem scores |
| `repository_summaries` | AI-generated summaries (executive, technical, recruiter) |
| `engineering_insights` | Identified strengths and weaknesses |
| `technical_debts` | Debt hours, days, category breakdown, line items |
| `improvement_recommendations` | Prioritized actionable recommendations |
| `executive_summaries` | Formatted executive report |
| `technical_summaries` | Formatted technical report |
| `benchmark_results` | Industry percentile rankings |
| `ai_generations` | AI prompt execution audit log |
| `prompt_templates` | Versioned AI prompt templates |

### 7. Enterprise Platform (Migration 007)
| Table | Purpose |
| :--- | :--- |
| `users` | User accounts with hashed passwords |
| `user_preferences` | User notification and UI preferences |
| `organizations` | Enterprise organization boundaries |
| `workspaces` | Team collaboration workspaces |
| `memberships` | User-workspace role assignments |
| `invitations` | Pending workspace membership invitations |
| `api_tokens` | User API tokens for CI/CD automation |
| `repository_syncs` | Git platform sync metadata |
| `webhooks` | Registered webhook configurations |
| `notifications` | In-app user notifications |
| `audit_logs` | Immutable compliance audit event log |
| `scan_histories` | Scheduled and manual scan execution records |
| `trend_metrics` | Time-series metric snapshots per repository |
| `repository_comparisons` | Saved multi-repository comparison views |

---

## Key Relationships

```
repositories ──< analysis_runs ──< repository_metrics
             ──< repository_file_indices
             ──< architecture_analyses ──< detected_patterns
             ──< security_analyses ──< secret_findings
             ──< maintainability_metrics ──< testing_analyses
             ──< repository_iqs ──< repository_summaries
             ──< trend_metrics
             ──< scan_histories

workspaces ──< memberships >── users
           ──< invitations
           ──< audit_logs

organizations ──< workspaces
```

---

## Migrations

| Migration | Description |
| :--- | :--- |
| `001_create_initial_tables.py` | Repositories, file index, analysis runs |
| `002_create_static_analysis_tables.py` | Metrics, functions, classes, smells, duplicates |
| `003_create_architecture_tables.py` | Architecture, patterns, dependency graphs |
| `004_create_security_tables.py` | SAST findings, secrets, CVEs |
| `005_create_maintainability_tables.py` | Docs, testing, CI, Git, community |
| `006_create_iq_tables.py` | IQ scores, summaries, debt, benchmarks |
| `007_create_enterprise_tables.py` | Users, orgs, workspaces, auth, webhooks |

Run all migrations with:
```bash
alembic -c backend/alembic.ini upgrade head
```
