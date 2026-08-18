import React, { useState } from 'react';
import { GitBranch, Shield, Sparkles } from 'lucide-react';
import { Button } from './ui/Button';
import { Modal } from './ui/Modal';

interface AddRepoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (url: string) => Promise<void>;
}

export const AddRepoModal: React.FC<AddRepoModalProps> = ({ isOpen, onClose, onSubmit }) => {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url || (!url.startsWith('http') && !url.includes('github.com'))) {
      setError('Please enter a valid GitHub repository URL.');
      return;
    }
    setError('');
    setIsLoading(true);
    try {
      await onSubmit(url);
      setUrl('');
      onClose();
    } catch {
      setError('Failed to ingest repository. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Ingest New Repository" maxWidth="md">
      <form onSubmit={handleSubmit} className="space-y-5">
        <div className="p-4 bg-blue-50/80 border border-blue-200/80 rounded-2xl flex items-start gap-3 text-xs text-blue-900 leading-relaxed shadow-sm">
          <Sparkles className="h-5 w-5 text-blue-600 shrink-0 mt-0.5" />
          <p>
            Enter any public GitHub repository URL. Cortex will analyze code structure, detect architectural patterns, run SAST security scanners, and calculate the Repository IQ score.
          </p>
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
            GitHub Repository URL
          </label>
          <div className="relative">
            <input
              type="text"
              placeholder="https://github.com/owner/repository"
              value={url}
              onChange={(e) => {
                setUrl(e.target.value);
                if (error) setError('');
              }}
              className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-blue-600 focus:bg-white focus:ring-4 focus:ring-blue-500/10 transition-all shadow-sm font-medium"
              required
            />
            <GitBranch className="absolute right-4 top-3.5 h-4 w-4 text-slate-400" />
          </div>
          {error && <p className="text-xs text-rose-500 font-medium mt-1.5">{error}</p>}
        </div>

        <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
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
            icon={<Shield className="h-3.5 w-3.5 text-slate-900" />}
            badgeColor="bg-emerald-300"
            size="md"
          >
            Ingest & Analyze
          </Button>
        </div>
      </form>
    </Modal>
  );
};
