import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DashboardPage from './pages/DashboardPage';
import FindingsPage from './pages/FindingsPage';
import MethodologyPage from './pages/MethodologyPage';
import AboutPage from './pages/AboutPage';
import FindingDetailModal from './components/FindingDetailModal';
import RunScanModal from './components/RunScanModal';
import { getDashboard, getFindings, resetAssessment } from './api/client';
import { Shield, AlertTriangle } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState(null);
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedFinding, setSelectedFinding] = useState(null);
  const [isScanModalOpen, setIsScanModalOpen] = useState(false);
  const [isScanning, setIsScanning] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [dash, fList] = await Promise.all([getDashboard(), getFindings()]);
      setDashboardData(dash);
      setFindings(fList);
    } catch (err) {
      console.error('Failed to load assessment data', err);
      setError('Unable to connect to backend server at http://localhost:8000.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleStatusUpdated = (findingUid, newStatus) => {
    // Update local findings state
    setFindings((prev) =>
      prev.map((f) => (f.uid === findingUid ? { ...f, status: newStatus } : f))
    );
    // Reload dashboard to update score live
    loadData();
  };

  const handleScanComplete = (scanResult) => {
    loadData();
    setActiveTab('dashboard');
  };

  const handleResetBaseline = async () => {
    if (window.confirm('Reset all findings back to the clean baseline demo dataset (78/100 Grade B)?')) {
      try {
        await resetAssessment();
        await loadData();
      } catch (err) {
        console.error('Failed to reset', err);
        alert('Failed to reset assessment dataset');
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenScanModal={() => setIsScanModalOpen(true)}
        isScanning={isScanning}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div className="text-xs space-y-1">
              <p className="font-bold">Backend Connection Notice</p>
              <p>{error}</p>
              <p className="text-amber-700">
                Make sure the FastAPI backend is running via <code>uvicorn backend.main:app --port 8000</code>.
              </p>
            </div>
          </div>
        )}

        {loading && !dashboardData ? (
          <div className="flex flex-col items-center justify-center py-24 text-slate-400 space-y-3">
            <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <p className="text-xs font-medium text-slate-500">Loading security assessment data...</p>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && (
              <DashboardPage
                dashboardData={dashboardData}
                onSelectFinding={(f) => setSelectedFinding(f)}
                onViewAllFindings={() => setActiveTab('findings')}
                onOpenScanModal={() => setIsScanModalOpen(true)}
                refreshDashboard={loadData}
                onResetBaseline={handleResetBaseline}
              />
            )}

            {activeTab === 'findings' && (
              <FindingsPage
                findings={findings}
                onSelectFinding={(f) => setSelectedFinding(f)}
                onRefresh={loadData}
              />
            )}

            {activeTab === 'methodology' && <MethodologyPage />}

            {activeTab === 'about' && <AboutPage />}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-6 mt-12 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center gap-1.5 font-medium text-slate-700">
            <Shield className="w-4 h-4 text-blue-600" />
            <span>SIH26163 Security Assessment Platform</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Designed for Smart India Hackathon 2026. Controlled Prototype Environment.
          </p>
        </div>
      </footer>

      {/* Finding Detail Modal */}
      {selectedFinding && (
        <FindingDetailModal
          finding={selectedFinding}
          onClose={() => setSelectedFinding(null)}
          onStatusUpdated={handleStatusUpdated}
        />
      )}

      {/* Run Scan Modal */}
      <RunScanModal
        isOpen={isScanModalOpen}
        onClose={() => setIsScanModalOpen(false)}
        onScanComplete={handleScanComplete}
      />
    </div>
  );
}
