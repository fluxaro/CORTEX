import React from 'react';
import { FolderGit2 } from 'lucide-react';
import { Button } from './Button';

interface EmptyStateProps {
  title: string;
  description: string;
  actionText?: string;
  onAction?: () => void;
  icon?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  actionText,
  onAction,
  icon,
}) => (
  <div className="flex flex-col items-center justify-center p-12 text-center border border-dashed border-border rounded-xl glass-panel my-6">
    <div className="p-3 bg-surface-hover/80 rounded-full text-primary-400 mb-4 border border-border">
      {icon || <FolderGit2 className="h-8 w-8" />}
    </div>
    <h3 className="text-lg font-semibold text-gray-200 mb-1">{title}</h3>
    <p className="text-sm text-gray-400 max-w-sm mb-6">{description}</p>
    {actionText && onAction && (
      <Button onClick={onAction} variant="primary">
        {actionText}
      </Button>
    )}
  </div>
);
