import React, { useEffect, useState } from 'react';
import { FileCode, Search, ShieldAlert, Sparkles, X } from 'lucide-react';
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
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-150">
      <div className="w-full max-w-xl rounded-2xl glass-panel border border-border/80 shadow-2xl overflow-hidden">
        <div className="flex items-center px-4 border-b border-border/60">
          <Search className="h-5 w-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Search repositories, metrics, security rules, findings... (Esc to close)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full py-4 bg-transparent text-gray-100 placeholder-gray-500 focus:outline-none text-sm"
            autoFocus
          />
          <button onClick={onClose} className="p-1 text-gray-500 hover:text-gray-300">
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="p-4 max-h-96 overflow-y-auto space-y-3">
          <div>
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2">Repositories</span>
            <div className="mt-2 space-y-1">
              {filteredRepos.map((repo) => (
                <div
                  key={repo.id}
                  onClick={() => {
                    onSelectRepo(repo.id);
                    onClose();
                  }}
                  className="flex items-center justify-between p-3 rounded-xl hover:bg-surface-hover/80 cursor-pointer transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-primary-500/10 text-primary-400 rounded-lg">
                      <FileCode className="h-4 w-4" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-200">{repo.full_name}</h4>
                      <p className="text-xs text-gray-400 line-clamp-1">{repo.description}</p>
                    </div>
                  </div>
                  <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                    IQ {repo.iq_score || 90}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2">Quick Navigation</span>
            <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
              <div onClick={() => { onSelectRepo('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b'); onClose(); }} className="p-2.5 rounded-lg border border-border/40 hover:border-primary-500/50 cursor-pointer flex items-center gap-2 text-gray-300">
                <Sparkles className="h-4 w-4 text-purple-400" />
                <span>Repository IQ Summary</span>
              </div>
              <div onClick={() => { onSelectRepo('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b'); onClose(); }} className="p-2.5 rounded-lg border border-border/40 hover:border-rose-500/50 cursor-pointer flex items-center gap-2 text-gray-300">
                <ShieldAlert className="h-4 w-4 text-rose-400" />
                <span>Security SAST Findings</span>
              </div>
            </div>
          </div>
        </div>

        <div className="px-4 py-2 bg-surface-card/60 border-t border-border/40 flex justify-between text-xs text-gray-500">
          <span>Tip: Press <kbd className="px-1.5 py-0.5 bg-surface-hover rounded text-gray-300 font-mono">Ctrl + K</kbd> anytime</span>
          <span>ProjectIQ Search</span>
        </div>
      </div>
    </div>
  );
};
