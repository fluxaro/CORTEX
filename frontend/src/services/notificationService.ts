import { Notification } from './types';

const LOCAL_STORAGE_NOTIFS_KEY = 'cortex_live_notifications';

// Initial dynamic notifications
const INITIAL_NOTIFICATIONS: Notification[] = [
  {
    id: 'notif-1',
    user_id: 'usr-1',
    title: 'High Severity SAST Vulnerability Alert',
    message: 'Hardcoded secret token pattern checked in fastapi/fastapi on branch main. 0 secrets leaked.',
    type: 'WARNING',
    is_read: false,
    created_at: new Date(Date.now() - 3600000 * 2).toISOString(),
  },
  {
    id: 'notif-2',
    user_id: 'usr-1',
    title: 'Repository IQ Scan Completed',
    message: 'Full AST analysis for vercel/next.js completed with 94.2 IQ Score (Grade A).',
    type: 'SUCCESS',
    is_read: false,
    created_at: new Date(Date.now() - 3600000 * 5).toISOString(),
  },
  {
    id: 'notif-3',
    user_id: 'usr-1',
    title: 'Architecture Layer Violation Audit',
    message: 'Evaluated Clean Architecture layer separation for facebook/react. Zero cyclic dependencies detected.',
    type: 'INFO',
    is_read: true,
    created_at: new Date(Date.now() - 3600000 * 12).toISOString(),
  },
];

export class NotificationService {
  static getNotifications(): Notification[] {
    try {
      const raw = localStorage.getItem(LOCAL_STORAGE_NOTIFS_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) return parsed;
      }
    } catch {
      // Fallback
    }
    this.saveNotifications(INITIAL_NOTIFICATIONS);
    return INITIAL_NOTIFICATIONS;
  }

  static saveNotifications(notifications: Notification[]) {
    try {
      localStorage.setItem(LOCAL_STORAGE_NOTIFS_KEY, JSON.stringify(notifications));
    } catch {
      // Storage full fallback
    }
  }

  static addNotification(notif: Omit<Notification, 'id' | 'created_at' | 'user_id'>): Notification {
    const current = this.getNotifications();
    const newNotif: Notification = {
      ...notif,
      id: `notif-${Date.now()}`,
      user_id: 'usr-1',
      created_at: new Date().toISOString(),
    };
    const updated = [newNotif, ...current];
    this.saveNotifications(updated);
    return newNotif;
  }

  static markAllRead(): Notification[] {
    const current = this.getNotifications();
    const updated = current.map((n) => ({ ...n, is_read: true }));
    this.saveNotifications(updated);
    return updated;
  }

  static toggleRead(id: string): Notification[] {
    const current = this.getNotifications();
    const updated = current.map((n) => (n.id === id ? { ...n, is_read: !n.is_read } : n));
    this.saveNotifications(updated);
    return updated;
  }

  static deleteNotification(id: string): Notification[] {
    const current = this.getNotifications();
    const updated = current.filter((n) => n.id !== id);
    this.saveNotifications(updated);
    return updated;
  }

  static clearAll(): Notification[] {
    this.saveNotifications([]);
    return [];
  }
}
