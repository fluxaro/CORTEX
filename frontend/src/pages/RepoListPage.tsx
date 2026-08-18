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
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-border/80">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Repositories</h1>
          <p className="text-xs text-gray-400">Ingested repositories evaluated by Cortex analysis engines.</p>
        </div>
        <Button onClick={onOpenAddRepo} variant="primary">
          <Plus className="h-4 w-4" />
          <span>Add Repository</span>
        </Button>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
          <input
            type="text"
            placeholder="Filter repositories by name, description, or owner..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-surface-card border border-border/80 rounded-xl text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-primary-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-gray-400" />
          <select
            value={selectedLang}
            onChange={(e) => setSelectedLang(e.target.value)}
            className="bg-surface-card border border-border/80 rounded-xl text-xs text-gray-300 px-3 py-2 focus:outline-none focus:border-primary-500"
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
          <Card
            key={repo.id}
            glass
            onClick={() => onSelectRepo(repo.id)}
            className="cursor-pointer hover:border-primary-500/50 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-gray-100 group-hover:text-primary-400 transition-colors">
                    {repo.full_name}
                  </h3>
                  <span className="text-[11px] text-gray-500 font-mono">Branch: {repo.default_branch}</span>
                </div>
                <Badge variant="success" size="sm">
                  IQ {repo.iq_score || 90}
                </Badge>
              </div>

              <p className="text-xs text-gray-400 line-clamp-2 leading-relaxed">
                {repo.description || 'No description available for this repository.'}
              </p>
            </div>

            <div className="pt-4 mt-4 border-t border-border/40 flex items-center justify-between text-xs text-gray-400">
              <div className="flex items-center gap-3">
                {repo.language && (
                  <span className="inline-flex items-center gap-1">
                    <span className="h-2 w-2 rounded-full bg-primary-400" />
                    {repo.language}
                  </span>
                )}
                <span className="inline-flex items-center gap-1">
                  <Star className="h-3.5 w-3.5 text-amber-400" />
                  {repo.stars}
                </span>
                <span className="inline-flex items-center gap-1">
                  <GitBranch className="h-3.5 w-3.5 text-gray-400" />
                  {repo.forks}
                </span>
              </div>
              <Badge variant="outline" size="sm">
                {repo.status}
              </Badge>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
