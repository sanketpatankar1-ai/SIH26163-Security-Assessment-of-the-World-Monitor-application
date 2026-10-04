import React from 'react';

export default function SourceBadge({ source }) {
  const isReal = source === 'Real';

  return (
    <span
      title={
        isReal
          ? 'Identified during active inspection of target application'
          : 'Curated sample finding for demonstration purposes'
      }
      className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold border ${
        isReal
          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
          : 'bg-indigo-50 text-indigo-700 border-indigo-200'
      }`}
    >
      {isReal ? '● Real Scan' : '◈ Demo Data'}
    </span>
  );
}
