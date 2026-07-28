import React from 'react';
import { cn } from './cn';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info' | 'purple' | 'outline';
  size?: 'sm' | 'md';
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  className,
  variant = 'default',
  size = 'sm',
  ...props
}) => {
  const baseStyles = 'inline-flex items-center font-medium rounded-full border transition-colors';

  const variants = {
    default: 'bg-gray-800 text-gray-300 border-gray-700',
    success: 'bg-emerald-950/60 text-emerald-400 border-emerald-800/50',
    warning: 'bg-amber-950/60 text-amber-400 border-amber-800/50',
    danger: 'bg-rose-950/60 text-rose-400 border-rose-800/50',
    info: 'bg-blue-950/60 text-blue-400 border-blue-800/50',
    purple: 'bg-purple-950/60 text-purple-400 border-purple-800/50',
    outline: 'bg-transparent text-gray-300 border-gray-700',
  };

  const sizes = {
    sm: 'px-2.5 py-0.5 text-xs gap-1',
    md: 'px-3 py-1 text-sm gap-1.5',
  };

  return (
    <span className={cn(baseStyles, variants[variant], sizes[size], className)} {...props}>
      {children}
    </span>
  );
};
