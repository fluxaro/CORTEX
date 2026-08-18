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
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="p-3 bg-primary-500/10 border border-primary-500/20 rounded-xl flex items-start gap-3 text-xs text-primary-300">
          <Sparkles className="h-5 w-5 text-primary-400 shrink-0 mt-0.5" />
          <p>
            Enter any public GitHub repository URL. Cortex will ingest metadata, perform static code analysis, architecture pattern detection, SAST security scanning, and calculate Repository IQ score.
          </p>
        </div>

        <div>
          <label className="block text-xs font-semibold text-gray-300 mb-1.5">
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
              className="w-full px-4 py-2.5 bg-surface-card border border-border rounded-xl text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-primary-500 transition-colors"
              required
            />
            <GitBranch className="absolute right-3 top-3 h-4 w-4 text-gray-500" />
          </div>
          {error && <p className="text-xs text-rose-400 mt-1">{error}</p>}
        </div>

        <div className="flex justify-end gap-3 pt-3 border-t border-border">
          <Button type="button" variant="ghost" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" isLoading={isLoading}>
            <Shield className="h-4 w-4" />
            <span>Ingest & Analyze</span>
          </Button>
        </div>
      </form>
    </Modal>
  );
};
