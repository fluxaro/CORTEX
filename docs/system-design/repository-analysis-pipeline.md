# System Design — Repository Analysis Pipeline

## Pipeline Overview

The repository analysis pipeline is a multi-stage, asynchronous workflow executed entirely by Celery workers. Each stage writes its results to PostgreSQL before the next stage begins.

---

## Stage-by-Stage Design

### Stage 1: Repository Acquisition
**Trigger:** `POST /api/v1/repositories { "url": "..." }`

```
URL Validation
     │
     ▼
GitHub/GitLab/Bitbucket API
  → fetch metadata (name, owner, stars, description, default_branch)
     │
     ▼
INSERT repositories (status=PENDING)
     │
     ▼
Dispatch clone_and_index_task to Celery
```

### Stage 2: Clone & Index
**Worker:** `clone_and_index_task`

```
git clone <url> /tmp/cortex/clones/<repo_id>
     │
     ▼
Walk file tree:
  → detect file language by extension
  → count lines of code
  → record file size and path
  → INSERT repository_file_indices
     │
     ▼
UPDATE repositories (status=INDEXING → ANALYZING)
     │
     ▼
Dispatch static_analysis_task
```

### Stage 3: Static Code Analysis
**Worker:** `static_analysis_task`

```
For each indexed file:
  ├─ Python → ast.parse() → functions, classes, complexity
  ├─ TypeScript → regex/pattern AST → functions, complexity
  ├─ JavaScript → similar to TS
  ├─ Go → function signature parsing
  ├─ Java → class and method parsing
  └─ Rust → fn/impl block parsing
     │
     ▼
Aggregate per-file metrics → repository-level summary
Cross-file duplication detection (rolling hash window)
Code smell detection (long function, god class, etc.)
     │
     ▼
INSERT file_metrics, function_metrics, class_metrics,
       duplicate_groups, code_smells, repository_metrics
     │
     ▼
Dispatch architecture_task, security_task, maintainability_task (parallel)
```

### Stage 4: Parallel Analysis
**Workers (run concurrently):**

```
architecture_analysis_task        security_analysis_task        maintainability_task
         │                               │                              │
Layer detection               Secret pattern scanning         README section parsing
Design pattern matching        SAST rule matching             Test file counting
Dependency graph building      Config file audit              CI/CD detection
Framework convention check     Dependency CVE lookup          Git log extraction
         │                               │                              │
INSERT architecture_*          INSERT security_*              INSERT maintainability_*
         │                               │                              │
         └──────────────────────────────┼──────────────────────────────┘
                                        │
                                 All complete → dispatch iq_engine_task
```

### Stage 5: IQ Engine
**Worker:** `iq_engine_task`

```
Collect all subsystem results from DB
     │
     ▼
Apply weighted scoring formula:
  IQ = Σ (subsystem_score × weight) / Σ weights
  Weights: static(15%) · arch(20%) · sec(25%) · docs(10%)
           testing(15%) · ci(5%) · git(5%) · community(5%)
     │
     ▼
Maturity classification
Technical debt estimation
Industry benchmark percentile calculation
AI prompt generation (if AI provider configured)
     │
     ▼
INSERT repository_iqs, repository_summaries, technical_debts,
       improvement_recommendations, benchmark_results
     │
     ▼
UPDATE repositories (status=COMPLETE)
```

---

## Error Handling

Each stage wraps its logic in try/except. On failure:
1. `UPDATE repositories SET status='FAILED', error_message=...`
2. Celery task is marked FAILURE
3. The failure is logged with the Request ID correlation

Retry policy: 3 automatic retries with 60-second backoff for transient network errors.
