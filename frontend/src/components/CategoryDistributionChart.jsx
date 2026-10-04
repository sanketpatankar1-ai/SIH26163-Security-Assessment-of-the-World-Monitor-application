import React from 'react';
import { Layers } from 'lucide-react';

export default function CategoryDistributionChart({ categoryCounts }) {
  const safeCounts = categoryCounts && typeof categoryCounts === 'object' ? categoryCounts : {};
  const entries = Object.entries(safeCounts);
  const total = entries.reduce((sum, [, count]) => sum + (typeof count === 'number' ? count : 0), 0);

  // Colors for different categories
  const categoryColors = {
    Authentication: 'bg-blue-500',
    Authorization: 'bg-indigo-500',
    'API Security': 'bg-cyan-500',
    'Input Validation': 'bg-amber-500',
    'Communication Security': 'bg-rose-500',
    'Client-Side Security': 'bg-teal-500',
    'Data Storage & Privacy': 'bg-purple-500',
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-600" />
          <h3 className="text-base font-bold text-slate-900">Findings by Assessment Domain</h3>
        </div>
        <span className="text-xs text-slate-500">{total} findings classified</span>
      </div>

      {entries.length === 0 ? (
        <div className="text-center py-8 text-sm text-slate-400">No category data available</div>
      ) : (
        <div className="space-y-3.5">
          {entries.map(([category, count]) => {
            const percentage = total > 0 ? Math.round((count / total) * 100) : 0;
            const barColor = categoryColors[category] || 'bg-slate-500';

            return (
              <div key={category} className="space-y-1">
                <div className="flex items-center justify-between text-xs font-medium">
                  <span className="text-slate-700">{category}</span>
                  <span className="text-slate-500">
                    {count} ({percentage}%)
                  </span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-2 rounded-full ${barColor} transition-all duration-500`}
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
