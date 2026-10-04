import React, { useState, useMemo } from 'react';
import { Search, Filter, RefreshCw, SlidersHorizontal, ExternalLink } from 'lucide-react';
import SeverityBadge from '../components/SeverityBadge';
import StatusBadge from '../components/StatusBadge';
import SourceBadge from '../components/SourceBadge';

export default function FindingsPage({ findings, onSelectFinding, onRefresh }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSeverity, setSelectedSeverity] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedStatus, setSelectedStatus] = useState('All');
  const [selectedSource, setSelectedSource] = useState('All');

  const filteredFindings = useMemo(() => {
    return (findings || []).filter((f) => {
      // Search
      const matchesSearch =
        (f.title || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
        (f.id || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
        (f.affected_component || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
        (f.description || '').toLowerCase().includes(searchTerm.toLowerCase());

      // Severity
      const matchesSeverity = selectedSeverity === 'All' || f.severity === selectedSeverity;
      // Category
      const matchesCategory = selectedCategory === 'All' || f.category === selectedCategory;
      // Status
      const matchesStatus = selectedStatus === 'All' || f.status === selectedStatus;
      // Source
      const matchesSource = selectedSource === 'All' || f.source === selectedSource;

      return matchesSearch && matchesSeverity && matchesCategory && matchesStatus && matchesSource;
    });
  }, [findings, searchTerm, selectedSeverity, selectedCategory, selectedStatus, selectedSource]);

  const categories = [
    'All',
    'Authentication',
    'Authorization',
    'API Security',
    'Input Validation',
    'Communication Security',
    'Client-Side Security',
    'Data Storage & Privacy',
  ];

  return (
    <div className="space-y-4 sm:space-y-6 animate-in fade-in duration-200">
      {/* Header & Controls */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 sm:p-5 shadow-sm space-y-3 sm:space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 sm:gap-3">
          <div>
            <h2 className="text-base sm:text-lg font-bold text-slate-900">Security Findings Repository</h2>
            <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5">
              Showing {filteredFindings.length} of {(findings || []).length} findings
            </p>
          </div>
          <button
            onClick={onRefresh}
            className="self-start sm:self-auto inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-semibold transition active:scale-95"
          >
            <RefreshCw className="w-3.5 h-3.5 text-slate-500" />
            Refresh
          </button>
        </div>

        {/* Responsive Filters Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5 sm:gap-3 pt-3 border-t border-slate-100">
          {/* Search */}
          <div className="relative lg:col-span-2">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search ID, keyword, endpoint..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Severity filter */}
          <div>
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="w-full py-1.5 px-2.5 text-xs rounded-lg border border-slate-300 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium text-slate-700"
            >
              <option value="All">Severity: All</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
              <option value="Informational">Informational</option>
            </select>
          </div>

          {/* Category filter */}
          <div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full py-1.5 px-2.5 text-xs rounded-lg border border-slate-300 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium text-slate-700 truncate"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat === 'All' ? 'Category: All' : cat}
                </option>
              ))}
            </select>
          </div>

          {/* Status filter */}
          <div>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full py-1.5 px-2.5 text-xs rounded-lg border border-slate-300 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium text-slate-700"
            >
              <option value="All">Status: All</option>
              <option value="Open">Open</option>
              <option value="In Progress">In Progress</option>
              <option value="Fixed">Fixed</option>
              <option value="Accepted Risk">Accepted Risk</option>
            </select>
          </div>
        </div>
      </div>

      {/* Findings Container */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        {/* Mobile View: Finding Cards (< md) */}
        <div className="md:hidden divide-y divide-slate-100">
          {filteredFindings.length === 0 ? (
            <div className="py-12 text-center text-xs text-slate-400">
              No findings match the selected filters.
            </div>
          ) : (
            filteredFindings.map((f) => (
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
                  <p className="text-[11px] text-slate-500 mt-1 line-clamp-2">{f.description}</p>
                  <p className="text-[11px] text-slate-500 font-mono mt-1 truncate">{f.affected_component}</p>
                </div>

                <div className="flex items-center justify-between pt-1 text-[11px] text-slate-500">
                  <span>{f.category}</span>
                  <span className="text-blue-600 font-semibold inline-flex items-center gap-1">
                    Details <ExternalLink className="w-3 h-3" />
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
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
                <th className="py-3 px-4">ID</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Finding & Summary</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Affected Component</th>
                <th className="py-3 px-4">Source</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredFindings.length === 0 ? (
                <tr>
                  <td colSpan="8" className="py-12 text-center text-slate-400">
                    No findings match the selected filters.
                  </td>
                </tr>
              ) : (
                filteredFindings.map((f) => (
                  <tr
                    key={f.uid}
                    onClick={() => onSelectFinding(f)}
                    className="hover:bg-blue-50/40 transition cursor-pointer group"
                  >
                    <td className="py-3 px-4 font-mono font-bold text-slate-700">{f.id}</td>
                    <td className="py-3 px-4">
                      <SeverityBadge severity={f.severity} />
                    </td>
                    <td className="py-3 px-4 max-w-sm">
                      <p className="font-semibold text-slate-800 group-hover:text-blue-600 transition">
                        {f.title}
                      </p>
                      <p className="text-[11px] text-slate-500 truncate mt-0.5">
                        {(f.description || '').slice(0, 75)}...
                      </p>
                    </td>
                    <td className="py-3 px-4 text-slate-600 font-medium">{f.category}</td>
                    <td className="py-3 px-4 font-mono text-slate-600 text-[11px] truncate max-w-xs">
                      {f.affected_component}
                    </td>
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
                        className="text-xs font-semibold text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                      >
                        View <ExternalLink className="w-3 h-3" />
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
