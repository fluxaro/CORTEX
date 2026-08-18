import { useEffect, useState } from 'react';
import { BarChart3, Code2, FileText, GitBranch, Github, Layers, LayoutDashboard, ShieldCheck } from 'lucide-react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AddRepoModal } from './components/AddRepoModal';
import { Navbar } from './components/Navbar';
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
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [selectedRepoId, setSelectedRepoId] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'overview' | 'static' | 'architecture' | 'security' | 'documentation' | 'grade'>('overview');

  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isAddRepoOpen, setIsAddRepoOpen] = useState(false);

  const [gradeReport, setGradeReport] = useState<RepositoryGradeReport | null>(null);
  const [staticMetrics, setStaticMetrics] = useState<StaticMetrics | null>(null);
  const [archReport, setArchReport] = useState<ArchitectureReport | null>(null);
  const [secReport, setSecReport] = useState<SecurityReport | null>(null);

  useEffect(() => {
    RepositoryService.getRepositories().then((repos) => {
      setRepositories(repos);
      if (repos.length > 0 && !selectedRepoId) {
        setSelectedRepoId(repos[0].id);
      }
    });
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
          <div className="space-y-8">
            {/* Repository Sub-header (Enterprise Dashboard Header) */}
            <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
              <div className="space-y-2">
                <div className="flex flex-wrap items-center gap-3">
                  <div className="w-10 h-10 rounded-2xl bg-slate-900 text-white flex items-center justify-center font-bold shadow-md">
                    <Github className="h-5 w-5 text-white" />
                  </div>
                  <h1 className="font-display text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                    {selectedRepo.full_name}
                  </h1>
                  <span className="px-3 py-1 rounded-full text-xs font-extrabold bg-purple-50 text-purple-700 border border-purple-200">
                    {gradeReport?.maturity_level || 'Enterprise Ready'}
                  </span>
                </div>
                <div className="flex flex-wrap items-center gap-4 text-xs font-semibold text-slate-500 pt-0.5">
                  <span className="flex items-center gap-1.5 text-slate-700">
                    <GitBranch className="h-3.5 w-3.5 text-slate-400" /> {selectedRepo.default_branch || 'main'}
                  </span>
                  <span>•</span>
                  <span className="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-bold border border-slate-200">
                    {selectedRepo.language || 'TypeScript'}
                  </span>
                  <span>•</span>
                  <span className="text-slate-500">
                    {selectedRepo.description || 'Ingested public repository analysis'}
                  </span>
                </div>
              </div>

              {/* Score Badge Card */}
              <div className="flex items-center gap-4 bg-slate-50 p-3.5 rounded-2xl border border-slate-200/80 shrink-0">
                <GradeBadge grade={gradeReport?.overall_grade || 'A'} size="md" />
                <div className="text-left">
                  <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Repository IQ</div>
                  <div className="font-display text-xl font-extrabold text-slate-900">
                    {gradeReport?.overall_score ? gradeReport.overall_score.toFixed(1) : '92.4'} <span className="text-xs font-semibold text-slate-400">/ 100</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Navigation Tab Bar */}
            <div className="flex items-center gap-2 border-b-2 border-slate-200/80 overflow-x-auto pb-1">
              {[
                { id: 'overview', label: 'Overview', icon: <LayoutDashboard className="h-4 w-4" /> },
                { id: 'static', label: 'Static Analysis', icon: <Code2 className="h-4 w-4" /> },
                { id: 'architecture', label: 'Architecture', icon: <Layers className="h-4 w-4" /> },
                { id: 'security', label: 'Security (SAST)', icon: <ShieldCheck className="h-4 w-4" /> },
                { id: 'documentation', label: 'Documentation', icon: <FileText className="h-4 w-4" /> },
                { id: 'grade', label: 'Grade Report & Narrative', icon: <BarChart3 className="h-4 w-4" /> },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`px-4 py-2.5 rounded-2xl text-xs font-extrabold transition-all whitespace-nowrap flex items-center gap-2 ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  {tab.icon}
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>

            {/* Sub-page Views */}
            {activeTab === 'overview' && gradeReport && <RepoOverviewPage repo={selectedRepo} iqReport={gradeReport} />}
            {activeTab === 'static' && staticMetrics && <StaticAnalysisPage staticMetrics={staticMetrics} />}
            {activeTab === 'architecture' && archReport && <ArchitecturePage architectureReport={archReport} />}
            {activeTab === 'security' && secReport && <SecurityPage securityReport={secReport} />}
            {activeTab === 'documentation' && <DocumentationPage />}
            {activeTab === 'grade' && gradeReport && <RepositoryGradePage gradeReport={gradeReport} />}
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
