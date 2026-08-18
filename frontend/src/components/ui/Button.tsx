import React from 'react';
import { cn } from './cn';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'glass';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  icon?: React.ReactNode;
  badgeColor?: string;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  className,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  icon,
  badgeColor = 'bg-rose-300',
  ...props
}) => {
  const baseStyles =
    'inline-flex items-center justify-between font-display font-bold text-slate-900 bg-slate-100 border-2 border-slate-900 rounded-full shadow-[3.5px_3.5px_0px_0px_#0f172a] hover:bg-white hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[2px_2px_0px_0px_#0f172a] active:translate-x-[3px.5] active:translate-y-[3px.5] active:shadow-none transition-all focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed';

  const sizes = {
    sm: 'text-xs pl-4 pr-1.5 py-1 gap-3.5',
    md: 'text-xs pl-5 pr-2 py-1.5 gap-4',
    lg: 'text-sm pl-6 pr-2.5 py-2 gap-5',
  };

  const badgeSizes = {
    sm: 'w-6 h-6 text-xs',
    md: 'w-7 h-7 text-xs',
    lg: 'w-8 h-8 text-sm',
  };

  return (
    <button
      className={cn(baseStyles, sizes[size], className)}
      disabled={disabled || isLoading}
      {...props}
    >
      <span className="whitespace-nowrap">{children}</span>

      {(icon || isLoading) && (
        <span
          className={cn(
            'rounded-full border border-slate-900 flex items-center justify-center shrink-0 shadow-sm transition-transform group-hover:scale-105',
            badgeColor,
            badgeSizes[size]
          )}
        >
          {isLoading ? (
            <svg className="animate-spin h-3.5 w-3.5 text-slate-900" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          ) : (
            icon
          )}
        </span>
      )}
    </button>
  );
};
