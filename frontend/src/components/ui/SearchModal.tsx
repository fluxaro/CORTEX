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
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 p-4 bg-slate-900/40 backdrop-blur-md animate-in fade-in duration-150">
      <div className="w-full max-w-xl rounded-3xl bg-white/95 backdrop-blur-xl border border-slate-200/90 shadow-2xl shadow-slate-900/15 overflow-hidden">
        <div className="flex items-center px-5 border-b border-slate-100 bg-slate-50/50">
          <Search className="h-5 w-5 text-slate-400 mr-3 shrink-0" />
          <input
            type="text"
            placeholder="Search repositories, metrics, security rules, findings... (Esc to close)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full py-4 bg-transparent text-slate-900 placeholder-slate-400 focus:outline-none text-sm font-medium"
            autoFocus
          />
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-slate-700 transition-colors">
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="p-5 max-h-96 overflow-y-auto space-y-4">
          <div>
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-2">Repositories</span>
            <div className="mt-2 space-y-1.5">
              {filteredRepos.map((repo) => (
                <div
                  key={repo.id}
                  onClick={() => {
                    onSelectRepo(repo.id);
                    onClose();
                  }}
                  className="flex items-center justify-between p-3.5 rounded-2xl hover:bg-blue-50/70 border border-transparent hover:border-blue-200/60 cursor-pointer transition-all"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 bg-blue-50 text-blue-600 rounded-xl border border-blue-100">
                      <FileCode className="h-4 w-4" />
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-slate-900">{repo.full_name}</h4>
                      <p className="text-xs text-slate-500 line-clamp-1">{repo.description}</p>
                    </div>
                  </div>
                  <span className="text-xs px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-bold">
                    IQ {repo.iq_score || 90}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-2">Quick Navigation</span>
            <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
              <div onClick={() => { onSelectRepo('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b'); onClose(); }} className="p-3 rounded-2xl border border-slate-200/80 bg-slate-50/50 hover:bg-purple-50 hover:border-purple-200 cursor-pointer flex items-center gap-2.5 text-slate-700 font-semibold transition-all">
                <Sparkles className="h-4 w-4 text-purple-600" />
                <span>Repository IQ Summary</span>
              </div>
              <div onClick={() => { onSelectRepo('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b'); onClose(); }} className="p-3 rounded-2xl border border-slate-200/80 bg-slate-50/50 hover:bg-rose-50 hover:border-rose-200 cursor-pointer flex items-center gap-2.5 text-slate-700 font-semibold transition-all">
                <ShieldAlert className="h-4 w-4 text-rose-600" />
                <span>Security SAST Findings</span>
              </div>
            </div>
          </div>
        </div>

        <div className="px-5 py-3 bg-slate-50 border-t border-slate-100 flex justify-between text-xs text-slate-500 font-medium">
          <span>Tip: Press <kbd className="px-2 py-0.5 bg-white border border-slate-200 rounded-md text-slate-700 font-mono text-[11px]">Ctrl + K</kbd> anytime</span>
          <span className="font-semibold text-slate-600">Cortex Search</span>
        </div>
      </div>
    </div>
  );
};
