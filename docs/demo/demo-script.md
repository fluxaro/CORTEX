# ProjectIQ Demo Script & Recording Guide

## Overview
This document is a complete guide for recording a professional ProjectIQ demo video.

---

## Pre-Recording Checklist

- [ ] ProjectIQ running locally (`docker-compose up -d`)
- [ ] Browser at `http://localhost:5173` — landing page visible
- [ ] Test repository ready: `https://github.com/tiangolo/fastapi`
- [ ] Microphone tested, background noise eliminated
- [ ] Screen recording software running (OBS / Loom / QuickTime)
- [ ] Browser zoom at 110%
- [ ] Notifications silenced

---

## 3-Minute Demo

**Target audience:** Developers, GitHub viewers, technical recruiters.

| Time | Action | Narration |
| :--- | :--- | :--- |
| 0:00 – 0:15 | Show landing page | "Meet ProjectIQ — the fastest way to know if a repository is worth cloning." |
| 0:15 – 0:30 | Paste a GitHub URL, click Analyze | "Just paste the URL. ProjectIQ does the rest — zero code execution, complete safety." |
| 0:30 – 1:00 | Analysis progress indicator | "In under a minute, six parallel analysis engines are inspecting this codebase." |
| 1:00 – 1:30 | Show IQ Score page | "The Repository IQ Score is a 0-to-100 composite across code quality, architecture, security, documentation, testing, and Git practices." |
| 1:30 – 2:00 | Show Security page — SAST findings | "Committed secrets, vulnerable dependencies, dangerous functions — all flagged with exact file and line number." |
| 2:00 – 2:30 | Show Architecture page — dependency graph | "An interactive dependency graph showing which modules depend on each other — and where architectural violations exist." |
| 2:30 – 3:00 | Show AI Summary | "And finally — an AI-generated executive summary tailored to different audiences: developer, manager, or technical recruiter." |

---

## 5-Minute Demo

Add to the 3-minute version:

| Time | Action | Narration |
| :--- | :--- | :--- |
| 3:00 – 3:30 | Technical Debt Breakdown | "Technical debt is expressed in hours and categorized: architecture, security, testing, documentation." |
| 3:30 – 4:00 | Improvement Recommendations | "A prioritized improvement roadmap — quick wins in days, structural changes for next quarter." |
| 4:00 – 4:30 | Trend Analysis | "Track how your IQ score, security posture, and technical debt change across scan versions over time." |
| 4:30 – 5:00 | Repository Comparison | "Compare any two repositories side-by-side — useful for evaluating open-source alternatives." |

---

## 10-Minute Demo

Add to the 5-minute version:

| Time | Action | Narration |
| :--- | :--- | :--- |
| 5:00 – 6:00 | Static Analysis deep dive | "Cyclomatic complexity, maintainability index, and code smell detection per function across 6 languages." |
| 6:00 – 7:00 | Enterprise Workspace | "Enterprise organizations can create team workspaces with role-based access control." |
| 7:00 – 8:00 | Git Platform Sync | "Connect GitHub, GitLab, or Bitbucket and synchronize repositories automatically via webhook events." |
| 8:00 – 9:00 | Scheduled Scans | "Configure automated daily, weekly, or monthly scans — and receive in-app notifications when findings change." |
| 9:00 – 10:00 | API Explorer (Swagger) | "Every feature is available as a REST API, fully documented with Swagger UI." |

---

## Key Talking Points

1. **No code execution** — complete security isolation from untrusted repositories.
2. **Fully deterministic** — identical inputs always produce identical scores, making it auditable.
3. **6 programming languages** — Python, TypeScript, JavaScript, Go, Java, Rust.
4. **20+ design patterns** detected statically without runtime inspection.
5. **AI is optional** — every feature works offline with the MockProvider fallback.
6. **Open source** — MIT licensed, self-hostable, extensible.
