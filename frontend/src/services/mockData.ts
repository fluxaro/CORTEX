import {
  ArchitectureReport,
  Repository,
  RepositoryGradeReport,
  SecurityReport,
  StaticMetrics,
} from './types';

export const MOCK_REPOSITORIES: Repository[] = [
  {
    id: '1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b',
    name: 'Cortex',
    owner: 'me-hv',
    full_name: 'me-hv/Cortex',
    description: 'AI-Powered Repository Intelligence Platform - Know your code before you clone it.',
    default_branch: 'main',
    stars: 1240,
    forks: 185,
    language: 'Python',
    license: 'MIT',
    clone_url: 'https://github.com/me-hv/Cortex.git',
    html_url: 'https://github.com/me-hv/Cortex',
    visibility: 'public',
    status: 'CLONED',
    local_path: '/storage/repositories/cortex',
    created_at: '2026-01-15T08:00:00Z',
    updated_at: '2026-07-28T07:30:00Z',
    iq_score: 92.4,
    overall_grade: 'A',
  },
  {
    id: '2b8a7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d',
    name: 'fastapi-microservices',
    owner: 'tiangolo',
    full_name: 'tiangolo/fastapi-microservices',
    description: 'Production-ready FastAPI microservices architecture blueprint.',
    default_branch: 'main',
    stars: 3420,
    forks: 512,
    language: 'Python',
    license: 'MIT',
    clone_url: 'https://github.com/tiangolo/fastapi-microservices.git',
    html_url: 'https://github.com/tiangolo/fastapi-microservices',
    visibility: 'public',
    status: 'CLONED',
    local_path: '/storage/repositories/fastapi-ms',
    created_at: '2025-11-20T10:00:00Z',
    updated_at: '2026-07-25T14:20:00Z',
    iq_score: 88.0,
    overall_grade: 'A',
  },
  {
    id: '3c7b6a5d-4e3f-2a1b-0c9d-8e7f6a5b4c3d',
    name: 'react-enterprise-boilerplate',
    owner: 'vercel',
    full_name: 'vercel/react-enterprise-boilerplate',
    description: 'Enterprise React 19 + Next.js App Router boilerplate with Tailwind CSS.',
    default_branch: 'main',
    stars: 8910,
    forks: 1240,
    language: 'TypeScript',
    license: 'Apache-2.0',
    clone_url: 'https://github.com/vercel/react-enterprise-boilerplate.git',
    html_url: 'https://github.com/vercel/react-enterprise-boilerplate',
    visibility: 'public',
    status: 'CLONED',
    local_path: '/storage/repositories/react-boilerplate',
    created_at: '2025-08-10T12:00:00Z',
    updated_at: '2026-07-27T18:45:00Z',
    iq_score: 95.1,
    overall_grade: 'A+',
  },
];

export const MOCK_REPOSITORY_IQ: RepositoryGradeReport = {
  id: 'grade-111',
  repository_id: '1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b',
  analysis_run_id: 'run-999',
  overall_score: 92.4,
  overall_grade: 'A',
  capped: false,
  cap_reason: null,
  maturity_level: 'Enterprise Ready',
  category_scores: {
    security: 88.0,
    architecture: 91.5,
    code_quality: 94.2,
    maintainability: 93.0,
    community_velocity: 92.0,
  },
  subsystem_scores: {
    static_analysis: 94.2,
    architecture: 91.5,
    security: 88.0,
    documentation: 96.0,
    testing: 90.0,
    ci: 100.0,
    git_practices: 89.0,
    repository_health: 95.0,
    community: 92.0,
  },
  narrative_summary:
    'Cortex is a software project demonstrating a Grade A (92.4/100) engineering posture. Its primary architectural strength is clean architecture with strict layer separation. The main operational risk is minor third-party dependency updates. It is a strong fit for teams requiring structured standards.',
  summary: {
    narrative_summary:
      'Cortex is a software project demonstrating a Grade A (92.4/100) engineering posture. Its primary architectural strength is clean architecture with strict layer separation. The main operational risk is minor third-party dependency updates. It is a strong fit for teams requiring structured standards.',
    executive_summary:
      'Cortex represents an exceptionally high-quality enterprise repository. It demonstrates a robust Clean Architecture pattern, high test coverage, 100% CI/CD automation, and zero critical security vulnerabilities.',
    technical_summary:
      'Built using FastAPI 0.111+, Python 3.13+, Pydantic v2, SQLAlchemy 2.x Async ORM, Celery, and Redis. The module dependency graph is acyclic with strict separation between API, Service, Engine, and Model layers.',
    architecture_summary:
      'Architecture Style: Hexagonal / Ports & Adapters. Modularity Score: 91.5/100. Design Patterns detected: Repository, Factory, Singleton, Strategy, Observer, Dependency Injection.',
    security_summary:
      'Security Posture: 88.0/100. Zero hardcoded committed secrets. Baseline static analysis rules passed with zero critical vulnerabilities.',
    maintainability_summary:
      'Maintainability Index: 94.2/100. 19/19 standard README sections present. Conventional Commits compliance: 98.5%.',
    recruiter_summary:
      'Engineering Maturity: Enterprise Ready. Grade: A (92.4/100). Codebase reflects senior architectural standards and production readiness.',
    engineering_manager_summary:
      'Estimated Technical Debt: 12.0 hours (1.5 days). Main technical debt consists of routine minor library upgrades and unit test expansion.',
  },
  insights: {
    strengths: [
      'Clean Architecture with strict layer separation and dependency injection.',
      'Comprehensive 100% CI/CD automation pipelines on GitHub Actions.',
      'High maintainability index with cyclomatic complexity average < 3.2.',
      'Extensive documentation coverage including architecture diagrams and API specs.',
      'Zero committed hardcoded credentials or API keys detected.',
    ],
    weaknesses: [
      'Minor third-party dependency update recommended for optional plugins.',
      'Code duplication detected in test fixture helper utilities.',
    ],
  },
  technical_debt: {
    total_hours: 12.0,
    total_days: 1.5,
    category_breakdown: {
      Architecture: 0.0,
      Security: 4.0,
      Testing: 4.0,
      Documentation: 0.0,
      Maintainability: 2.0,
      Dependency: 2.0,
      Configuration: 0.0,
    },
    items: [
      {
        category: 'Dependency',
        description: 'Upgrade minor patch versions of third-party helper libraries.',
        estimated_hours: 2.0,
      },
      {
        category: 'Testing',
        description: 'Expand end-to-end integration test coverage for background worker edge cases.',
        estimated_hours: 4.0,
      },
      {
        category: 'Security',
        description: 'Audit CORS whitelist configuration for staging environment deployment.',
        estimated_hours: 4.0,
      },
      {
        category: 'Maintainability',
        description: 'Refactor test fixture setup to reduce duplicate code blocks.',
        estimated_hours: 2.0,
      },
    ],
  },
  benchmark: {
    overall_percentile: 94.5,
    quality_percentile: 96.2,
    security_percentile: 91.0,
    architecture_percentile: 93.8,
    maintainability_percentile: 95.0,
  },
  created_at: '2026-07-28T08:00:00Z',
  updated_at: '2026-07-28T08:00:00Z',
};

export const MOCK_STATIC_METRICS: StaticMetrics = {
  repository_id: '1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b',
  total_files: 148,
  total_loc: 18450,
  code_loc: 14200,
  comment_loc: 2850,
  blank_loc: 1400,
  average_cyclomatic_complexity: 2.8,
  maintainability_index: 94.2,
  duplication_percentage: 1.4,
  complexity_rank: 'A (Low Complexity)',
};

export const MOCK_ARCHITECTURE_REPORT: ArchitectureReport = {
  repository_id: '1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b',
  architecture_style: 'Clean Architecture (Hexagonal)',
  confidence_score: 0.94,
  modularity_score: 91.5,
  coupling_score: 18.2,
  layer_separation_score: 95.0,
  patterns: [
    {
      pattern_name: 'Repository Pattern',
      category: 'Data Access',
      confidence: 0.98,
      file_path: 'backend/app/repositories/base.py',
    },
    {
      pattern_name: 'Factory Method',
      category: 'Creational',
      confidence: 0.95,
      file_path: 'backend/app/core/ai/factory.py',
    },
    {
      pattern_name: 'Strategy Pattern',
      category: 'Behavioral',
      confidence: 0.92,
      file_path: 'backend/app/analyzers/base/registry.py',
    },
  ],
  frameworks: [
    { framework_name: 'FastAPI', category: 'Backend Web Framework', version: '0.111.0' },
    { framework_name: 'React', category: 'Frontend UI Framework', version: '18.3.1' },
    { framework_name: 'SQLAlchemy', category: 'ORM / Database', version: '2.0.30' },
  ],
  violations: [],
};

export const MOCK_SECURITY_REPORT: SecurityReport = {
  repository_id: '1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b',
  critical_count: 0,
  high_count: 0,
  medium_count: 1,
  low_count: 2,
  info_count: 4,
  secret_count: 0,
  dependency_vuln_count: 0,
  config_issues_count: 1,
  findings: [
    {
      id: 'sec-001',
      rule_id: 'SEC-CONFIG-001',
      rule_name: 'CORS Wildcard In Staging Config',
      category: 'Configuration',
      severity: 'Medium',
      confidence: 'HIGH',
      file_path: 'backend/app/core/config/settings.py',
      line_number: 42,
      description: 'Ensure CORS origins whitelist strictly limits production domains.',
      cvss_score: 4.3,
    },
  ],
};
