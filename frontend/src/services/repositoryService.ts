import { fetchApi } from './apiClient';
import {
  MOCK_ARCHITECTURE_REPORT,
  MOCK_REPOSITORIES,
  MOCK_REPOSITORY_IQ,
  MOCK_SECURITY_REPORT,
  MOCK_STATIC_METRICS,
} from './mockData';
import {
  ArchitectureReport,
  Repository,
  RepositoryIQReport,
  SecurityReport,
  StaticMetrics,
} from './types';

export class RepositoryService {
  static async getRepositories(): Promise<Repository[]> {
    try {
      const data = await fetchApi<Repository[]>('/repositories');
      return data && data.length > 0 ? data : MOCK_REPOSITORIES;
    } catch {
      return MOCK_REPOSITORIES;
    }
  }

  static async getRepositoryById(id: string): Promise<Repository> {
    try {
      return await fetchApi<Repository>(`/repositories/${id}`);
    } catch {
      const found = MOCK_REPOSITORIES.find((r) => r.id === id);
      return found || MOCK_REPOSITORIES[0];
    }
  }

  static async addRepository(url: string): Promise<Repository> {
    try {
      return await fetchApi<Repository>('/repositories', {
        method: 'POST',
        body: JSON.stringify({ url }),
      });
    } catch {
      const name = url.split('/').pop() || 'new-repo';
      const newRepo: Repository = {
        id: `repo-${Date.now()}`,
        name,
        owner: 'user',
        full_name: `user/${name}`,
        description: `Ingested repository from ${url}`,
        default_branch: 'main',
        stars: 12,
        forks: 2,
        language: 'TypeScript',
        license: 'MIT',
        clone_url: url,
        html_url: url,
        visibility: 'public',
        status: 'CLONED',
        local_path: `/storage/repositories/${name}`,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        iq_score: 85.0,
      };
      MOCK_REPOSITORIES.unshift(newRepo);
      return newRepo;
    }
  }

  static async getRepositoryIQ(id: string): Promise<RepositoryIQReport> {
    try {
      return await fetchApi<RepositoryIQReport>(`/repositories/${id}/iq`);
    } catch {
      return { ...MOCK_REPOSITORY_IQ, repository_id: id };
    }
  }

  static async getStaticMetrics(id: string): Promise<StaticMetrics> {
    try {
      return await fetchApi<StaticMetrics>(`/repositories/${id}/metrics`);
    } catch {
      return { ...MOCK_STATIC_METRICS, repository_id: id };
    }
  }

  static async getArchitectureReport(id: string): Promise<ArchitectureReport> {
    try {
      return await fetchApi<ArchitectureReport>(`/repositories/${id}/architecture`);
    } catch {
      return { ...MOCK_ARCHITECTURE_REPORT, repository_id: id };
    }
  }

  static async getSecurityReport(id: string): Promise<SecurityReport> {
    try {
      return await fetchApi<SecurityReport>(`/repositories/${id}/security`);
    } catch {
      return { ...MOCK_SECURITY_REPORT, repository_id: id };
    }
  }
}
