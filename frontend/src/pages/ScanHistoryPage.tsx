import React from 'react';
import { Calendar, Clock, GitCommit, Play, RotateCcw } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { MOCK_SCAN_HISTORIES } from '../services/mockEnterpriseData';

export const ScanHistoryPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      <div className="flex justify-between items-center pb-4 border-b border-border/80">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Scan History & Schedules</h1>
          <p className="text-xs text-gray-400">Historical analysis execution log and automated scan schedules.</p>
        </div>
        <Button variant="primary">
          <Play className="h-4 w-4" />
          <span>Trigger Manual Scan</span>
        </Button>
      </div>

      <Card glass>
        <CardHeader>
          <CardTitle>Execution Logs</CardTitle>
          <CardDescription>All manual, scheduled, and webhook-triggered repository scans.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {MOCK_SCAN_HISTORIES.map((scan) => (
              <div key={scan.id} className="flex items-center justify-between p-4 bg-surface-card rounded-xl border border-border/60 text-xs">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="success">{scan.status}</Badge>
                    <span className="font-semibold text-gray-200"> me-hv/Cortex</span>
                    <span className="text-gray-500 font-mono">({scan.branch})</span>
                  </div>
                  <div className="flex items-center gap-4 text-gray-400 text-[11px]">
                    <span className="flex items-center gap-1"><GitCommit className="h-3.5 w-3.5" /> Commit {scan.commit_hash}</span>
                    <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" /> Duration {scan.duration_seconds}s</span>
                    <span className="flex items-center gap-1"><Calendar className="h-3.5 w-3.5" /> {new Date(scan.created_at).toLocaleString()}</span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Badge variant="outline">{scan.triggered_by}</Badge>
                  <Button variant="ghost" size="sm">
                    <RotateCcw className="h-3.5 w-3.5" />
                    <span>Retry</span>
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
