import React from 'react';
import {
  Bell,
  LogOut,
  Plus,
  Search,
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
    <header className="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-md border-b border-slate-200/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        {/* Logo & Brand Lockup */}
        <div
          className="flex items-center gap-3 cursor-pointer select-none group"
          onClick={() => onNavigate('landing')}
        >
          <div className="w-10 h-10 rounded-xl overflow-hidden shadow-xs border border-slate-200/80 group-hover:shadow-md transition-all">
            <img src="/cortex_logo.jpg" alt="CORTEX Logo" className="w-full h-full object-cover" />
          </div>
          <span className="font-display font-extrabold text-2xl text-slate-900 tracking-tight group-hover:text-blue-600 transition-colors">
            Cortex
          </span>
        </div>

        {/* Floating Center Pill Navigation */}
        <nav className="hidden md:flex items-center gap-1 bg-slate-100/90 p-1.5 rounded-full border border-slate-200/80 shadow-inner">
          <button
            onClick={() => onNavigate('landing')}
            className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
              activePage === 'landing'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Home
          </button>
          <button
            onClick={() => onNavigate('repositories')}
            className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
              activePage === 'repositories'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Repos
          </button>
          <button
            onClick={() => onNavigate('workspaces')}
            className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
              activePage === 'workspaces'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Workspaces
          </button>
          <button
            onClick={() => onNavigate('sync')}
            className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
              activePage === 'sync'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Git Sync
          </button>
          <button
            onClick={() => onNavigate('trends')}
            className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
              activePage === 'trends'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Trends
          </button>
          <button
            onClick={() => onNavigate('compare')}
            className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
              activePage === 'compare'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Compare
          </button>
        </nav>

        {/* Right Actions */}
        <div className="flex items-center gap-3">
          <button
            onClick={onOpenSearch}
            className="p-2 rounded-full border border-slate-200 hover:bg-slate-100 text-slate-600 hover:text-slate-900 transition-colors"
            title="Search (Ctrl+K)"
          >
            <Search className="h-4 w-4" />
          </button>

          <button
            onClick={() => onNavigate('notifications')}
            className="p-2 rounded-full border border-slate-200 hover:bg-slate-100 text-slate-600 hover:text-slate-900 transition-colors relative"
            title="Notifications"
          >
            <Bell className="h-4 w-4" />
            <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-rose-500" />
          </button>

          <Button
            onClick={onOpenAddRepo}
            icon={<Plus className="h-3.5 w-3.5 text-slate-900" />}
            badgeColor="bg-rose-300"
            size="sm"
            className="hidden sm:inline-flex"
          >
            Add Repo
          </Button>

          {isAuthenticated ? (
            <button
              onClick={onLogout}
              className="p-2 rounded-full border-2 border-slate-900 bg-slate-100 hover:bg-rose-50 text-slate-900 shadow-[2px_2px_0px_0px_#0f172a] transition-all"
              title="Logout"
            >
              <LogOut className="h-4 w-4" />
            </button>
          ) : (
            <Button
              onClick={() => onNavigate('login')}
              icon={<UserIcon className="h-3.5 w-3.5 text-slate-900" />}
              badgeColor="bg-amber-300"
              size="sm"
            >
              Log In
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};

