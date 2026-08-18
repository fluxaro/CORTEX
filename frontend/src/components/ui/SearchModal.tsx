import React, { useEffect, useState } from 'react';
import {
  Folder,
  History,
  LayoutDashboard,
  Search,
  ShieldCheck,
  Users,
  X,
} from 'lucide-react';
import { MOCK_REPOSITORIES } from '../../services/mockData';

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectRepo: (repoId: string) => void;
}

export const SearchModal: React.FC<SearchModalProps> = ({ isOpen, onClose, onSelectRepo }) => {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        isOpen ? onClose() : null;
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const filteredRepos = MOCK_REPOSITORIES.filter(
    (r) =>
      r.name.toLowerCase().includes(query.toLowerCase()) ||
      r.description?.toLowerCase().includes(query.toLowerCase()) ||
      r.language?.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 p-4 bg-slate-900/30 backdrop-blur-xs animate-in fade-in duration-100">
      {/* Clean Linear/GitHub Style Modal Container */}
      <div className="w-full max-w-xl bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col">
        
        {/* Search Input Bar */}
        <div className="flex items-center px-4 border-b border-slate-200 bg-white">
          <Search className="h-4 w-4 text-slate-400 mr-3 shrink-0" />
          <input
            type="text"
            placeholder="Search repositories or jump to..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full py-3.5 bg-transparent text-slate-900 placeholder-slate-400 focus:outline-none text-xs sm:text-sm font-medium"
            autoFocus
          />
          {query ? (
            <button
              onClick={() => setQuery('')}
              className="p-1 text-slate-400 hover:text-slate-600 mr-2"
            >
              <X className="h-4 w-4" />
            </button>
          ) : (
            <kbd className="px-2 py-0.5 text-[10px] font-mono font-bold bg-slate-100 text-slate-500 rounded border border-slate-200">
              ESC
            </kbd>
          )}
        </div>

        {/* Search Results */}
        <div className="p-3 max-h-80 overflow-y-auto space-y-4 text-xs">
          
          {/* Repositories Group */}
          <div>
            <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-3 py-1">
              Repositories ({filteredRepos.length})
            </div>
            <div className="mt-1 space-y-1">
              {filteredRepos.map((repo) => (
                <div
                  key={repo.id}
                  onClick={() => {
                    onSelectRepo(repo.id);
                    onClose();
                  }}
                  className="flex items-center justify-between p-2.5 rounded-xl hover:bg-slate-100 cursor-pointer transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <Folder className="h-4 w-4 text-slate-400 shrink-0" />
                    <div>
                      <span className="font-bold text-slate-900">{repo.full_name}</span>
                      <p className="text-[11px] text-slate-500 line-clamp-1">{repo.description}</p>
                    </div>
                  </div>
                  <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">
                    {repo.language || 'TypeScript'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Navigation Commands */}
          <div className="pt-2 border-t border-slate-100">
            <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-3 py-1">
              Navigation
            </div>
            <div className="mt-1 space-y-1">
              <div
                onClick={() => {
                  onSelectRepo('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b');
                  onClose();
                }}
                className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-slate-100 cursor-pointer text-slate-700 font-semibold transition-colors"
              >
                <LayoutDashboard className="h-4 w-4 text-slate-400" />
                <span>Workspace Dashboard</span>
              </div>

              <div
                onClick={() => {
                  onSelectRepo('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b');
                  onClose();
                }}
                className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-slate-100 cursor-pointer text-slate-700 font-semibold transition-colors"
              >
                <ShieldCheck className="h-4 w-4 text-slate-400" />
                <span>Security SAST Findings</span>
              </div>

              <div
                onClick={() => {
                  onSelectRepo('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b');
                  onClose();
                }}
                className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-slate-100 cursor-pointer text-slate-700 font-semibold transition-colors"
              >
                <History className="h-4 w-4 text-slate-400" />
                <span>Scan History & Audit Logs</span>
              </div>

              <div
                onClick={() => {
                  onSelectRepo('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b');
                  onClose();
                }}
                className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-slate-100 cursor-pointer text-slate-700 font-semibold transition-colors"
              >
                <Users className="h-4 w-4 text-slate-400" />
                <span>Organization Members</span>
              </div>
            </div>
          </div>

        </div>

        {/* Minimal Footer */}
        <div className="px-4 py-2.5 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500 font-medium">
          <span>Press <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px]">↵</kbd> to select</span>
          <span>Press <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px]">ESC</kbd> to exit</span>
        </div>

      </div>
    </div>
  );
};
