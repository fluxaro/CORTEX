import {
  AuditLog,
  Invitation,
  Membership,
  Notification,
  Organization,
  ScanHistory,
  TrendMetric,
  User,
  Workspace,
} from './types';

export const MOCK_CURRENT_USER: User = {
  id: 'usr-1',
  email: 'alex.architect@cortex.io',
  full_name: 'Alex Architect',
  avatar_url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80',
  role: 'OWNER',
  is_active: true,
  is_verified: true,
  created_at: '2026-01-01T00:00:00Z',
};

export const MOCK_ORGANIZATIONS: Organization[] = [
  {
    id: 'org-1',
    name: 'Acme Enterprise Engineering',
    slug: 'acme-enterprise',
    avatar_url: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=100&auto=format&fit=crop&q=80',
    owner_id: 'usr-1',
    created_at: '2026-01-10T00:00:00Z',
  },
];

export const MOCK_WORKSPACES: Workspace[] = [
  {
    id: 'ws-1',
    name: 'Core Platform Engineering',
    slug: 'core-platform',
    type: 'ORGANIZATION',
    organization_id: 'org-1',
    owner_id: 'usr-1',
    created_at: '2026-01-15T00:00:00Z',
  },
  {
    id: 'ws-2',
    name: 'Personal Sandbox',
    slug: 'alex-sandbox',
    type: 'PERSONAL',
    owner_id: 'usr-1',
    created_at: '2026-02-01T00:00:00Z',
  },
];

export const MOCK_MEMBERSHIPS: Membership[] = [
  {
    id: 'mem-1',
    user_id: 'usr-1',
    workspace_id: 'ws-1',
    role: 'OWNER',
    status: 'ACTIVE',
    created_at: '2026-01-15T00:00:00Z',
    user: MOCK_CURRENT_USER,
  },
  {
    id: 'mem-2',
    user_id: 'usr-2',
    workspace_id: 'ws-1',
    role: 'ADMIN',
    status: 'ACTIVE',
    created_at: '2026-01-20T00:00:00Z',
    user: {
      id: 'usr-2',
      email: 'sarah.devops@cortex.io',
      full_name: 'Sarah DevOps',
      role: 'ADMIN',
      is_active: true,
      is_verified: true,
      created_at: '2026-01-20T00:00:00Z',
    },
  },
];

export const MOCK_INVITATIONS: Invitation[] = [
  {
    id: 'inv-1',
    email: 'dev.lead@cortex.io',
    workspace_id: 'ws-1',
    role: 'MAINTAINER',
    status: 'PENDING',
    expires_at: '2026-08-04T00:00:00Z',
    created_at: '2026-07-28T00:00:00Z',
  },
];

export const MOCK_NOTIFICATIONS: Notification[] = [
  {
    id: 'notif-1',
    user_id: 'usr-1',
    title: 'High Severity SAST Vulnerability Alert',
    message: 'Hardcoded secret token pattern detected in fastapi/fastapi on branch main.',
    type: 'WARNING',
    is_read: false,
    created_at: '2026-08-18T22:30:00Z',
  },
  {
    id: 'notif-2',
    user_id: 'usr-1',
    title: 'Repository IQ Scan Completed',
    message: 'Full AST analysis for vercel/next.js completed with 94.2 IQ Score (Grade A).',
    type: 'SUCCESS',
    is_read: false,
    created_at: '2026-08-18T21:15:00Z',
  },
  {
    id: 'notif-3',
    user_id: 'usr-1',
    title: 'Architecture Layer Violation',
    message: 'Cyclic dependency detected between Controller and Database model layer in facebook/react.',
    type: 'WARNING',
    is_read: true,
    created_at: '2026-08-18T18:00:00Z',
  },
  {
    id: 'notif-4',
    user_id: 'usr-1',
    title: 'GitHub Webhook Sync Successful',
    message: 'Synced 14 new commits for fluxaro/CORTEX.',
    type: 'INFO',
    is_read: true,
    created_at: '2026-08-18T14:45:00Z',
  },
  {
    id: 'notif-5',
    user_id: 'usr-1',
    title: 'Technical Debt Threshold Warning',
    message: 'Refactor time estimate exceeded 20 hours threshold for repository tailwindlabs/tailwindcss.',
    type: 'WARNING',
    is_read: true,
    created_at: '2026-08-17T11:20:00Z',
  },
];

export const MOCK_AUDIT_LOGS: AuditLog[] = [
  {
    id: 'audit-1',
    user_id: 'usr-1',
    workspace_id: 'ws-1',
    action: 'REPOSITORY_IMPORT',
    entity_type: 'Repository',
    entity_id: '1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b',
    details_json: { url: 'https://github.com/me-hv/Cortex', provider: 'GITHUB' },
    created_at: '2026-07-28T07:30:00Z',
  },
  {
    id: 'audit-2',
    user_id: 'usr-1',
    workspace_id: 'ws-1',
    action: 'USER_INVITATION',
    entity_type: 'Invitation',
    details_json: { email: 'dev.lead@cortex.io', role: 'MAINTAINER' },
    created_at: '2026-07-28T05:15:00Z',
  },
];

export const MOCK_SCAN_HISTORIES: ScanHistory[] = [
  {
    id: 'scan-1',
    repository_id: '1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b',
    status: 'COMPLETED',
    duration_seconds: 14.2,
    commit_hash: '8dd737c',
    branch: 'main',
    triggered_by: 'SCHEDULED',
    created_at: '2026-07-28T07:30:00Z',
  },
  {
    id: 'scan-2',
    repository_id: '1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b',
    status: 'COMPLETED',
    duration_seconds: 12.8,
    commit_hash: '2d7a62e',
    branch: 'main',
    triggered_by: 'MANUAL',
    created_at: '2026-07-27T18:00:00Z',
  },
];

export const MOCK_TREND_METRICS: TrendMetric[] = [
  { id: 't-1', repository_id: '1a9e8b7c', recorded_at: '2026-07-22T00:00:00Z', overall_iq: 84.5, security_score: 80.0, architecture_score: 85.0, complexity_score: 82.0, documentation_score: 90.0, debt_hours: 24.0, testing_score: 80.0 },
  { id: 't-2', repository_id: '1a9e8b7c', recorded_at: '2026-07-24T00:00:00Z', overall_iq: 88.0, security_score: 84.0, architecture_score: 88.0, complexity_score: 86.0, documentation_score: 92.0, debt_hours: 18.0, testing_score: 85.0 },
  { id: 't-3', repository_id: '1a9e8b7c', recorded_at: '2026-07-26T00:00:00Z', overall_iq: 90.5, security_score: 86.0, architecture_score: 90.0, complexity_score: 90.0, documentation_score: 95.0, debt_hours: 14.0, testing_score: 88.0 },
  { id: 't-4', repository_id: '1a9e8b7c', recorded_at: '2026-07-28T00:00:00Z', overall_iq: 92.4, security_score: 88.0, architecture_score: 91.5, complexity_score: 94.2, documentation_score: 96.0, debt_hours: 12.0, testing_score: 90.0 },
];
