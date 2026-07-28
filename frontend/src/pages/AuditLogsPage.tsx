import React from 'react';
import { Shield } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { MOCK_AUDIT_LOGS } from '../services/mockEnterpriseData';

export const AuditLogsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      <div className="pb-4 border-b border-border/80">
        <h1 className="text-2xl font-bold text-white tracking-tight">Security Audit Logs</h1>
        <p className="text-xs text-gray-400">Immutable audit log trail of enterprise actions, invitations, and permissions.</p>
      </div>

      <Card glass>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-purple-400" />
            <span>Immutable Audit Trail</span>
          </CardTitle>
          <CardDescription>Security events recorded for compliance & auditing.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {MOCK_AUDIT_LOGS.map((log) => (
              <div key={log.id} className="p-4 bg-surface-card rounded-xl border border-border/60 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge variant="purple">{log.action}</Badge>
                    <span className="font-semibold text-gray-200">{log.entity_type}</span>
                  </div>
                  <span className="text-[10px] text-gray-500 font-mono">{new Date(log.created_at).toLocaleString()}</span>
                </div>
                <div className="text-gray-400 font-mono text-[11px] pt-1">
                  Details: {JSON.stringify(log.details_json)}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
