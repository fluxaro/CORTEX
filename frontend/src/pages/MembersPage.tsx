import React, { useState } from 'react';
import { UserPlus } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Modal } from '../components/ui/Modal';
import { MOCK_MEMBERSHIPS } from '../services/mockEnterpriseData';

export const MembersPage: React.FC = () => {
  const [isInviteOpen, setIsInviteOpen] = useState(false);
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState('DEVELOPER');

  const handleInvite = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Invitation sent to ${inviteEmail} with role ${inviteRole}`);
    setIsInviteOpen(false);
    setInviteEmail('');
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      <div className="flex justify-between items-center pb-4 border-b border-border/80">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Team Members & RBAC</h1>
          <p className="text-xs text-gray-400">Manage workspace members and Role-Based Access Control permissions.</p>
        </div>
        <Button onClick={() => setIsInviteOpen(true)} variant="primary">
          <UserPlus className="h-4 w-4" />
          <span>Invite Member</span>
        </Button>
      </div>

      <Card glass>
        <CardHeader>
          <CardTitle>Active Members</CardTitle>
          <CardDescription>Members with access to this workspace.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {MOCK_MEMBERSHIPS.map((mem) => (
              <div key={mem.id} className="flex items-center justify-between p-4 bg-surface-card rounded-xl border border-border/60 text-xs">
                <div className="flex items-center gap-3">
                  <img
                    src={mem.user?.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100'}
                    alt="avatar"
                    className="h-9 w-9 rounded-full object-cover border border-border"
                  />
                  <div>
                    <h4 className="font-semibold text-gray-100">{mem.user?.full_name || 'Team Member'}</h4>
                    <span className="text-gray-400 text-[11px]">{mem.user?.email}</span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Badge variant={mem.role === 'OWNER' ? 'purple' : mem.role === 'ADMIN' ? 'info' : 'default'}>
                    {mem.role}
                  </Badge>
                  <span className="text-[10px] text-gray-500 font-mono">Status: {mem.status}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Modal isOpen={isInviteOpen} onClose={() => setIsInviteOpen(false)} title="Invite Team Member">
        <form onSubmit={handleInvite} className="space-y-4 text-xs">
          <div>
            <label className="block text-gray-300 font-semibold mb-1">Email Address</label>
            <input
              type="email"
              required
              value={inviteEmail}
              onChange={(e) => setInviteEmail(e.target.value)}
              placeholder="colleague@projectiq.io"
              className="w-full px-3 py-2 bg-surface-card border border-border rounded-xl text-gray-200 focus:outline-none focus:border-primary-500"
            />
          </div>

          <div>
            <label className="block text-gray-300 font-semibold mb-1">RBAC Role</label>
            <select
              value={inviteRole}
              onChange={(e) => setInviteRole(e.target.value)}
              className="w-full px-3 py-2 bg-surface-card border border-border rounded-xl text-gray-200 focus:outline-none focus:border-primary-500"
            >
              <option value="ADMIN">Admin (Manage settings & members)</option>
              <option value="MAINTAINER">Maintainer (Manage repos & trigger scans)</option>
              <option value="DEVELOPER">Developer (View metrics & run manual scans)</option>
              <option value="VIEWER">Viewer (Read-only)</option>
            </select>
          </div>

          <div className="flex justify-end gap-2 pt-3 border-t border-border">
            <Button type="button" variant="ghost" onClick={() => setIsInviteOpen(false)}>Cancel</Button>
            <Button type="submit" variant="primary">Send Invitation</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
