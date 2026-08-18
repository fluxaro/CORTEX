import React, { useState } from 'react';
import { ArrowRight, Github, X } from 'lucide-react';
import { Button } from './ui/Button';
import { Modal } from './ui/Modal';

interface AddRepoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (url: string) => Promise<void>;
}

const POPULAR_REPOS = [
  { name: 'fastapi/fastapi', url: 'https://github.com/fastapi/fastapi' },
  { name: 'vercel/next.js', url: 'https://github.com/vercel/next.js' },
  { name: 'facebook/react', url: 'https://github.com/facebook/react' },
  { name: 'tailwindlabs/tailwindcss', url: 'https://github.com/tailwindlabs/tailwindcss' },
];

export const AddRepoModal: React.FC<AddRepoModalProps> = ({ isOpen, onClose, onSubmit }) => {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url || (!url.startsWith('http') && !url.includes('github.com'))) {
      setError('Please enter a valid public GitHub repository URL.');
      return;
    }
    setError('');
    setIsLoading(true);
    try {
      await onSubmit(url);
      setUrl('');
      onClose();
    } catch {
      setError('Failed to ingest repository. Please verify the URL and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Ingest New Repository"
      subtitle="Analyze code architecture, security scanners, and repository health metrics."
      maxWidth="md"
    >
      <form onSubmit={handleSubmit} className="space-y-5">
        <p className="text-xs text-slate-600 leading-relaxed font-medium">
          Enter any public GitHub repository URL to initiate automated static analysis, architecture dependency mapping, and SAST security checks.
        </p>

        <div className="space-y-1.5">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider">
            Repository URL
          </label>
          <div className="relative flex items-center">
            <Github className="absolute left-3.5 h-4 w-4 text-slate-400 pointer-events-none" />
            <input
              type="text"
              placeholder="https://github.com/owner/repository"
              value={url}
              onChange={(e) => {
                setUrl(e.target.value);
                if (error) setError('');
              }}
              className="w-full pl-10 pr-9 py-2.5 bg-white border border-slate-300 rounded-xl text-sm text-slate-900 placeholder-slate-400 font-medium focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-500/20 transition-all"
              required
              autoFocus
            />
            {url && (
              <button
                type="button"
                onClick={() => setUrl('')}
                className="absolute right-3 p-1 text-slate-400 hover:text-slate-600 rounded-md transition-colors"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
          {error && <p className="text-xs text-rose-600 font-medium mt-1">{error}</p>}
        </div>

        {/* Quick select samples */}
        <div className="space-y-1.5 pt-1">
          <span className="text-[11px] font-semibold text-slate-500">
            Or select a sample repository:
          </span>
          <div className="flex flex-wrap gap-2">
            {POPULAR_REPOS.map((sample) => (
              <button
                key={sample.name}
                type="button"
                onClick={() => {
                  setUrl(sample.url);
                  setError('');
                }}
                className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200/80 border border-slate-200 text-xs font-medium text-slate-700 transition-colors"
              >
                {sample.name}
              </button>
            ))}
          </div>
        </div>

        {/* Form Footer Buttons using UI Button component */}
        <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
          <Button
            type="button"
            onClick={onClose}
            disabled={isLoading}
            variant="ghost"
            size="sm"
          >
            Cancel
          </Button>

          <Button
            type="submit"
            isLoading={isLoading}
            icon={<ArrowRight className="h-3.5 w-3.5 text-slate-900" />}
            badgeColor="bg-cyan-300"
            size="md"
          >
            Ingest & Analyze
          </Button>
        </div>
      </form>
    </Modal>
  );
};
