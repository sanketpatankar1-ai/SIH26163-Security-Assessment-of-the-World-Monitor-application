import React from 'react';
import { Shield, ChevronRight, AlertCircle, RefreshCw, ExternalLink } from 'lucide-react';
import ScoreCard from '../components/ScoreCard';
import SeverityOverviewCard from '../components/SeverityOverviewCard';
import CategoryDistributionChart from '../components/CategoryDistributionChart';
import SeverityBadge from '../components/SeverityBadge';
import StatusBadge from '../components/StatusBadge';
import SourceBadge from '../components/SourceBadge';

export default function DashboardPage({
  dashboardData,
  onSelectFinding,
  onViewAllFindings,
  onOpenScanModal,
  refreshDashboard,
  onResetBaseline,
}) {
  const recentFindings = dashboardData?.recent_findings || [];

  return (
    <div className="space-y-4 sm:space-y-6 animate-in fade-in duration-200">
      {/* Top Banner / Assessment Meta */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-3.5 sm:p-4 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex items-center gap-2.5 sm:gap-3 min-w-0">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse flex-shrink-0" />
          <div className="min-w-0">
            <h2 className="text-xs sm:text-sm font-bold text-slate-800 truncate">
              Target: World Monitor (Simulated Target)
            </h2>
            <p className="text-[10px] sm:text-xs text-slate-500 truncate">
              Last Assessed: {dashboardData?.last_assessment ? new Date(dashboardData.last_assessment).toLocaleString() : 'Just now'}
            </p>
          </div>
        </div>

        {/* Action button row */}
        <div className="flex items-center gap-1.5 sm:gap-2 flex-wrap justify-start sm:justify-end">
          <button
            onClick={refreshDashboard}
            title="Refresh dashboard metrics"
            className="inline-flex items-center gap-1 sm:gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-semibold transition active:scale-95"
          >
            <RefreshCw className="w-3.5 h-3.5 text-slate-500" />
            Refresh
          </button>
          {onResetBaseline && (
            <button
              onClick={onResetBaseline}
              title="Reset findings to baseline demo dataset"
              className="inline-flex items-center gap-1 sm:gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg border border-amber-200 bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-semibold transition active:scale-95"
            >
              Reset Baseline
            </button>
          )}
          <button
            onClick={onOpenScanModal}
            className="inline-flex items-center gap-1 sm:gap-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-sm transition active:scale-95"
          >
            Run New Scan
          </button>
        </div>
      </div>

      {/* Primary Metrics Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        {/* Security Score */}
        <div className="lg:col-span-1">
          <ScoreCard
            score={dashboardData?.security_score}
            grade={dashboardData?.grade}
            gradeLabel={dashboardData?.grade_label}
            totalDeduction={
              (dashboardData?.severity_counts?.Critical || 0) * 15 +
              (dashboardData?.severity_counts?.High || 0) * 8 +
              (dashboardData?.severity_counts?.Medium || 0) * 4 +
              (dashboardData?.severity_counts?.Low || 0) * 1
            }
            openFindings={dashboardData?.open_findings}
          />
        </div>

        {/* Severity Count Grid & Category Chart */}
        <div className="lg:col-span-2 space-y-4 sm:space-y-6">
          <SeverityOverviewCard counts={dashboardData?.severity_counts} />
          <CategoryDistributionChart categoryCounts={dashboardData?.category_counts} />
        </div>
      </div>

      {/* Priority Findings Section */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-4 sm:px-6 py-3.5 sm:py-4 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h3 className="text-sm sm:text-base font-bold text-slate-900">Highest Priority Findings</h3>
            <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5">
              Key vulnerabilities requiring developer attention or triage
            </p>
          </div>
          <button
            onClick={onViewAllFindings}
            className="inline-flex items-center gap-0.5 sm:gap-1 text-xs font-semibold text-blue-600 hover:text-blue-800 transition whitespace-nowrap"
          >
            View All ({dashboardData?.total_findings || 0}) <ChevronRight className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          </button>
        </div>

        {/* Mobile View: Cards (< md) */}
        <div className="md:hidden divide-y divide-slate-100">
          {recentFindings.length === 0 ? (
            <div className="py-8 text-center text-xs text-slate-400">
              No findings recorded. Run an assessment to populate data.
            </div>
          ) : (
            recentFindings.map((f) => (
              <div
                key={f.uid}
                onClick={() => onSelectFinding(f)}
                className="p-3.5 space-y-2 hover:bg-blue-50/40 transition cursor-pointer active:bg-slate-100"
              >
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-slate-700">{f.id}</span>
                    <SeverityBadge severity={f.severity} />
                  </div>
                  <div className="flex items-center gap-1.5">
                    <SourceBadge source={f.source} />
                    <StatusBadge status={f.status} />
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-slate-900 leading-snug">{f.title}</h4>
                  <p className="text-[11px] text-slate-500 font-mono mt-0.5 truncate">{f.affected_component}</p>
                </div>

                <div className="flex items-center justify-between pt-1 text-[11px] text-slate-500">
                  <span>{f.category}</span>
                  <span className="text-blue-600 font-semibold inline-flex items-center gap-1">
                    Inspect <ExternalLink className="w-3 h-3" />
                  </span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Desktop / Tablet View: Table (>= md) */}
        <div className="hidden md:block overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-50/75 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
                <th className="py-3 px-4">ID</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Finding & Summary</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Source</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {recentFindings.length === 0 ? (
                <tr>
                  <td colSpan="7" className="py-8 text-center text-slate-400">
                    No findings recorded. Run an assessment to populate data.
                  </td>
                </tr>
              ) : (
                recentFindings.map((f) => (
                  <tr
                    key={f.uid}
                    onClick={() => onSelectFinding(f)}
                    className="hover:bg-blue-50/40 transition cursor-pointer group"
                  >
                    <td className="py-3 px-4 font-mono font-bold text-slate-700">{f.id}</td>
                    <td className="py-3 px-4">
                      <SeverityBadge severity={f.severity} />
                    </td>
                    <td className="py-3 px-4 max-w-xs sm:max-w-md">
                      <p className="font-semibold text-slate-800 group-hover:text-blue-600 transition">
                        {f.title}
                      </p>
                      <p className="text-[11px] text-slate-500 truncate mt-0.5">
                        {f.affected_component}
                      </p>
                    </td>
                    <td className="py-3 px-4 text-slate-600 font-medium">{f.category}</td>
                    <td className="py-3 px-4">
                      <SourceBadge source={f.source} />
                    </td>
                    <td className="py-3 px-4">
                      <StatusBadge status={f.status} />
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectFinding(f);
                        }}
                        className="text-xs font-semibold text-blue-600 hover:text-blue-800 hover:underline inline-flex items-center gap-1"
                      >
                        Inspect <ExternalLink className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
