/** TypeScript types for ProjectIQ frontend application. */

export interface Repository {
  id: string;
  name: string;
  owner: string;
  full_name: string;
  description: string | null;
  default_branch: string;
  stars: number;
  forks: number;
  language: string | null;
  license: string | null;
  clone_url: string;
  html_url: string;
  visibility: string;
  status: 'PENDING' | 'CLONING' | 'CLONED' | 'FAILED';
  local_path: string | null;
  created_at: string;
  updated_at: string;
  iq_score?: number;
}

export interface SubsystemScores {
  static_analysis: number;
  architecture: number;
  security: number;
  documentation: number;
  testing: number;
  ci: number;
  git_practices: number;
  repository_health: number;
  community: number;
}

export interface TechnicalDebtItem {
  category: string;
  description: string;
  estimated_hours: number;
}

export interface TechnicalDebt {
  total_hours: number;
  total_days: number;
  category_breakdown: Record<string, number>;
  items: TechnicalDebtItem[];
}

export interface Recommendation {
  id: string;
  category: string;
  title: string;
  description: string;
  timeframe: 'Immediate' | 'Short-term' | 'Medium-term' | 'Long-term';
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
  difficulty: 'Easy' | 'Medium' | 'Hard';
  estimated_hours: number;
}

export interface Benchmark {
  overall_percentile: number;
  quality_percentile: number;
  security_percentile: number;
  architecture_percentile: number;
  maintainability_percentile: number;
}

export interface RepositoryIQReport {
  id: string;
  repository_id: string;
  analysis_run_id: string;
  overall_score: number;
  maturity_level: string;
  subsystem_scores: SubsystemScores;
  summary?: {
    executive_summary: string;
    technical_summary: string;
    architecture_summary: string;
    security_summary: string;
    maintainability_summary: string;
    recruiter_summary: string;
    engineering_manager_summary: string;
  };
  insights?: {
    strengths: string[];
    weaknesses: string[];
  };
  technical_debt?: TechnicalDebt;
  benchmark?: Benchmark;
  created_at: string;
  updated_at: string;
}

export interface StaticMetrics {
  repository_id: string;
  total_files: number;
  total_loc: number;
  code_loc: number;
  comment_loc: number;
  blank_loc: number;
  average_cyclomatic_complexity: number;
  maintainability_index: number;
  duplication_percentage: number;
  complexity_rank: string;
}

export interface ArchitectureReport {
  repository_id: string;
  architecture_style: string;
  confidence_score: number;
  modularity_score: number;
  coupling_score: number;
  layer_separation_score: number;
  patterns: Array<{
    pattern_name: string;
    category: string;
    confidence: number;
    file_path: string;
  }>;
  frameworks: Array<{
    framework_name: string;
    category: string;
    version: string | null;
  }>;
  violations: Array<{
    rule_name: string;
    source_file: string;
    target_file: string;
    description: string;
  }>;
}

export interface SecurityFinding {
  id: string;
  rule_id: string;
  rule_name: string;
  category: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low' | 'Info';
  confidence: string;
  file_path: string;
  line_number: number;
  description: string;
  cvss_score: number;
}

export interface SecurityReport {
  repository_id: string;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  info_count: number;
  secret_count: number;
  dependency_vuln_count: number;
  config_issues_count: number;
  findings: SecurityFinding[];
}
