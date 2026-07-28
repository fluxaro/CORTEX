import React from 'react';
import { Building2 } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { MOCK_ORGANIZATIONS } from '../services/mockEnterpriseData';

export const OrganizationDashboardPage: React.FC = () => {
  const org = MOCK_ORGANIZATIONS[0];

  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      <div className="pb-4 border-b border-border/80">
        <h1 className="text-2xl font-bold text-white tracking-tight">Organization Overview</h1>
        <p className="text-xs text-gray-400">Enterprise organization governance, SSO, and team seats.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card glass className="p-6 text-center space-y-3">
          <Building2 className="h-10 w-10 text-purple-400 mx-auto" />
          <h2 className="text-xl font-bold text-white">{org.name}</h2>
          <Badge variant="purple">Enterprise Plan</Badge>
        </Card>

        <Card glass className="md:col-span-2 space-y-4">
          <CardHeader>
            <CardTitle>Organization Settings</CardTitle>
            <CardDescription>Domain verification, security controls, and member seats.</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-2 gap-4 text-xs">
            <div className="p-3 bg-surface-card rounded-xl border border-border/40">
              <span className="text-gray-400 block">Total Member Seats</span>
              <span className="text-lg font-bold text-white">24 / 50 Active Seats</span>
            </div>
            <div className="p-3 bg-surface-card rounded-xl border border-border/40">
              <span className="text-gray-400 block">Domain Restrictions</span>
              <span className="text-lg font-bold text-emerald-400">@projectiq.io Verified</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
