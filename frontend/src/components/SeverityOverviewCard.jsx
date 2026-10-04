import React from 'react';
import { AlertOctagon, AlertTriangle, AlertCircle, Info, ShieldAlert } from 'lucide-react';

export default function SeverityOverviewCard({ counts }) {
  const severities = [
    {
      key: 'Critical',
      label: 'Critical',
      count: counts?.Critical || 0,
      color: 'text-rose-600',
      bg: 'bg-rose-50',
      border: 'border-rose-200',
      icon: AlertOctagon,
      deduction: '-15 pts/each',
    },
    {
      key: 'High',
      label: 'High',
      count: counts?.High || 0,
      color: 'text-orange-600',
      bg: 'bg-orange-50',
      border: 'border-orange-200',
      icon: AlertTriangle,
      deduction: '-8 pts/each',
    },
    {
      key: 'Medium',
      label: 'Medium',
      count: counts?.Medium || 0,
      color: 'text-amber-600',
      bg: 'bg-amber-50',
      border: 'border-amber-200',
      icon: AlertCircle,
      deduction: '-4 pts/each',
    },
    {
      key: 'Low',
      label: 'Low',
      count: counts?.Low || 0,
      color: 'text-blue-600',
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      icon: Info,
      deduction: '-1 pt/each',
    },
    {
      key: 'Informational',
      label: 'Info',
      count: counts?.Informational || 0,
      color: 'text-slate-600',
      bg: 'bg-slate-50',
      border: 'border-slate-200',
      icon: ShieldAlert,
      deduction: '0 pts',
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
      {severities.map((item) => {
        const Icon = item.icon;
        return (
          <div
            key={item.key}
            className={`p-4 rounded-xl border ${item.border} ${item.bg} flex flex-col justify-between transition hover:shadow-sm`}
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-600">{item.label}</span>
              <Icon className={`w-4 h-4 ${item.color}`} />
            </div>
            <div className="mt-3">
              <span className={`text-2xl font-bold ${item.color}`}>{item.count}</span>
              <p className="text-[11px] text-slate-500 mt-0.5">{item.deduction}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
