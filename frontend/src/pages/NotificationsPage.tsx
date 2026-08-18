import React, { useEffect, useState } from 'react';
import {
  Bell,
  CheckCircle2,
  CheckCheck,
  Clock,
  Info,
  ShieldAlert,
  Trash2,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { NotificationService } from '../services/notificationService';
import { Notification } from '../services/types';

export const NotificationsPage: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [activeFilter, setActiveFilter] = useState<'all' | 'unread' | 'security' | 'scans'>('all');

  useEffect(() => {
    setNotifications(NotificationService.getNotifications());
  }, []);

  // Interactive Action Handlers (Persisted in LocalStorage)
  const handleMarkAllRead = () => {
    const updated = NotificationService.markAllRead();
    setNotifications(updated);
  };

  const handleClearAll = () => {
    const updated = NotificationService.clearAll();
    setNotifications(updated);
  };

  const handleToggleRead = (id: string) => {
    const updated = NotificationService.toggleRead(id);
    setNotifications(updated);
  };

  const handleDeleteNotif = (id: string) => {
    const updated = NotificationService.deleteNotification(id);
    setNotifications(updated);
  };

  // Filter Logic
  const unreadCount = notifications.filter((n) => !n.is_read).length;

  const filteredNotifications = notifications.filter((n) => {
    if (activeFilter === 'unread') return !n.is_read;
    if (activeFilter === 'security') return n.type === 'WARNING' || n.title.toLowerCase().includes('sast');
    if (activeFilter === 'scans') return n.type === 'SUCCESS' || n.title.toLowerCase().includes('scan');
    return true;
  });

  return (
    <div className="space-y-8 max-w-5xl mx-auto px-4 py-4">
      {/* Top Header Card */}
      <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center border border-blue-200 shrink-0">
            <Bell className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="font-display text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                Notifications Center
              </h1>
              {unreadCount > 0 && (
                <span className="px-3 py-0.5 rounded-full text-xs font-extrabold bg-blue-600 text-white shadow-xs">
                  {unreadCount} Unread
                </span>
              )}
            </div>
            <p className="text-xs text-slate-500 font-medium mt-1">
              Real-time security vulnerability alerts, AST scan completions, and workspace audit updates.
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3 shrink-0">
          <Button
            type="button"
            onClick={handleMarkAllRead}
            disabled={unreadCount === 0}
            icon={<CheckCheck className="h-4 w-4 text-slate-700" />}
            badgeColor="bg-slate-200"
            size="sm"
          >
            Mark All Read
          </Button>
          <Button
            type="button"
            onClick={handleClearAll}
            disabled={notifications.length === 0}
            icon={<Trash2 className="h-4 w-4 text-slate-700" />}
            badgeColor="bg-rose-200"
            size="sm"
          >
            Clear All
          </Button>
        </div>
      </div>

      {/* Category Filter Tabs */}
      <div className="flex items-center gap-2 border-b-2 border-slate-200/80 overflow-x-auto pb-1">
        {[
          { id: 'all', label: `All Alerts (${notifications.length})` },
          { id: 'unread', label: `Unread (${unreadCount})` },
          { id: 'security', label: 'Security & Vulnerabilities' },
          { id: 'scans', label: 'Scan Completions' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveFilter(tab.id as any)}
            className={`px-4 py-2.5 rounded-2xl text-xs font-extrabold transition-all whitespace-nowrap ${
              activeFilter === tab.id
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Notifications List Container */}
      <div className="space-y-4">
        {filteredNotifications.length === 0 ? (
          <div className="bg-white rounded-3xl p-12 border-2 border-slate-200/80 text-center space-y-3">
            <div className="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
              <CheckCircle2 className="h-6 w-6" />
            </div>
            <h3 className="font-display text-lg font-bold text-slate-800">No Notifications Found</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto font-medium">
              You are all caught up! There are no alerts matching your selected filter.
            </p>
          </div>
        ) : (
          filteredNotifications.map((n) => {
            const isWarning = n.type === 'WARNING';
            const isSuccess = n.type === 'SUCCESS';

            return (
              <div
                key={n.id}
                className={`p-5 rounded-3xl border-2 transition-all flex items-start gap-4 ${
                  !n.is_read
                    ? 'bg-white border-blue-200 shadow-sm'
                    : 'bg-slate-50/70 border-slate-200/80 opacity-90'
                }`}
              >
                {/* Icon Badge */}
                <div
                  className={`w-10 h-10 rounded-2xl flex items-center justify-center shrink-0 mt-0.5 ${
                    isWarning
                      ? 'bg-rose-50 text-rose-600 border border-rose-200'
                      : isSuccess
                      ? 'bg-emerald-50 text-emerald-600 border border-emerald-200'
                      : 'bg-blue-50 text-blue-600 border border-blue-200'
                  }`}
                >
                  {isWarning ? (
                    <ShieldAlert className="h-5 w-5" />
                  ) : isSuccess ? (
                    <CheckCircle2 className="h-5 w-5" />
                  ) : (
                    <Info className="h-5 w-5" />
                  )}
                </div>

                {/* Content Area */}
                <div className="flex-1 space-y-1">
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <h4 className="font-display text-sm font-extrabold text-slate-900">{n.title}</h4>
                      {!n.is_read && (
                        <span className="w-2 h-2 rounded-full bg-blue-600" title="Unread" />
                      )}
                    </div>
                    <span className="text-[11px] font-semibold text-slate-400 flex items-center gap-1 shrink-0">
                      <Clock className="h-3 w-3" />
                      {new Date(n.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>

                  <p className="text-xs text-slate-600 font-medium leading-relaxed">{n.message}</p>

                  {/* Bottom Action Footer */}
                  <div className="pt-2 flex items-center gap-4 text-[11px] font-bold">
                    <button
                      onClick={() => handleToggleRead(n.id)}
                      className="text-blue-600 hover:text-blue-800 hover:underline transition-colors"
                    >
                      {n.is_read ? 'Mark as Unread' : 'Mark as Read'}
                    </button>
                    <span className="text-slate-300">•</span>
                    <button
                      onClick={() => handleDeleteNotif(n.id)}
                      className="text-slate-400 hover:text-rose-600 transition-colors"
                    >
                      Dismiss
                    </button>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
