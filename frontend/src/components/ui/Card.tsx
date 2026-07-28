import React from 'react';
import { cn } from './cn';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  glass?: boolean;
}

export const Card: React.FC<CardProps> = ({ children, className, glass = true, ...props }) => {
  return (
    <div
      className={cn(
        'rounded-xl border p-5 transition-all duration-200',
        glass ? 'glass-card border-border' : 'bg-surface-card border-border',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={cn('flex flex-col space-y-1.5 pb-3 border-b border-border/50 mb-4', className)} {...props}>
    {children}
  </div>
);

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({ children, className, ...props }) => (
  <h3 className={cn('text-lg font-semibold text-gray-100 tracking-tight', className)} {...props}>
    {children}
  </h3>
);

export const CardDescription: React.FC<React.HTMLAttributes<HTMLParagraphElement>> = ({ children, className, ...props }) => (
  <p className={cn('text-xs text-gray-400', className)} {...props}>
    {children}
  </p>
);

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={cn('', className)} {...props}>
    {children}
  </div>
);
