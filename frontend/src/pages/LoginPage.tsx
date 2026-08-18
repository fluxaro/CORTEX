import React, { useState } from 'react';
import { Github, Lock, Mail, ShieldCheck, Sparkles } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';

interface LoginPageProps {
  onLoginSuccess: () => void;
  onSwitchToRegister: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess, onSwitchToRegister }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      onLoginSuccess();
    }, 600);
  };

  return (
    <div className="min-h-[75vh] flex items-center justify-center p-4">
      <Card glass className="w-full max-w-md p-6 space-y-6 shadow-2xl border-primary-500/30">
        <div className="text-center space-y-2">
          <div className="p-3 bg-gradient-to-tr from-primary-600 to-accent-purple rounded-2xl shadow-glow w-fit mx-auto">
            <ShieldCheck className="h-8 w-8 text-white" />
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Sign in to Cortex</h2>
          <p className="text-xs text-gray-400">Enterprise Repository Intelligence Platform</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-300 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex.architect@cortex.io"
                className="w-full pl-9 pr-4 py-2 bg-surface-card border border-border/80 rounded-xl text-xs text-gray-200 focus:outline-none focus:border-primary-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-300 mb-1">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full pl-9 pr-4 py-2 bg-surface-card border border-border/80 rounded-xl text-xs text-gray-200 focus:outline-none focus:border-primary-500"
              />
            </div>
          </div>

          <Button type="submit" variant="primary" className="w-full" isLoading={isLoading}>
            <span>Sign In</span>
          </Button>
        </form>

        <div className="relative my-4 text-center">
          <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-border/60" /></div>
          <span className="relative px-2 bg-background text-[10px] text-gray-500 uppercase font-semibold">Or continue with OAuth</span>
        </div>

        <div className="grid grid-cols-2 gap-3 text-xs">
          <Button variant="secondary" onClick={onLoginSuccess} className="w-full">
            <Github className="h-4 w-4" />
            <span>GitHub</span>
          </Button>
          <Button variant="secondary" onClick={onLoginSuccess} className="w-full">
            <Sparkles className="h-4 w-4 text-purple-400" />
            <span>Google</span>
          </Button>
        </div>

        <div className="text-center text-xs text-gray-400 pt-2">
          Don't have an account?{' '}
          <button onClick={onSwitchToRegister} className="text-primary-400 font-semibold hover:underline">
            Register Workspace
          </button>
        </div>
      </Card>
    </div>
  );
};
