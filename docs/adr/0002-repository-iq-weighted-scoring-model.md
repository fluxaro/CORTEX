# ADR 0002: Repository IQ Weighted Scoring Model

## Context
Aggregating disparate software engineering metrics (cyclomatic complexity, secret findings, test coverage, documentation completeness) into a single actionable score (0-100) requires a transparent and configurable weighting matrix.

## Decision
Cortex implements `IQScorer` using configurable subsystem weights across 8 engineering dimensions:
1. Static Analysis & Complexity
2. Architecture & Modularity
3. Security Intelligence (SAST)
4. Documentation Structure
5. Testing Maturity
6. CI/CD Automation
7. Git Practices & Velocity
8. Open Source Community Health

## Consequences
- **Repeatability**: Identical codebase inputs always yield identical Repository IQ scores.
- **Customizability**: Enterprises can adjust subsystem weights based on internal compliance targets.
