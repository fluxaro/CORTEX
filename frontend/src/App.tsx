import { useEffect, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AddRepoModal } from './components/AddRepoModal';
import { Navbar } from './components/Navbar';
import { Badge } from './components/ui/Badge';
import { SearchModal } from './components/ui/SearchModal';
import { ArchitecturePage } from './pages/ArchitecturePage';
import { DocumentationPage } from './pages/DocumentationPage';
import { LandingPage } from './pages/LandingPage';
import { NotFoundPage } from './pages/NotFoundPage';
import { RepoListPage } from './pages/RepoListPage';
import { RepoOverviewPage } from './pages/RepoOverviewPage';
import { RepositoryIQPage } from './pages/RepositoryIQPage';
import { SecurityPage } from './pages/SecurityPage';
import { SettingsPage } from './pages/SettingsPage';
import { StaticAnalysisPage } from './pages/StaticAnalysisPage';
import {
  MOCK_ARCHITECTURE_REPORT,
  MOCK_REPOSITORIES,
  MOCK_REPOSITORY_IQ,
  MOCK_SECURITY_REPORT,
  MOCK_STATIC_METRICS,
} from './services/mockData';
import { RepositoryService } from './services/repositoryService';
import {
  ArchitectureReport,
  Repository,
  RepositoryIQReport,
  SecurityReport,
  StaticMetrics,
} from './services/types';

const queryClient = new QueryClient();

export function AppContent() {
  const [activePage, setActivePage] = useState<string>('landing');
  const [repositories, setRepositories] = useState<Repository[]>(MOCK_REPOSITORIES);
  const [selectedRepoId, setSelectedRepoId] = useState<string>('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b');
  const [activeTab, setActiveTab] = useState<'overview' | 'static' | 'architecture' | 'security' | 'documentation' | 'iq'>('overview');

  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isAddRepoOpen, setIsAddRepoOpen] = useState(false);

  const [iqReport, setIqReport] = useState<RepositoryIQReport>(MOCK_REPOSITORY_IQ);
  const [staticMetrics, setStaticMetrics] = useState<StaticMetrics>(MOCK_STATIC_METRICS);
  const [archReport, setArchReport] = useState<ArchitectureReport>(MOCK_ARCHITECTURE_REPORT);
  const [secReport, setSecReport] = useState<SecurityReport>(MOCK_SECURITY_REPORT);

  useEffect(() => {
    RepositoryService.getRepositories().then(setRepositories);
  }, []);

  useEffect(() => {
    if (selectedRepoId) {
      RepositoryService.getRepositoryIQ(selectedRepoId).then(setIqReport);
      RepositoryService.getStaticMetrics(selectedRepoId).then(setStaticMetrics);
      RepositoryService.getArchitectureReport(selectedRepoId).then(setArchReport);
      RepositoryService.getSecurityReport(selectedRepoId).then(setSecReport);
    }
  }, [selectedRepoId]);

  const handleSelectRepo = (repoId: string) => {
    setSelectedRepoId(repoId);
    setActivePage('repo-details');
    setActiveTab('overview');
  };

  const handleAddRepo = async (url: string) => {
    const newRepo = await RepositoryService.addRepository(url);
    setRepositories((prev) => [newRepo, ...prev]);
    handleSelectRepo(newRepo.id);
  };

  const selectedRepo = repositories.find((r) => r.id === selectedRepoId) || repositories[0];

  return (
    <div className="min-h-screen bg-background flex flex-col font-sans antialiased text-gray-100">
      <Navbar
        onOpenSearch={() => setIsSearchOpen(true)}
        onOpenAddRepo={() => setIsAddRepoOpen(true)}
        onNavigate={setActivePage}
        activePage={activePage}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activePage === 'landing' && (
          <LandingPage
            onNavigate={setActivePage}
            onOpenAddRepo={() => setIsAddRepoOpen(true)}
          />
        )}

        {activePage === 'repositories' && (
          <RepoListPage
            repositories={repositories}
            onSelectRepo={handleSelectRepo}
            onOpenAddRepo={() => setIsAddRepoOpen(true)}
          />
        )}

        {activePage === 'settings' && <SettingsPage />}

        {activePage === 'repo-details' && selectedRepo && (
          <div className="space-y-6">
            {/* Repository Sub-header */}
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-border/80">
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="text-2xl font-bold text-white tracking-tight">{selectedRepo.full_name}</h1>
                  <Badge variant="purple" size="md">{iqReport.maturity_level}</Badge>
                </div>
                <p className="text-xs text-gray-400 mt-0.5">{selectedRepo.description}</p>
              </div>

              <div className="flex items-center gap-2">
                <Badge variant="success">IQ {iqReport.overall_score.toFixed(1)}</Badge>
                <Badge variant="outline">{selectedRepo.language || 'Python'}</Badge>
              </div>
            </div>

            {/* Navigation Tabs */}
            <div className="flex border-b border-border/80 space-x-2 text-xs overflow-x-auto">
              {[
                { id: 'overview', label: 'Overview' },
                { id: 'static', label: 'Static Analysis' },
                { id: 'architecture', label: 'Architecture' },
                { id: 'security', label: 'Security (SAST)' },
                { id: 'documentation', label: 'Documentation' },
                { id: 'iq', label: 'Repository IQ & AI' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`pb-3 px-3 font-medium transition-colors border-b-2 whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-400'
                      : 'border-transparent text-gray-400 hover:text-white'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Sub-page Views */}
            {activeTab === 'overview' && <RepoOverviewPage repo={selectedRepo} iqReport={iqReport} />}
            {activeTab === 'static' && <StaticAnalysisPage staticMetrics={staticMetrics} />}
            {activeTab === 'architecture' && <ArchitecturePage architectureReport={archReport} />}
            {activeTab === 'security' && <SecurityPage securityReport={secReport} />}
            {activeTab === 'documentation' && <DocumentationPage />}
            {activeTab === 'iq' && <RepositoryIQPage iqReport={iqReport} />}
          </div>
        )}

        {activePage !== 'landing' && activePage !== 'repositories' && activePage !== 'settings' && activePage !== 'repo-details' && (
          <NotFoundPage onNavigateHome={() => setActivePage('landing')} />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-border/80 bg-surface/50 py-6 mt-12 text-center text-xs text-gray-500">
        <p>ProjectIQ Platform &copy; 2026. Know your code before you clone it.</p>
      </footer>

      {/* Modals */}
      <SearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        onSelectRepo={handleSelectRepo}
      />

      <AddRepoModal
        isOpen={isAddRepoOpen}
        onClose={() => setIsAddRepoOpen(false)}
        onSubmit={handleAddRepo}
      />
    </div>
  );
}

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}

export default App;
