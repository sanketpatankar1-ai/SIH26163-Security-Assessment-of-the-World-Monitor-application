import React, { useState } from 'react';
import { X, Play, CheckCircle2, Loader2, ShieldCheck, Server } from 'lucide-react';
import { triggerAssessment } from '../api/client';

export default function RunScanModal({ isOpen, onClose, onScanComplete }) {
  const [targetUrl, setTargetUrl] = useState('http://localhost:5001');
  const [includeDemo, setIncludeDemo] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const [currentStep, setCurrentStep] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  if (!isOpen) return null;

  const modules = [
    'Authentication & Rate Limiting',
    'Authorization & Broken Access Control',
    'API Security & HTTP Headers',
    'Input Validation & Injection Indicators',
    'Communication & Transport Security',
    'Client-Side Configuration & Cookie Security',
    'Data Storage & Privacy Exposure',
  ];

  const handleStartScan = async () => {
    setIsScanning(true);
    setErrorMsg('');

    try {
      // Step updates for visual feedback
      for (let i = 0; i < modules.length; i++) {
        setCurrentStep(modules[i]);
        await new Promise((res) => setTimeout(res, 250));
      }

      const result = await triggerAssessment(targetUrl, includeDemo);
      setCurrentStep('Calculating Security Score...');
      await new Promise((res) => setTimeout(res, 300));

      if (onScanComplete) {
        onScanComplete(result);
      }
      onClose();
    } catch (err) {
      console.error(err);
      setErrorMsg('Failed to run assessment. Ensure target app or backend is active.');
    } finally {
      setIsScanning(false);
      setCurrentStep('');
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4">
      <div className="bg-white rounded-xl sm:rounded-2xl border border-slate-200 shadow-2xl max-w-lg w-full overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <div className="px-4 sm:px-6 py-3.5 sm:py-5 border-b border-slate-200 flex items-center justify-between bg-slate-50/75">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-blue-600" />
            <h3 className="text-sm sm:text-base font-bold text-slate-900">Run Security Assessment</h3>
          </div>
          <button
            onClick={onClose}
            disabled={isScanning}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 sm:p-6 space-y-4 sm:space-y-5 text-xs sm:text-sm">
          {/* Target URL input */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Target Application URL
            </label>
            <div className="relative">
              <Server className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                disabled={isScanning}
                className="w-full pl-9 pr-3 py-2 text-xs font-mono rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="http://localhost:5001"
              />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">
              Pointing to local simulated World Monitor container/instance.
            </p>
          </div>

          {/* Include Demo Dataset Checkbox */}
          <div className="p-3 bg-blue-50/50 rounded-xl border border-blue-100 flex items-start gap-2.5">
            <input
              type="checkbox"
              id="include-demo"
              checked={includeDemo}
              onChange={(e) => setIncludeDemo(e.target.checked)}
              disabled={isScanning}
              className="mt-0.5 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
            />
            <label htmlFor="include-demo" className="text-xs text-slate-700 select-none cursor-pointer">
              <strong className="text-slate-900 block font-semibold">
                Include Demo Findings Alongside Scan
              </strong>
              Augment active scan with curated demonstration findings for presentation.
            </label>
          </div>

          {/* Scan Progress State */}
          {isScanning && (
            <div className="p-3.5 sm:p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div className="flex items-center gap-2 text-blue-600 font-semibold text-xs truncate">
                <Loader2 className="w-4 h-4 animate-spin flex-shrink-0" />
                <span className="truncate">Executing: {currentStep}</span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
                <div className="bg-blue-600 h-1.5 rounded-full animate-pulse w-3/4" />
              </div>
            </div>
          )}

          {errorMsg && (
            <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-xs text-rose-700 font-medium">
              {errorMsg}
            </div>
          )}
        </div>

        <div className="px-4 sm:px-6 py-3 sm:py-4 border-t border-slate-200 bg-slate-50 flex items-center justify-end gap-2">
          <button
            onClick={onClose}
            disabled={isScanning}
            className="px-3 py-1.5 text-xs font-semibold text-slate-600 hover:text-slate-800 transition active:scale-95"
          >
            Cancel
          </button>
          <button
            onClick={handleStartScan}
            disabled={isScanning}
            className="inline-flex items-center gap-1.5 px-3.5 sm:px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-sm transition disabled:opacity-50 active:scale-95"
          >
            {isScanning ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                Scanning...
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5" />
                Start Scan
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
