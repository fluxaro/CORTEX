import React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle2, Info } from 'lucide-react';
import { cn } from './cn';

interface AlertProps {
  variant?: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  children: React.ReactNode;
  className?: string;
}

export const Alert: React.FC<AlertProps> = ({
  variant = 'info',
  title,
  children,
  className,
}) => {
  const icons = {
    info: <Info className="h-5 w-5 text-blue-400 shrink-0" />,
    success: <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0" />,
    warning: <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0" />,
    error: <AlertCircle className="h-5 w-5 text-rose-400 shrink-0" />,
  };

  const variants = {
    info: 'bg-blue-950/40 border-blue-800/50 text-blue-200',
    success: 'bg-emerald-950/40 border-emerald-800/50 text-emerald-200',
    warning: 'bg-amber-950/40 border-amber-800/50 text-amber-200',
    error: 'bg-rose-950/40 border-rose-800/50 text-rose-200',
  };

  return (
    <div className={cn('p-4 rounded-xl border flex gap-3 text-sm', variants[variant], className)}>
      {icons[variant]}
      <div className="space-y-1">
        {title && <h4 className="font-semibold leading-tight">{title}</h4>}
        <div className="text-xs leading-relaxed opacity-90">{children}</div>
      </div>
    </div>
  );
};
