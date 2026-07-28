import React from 'react';
import { GitBranch, Github, RefreshCw, ShieldCheck } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';

export const RepoSyncPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      <div className="flex justify-between items-center pb-4 border-b border-border/80">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Git Platform Synchronization</h1>
          <p className="text-xs text-gray-400">Import and synchronize repositories from GitHub, GitLab, and Bitbucket.</p>
        </div>
        <Button variant="primary">
          <RefreshCw className="h-4 w-4" />
          <span>Sync All Providers</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card glass className="p-5 space-y-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Github className="h-6 w-6 text-white" />
              <h3 className="font-bold text-white">GitHub Integration</h3>
            </div>
            <Badge variant="success">Connected</Badge>
          </div>
          <p className="text-xs text-gray-400">OAuth & GitHub App integration active. Webhook auto-registration enabled.</p>
        </Card>

        <Card glass className="p-5 space-y-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <GitBranch className="h-6 w-6 text-orange-400" />
              <h3 className="font-bold text-white">GitLab Support</h3>
            </div>
            <Badge variant="purple">Connected</Badge>
          </div>
          <p className="text-xs text-gray-400">GitLab.com and self-hosted instances supported via OAuth tokens.</p>
        </Card>

        <Card glass className="p-5 space-y-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-6 w-6 text-blue-400" />
              <h3 className="font-bold text-white">Bitbucket Support</h3>
            </div>
            <Badge variant="info">Connected</Badge>
          </div>
          <p className="text-xs text-gray-400">Bitbucket Cloud workspace synchronization and webhook automation.</p>
        </Card>
      </div>
    </div>
  );
};
