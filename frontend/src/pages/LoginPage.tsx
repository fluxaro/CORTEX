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

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-semibold text-xs shadow-md shadow-blue-500/20 transition-all hover:scale-[1.02]"
          >
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className="relative my-4 text-center">
          <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-200" /></div>
          <span className="relative px-3 bg-white text-[10px] text-slate-400 uppercase font-bold tracking-wider">Or continue with OAuth</span>
        </div>

        <div className="grid grid-cols-2 gap-3 text-xs">
          <button
            type="button"
            onClick={onLoginSuccess}
            className="flex items-center justify-center gap-2 py-2.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-full font-semibold text-slate-700 transition-all"
          >
            <Github className="h-4 w-4" />
            <span>GitHub</span>
          </button>
          <button
            type="button"
            onClick={onLoginSuccess}
            className="flex items-center justify-center gap-2 py-2.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-full font-semibold text-slate-700 transition-all"
          >
            <Sparkles className="h-4 w-4 text-purple-600" />
            <span>Google</span>
          </button>
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
