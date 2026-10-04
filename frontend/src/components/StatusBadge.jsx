import React from 'react';

const STATUS_STYLES = {
  Open: 'bg-rose-50 text-rose-700 border-rose-200',
  'In Progress': 'bg-amber-50 text-amber-700 border-amber-200',
  Fixed: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  'Accepted Risk': 'bg-slate-100 text-slate-700 border-slate-300',
};

export default function StatusBadge({ status }) {
  const style = STATUS_STYLES[status] || STATUS_STYLES.Open;

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${style}`}>
      {status}
    </span>
  );
}
