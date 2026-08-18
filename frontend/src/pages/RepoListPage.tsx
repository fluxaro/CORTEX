import React, { useState } from 'react';
import { Filter, GitBranch, Plus, Search, Star } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Repository } from '../services/types';

interface RepoListPageProps {
  repositories: Repository[];
  onSelectRepo: (repoId: string) => void;
  onOpenAddRepo: () => void;
}

export const RepoListPage: React.FC<RepoListPageProps> = ({
  repositories,
  onSelectRepo,
  onOpenAddRepo,
}) => {
  const [search, setSearch] = useState('');
  const [selectedLang, setSelectedLang] = useState<string>('ALL');

  const filtered = repositories.filter((repo) => {
    const matchesSearch =
      repo.name.toLowerCase().includes(search.toLowerCase()) ||
      repo.owner.toLowerCase().includes(search.toLowerCase()) ||
      (repo.description && repo.description.toLowerCase().includes(search.toLowerCase()));
    const matchesLang = selectedLang === 'ALL' || repo.language === selectedLang;
    return matchesSearch && matchesLang;
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto px-4">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-slate-200/80">
        <div>
          <h1 className="font-display text-3xl font-bold text-slate-900 tracking-tight">Repositories</h1>
          <p className="text-xs text-slate-500 font-medium mt-1">Ingested repositories evaluated by Cortex analysis engines.</p>
        </div>
        <Button
          onClick={onOpenAddRepo}
          icon={<Plus className="h-3.5 w-3.5 text-slate-900" />}
          badgeColor="bg-rose-300"
          size="md"
        >
          Add Repository
        </Button>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-3 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Filter repositories by name, description, or owner..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-2xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-blue-600 shadow-sm font-medium"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-slate-400" />
          <select
            value={selectedLang}
            onChange={(e) => setSelectedLang(e.target.value)}
            className="bg-white border border-slate-200 rounded-2xl text-xs font-semibold text-slate-700 px-4 py-2.5 focus:outline-none focus:border-blue-600 shadow-sm"
          >
            <option value="ALL">All Languages</option>
            <option value="Python">Python</option>
            <option value="TypeScript">TypeScript</option>
            <option value="JavaScript">JavaScript</option>
            <option value="Go">Go</option>
          </select>
        </div>
      </div>

      {/* Repository Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((repo) => (
          <div
            key={repo.id}
            onClick={() => onSelectRepo(repo.id)}
            className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm hover:shadow-xl hover:border-blue-400 cursor-pointer transition-all duration-300 flex flex-col justify-between group"
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-display font-bold text-lg text-slate-900 group-hover:text-blue-600 transition-colors">
                    {repo.full_name}
                  </h3>
                  <span className="text-[11px] text-slate-400 font-mono">Branch: {repo.default_branch}</span>
                </div>
                <Badge variant="success" size="sm">
                  IQ {repo.iq_score || 90}
                </Badge>
              </div>

              <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed font-medium">
                {repo.description || 'No description available for this repository.'}
              </p>
            </div>

            <div className="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
              <div className="flex items-center gap-3">
                {repo.language && (
                  <span className="inline-flex items-center gap-1.5 font-semibold text-slate-700">
                    <span className="h-2 w-2 rounded-full bg-blue-600" />
                    {repo.language}
                  </span>
                )}
                <span className="inline-flex items-center gap-1">
                  <Star className="h-3.5 w-3.5 text-amber-500 fill-amber-400" />
                  {repo.stars}
                </span>
                <span className="inline-flex items-center gap-1">
                  <GitBranch className="h-3.5 w-3.5 text-slate-400" />
                  {repo.forks}
                </span>
              </div>
              <Badge variant="outline" size="sm">
                {repo.status}
              </Badge>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
