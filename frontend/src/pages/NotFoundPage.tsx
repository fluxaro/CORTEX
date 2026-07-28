import React from 'react';
import { Home } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const NotFoundPage: React.FC<{ onNavigateHome: () => void }> = ({ onNavigateHome }) => (
  <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-6 space-y-4">
    <span className="text-7xl font-extrabold text-primary-500 tracking-tight">404</span>
    <h2 className="text-2xl font-bold text-white">Page Not Found</h2>
    <p className="text-xs sm:text-sm text-gray-400 max-w-md">
      The requested repository analysis path or intelligence page does not exist.
    </p>
    <Button onClick={onNavigateHome} variant="primary">
      <Home className="h-4 w-4" />
      <span>Back to Home</span>
    </Button>
  </div>
);
