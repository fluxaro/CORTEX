# Glossary

Key terms and definitions used throughout the Cortex codebase and documentation.

---

| Term | Definition |
| :--- | :--- |
| **Analysis Run** | A single execution of the Cortex analysis pipeline against a repository. |
| **Architecture Engine** | The Cortex subsystem responsible for detecting architectural styles, design patterns, and module dependency relationships. |
| **AST** | Abstract Syntax Tree. A tree representation of the syntactic structure of source code used for static analysis. |
| **Celery** | A distributed asynchronous task queue used by Cortex to run repository cloning and analysis in the background. |
| **Cyclomatic Complexity** | A software metric measuring the number of independent paths through a function's source code. Lower is better. |
| **CVSS** | Common Vulnerability Scoring System. A standardized score (0–10) measuring the severity of a security vulnerability. |
| **CVE** | Common Vulnerabilities and Exposures. A public identifier for a known security vulnerability. |
| **Debt Hours** | Technical debt expressed as estimated remediation hours based on finding counts and severity. |
| **Dependency Graph** | A directed graph showing which modules import or depend on other modules in the repository. |
| **IQ Score** | The Repository IQ Score (0–100) — Cortex's composite engineering quality score. |
| **JWT** | JSON Web Token. A compact, signed authentication token used by Cortex for API authentication. |
| **Maintainability Index** | A composite metric (0–100) measuring how maintainable a file or function is. Higher is better. |
| **Maturity Level** | A qualitative classification of a repository's engineering readiness: Prototype → Personal → Learning → Production → Enterprise → Open Source Mature. |
| **PBKDF2** | Password-Based Key Derivation Function 2. The password hashing algorithm used by Cortex. |
| **RBAC** | Role-Based Access Control. Cortex enforces OWNER > ADMIN > MAINTAINER > DEVELOPER > VIEWER roles. |
| **Repository** | A source code repository hosted on GitHub, GitLab, or Bitbucket that Cortex can analyze. |
| **SAST** | Static Application Security Testing. Analysis of source code for security vulnerabilities without executing the code. |
| **Subsystem Score** | An individual dimensional score (0–100) for one of the 8 engineering dimensions: static analysis, architecture, security, documentation, testing, CI/CD, Git practices, community. |
| **Technical Debt** | The accumulated cost of engineering decisions that require future remediation work. |
| **Workspace** | A multi-tenant collaboration boundary in Cortex's enterprise platform containing repositories and team members. |
