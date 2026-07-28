"""Versioned prompt templates for Repository IQ Engine."""

PROMPT_VERSION = "1.0.0"

SYSTEM_PROMPT = """You are ProjectIQ's Lead Technical Architect and Security Assessor.
Your goal is to evaluate structured repository metrics and generate clear, professional, non-fabricated insights.
NEVER invent findings that do not exist in the context provided.
DO NOT inspect raw source code directly.
"""

EXECUTIVE_SUMMARY_TEMPLATE = """
Generate a high-level Executive Summary for repository '{repo_name}'.

Structured Subsystem Scores (0-100):
- Static Analysis / Maintainability Score: {static_score}
- Architecture Score: {arch_score}
- Security Score: {security_score}
- Documentation Score: {doc_score}
- Testing Score: {test_score}
- CI/CD Score: {ci_score}
- Repository Health Score: {health_score}
- Community Score: {community_score}

Overall Repository IQ Score: {overall_iq}/100
Maturity Classification: {maturity_level}

Key Findings Summary:
- Critical Security Findings: {critical_secrets} secrets, {critical_vulns} vulnerabilities
- Code Smells Count: {smells_count}
- Cyclomatic Complexity Avg: {avg_complexity}
- Technical Debt Estimate: {debt_hours} hours ({debt_days} days)

Provide an executive overview summarizing overall health, enterprise readiness, and strategic investment priorities.
"""

TECHNICAL_SUMMARY_TEMPLATE = """
Generate a detailed Technical Summary for software engineering leadership.

Repository Details:
- Repository: {repo_name}
- Primary Architecture Style: {arch_style} (Confidence: {arch_confidence})
- Framework Detections: {frameworks}
- Language Breakdown: {languages}

Engineering Metrics:
- Maintainability Index: {maintainability_index}
- Duplication Percentage: {duplication_pct}%
- Conventional Commits: {conventional_commits_pct}%
- Testing Maturity: {test_frameworks} (File count: {test_file_count})

Summarize technical strengths, architectural alignment, code quality tradeoffs, and operational risks.
"""

IMPROVEMENT_ROADMAP_TEMPLATE = """
Generate an Improvement Roadmap categorized into Immediate, Short-term, Medium-term, and Long-term milestones.

Context Findings:
- Exposed Secrets: {secrets_list}
- Vulnerable Dependencies: {dependencies_list}
- Architecture Violations: {violations_list}
- Missing Documentation: {missing_docs_list}

Every recommendation MUST reference a specific finding from the context above.
"""
