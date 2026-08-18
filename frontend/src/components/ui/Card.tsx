import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import { cn } from './cn';

export type CardVariant = 'blue' | 'indigo' | 'cyan' | 'emerald' | 'slate' | 'sky' | 'purple' | 'lime' | 'rose' | 'amber' | 'white' | 'glass';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: CardVariant;
  glass?: boolean;
}

const variantStyles: Record<CardVariant, string> = {
  blue: 'bg-blue-50/90 border-2 border-blue-200/80 text-slate-900 shadow-lg shadow-blue-500/5 hover:border-blue-500 hover:shadow-blue-500/15',
  indigo: 'bg-indigo-50/90 border-2 border-indigo-200/80 text-slate-900 shadow-lg shadow-indigo-500/5 hover:border-indigo-500 hover:shadow-indigo-500/15',
  cyan: 'bg-cyan-50/90 border-2 border-cyan-200/80 text-slate-900 shadow-lg shadow-cyan-500/5 hover:border-cyan-500 hover:shadow-cyan-500/15',
  emerald: 'bg-emerald-50/90 border-2 border-emerald-200/80 text-slate-900 shadow-lg shadow-emerald-500/5 hover:border-emerald-500 hover:shadow-emerald-500/15',
  slate: 'bg-slate-900 border-2 border-slate-800 text-white shadow-xl shadow-slate-950/20 hover:border-blue-500',
  sky: 'bg-sky-50/90 border-2 border-sky-200/80 text-slate-900 shadow-lg shadow-sky-500/5 hover:border-sky-500 hover:shadow-sky-500/15',
  purple: 'bg-purple-50/90 border-2 border-purple-200/80 text-slate-900 shadow-lg shadow-purple-500/5 hover:border-purple-500 hover:shadow-purple-500/15',
  lime: 'bg-lime-50/90 border-2 border-lime-200/80 text-slate-900 shadow-lg shadow-lime-500/5 hover:border-lime-500 hover:shadow-lime-500/15',
  rose: 'bg-rose-50/90 border-2 border-rose-200/80 text-slate-900 shadow-lg shadow-rose-500/5 hover:border-rose-500 hover:shadow-rose-500/15',
  amber: 'bg-amber-50/90 border-2 border-amber-200/80 text-slate-900 shadow-lg shadow-amber-500/5 hover:border-amber-500 hover:shadow-amber-500/15',
  white: 'bg-white border-2 border-slate-200/90 text-slate-900 shadow-sm hover:shadow-xl hover:border-blue-500',
  glass: 'glass-card text-slate-900 border-2 border-blue-200/60',
};

export const Card: React.FC<CardProps> = ({ children, className, variant = 'white', glass = false, ...props }) => {
  const activeVariant = glass ? 'glass' : variant;
  return (
    <div
      className={cn(
        'rounded-[32px] p-7 transition-all duration-300 relative overflow-hidden flex flex-col justify-between group',
        variantStyles[activeVariant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={cn('flex flex-col space-y-1.5 pb-4 mb-2', className)} {...props}>
    {children}
  </div>
);

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({ children, className, ...props }) => (
  <h3 className={cn('font-display text-xl font-extrabold tracking-tight leading-tight', className)} {...props}>
    {children}
  </h3>
);

export const CardDescription: React.FC<React.HTMLAttributes<HTMLParagraphElement>> = ({ children, className, ...props }) => (
  <p className={cn('text-xs font-medium leading-relaxed mt-1 opacity-80', className)} {...props}>
    {children}
  </p>
);

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={cn('relative z-10', className)} {...props}>
    {children}
  </div>
);

// Starburst SVG Vector Shapes (Tech Blue / Cyan / Indigo Palette)
export const StarburstShape: React.FC<{ className?: string; color?: string }> = ({ className, color = 'fill-blue-500/20' }) => (
  <svg viewBox="0 0 100 100" className={cn("w-28 h-28 pointer-events-none transition-transform duration-500 group-hover:scale-110 group-hover:rotate-12", color, className)}>
    <path d="M50 0 L59 31 L89 12 L71 42 L100 50 L71 58 L89 88 L59 69 L50 100 L41 69 L11 88 L29 58 L0 50 L29 42 L11 12 L41 31 Z" />
  </svg>
);

export const StarburstShape2: React.FC<{ className?: string; color?: string }> = ({ className, color = 'fill-cyan-500/20' }) => (
  <svg viewBox="0 0 100 100" className={cn("w-28 h-28 pointer-events-none transition-transform duration-500 group-hover:scale-110 group-hover:-rotate-12", color, className)}>
    <path d="M50 4 L62 26 L86 16 L76 39 L98 50 L76 61 L86 84 L62 74 L50 96 L38 74 L14 84 L24 61 L2 50 L24 39 L14 16 L38 26 Z" />
  </svg>
);

export const ScribbleLoopShape: React.FC<{ className?: string; color?: string }> = ({ className, color = 'stroke-blue-400/60' }) => (
  <svg viewBox="0 0 120 120" className={cn("w-32 h-32 fill-none stroke-[8] pointer-events-none opacity-90 stroke-round", color, className)}>
    <path d="M20 60 C 20 20, 100 20, 100 60 C 100 100, 40 90, 60 50 C 75 20, 110 50, 95 85" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

interface PlayfulCardProps {
  tag: string;
  title: string;
  subtitle?: string;
  variant?: CardVariant;
  arrowPosition?: 'top-right' | 'bottom-right';
  starburstType?: 'blue' | 'cyan' | 'indigo' | 'emerald' | 'scribble' | 'none';
  centerImage?: string;
  centerIcon?: React.ReactNode;
  children?: React.ReactNode;
  onClick?: () => void;
  className?: string;
}

export const PlayfulCard: React.FC<PlayfulCardProps> = ({
  tag,
  title,
  subtitle,
  variant = 'blue',
  arrowPosition = 'top-right',
  starburstType = 'blue',
  centerImage,
  centerIcon,
  children,
  onClick,
  className,
}) => {
  const isDark = variant === 'slate';

  return (
    <Card
      variant={variant}
      onClick={onClick}
      className={cn(
        'min-h-[300px] flex flex-col justify-between cursor-pointer transform hover:-translate-y-2 transition-all duration-300 select-none shadow-md hover:shadow-2xl',
        className
      )}
    >
      {/* Top Header Row */}
      <div className="flex items-start justify-between z-10 w-full">
        {/* Pill Tag */}
        <span
          className={cn(
            'inline-flex items-center px-3.5 py-1 rounded-full text-xs font-extrabold tracking-tight border backdrop-blur-sm',
            isDark
              ? 'border-blue-400/40 text-blue-300 bg-blue-950/60'
              : 'border-slate-300/80 text-slate-900 bg-white/80'
          )}
        >
          {tag}
        </span>

        {/* Top-Right Arrow Button */}
        {arrowPosition === 'top-right' && (
          <button
            type="button"
            className={cn(
              'w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg shadow-md group-hover:scale-110 transition-all',
              isDark
                ? 'bg-blue-600 text-white group-hover:bg-blue-500'
                : 'bg-slate-900 text-white group-hover:bg-blue-600'
            )}
          >
            <ArrowUpRight className="h-5 w-5 stroke-[2.5]" />
          </button>
        )}
      </div>

      {/* Top Right Scribble Accent */}
      {starburstType === 'scribble' && (
        <div className="absolute top-0 right-0 -mt-2 -mr-2">
          <ScribbleLoopShape color={isDark ? 'stroke-cyan-400/40' : 'stroke-blue-400/60'} />
        </div>
      )}

      {/* Optional Center Icon/Thumbnail Container */}
      {centerImage || centerIcon ? (
        <div className="my-4 z-10 flex justify-center">
          <div
            className={cn(
              'w-20 h-20 rounded-2xl backdrop-blur-md border p-2 shadow-inner flex items-center justify-center overflow-hidden',
              isDark
                ? 'bg-slate-800/80 border-slate-700'
                : 'bg-white/60 border-slate-200/80'
            )}
          >
            {centerImage ? (
              <img src={centerImage} alt={title} className="w-full h-full object-cover rounded-xl" />
            ) : (
              centerIcon
            )}
          </div>
        </div>
      ) : null}

      {/* Main Title & Content Section */}
      <div className="z-10 mt-auto pt-4 space-y-2">
        <h3
          className={cn(
            'font-display text-2xl sm:text-3xl font-extrabold tracking-tight leading-tight max-w-[90%]',
            isDark ? 'text-white' : 'text-slate-900'
          )}
        >
          {title}
        </h3>
        {subtitle && (
          <p
            className={cn(
              'text-xs sm:text-sm font-semibold leading-relaxed',
              isDark ? 'text-slate-300' : 'text-slate-600'
            )}
          >
            {subtitle}
          </p>
        )}
        {children && <div className="pt-2">{children}</div>}
      </div>

      {/* Bottom Row (Bottom-Right Arrow + Bottom Starburst Graphic) */}
      <div className="relative w-full z-10 flex items-end justify-between min-h-[44px] pointer-events-none mt-4">
        {/* Bottom Starburst Accent Graphic */}
        <div className="absolute -bottom-6 -left-6 pointer-events-none">
          {starburstType === 'blue' && <StarburstShape color={isDark ? 'fill-blue-500/30' : 'fill-blue-500/20'} />}
          {starburstType === 'cyan' && <StarburstShape2 color={isDark ? 'fill-cyan-500/30' : 'fill-cyan-500/20'} />}
          {starburstType === 'indigo' && <StarburstShape color={isDark ? 'fill-indigo-500/30' : 'fill-indigo-500/20'} />}
          {starburstType === 'emerald' && <StarburstShape2 color={isDark ? 'fill-emerald-500/30' : 'fill-emerald-500/20'} />}
        </div>

        {/* Bottom-Right Arrow Button */}
        {arrowPosition === 'bottom-right' && (
          <div className="ml-auto pointer-events-auto">
            <button
              type="button"
              className={cn(
                'w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg shadow-md group-hover:scale-110 transition-all',
                isDark
                  ? 'bg-blue-600 text-white group-hover:bg-blue-500'
                  : 'bg-slate-900 text-white group-hover:bg-blue-600'
              )}
            >
              <ArrowUpRight className="h-5 w-5 stroke-[2.5]" />
            </button>
          </div>
        )}
      </div>
    </Card>
  );
};
