import React, { useState } from 'react';
import { Shield, Play, FileDown, Menu, X, CheckCircle2 } from 'lucide-react';
import { getReportUrl } from '../api/client';

export default function Navbar({ activeTab, setActiveTab, onOpenScanModal, isScanning }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'findings', label: 'All Findings' },
    { id: 'methodology', label: 'Methodology' },
    { id: 'about', label: 'About SIH26163' },
  ];

  const handleNavClick = (tabId) => {
    setActiveTab(tabId);
    setIsMobileMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-30 bg-white border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand */}
          <div className="flex items-center gap-2.5 sm:gap-3 min-w-0">
            <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-sm shadow-blue-200 flex-shrink-0">
              <Shield className="w-5 h-5 sm:w-6 sm:h-6" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-1.5 sm:gap-2 flex-wrap">
                <h1 className="text-sm sm:text-base font-bold text-slate-900 tracking-tight truncate">
                  World Monitor
                </h1>
                <span className="hidden xs:inline-block text-[10px] sm:text-[11px] font-semibold bg-blue-50 text-blue-700 px-1.5 sm:px-2 py-0.5 rounded border border-blue-200 whitespace-nowrap">
                  SIH26163
                </span>
              </div>
              <p className="text-[10px] sm:text-xs text-slate-500 truncate">
                Security Assessment Platform
              </p>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((tab) => (
              <button
                key={tab.id}
                onClick={() => handleNavClick(tab.id)}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-slate-100 text-blue-700 font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>

          {/* Action Buttons & Mobile Hamburger */}
          <div className="flex items-center gap-2">
            {/* Run Assessment Button */}
            <button
              onClick={onOpenScanModal}
              disabled={isScanning}
              title="Run Security Scan"
              className="inline-flex items-center gap-1 sm:gap-1.5 px-2.5 sm:px-3.5 py-1.5 sm:py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-sm transition disabled:opacity-50"
            >
              <Play className={`w-3.5 h-3.5 ${isScanning ? 'animate-spin' : ''}`} />
              <span className="hidden sm:inline">{isScanning ? 'Scanning...' : 'Run Assessment'}</span>
              <span className="sm:hidden">{isScanning ? '...' : 'Scan'}</span>
            </button>

            {/* Download PDF Button */}
            <a
              href={getReportUrl()}
              target="_blank"
              rel="noopener noreferrer"
              title="Download PDF Report"
              className="inline-flex items-center gap-1 sm:gap-1.5 px-2.5 sm:px-3.5 py-1.5 sm:py-2 rounded-md bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold shadow-sm transition"
            >
              <FileDown className="w-3.5 h-3.5 text-slate-500" />
              <span className="hidden sm:inline">Report</span>
              <span className="sm:hidden">PDF</span>
            </a>

            {/* Mobile Hamburger Toggle Button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="lg:hidden p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition"
              aria-label="Toggle Navigation Menu"
            >
              {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Collapsible Navigation Menu */}
      {isMobileMenuOpen && (
        <div className="lg:hidden border-t border-slate-200 bg-white px-4 pt-2 pb-4 space-y-1 shadow-lg animate-in slide-in-from-top-2 duration-150">
          {navItems.map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleNavClick(tab.id)}
              className={`w-full text-left px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                activeTab === tab.id
                  ? 'bg-blue-50 text-blue-700 font-bold border-l-4 border-blue-600'
                  : 'text-slate-700 hover:bg-slate-50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      )}
    </header>
  );
}
