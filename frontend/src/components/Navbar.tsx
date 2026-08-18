import React from 'react';
import {
  Bell,
  LogOut,
  Plus,
  Search,
  User as UserIcon,
} from 'lucide-react';

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
        
        {/* Logo & Brand */}
        <div className="flex items-center gap-3 cursor-pointer group" onClick={() => onNavigate('landing')}>
          <div className="relative w-10 h-10 rounded-xl overflow-hidden shadow-sm group-hover:scale-105 transition-transform border border-slate-200">
            <img src="/cortex_logo.jpg" alt="CORTEX Logo" className="w-full h-full object-cover" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-display font-bold text-2xl text-slate-900 tracking-tight">Cortex</span>
              <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-blue-50 text-blue-600 border border-blue-200/60">
                v1.0
              </span>
            </div>
          </div>
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

          <button
            onClick={onOpenAddRepo}
            className="hidden sm:flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-2 rounded-full shadow-md shadow-blue-500/20 transition-all hover:scale-105"
          >
            <Plus className="h-4 w-4" />
            <span>Add Repo</span>
          </button>

          {isAuthenticated ? (
            <button
              onClick={onLogout}
              className="p-2 rounded-full border border-slate-200 hover:bg-rose-50 text-rose-600 transition-colors"
              title="Logout"
            >
              <LogOut className="h-4 w-4" />
            </button>
          ) : (
            <button
              onClick={() => onNavigate('login')}
              className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold px-5 py-2 rounded-full shadow-sm transition-all hover:scale-105"
            >
              <UserIcon className="h-3.5 w-3.5" />
              <span>Log In</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

