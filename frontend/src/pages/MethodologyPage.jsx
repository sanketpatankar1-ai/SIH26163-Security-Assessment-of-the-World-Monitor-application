import React from 'react';
import { Calculator, ShieldCheck, CheckCircle2, AlertOctagon, Scale, BookOpen } from 'lucide-react';

export default function MethodologyPage() {
  const scoringTable = [
    { severity: 'Critical', points: '-15 pts', color: 'text-rose-600', desc: 'Flaws allowing immediate full compromise or unauthorized admin access' },
    { severity: 'High', points: '-8 pts', color: 'text-orange-600', desc: 'Significant flaws with high impact, such as unauthenticated data access' },
    { severity: 'Medium', points: '-4 pts', color: 'text-amber-600', desc: 'Flaws requiring specific conditions or moderate impact, e.g. missing CSP' },
    { severity: 'Low', points: '-1 pt', color: 'text-blue-600', desc: 'Minor security issues or deviation from hardening best practices' },
    { severity: 'Informational', points: '0 pts', color: 'text-slate-500', desc: 'Informational observations, technology banners, no direct risk' },
  ];

  const domains = [
    { name: 'Authentication & Sessions', icon: '🔑', focus: 'Rate limiting, weak credentials, predictable tokens, session lifetime' },
    { name: 'Authorization & Access Control', icon: '🛡️', focus: 'Broken access control (OWASP #1), admin endpoint exposure, RBAC enforcement' },
    { name: 'API Security & Headers', icon: '🌐', focus: 'HTTP security headers (CSP, X-Frame-Options), CORS wildcards, method enforcement' },
    { name: 'Input Validation & Handling', icon: '📝', focus: 'Reflected input indicators, verbose stack traces, error message leakage' },
    { name: 'Communication Security', icon: '🔒', focus: 'HTTP vs HTTPS, plaintext credential transmission, HSTS transport policy' },
    { name: 'Client-Side Security', icon: '💻', focus: 'Cookie security flags (HttpOnly, Secure, SameSite), info disclosure' },
    { name: 'Data Storage & Privacy', icon: '🗄️', focus: 'Exposed environment variables, debug diagnostics, data minimization' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-4 sm:space-y-8 animate-in fade-in duration-200">
      {/* Overview Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 sm:p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center flex-shrink-0">
            <Scale className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base sm:text-xl font-bold text-slate-900 leading-snug">
              Security Assessment Methodology & Scoring
            </h2>
            <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5">
              Transparent, deterministic evaluation framework for SIH26163
            </p>
          </div>
        </div>
        <p className="mt-3 sm:mt-4 text-xs sm:text-sm text-slate-600 leading-relaxed">
          The World Monitor Security Assessment Platform uses a modular, transparent, and reproducible
          auditing methodology. Rather than fabricating arbitrary scores, the platform calculates
          a <strong>Prototype Security Score</strong> based on open, active findings across seven security domains.
        </p>
      </div>

      {/* Scoring Formula Card */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 sm:p-6 shadow-sm space-y-3 sm:space-y-4">
        <div className="flex items-center gap-2 text-slate-900 font-bold text-sm sm:text-base">
          <Calculator className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600" />
          <h3>Prototype Scoring Mathematical Model</h3>
        </div>

        <div className="p-3 sm:p-4 bg-slate-900 text-slate-100 rounded-xl font-mono text-[11px] sm:text-xs leading-relaxed overflow-x-auto">
          <code>
            Score = MAX( 0, 100 - ∑ ( Count(Open Findings at Severity_i) × Deduction_i ) )
          </code>
        </div>

        <p className="text-[11px] sm:text-xs text-slate-600 leading-relaxed">
          * Notice that deductions apply <strong>only to findings with status "Open"</strong>. When a team
          or developer mitigates an issue and marks it as <strong>"Fixed"</strong>, the deduction is removed
          and the application's security score automatically recovers.
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left border-collapse min-w-[320px]">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase">
                <th className="py-2.5 px-3">Severity</th>
                <th className="py-2.5 px-3">Point Deduction</th>
                <th className="py-2.5 px-3">Evaluation Criteria</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {scoringTable.map((row) => (
                <tr key={row.severity}>
                  <td className={`py-2.5 px-3 font-bold ${row.color}`}>{row.severity}</td>
                  <td className="py-2.5 px-3 font-mono font-bold text-slate-800">{row.points}</td>
                  <td className="py-2.5 px-3 text-slate-600">{row.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 7 Assessment Domains */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 sm:p-6 shadow-sm space-y-3 sm:space-y-4">
        <div className="flex items-center gap-2 text-slate-900 font-bold text-sm sm:text-base">
          <BookOpen className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600" />
          <h3>The 7 Security Assessment Domains</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-3.5">
          {domains.map((dom) => (
            <div key={dom.name} className="p-3 sm:p-3.5 rounded-lg border border-slate-200 bg-slate-50/50">
              <div className="flex items-center gap-2 font-bold text-xs text-slate-800">
                <span>{dom.icon}</span>
                <span>{dom.name}</span>
              </div>
              <p className="text-[11px] text-slate-600 mt-1.5 leading-relaxed">{dom.focus}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Ethical & Safe Testing Disclosure */}
      <div className="bg-emerald-50 rounded-xl border border-emerald-200 p-4 sm:p-6 space-y-2 text-xs text-emerald-900 leading-relaxed">
        <h4 className="font-bold flex items-center gap-1.5 text-xs sm:text-sm">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          Ethical Security Testing & Scope Boundaries
        </h4>
        <p>
          This prototype strictly follows ethical security guidelines:
        </p>
        <ul className="list-disc pl-5 space-y-1 mt-2 text-emerald-800 text-[11px] sm:text-xs">
          <li>Assessment is performed strictly against the designated local or simulated World Monitor instance.</li>
          <li>No destructive testing, fuzzing, or Denial of Service (DoS) attacks are conducted.</li>
          <li>Observational inspection (checking headers, responses, status codes) is favored over intrusive exploitation.</li>
          <li>Curated demo findings are clearly demarcated from real live scan results.</li>
        </ul>
      </div>
    </div>
  );
}
