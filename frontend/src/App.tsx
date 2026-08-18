import { useEffect, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AddRepoModal } from './components/AddRepoModal';
import { Navbar } from './components/Navbar';
import { Badge } from './components/ui/Badge';
import { GradeBadge } from './components/ui/GradeBadge';
import { SearchModal } from './components/ui/SearchModal';
import { ArchitecturePage } from './pages/ArchitecturePage';
import { AuditLogsPage } from './pages/AuditLogsPage';
import { DocumentationPage } from './pages/DocumentationPage';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { MembersPage } from './pages/MembersPage';
import { NotFoundPage } from './pages/NotFoundPage';
import { NotificationsPage } from './pages/NotificationsPage';
import { OrganizationDashboardPage } from './pages/OrganizationDashboardPage';
import { RegisterPage } from './pages/RegisterPage';
import { RepoComparisonPage } from './pages/RepoComparisonPage';
import { RepoListPage } from './pages/RepoListPage';
import { RepoOverviewPage } from './pages/RepoOverviewPage';
import { RepositoryGradePage } from './pages/RepositoryGradePage';
import { RepoSyncPage } from './pages/RepoSyncPage';
import { ScanHistoryPage } from './pages/ScanHistoryPage';
import { SecurityPage } from './pages/SecurityPage';
import { SettingsPage } from './pages/SettingsPage';
import { StaticAnalysisPage } from './pages/StaticAnalysisPage';
import { TrendAnalysisPage } from './pages/TrendAnalysisPage';
import { WorkspaceDashboardPage } from './pages/WorkspaceDashboardPage';
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
  RepositoryGradeReport,
  SecurityReport,
  StaticMetrics,
} from './services/types';

const queryClient = new QueryClient();

export function AppContent() {
  const [activePage, setActivePage] = useState<string>('landing');
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(true);
  const [repositories, setRepositories] = useState<Repository[]>(MOCK_REPOSITORIES);
  const [selectedRepoId, setSelectedRepoId] = useState<string>('1a9e8b7c-6d5f-4e3d-2c1b-0a9f8e7d6c5b');
  const [activeTab, setActiveTab] = useState<'overview' | 'static' | 'architecture' | 'security' | 'documentation' | 'grade'>('overview');

  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isAddRepoOpen, setIsAddRepoOpen] = useState(false);

  const [gradeReport, setGradeReport] = useState<RepositoryGradeReport>(MOCK_REPOSITORY_IQ);
  const [staticMetrics, setStaticMetrics] = useState<StaticMetrics>(MOCK_STATIC_METRICS);
  const [archReport, setArchReport] = useState<ArchitectureReport>(MOCK_ARCHITECTURE_REPORT);
  const [secReport, setSecReport] = useState<SecurityReport>(MOCK_SECURITY_REPORT);

  useEffect(() => {
    RepositoryService.getRepositories().then(setRepositories);
  }, []);

  useEffect(() => {
    if (selectedRepoId) {
      RepositoryService.getRepositoryIQ(selectedRepoId).then(setGradeReport);
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
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans antialiased text-slate-900">
      <Navbar
        onOpenSearch={() => setIsSearchOpen(true)}
        onOpenAddRepo={() => setIsAddRepoOpen(true)}
        onNavigate={setActivePage}
        activePage={activePage}
        isAuthenticated={isAuthenticated}
        onLogout={() => setIsAuthenticated(false)}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activePage === 'landing' && (
          <LandingPage
            onNavigate={setActivePage}
            onOpenAddRepo={() => setIsAddRepoOpen(true)}
          />
        )}

        {activePage === 'login' && (
          <LoginPage
            onLoginSuccess={() => {
              setIsAuthenticated(true);
              setActivePage('workspaces');
            }}
            onSwitchToRegister={() => setActivePage('register')}
          />
        )}

        {activePage === 'register' && (
          <RegisterPage
            onRegisterSuccess={() => {
              setIsAuthenticated(true);
              setActivePage('workspaces');
            }}
            onSwitchToLogin={() => setActivePage('login')}
          />
        )}

        {activePage === 'repositories' && (
          <RepoListPage
            repositories={repositories}
            onSelectRepo={handleSelectRepo}
            onOpenAddRepo={() => setIsAddRepoOpen(true)}
          />
        )}

        {activePage === 'workspaces' && <WorkspaceDashboardPage onNavigate={setActivePage} />}
        {activePage === 'org' && <OrganizationDashboardPage />}
        {activePage === 'members' && <MembersPage />}
        {activePage === 'sync' && <RepoSyncPage />}
        {activePage === 'scans' && <ScanHistoryPage />}
        {activePage === 'trends' && <TrendAnalysisPage />}
        {activePage === 'compare' && <RepoComparisonPage />}
        {activePage === 'notifications' && <NotificationsPage />}
        {activePage === 'audit' && <AuditLogsPage />}
        {activePage === 'settings' && <SettingsPage />}

        {activePage === 'repo-details' && selectedRepo && (
          <div className="space-y-6">
            {/* Repository Sub-header */}
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-slate-200/80">
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="font-display text-3xl font-bold text-slate-900 tracking-tight">{selectedRepo.full_name}</h1>
                  <Badge variant="purple" size="md">{gradeReport.maturity_level}</Badge>
                </div>
                <p className="text-xs text-slate-500 font-medium mt-1">{selectedRepo.description}</p>
              </div>

              <div className="flex items-center gap-3">
                <GradeBadge grade={gradeReport.overall_grade || 'C'} size="sm" />
                <Badge variant="success">Score {gradeReport.overall_score.toFixed(1)}</Badge>
                <Badge variant="outline">{selectedRepo.language || 'Python'}</Badge>
              </div>
            </div>

            {/* Navigation Pill Tabs */}
            <div className="flex items-center gap-1 bg-slate-100/90 p-1.5 rounded-full border border-slate-200/80 shadow-inner overflow-x-auto w-fit">
              {[
                { id: 'overview', label: 'Overview' },
                { id: 'static', label: 'Static Analysis' },
                { id: 'architecture', label: 'Architecture' },
                { id: 'security', label: 'Security (SAST)' },
                { id: 'documentation', label: 'Documentation' },
                { id: 'grade', label: 'Grade Report & Narrative' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`px-4 py-2 rounded-full text-xs font-semibold transition-all whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Sub-page Views */}
            {activeTab === 'overview' && <RepoOverviewPage repo={selectedRepo} iqReport={gradeReport} />}
            {activeTab === 'static' && <StaticAnalysisPage staticMetrics={staticMetrics} />}
            {activeTab === 'architecture' && <ArchitecturePage architectureReport={archReport} />}
            {activeTab === 'security' && <SecurityPage securityReport={secReport} />}
            {activeTab === 'documentation' && <DocumentationPage />}
            {activeTab === 'grade' && <RepositoryGradePage gradeReport={gradeReport} />}
          </div>
        )}

        {![
          'landing',
          'login',
          'register',
          'repositories',
          'workspaces',
          'org',
          'members',
          'sync',
          'scans',
          'trends',
          'compare',
          'notifications',
          'audit',
          'settings',
          'repo-details',
        ].includes(activePage) && <NotFoundPage onNavigateHome={() => setActivePage('landing')} />}
      </main>

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

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}
