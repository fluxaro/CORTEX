import React from 'react';
import { cn } from './cn';

export const SkeletonLoader: React.FC<{ className?: string }> = ({ className }) => (
  <div className={cn('animate-pulse bg-surface-hover/60 rounded-md', className)} />
);
