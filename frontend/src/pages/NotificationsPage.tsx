import React from 'react';
import { Bell, CheckCircle2 } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { MOCK_NOTIFICATIONS } from '../services/mockEnterpriseData';

export const NotificationsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      <div className="flex justify-between items-center pb-4 border-b border-border/80">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Notifications Center</h1>
          <p className="text-xs text-gray-400">In-app notifications for security findings, scan completions, and imports.</p>
        </div>
        <Button variant="outline" size="sm">
          <CheckCircle2 className="h-4 w-4" />
          <span>Mark All Read</span>
        </Button>
      </div>

      <Card glass>
        <CardHeader>
          <CardTitle>Recent Notifications</CardTitle>
          <CardDescription>Alerts and notifications across workspaces.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {MOCK_NOTIFICATIONS.map((n) => (
              <div key={n.id} className="flex items-start gap-3 p-4 bg-surface-card rounded-xl border border-border/60 text-xs">
                <div className="p-2 bg-primary-500/10 text-primary-400 rounded-lg shrink-0 mt-0.5">
                  <Bell className="h-4 w-4" />
                </div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold text-gray-200">{n.title}</h4>
                    <span className="text-[10px] text-gray-500">{new Date(n.created_at).toLocaleString()}</span>
                  </div>
                  <p className="text-gray-400 leading-relaxed">{n.message}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
