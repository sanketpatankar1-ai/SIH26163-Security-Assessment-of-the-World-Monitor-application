import React from 'react';
import { ShieldCheck, AlertTriangle, Info } from 'lucide-react';

export default function ScoreCard({ score, grade, gradeLabel, totalDeduction, openFindings }) {
  const numScore = typeof score === 'number' ? score : 78;
  const safeGrade = grade || 'B';
  const safeLabel = gradeLabel || 'Good';

  // Determine color theme based on score
  let scoreColor = 'text-emerald-600 border-emerald-200 bg-emerald-50';
  let badgeColor = 'bg-emerald-100 text-emerald-800';
  if (numScore < 40) {
    scoreColor = 'text-rose-600 border-rose-200 bg-rose-50';
    badgeColor = 'bg-rose-100 text-rose-800';
  } else if (numScore < 60) {
    scoreColor = 'text-orange-600 border-orange-200 bg-orange-50';
    badgeColor = 'bg-orange-100 text-orange-800';
  } else if (numScore < 75) {
    scoreColor = 'text-amber-600 border-amber-200 bg-amber-50';
    badgeColor = 'bg-amber-100 text-amber-800';
  } else if (numScore < 90) {
    scoreColor = 'text-blue-600 border-blue-200 bg-blue-50';
    badgeColor = 'bg-blue-100 text-blue-800';
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:shadow transition">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Prototype Security Posture
          </span>
          <h2 className="text-xl font-bold text-slate-900 mt-1">Security Score</h2>
        </div>
        <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${badgeColor}`}>
          Grade {safeGrade} — {safeLabel}
        </span>
      </div>

      <div className="mt-6 flex items-baseline gap-3">
        <span className="text-5xl font-extrabold tracking-tight text-slate-900">
          {score ?? 100}
        </span>
        <span className="text-xl font-medium text-slate-400">/ 100</span>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-100 rounded-full h-2.5 mt-4 overflow-hidden">
        <div
          className={`h-2.5 rounded-full transition-all duration-500 ${
            score < 50 ? 'bg-rose-500' : score < 75 ? 'bg-amber-500' : 'bg-blue-600'
          }`}
          style={{ width: `${Math.min(100, Math.max(0, score ?? 100))}%` }}
        />
      </div>

      {/* Deduction metrics */}
      <div className="mt-5 grid grid-cols-2 gap-3 pt-4 border-t border-slate-100 text-xs">
        <div>
          <span className="text-slate-500">Total Deductions</span>
          <p className="font-semibold text-rose-600 mt-0.5">-{totalDeduction ?? 0} pts</p>
        </div>
        <div>
          <span className="text-slate-500">Open Findings</span>
          <p className="font-semibold text-slate-800 mt-0.5">{openFindings ?? 0} active</p>
        </div>
      </div>

      {/* Transparent Disclaimer */}
      <div className="mt-4 p-2.5 bg-slate-50 rounded-lg border border-slate-100 flex items-start gap-2 text-[11px] text-slate-500 leading-relaxed">
        <Info className="w-3.5 h-3.5 text-slate-400 flex-shrink-0 mt-0.5" />
        <span>
          Mathematical score based on transparent weights (Critical: -15, High: -8, Med: -4, Low: -1).
          Applies only to open findings in the prototype target.
        </span>
      </div>
    </div>
  );
}
