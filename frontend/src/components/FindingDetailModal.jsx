import React, { useState } from 'react';
import { X, ShieldAlert, CheckCircle2, Terminal, AlertTriangle, Lightbulb, ExternalLink } from 'lucide-react';
import SeverityBadge from './SeverityBadge';
import SourceBadge from './SourceBadge';
import StatusBadge from './StatusBadge';
import { updateFindingStatus } from '../api/client';

export default function FindingDetailModal({ finding, onClose, onStatusUpdated }) {
  const [status, setStatus] = useState(finding?.status || 'Open');
  const [isUpdating, setIsUpdating] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  if (!finding) return null;

  const handleStatusChange = async (newStatus) => {
    try {
      setIsUpdating(true);
      await updateFindingStatus(finding.uid, newStatus);
      setStatus(newStatus);
      setSuccessMsg(`Status updated to "${newStatus}"`);
      if (onStatusUpdated) onStatusUpdated(finding.uid, newStatus);
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err) {
      console.error('Failed to update status', err);
      alert('Failed to update finding status');
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-2.5 sm:p-4 md:p-6">
      <div className="bg-white rounded-xl sm:rounded-2xl border border-slate-200 shadow-2xl max-w-3xl w-full max-h-[92vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="px-4 sm:px-6 py-3.5 sm:py-5 border-b border-slate-200 flex items-start justify-between bg-slate-50/75">
          <div className="pr-2">
            <div className="flex items-center gap-1.5 sm:gap-2.5 flex-wrap">
              <span className="font-mono text-[11px] sm:text-xs font-bold px-2 py-0.5 rounded bg-slate-200 text-slate-800">
                {finding.id}
              </span>
              <SeverityBadge severity={finding.severity} size="sm" />
              <SourceBadge source={finding.source} />
              <span className="text-[11px] sm:text-xs font-medium text-slate-500">• {finding.category}</span>
            </div>
            <h2 className="text-sm sm:text-lg font-bold text-slate-900 mt-1.5 sm:mt-2 leading-snug">
              {finding.title}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition flex-shrink-0"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="px-4 sm:px-6 py-4 sm:py-5 overflow-y-auto space-y-4 sm:space-y-6 text-xs sm:text-sm">
          {/* Status Bar */}
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs font-semibold text-slate-600">Audit Status:</span>
              <StatusBadge status={status} />
              {successMsg && (
                <span className="text-xs font-medium text-emerald-600 ml-1">
                  ✓ {successMsg}
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              <label htmlFor="status-select" className="text-xs text-slate-500 font-medium whitespace-nowrap">
                Change Status:
              </label>
              <select
                id="status-select"
                value={status}
                disabled={isUpdating}
                onChange={(e) => handleStatusChange(e.target.value)}
                className="text-xs font-semibold bg-white border border-slate-300 rounded-md px-2.5 py-1 text-slate-700 hover:border-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="Open">Open</option>
                <option value="In Progress">In Progress</option>
                <option value="Fixed">Fixed</option>
                <option value="Accepted Risk">Accepted Risk</option>
              </select>
            </div>
          </div>

          {/* Description */}
          <div>
            <h4 className="text-[11px] sm:text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">
              Description
            </h4>
            <p className="text-slate-700 leading-relaxed bg-slate-50/50 p-3 rounded-lg border border-slate-100">
              {finding.description}
            </p>
          </div>

          {/* Affected Component */}
          <div>
            <h4 className="text-[11px] sm:text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">
              Affected Component / Target Endpoint
            </h4>
            <code className="text-xs font-mono font-semibold bg-slate-100 text-blue-800 px-2.5 py-1.5 rounded block border border-slate-200 break-all">
              {finding.affected_component}
            </code>
          </div>

          {/* Controlled Evidence */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <h4 className="text-[11px] sm:text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5 text-slate-500" />
                Controlled Evidence & Verification
              </h4>
              <span className="text-[10px] sm:text-[11px] text-slate-400 hidden xs:inline">Safe Observational Inspection</span>
            </div>
            <pre className="p-3 sm:p-3.5 bg-slate-900 text-slate-100 font-mono text-[11px] sm:text-xs rounded-xl overflow-x-auto whitespace-pre-wrap leading-relaxed border border-slate-800 break-all">
              {finding.evidence}
            </pre>
          </div>

          {/* Impact */}
          <div>
            <h4 className="text-[11px] sm:text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5 text-rose-500" />
              Potential Business & Security Impact
            </h4>
            <div className="p-3 bg-rose-50/40 rounded-xl border border-rose-100 text-slate-700 leading-relaxed">
              {finding.impact}
            </div>
          </div>

          {/* Recommendation */}
          <div>
            <h4 className="text-[11px] sm:text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <Lightbulb className="w-3.5 h-3.5 text-amber-500" />
              Developer Remediation Recommendation
            </h4>
            <div className="p-3 sm:p-3.5 bg-emerald-50/40 rounded-xl border border-emerald-100 text-slate-800 whitespace-pre-wrap leading-relaxed text-[11px] sm:text-xs font-mono break-words">
              {finding.recommendation}
            </div>
          </div>

          {/* References / Standards */}
          {finding.cwe_id && (
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
              <span>Standard Classification:</span>
              <a
                href={`https://cwe.mitre.org/data/definitions/${finding.cwe_id.replace('CWE-', '')}.html`}
                target="_blank"
                rel="noreferrer"
                className="font-mono text-blue-600 hover:underline inline-flex items-center gap-1"
              >
                {finding.cwe_id} <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-4 sm:px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
          <span className="text-[10px] sm:text-[11px] text-slate-500 truncate mr-2">
            SIH26163 Assessment Record
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-800 font-semibold rounded-lg text-xs transition active:scale-95"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
