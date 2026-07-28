import React from 'react';
import { cn } from './cn';

interface ProgressBarProps {
  value: number; // 0 - 100
  label?: string;
  showValue?: boolean;
  color?: 'primary' | 'emerald' | 'amber' | 'rose' | 'purple';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  label,
  showValue = true,
  color = 'primary',
  size = 'md',
  className,
}) => {
  const safeValue = Math.min(Math.max(value, 0), 100);

  const colors = {
    primary: 'bg-primary-500',
    emerald: 'bg-emerald-500',
    amber: 'bg-amber-500',
    rose: 'bg-rose-500',
    purple: 'bg-purple-500',
  };

  const sizes = {
    sm: 'h-1.5',
    md: 'h-2.5',
    lg: 'h-3.5',
  };

  return (
    <div className={cn('w-full space-y-1.5', className)}>
      {(label || showValue) && (
        <div className="flex justify-between items-center text-xs font-medium text-gray-300">
          {label && <span>{label}</span>}
          {showValue && <span>{safeValue.toFixed(1)}%</span>}
        </div>
      )}
      <div className={cn('w-full bg-surface-card rounded-full overflow-hidden border border-border/40', sizes[size])}>
        <div
          className={cn('h-full transition-all duration-500 ease-out rounded-full', colors[color])}
          style={{ width: `${safeValue}%` }}
        />
      </div>
    </div>
  );
};
