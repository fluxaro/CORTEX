import React, { useState } from 'react';
import { Cpu, Save, Sliders } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';

export const SettingsPage: React.FC = () => {
  const [provider, setProvider] = useState('mock');
  const [weights, setWeights] = useState({
    static: 15,
    architecture: 15,
    security: 25,
    documentation: 10,
    testing: 15,
    ci: 5,
    git: 5,
    health: 10,
  });

  const handleSave = () => {
    alert('IQ Weights and AI Provider configuration saved!');
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto px-4">
      <div className="pb-4 border-b border-border/80">
        <h1 className="text-2xl font-bold text-white tracking-tight">Settings & Engine Configuration</h1>
        <p className="text-xs text-gray-400">Configure Repository IQ score subsystem weighting and AI Provider abstractions.</p>
      </div>

      {/* AI Provider Abstraction */}
      <Card glass>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Cpu className="h-5 w-5 text-primary-400" />
            <span>AI Provider Selection</span>
          </CardTitle>
          <CardDescription>Select the LLM provider for executing structured prompt templates.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs">
            {['mock', 'openai', 'gemini', 'anthropic', 'ollama'].map((p) => (
              <button
                key={p}
                onClick={() => setProvider(p)}
                className={`p-3 rounded-xl border capitalize text-center transition-all ${
                  provider === p
                    ? 'bg-primary-600/20 border-primary-500 text-white font-semibold'
                    : 'bg-surface-card border-border/60 text-gray-400 hover:text-white'
                }`}
              >
                {p} Provider
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Configurable IQ Subsystem Weights */}
      <Card glass>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sliders className="h-5 w-5 text-purple-400" />
            <span>Subsystem Weighting Matrix (100%)</span>
          </CardTitle>
          <CardDescription>Adjust the contribution percentage of each subsystem engine to the overall Repository IQ score.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 text-xs">
          {Object.entries(weights).map(([key, val]) => (
            <div key={key} className="space-y-1">
              <div className="flex justify-between text-gray-300">
                <span className="capitalize">{key} Subsystem Weight</span>
                <span className="font-semibold text-primary-400">{val}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="50"
                value={val}
                onChange={(e) =>
                  setWeights({ ...weights, [key]: parseInt(e.target.value, 10) })
                }
                className="w-full h-1.5 bg-surface-card rounded-lg appearance-none cursor-pointer accent-primary-500"
              />
            </div>
          ))}

          <div className="pt-4 border-t border-border flex justify-end">
            <Button onClick={handleSave} variant="primary">
              <Save className="h-4 w-4" />
              <span>Save Configuration</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
