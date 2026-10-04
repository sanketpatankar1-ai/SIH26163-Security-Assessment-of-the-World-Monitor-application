import React from 'react';

const SEVERITY_CONFIG = {
  Critical: {
    bg: 'bg-rose-50 text-rose-700 border-rose-200',
    dot: 'bg-rose-600',
  },
  High: {
    bg: 'bg-orange-50 text-orange-700 border-orange-200',
    dot: 'bg-orange-500',
  },
  Medium: {
    bg: 'bg-amber-50 text-amber-700 border-amber-200',
    dot: 'bg-amber-500',
  },
  Low: {
    bg: 'bg-blue-50 text-blue-700 border-blue-200',
    dot: 'bg-blue-500',
  },
  Informational: {
    bg: 'bg-slate-50 text-slate-700 border-slate-200',
    dot: 'bg-slate-400',
  },
};

export default function SeverityBadge({ severity, size = 'sm' }) {
  const config = SEVERITY_CONFIG[severity] || SEVERITY_CONFIG.Informational;
  const isSm = size === 'sm';

  return (
    <span
      className={`inline-flex items-center gap-1.5 font-medium border rounded-full ${config.bg} ${
        isSm ? 'px-2.5 py-0.5 text-xs' : 'px-3 py-1 text-sm'
      }`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${config.dot}`} />
      {severity}
    </span>
  );
}
