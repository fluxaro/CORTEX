import React, { useState } from 'react';
import { ArrowRight, Github, Lock, Mail, ShieldCheck, Sparkles } from 'lucide-react';
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
      <div className="w-full max-w-md p-8 rounded-3xl bg-white border border-slate-200/90 shadow-2xl shadow-slate-900/10 space-y-6">
        <div className="text-center space-y-3">
          <img src="/cortex_logo.jpg" alt="CORTEX Logo" className="w-14 h-14 rounded-2xl mx-auto border border-slate-200 shadow-sm" />
          <h2 className="font-display text-2xl font-bold text-slate-900 tracking-tight">Sign in to Cortex</h2>
          <p className="text-xs text-slate-500 font-medium">Enterprise Repository Intelligence Platform</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-4 top-3.5 h-4 w-4 text-slate-400" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex.architect@cortex.io"
                className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-blue-600 focus:bg-white transition-all shadow-sm font-medium"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Password</label>
            <div className="relative">
              <Lock className="absolute left-4 top-3.5 h-4 w-4 text-slate-400" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-blue-600 focus:bg-white transition-all shadow-sm font-medium"
              />
            </div>
          </div>

          <Button
            type="submit"
            isLoading={isLoading}
            icon={<ArrowRight className="h-4 w-4 text-slate-900" />}
            badgeColor="bg-blue-300"
            size="lg"
            className="w-full"
          >
            Sign In
          </Button>
        </form>

        <div className="relative my-4 text-center">
          <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-200" /></div>
          <span className="relative px-3 bg-white text-[10px] text-slate-400 uppercase font-bold tracking-wider">Or continue with OAuth</span>
        </div>

        <div className="grid grid-cols-2 gap-3 text-xs">
          <Button
            type="button"
            onClick={onLoginSuccess}
            icon={<Github className="h-3.5 w-3.5 text-slate-900" />}
            badgeColor="bg-slate-300"
            size="md"
            className="w-full"
          >
            GitHub
          </Button>
          <Button
            type="button"
            onClick={onLoginSuccess}
            icon={<Sparkles className="h-3.5 w-3.5 text-slate-900" />}
            badgeColor="bg-purple-300"
            size="md"
            className="w-full"
          >
            Google
          </Button>
        </div>

        <div className="text-center text-xs text-slate-500 font-medium pt-2">
          Don't have an account?{' '}
          <button onClick={onSwitchToRegister} className="text-blue-600 font-bold hover:underline">
            Register Workspace
          </button>
        </div>
      </div>
    </div>
  );
};
