import { Plus, Search, ShieldCheck, Settings } from 'lucide-react';
import { Button } from './ui/Button';

interface NavbarProps {
  onOpenSearch: () => void;
  onOpenAddRepo: () => void;
  onNavigate: (page: string) => void;
  activePage: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenSearch,
  onOpenAddRepo,
  onNavigate,
  activePage,
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
              <span className="font-bold text-lg text-white tracking-tight">ProjectIQ</span>
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20">
                v1.0
              </span>
            </div>
            <p className="text-[11px] text-gray-400 hidden sm:block">Know your code before you clone it.</p>
          </div>
        </div>

        {/* Center Search Bar Trigger */}
        <button
          onClick={onOpenSearch}
          className="hidden md:flex items-center gap-3 px-4 py-2 rounded-xl bg-surface-card border border-border/60 text-xs text-gray-400 hover:border-primary-500/40 hover:text-gray-200 transition-all w-64 shadow-inner"
        >
          <Search className="h-4 w-4 text-gray-400" />
          <span>Search repositories...</span>
          <kbd className="ml-auto px-1.5 py-0.5 text-[10px] font-mono bg-surface-hover rounded text-gray-400">Ctrl K</kbd>
        </button>

        {/* Right Action Controls */}
        <div className="flex items-center gap-3">
          <nav className="flex items-center gap-1 mr-2">
            <button
              onClick={() => onNavigate('landing')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                activePage === 'landing' ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-gray-400 hover:text-white'
              }`}
            >
              Home
            </button>
            <button
              onClick={() => onNavigate('repositories')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                activePage === 'repositories' ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-gray-400 hover:text-white'
              }`}
            >
              Repositories
            </button>
          </nav>

          <Button onClick={onOpenAddRepo} variant="primary" size="sm">
            <Plus className="h-4 w-4" />
            <span>Add Repository</span>
          </Button>

          <button
            onClick={() => onNavigate('settings')}
            className="p-2 rounded-xl border border-border/60 hover:bg-surface-hover text-gray-400 hover:text-white transition-colors"
            title="Settings & IQ Configuration"
          >
            <Settings className="h-4 w-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
