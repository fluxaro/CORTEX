# 11. CORTEX Rebrand & 5-Category Letter Grade System with Guardrail Caps

* Status: **Accepted** (Supersedes ADR 0002: Repository IQ Weighted Scoring Model)
* Date: 2026-08-18

## Context and Problem Statement

The legacy 0–100 Repository IQ Score aggregated 8 individual subsystem metrics directly into a single floating-point number. While granular, numeric scores can be difficult for executive and engineering stakeholders to interpret quickly. Furthermore, a repository with critical security vulnerabilities could still achieve a high overall score (e.g. 85/100) if its code quality and architecture scores were near 100.

## Decision Drivers

* **Clarity & Executive Communication**: Letter grades (A+ to F) provide instant, universally understood quality signals.
* **Security Guardrails**: Critical security risks must prevent a repository from receiving an A or B overall grade, regardless of how clean the code structure is.
* **Explainability**: Cap enforcement must be explicitly logged and surfaced to users with human-readable explanations.

## Decision Outcome

We rebrand the platform to **CORTEX** and replace the 8-subsystem IQ score with a **5-Category Letter Grade System**:

### 1. Consolidated Category Structure & Weights

| Category | Absorbed Components | Weight |
| :--- | :--- | :--- |
| **Security** | Secret scanning, dependency CVEs, SAST static rules, auth/authz checks | **30%** |
| **Architecture** | Architectural style detection, design pattern findings, module dependency health | **20%** |
| **Code Quality** | Cyclomatic complexity, maintainability index, code smells, duplication | **20%** |
| **Maintainability** | README completeness, testing maturity, CI/CD pipeline automation | **20%** |
| **Community & Velocity** | Git commit activity, contributor velocity, conventional commits, community health files | **10%** |

### 2. Score to Grade Mapping Table

| Numeric Range | Letter Grade |
| :--- | :--- |
| **93–100** | **A+** |
| **87–92** | **A** |
| **80–86** | **A-** |
| **73–79** | **B+** |
| **67–72** | **B** |
| **60–66** | **B-** |
| **53–59** | **C+** |
| **47–52** | **C** |
| **40–46** | **C-** |
| **30–39** | **D** |
| **0–29** | **F** |

Overall numeric score is the weighted average of the 5 category numeric scores. The overall letter grade is mapped from this weighted average.

### 3. Security Guardrail Cap Rules

1. **Security = F (0–29)**: Overall grade is capped at **C** max (maximum numeric score 52.0).
   - `capped`: `true`
   - `cap_reason`: `"Overall grade capped at C due to critical security findings"`
2. **Security = D (30–39)**: Overall grade is capped at **B** max (maximum numeric score 72.0).
   - `capped`: `true`
   - `cap_reason`: `"Overall grade capped at B due to moderate security risks"`
3. **Security >= C- (40+)**: No cap applied.

## Consequences

* Provides a narrative-first evaluation model.
* Ensures security vulnerabilities strictly limit the maximum achievable rating.
* API responses explicitly report `capped` status and `cap_reason` for visual UI rendering.
