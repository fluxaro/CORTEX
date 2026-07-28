import React from 'react';
import { Building, FolderGit2, Users } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { MOCK_WORKSPACES } from '../services/mockEnterpriseData';

interface WorkspaceDashboardPageProps {
  onNavigate: (page: string) => void;
}

export const WorkspaceDashboardPage: React.FC<WorkspaceDashboardPageProps> = ({ onNavigate }) => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      <div className="flex justify-between items-center pb-4 border-b border-border/80">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Workspaces</h1>
          <p className="text-xs text-gray-400">Manage team collaboration boundaries, members, and repository access.</p>
        </div>
        <Button variant="primary">
          <Building className="h-4 w-4" />
          <span>Create Workspace</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {MOCK_WORKSPACES.map((ws) => (
          <Card key={ws.id} glass className="p-6 space-y-4 hover:border-primary-500/50 transition-all">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-bold text-white">{ws.name}</h3>
                <span className="text-xs text-gray-500 font-mono">slug: {ws.slug}</span>
              </div>
              <Badge variant={ws.type === 'ORGANIZATION' ? 'purple' : 'info'}>{ws.type}</Badge>
            </div>

            <p className="text-xs text-gray-400">
              Workspace created on {new Date(ws.created_at).toLocaleDateString()}. Enforces Role-Based Access Control (RBAC).
            </p>

            <div className="pt-4 border-t border-border/40 flex justify-between items-center text-xs text-gray-300">
              <div className="flex items-center gap-4">
                <span className="flex items-center gap-1.5"><Users className="h-4 w-4 text-primary-400" /> 8 Members</span>
                <span className="flex items-center gap-1.5"><FolderGit2 className="h-4 w-4 text-emerald-400" /> 12 Repos</span>
              </div>
              <Button onClick={() => onNavigate('members')} variant="outline" size="sm">
                Manage Members
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
