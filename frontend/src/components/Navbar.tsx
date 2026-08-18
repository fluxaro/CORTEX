import React from 'react';
import {
  Bell,
  LogOut,
  Plus,
  Search,
  ShieldCheck,
  User as UserIcon,
} from 'lucide-react';
import { Button } from './ui/Button';

interface NavbarProps {
  onOpenSearch: () => void;
  onOpenAddRepo: () => void;
  onNavigate: (page: string) => void;
  activePage: string;
  isAuthenticated: boolean;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenSearch,
  onOpenAddRepo,
  onNavigate,
  activePage,
  isAuthenticated,
  onLogout,
}) => {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-border/80 glass-panel">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo & Tagline */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => onNavigate('landing')}>
          <div className="p-2 bg-gradient-to-tr from-primary-600 to-accent-purple rounded-xl shadow-glow">
            <ShieldCheck className="h-5 w-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-white tracking-tight">Cortex</span>
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20">
                Enterprise
              </span>
            </div>
            <p className="text-[11px] text-gray-400 hidden sm:block">Know your code before you clone it.</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="hidden lg:flex items-center gap-1">
          <button
            onClick={() => onNavigate('repositories')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activePage === 'repositories' ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-gray-400 hover:text-white'
            }`}
          >
            Repos
          </button>
          <button
            onClick={() => onNavigate('workspaces')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activePage === 'workspaces' ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-gray-400 hover:text-white'
            }`}
          >
            Workspaces
          </button>
          <button
            onClick={() => onNavigate('sync')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activePage === 'sync' ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-gray-400 hover:text-white'
            }`}
          >
            Git Sync
          </button>
          <button
            onClick={() => onNavigate('scans')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activePage === 'scans' ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-gray-400 hover:text-white'
            }`}
          >
            Scan History
          </button>
          <button
            onClick={() => onNavigate('trends')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activePage === 'trends' ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-gray-400 hover:text-white'
            }`}
          >
            Trends
          </button>
          <button
            onClick={() => onNavigate('compare')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activePage === 'compare' ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-gray-400 hover:text-white'
            }`}
          >
            Compare
          </button>
          <button
            onClick={() => onNavigate('audit')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activePage === 'audit' ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-gray-400 hover:text-white'
            }`}
          >
            Audit Logs
          </button>
        </nav>

        {/* Right Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={onOpenSearch}
            className="p-2 rounded-xl border border-border/60 hover:bg-surface-hover text-gray-400 hover:text-white transition-colors"
            title="Search (Ctrl+K)"
          >
            <Search className="h-4 w-4" />
          </button>

          <button
            onClick={() => onNavigate('notifications')}
            className="p-2 rounded-xl border border-border/60 hover:bg-surface-hover text-gray-400 hover:text-white transition-colors relative"
            title="Notifications"
          >
            <Bell className="h-4 w-4" />
            <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-rose-500" />
          </button>

          <Button onClick={onOpenAddRepo} variant="primary" size="sm">
            <Plus className="h-4 w-4" />
            <span>Add Repo</span>
          </Button>

          {isAuthenticated ? (
            <button
              onClick={onLogout}
              className="p-2 rounded-xl border border-border/60 hover:bg-surface-hover text-rose-400 hover:text-rose-300 transition-colors"
              title="Logout"
            >
              <LogOut className="h-4 w-4" />
            </button>
          ) : (
            <Button onClick={() => onNavigate('login')} variant="outline" size="sm">
              <UserIcon className="h-4 w-4" />
              <span>Login</span>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};
