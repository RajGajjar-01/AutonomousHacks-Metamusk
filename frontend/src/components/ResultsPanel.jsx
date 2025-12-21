import { useState } from 'react'
import AgentCard from './AgentCard'

function ResultsPanel({ result, language }) {
  const [expandedAgents, setExpandedAgents] = useState({
    Scanner: false,
    Fixer: true,
    Validator: false,
  })

  const toggleAgent = agent => {
    setExpandedAgents(prev => ({
      ...prev,
      [agent]: !prev[agent],
    }))
  }

  if (!result) return null

  return (
    <div className="space-y-6 animate-fadeIn w-full">
      {/* Status Header */}
      <div
        className={`alert ${result.success ? 'alert-success' : 'alert-error'} shadow-lg border border-base-content/10 bg-base-200`}
      >
        {result.success ? (
          <svg className="w-6 h-6 stroke-current" viewBox="0 0 24 24" fill="none" strokeWidth="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
        ) : (
          <svg className="w-6 h-6 stroke-current" viewBox="0 0 24 24" fill="none" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
        )}
        <div>
          <h3 className="font-bold">{result.success ? 'Success' : 'Failed'}</h3>
          <div className="text-xs">{result.message}</div>
        </div>
        <div className="badge badge-lg bg-base-100/20 border-none text-current font-mono">
          {result.workflow_metadata?.total_time}s
        </div>
      </div>

      {/* Summary Stats */}
      {result.summary && (
        <div className="stats stats-vertical lg:stats-horizontal shadow-lg w-full bg-base-200 border border-base-content/10">
          <div className="stat">
            <div className="stat-figure text-error">
              <svg
                className="inline-block w-8 h-8 stroke-current"
                viewBox="0 0 24 24"
                fill="none"
                strokeWidth="2"
              >
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
            </div>
            <div className="stat-title">Errors Found</div>
            <div className="stat-value text-error">{result.summary.errors_found || 0}</div>
            <div className="stat-desc">Issues detected</div>
          </div>

          <div className="stat">
            <div className="stat-figure text-success">
              <svg
                className="inline-block w-8 h-8 stroke-current"
                viewBox="0 0 24 24"
                fill="none"
                strokeWidth="2"
              >
                <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
              </svg>
            </div>
            <div className="stat-title">Fixed</div>
            <div className="stat-value text-success">{result.summary.errors_fixed || 0}</div>
            <div className="stat-desc">Auto-corrected</div>
          </div>

          <div className="stat">
            <div className="stat-title">Confidence</div>
            <div className="stat-value">
              {((result.summary.validation_score || 0) * 100).toFixed(0)}%
            </div>
            <div className="stat-desc">Validation Score</div>
          </div>

          <div className="stat">
            <div className="stat-title">Iterations</div>
            <div className="stat-value">{result.workflow_metadata?.iterations || 1}</div>
            <div className="stat-desc">Refinement loops</div>
          </div>
        </div>
      )}

      {/* Fixed Code Display */}
      {result.final_code && (
        <div className="card bg-base-200 shadow-lg border border-success/20">
          <div className="card-body p-0">
            <div className="flex justify-between items-center p-4 bg-success/5 rounded-t-xl border-b border-success/20">
              <span className="font-bold text-lg flex items-center gap-2">
                <svg className="w-6 h-6 text-success" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z" />
                </svg>
                Fixed Code
              </span>
              <button
                className="btn btn-sm btn-success btn-outline"
                onClick={() => navigator.clipboard.writeText(result.final_code)}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                  />
                </svg>
                Copy
              </button>
            </div>
            <pre className="min-h-[400px] h-[500px] lg:h-[600px] overflow-auto p-5 font-mono text-sm leading-relaxed whitespace-pre bg-base-100 text-base-content rounded-b-xl border-t border-success/10">
              <code>{result.final_code}</code>
            </pre>
          </div>
        </div>
      )}

      {/* Agent Cards */}
      <div className="space-y-4">
        {result.scanner_result && (
          <AgentCard
            agent="Scanner"
            data={result.scanner_result}
            isExpanded={expandedAgents.Scanner}
            onToggle={() => toggleAgent('Scanner')}
          />
        )}

        {result.fixer_result && (
          <AgentCard
            agent="Fixer"
            data={result.fixer_result}
            isExpanded={expandedAgents.Fixer}
            onToggle={() => toggleAgent('Fixer')}
          />
        )}

        {result.validator_result && (
          <AgentCard
            agent="Validator"
            data={result.validator_result}
            isExpanded={expandedAgents.Validator}
            onToggle={() => toggleAgent('Validator')}
          />
        )}
      </div>
    </div>
  )
}

export default ResultsPanel
