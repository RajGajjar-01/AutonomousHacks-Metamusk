function AgentCard({ agent, data, isExpanded, onToggle }) {
  if (!data) return null

  const getAgentIcon = () => {
    switch (agent) {
      case 'Scanner':
        return (
          <svg
            className="w-6 h-6"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
        )
      case 'Fixer':
        return (
          <svg
            className="w-6 h-6"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
          </svg>
        )
      case 'Validator':
        return (
          <svg
            className="w-6 h-6"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            <polyline points="9,12 12,15 16,10" />
          </svg>
        )
      default:
        return null
    }
  }

  const getColorClass = () => {
    switch (agent) {
      case 'Scanner':
        return 'primary'
      case 'Fixer':
        return 'secondary'
      case 'Validator':
        return 'accent'
      default:
        return 'neutral'
    }
  }

  const renderScannerContent = () => (
    <div className="grid gap-4">
      <div className="flex flex-wrap gap-2 items-center">
        <div className="badge badge-error gap-2 p-3">
          <span className="font-bold">{data.total_errors || 0}</span> Errors
        </div>
        <div className="badge badge-warning gap-2 p-3">
          <span className="font-bold">{data.total_warnings || 0}</span> Warnings
        </div>
        <div className="badge badge-info gap-2 p-3">
          <span className="font-bold">{data.code_quality_score?.toFixed(1) || 'N/A'}</span> Quality
        </div>
      </div>

      {data.errors?.length > 0 && (
        <div className="space-y-3">
          <h4 className="font-bold text-sm uppercase opacity-70 tracking-wider">Errors Found</h4>
          {data.errors.map((error, idx) => (
            <div
              key={idx}
              className="card bg-base-100 shadow-sm border border-base-content/10 overflow-hidden group"
            >
              <div className="flex flex-col sm:flex-row gap-3 p-4">
                <div className="flex items-start gap-2 min-w-[100px]">
                  <span className="badge badge-sm badge-error badge-outline font-mono opacity-80 mt-0.5">
                    Line {error.line}
                  </span>
                  {error.error_id && (
                    <span className="text-xs font-mono opacity-50 hidden sm:inline-block">{error.error_id}</span>
                  )}
                </div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-baseline justify-between">
                    <span className="font-bold text-error">{error.type}</span>
                    <span className="text-xs font-mono uppercase opacity-50 border border-current px-1 rounded">{error.severity || 'high'}</span>
                  </div>
                  <p className="opacity-90 leading-relaxed text-sm">{error.description}</p>
                  {error.suggestion && (
                    <div className="mt-2 text-xs bg-base-200/50 p-2 rounded border-l-2 border-info/50 text-base-content/80">
                      <span className="font-bold text-info mr-1">Fix:</span> {error.suggestion}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {data.warnings?.length > 0 && (
        <div className="space-y-3 mt-2">
          <h4 className="font-bold text-sm uppercase opacity-70 tracking-wider">Warnings</h4>
          {data.warnings.map((warning, idx) => (
            <div
              key={idx}
              className="card bg-base-100 shadow-sm border border-warning/20 overflow-hidden"
            >
              <div className="flex gap-3 p-3 items-start">
                <div className="min-w-[80px]">
                  <span className="badge badge-sm badge-warning badge-outline font-mono">Line {warning.line}</span>
                </div>
                <div className="flex-1">
                  <div className="font-bold text-warning text-sm mb-1">{warning.type}</div>
                  <p className="text-sm opacity-80">{warning.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )

  const renderFixerContent = () => (
    <div className="grid gap-4">
      <div className="flex gap-2 items-center">
        <div className="badge badge-success gap-2 p-3">
          <span className="font-bold">{data.total_changes || 0}</span> Changes applied
        </div>
        {data.total_changes > 0 && (
          <span className="text-xs opacity-50 ml-1">
            {(data.confidence_score * 100).toFixed(0)}% Confidence
          </span>
        )}
      </div>

      {data.changes?.length > 0 && (
        <div className="space-y-4">
          <h4 className="font-bold text-sm uppercase opacity-70 tracking-wider">Changes Made</h4>
          {data.changes.map((change, idx) => (
            <div key={idx} className="card bg-base-100 shadow-sm border border-base-content/10 overflow-hidden group">
              <div className="px-4 py-2 bg-base-200/50 border-b border-base-content/10 flex justify-between items-center">
                <div className="badge badge-sm badge-neutral font-mono rounded">Line {change.line_number}</div>
                <div className="text-xs opacity-50 italic group-hover:opacity-100 transition-opacity">
                  {change.reason}
                </div>
              </div>
              <div className="font-mono text-sm leading-6">
                {change.original && (
                  <div className="bg-error/10 text-error px-4 py-1 border-b border-error/5 flex gap-3 select-none">
                    <span className="w-4 inline-block text-center opacity-50">-</span>
                    <span className="select-text">{change.original}</span>
                  </div>
                )}
                <div className="bg-success/10 text-success px-4 py-1 flex gap-3">
                  <span className="w-4 inline-block text-center opacity-50">+</span>
                  <span>{change.fixed}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {data.explanation && (
        <div className="mt-2">
          <h4 className="font-bold text-sm uppercase opacity-70 mb-2 tracking-wider">Summary</h4>
          <p className="text-sm opacity-80 leading-relaxed bg-base-100 border border-base-content/5 p-4 rounded-xl">
            {data.explanation}
          </p>
        </div>
      )}
    </div>
  )

  const renderValidatorContent = () => (
    <div className="grid gap-4">
      <div className="flex gap-2">
        <div
          className={`badge ${data.validation_status === 'approved' ? 'badge-success' : 'badge-warning'} gap-2 p-3`}
        >
          <span className="font-bold">{(data.confidence_score * 100).toFixed(0)}%</span> Confidence
        </div>
        <div
          className={`badge ${data.validation_status === 'approved' ? 'badge-success' : 'badge-warning'} badge-outline p-3 uppercase font-bold`}
        >
          {data.validation_status}
        </div>
      </div>

      {data.checks_performed?.length > 0 && (
        <div className="space-y-2">
          <h4 className="font-bold text-sm uppercase opacity-70">Checks Performed</h4>
          {data.checks_performed.map((check, idx) => (
            <div
              key={idx}
              className={`alert ${check.status === 'passed' ? 'alert-success' : check.status === 'failed' ? 'alert-error' : 'alert-warning'} text-sm py-2 px-3 flex-row items-center gap-2 shadow-sm`}
            >
              <span className="font-bold text-lg">
                {check.status === 'passed' ? '✓' : check.status === 'failed' ? '✗' : '⚠'}
              </span>
              <div className="flex-1">
                <span className="font-bold uppercase text-xs opacity-80 mr-2">
                  {check.check_type?.replace(/_/g, ' ')}:
                </span>
                <span>{check.message}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {data.final_verdict && (
        <div className="mt-2">
          <h4 className="font-bold text-sm uppercase opacity-70 mb-1">Final Verdict</h4>
          <p className="text-sm opacity-90 leading-relaxed bg-base-200 p-3 rounded-lg">
            {data.final_verdict}
          </p>
        </div>
      )}

      {data.issues_found?.length > 0 && (
        <div className="mt-2">
          <h4 className="font-bold text-sm uppercase opacity-70 mb-2">Issues Found</h4>
          <ul className="menu bg-error/10 rounded-box p-2 text-sm">
            {data.issues_found.map((issue, idx) => (
              <li key={idx}>
                <a className="text-error">⚠ {issue}</a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.recommendations?.length > 0 && (
        <div className="mt-2">
          <h4 className="font-bold text-sm uppercase opacity-70 mb-2">Recommendations</h4>
          <ul className="menu bg-base-200 rounded-box p-2 text-sm">
            {data.recommendations.map((rec, idx) => (
              <li key={idx}>
                <a>• {rec}</a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )

  return (
    <div className={`collapse collapse-arrow bg-base-200 border border-${getColorClass()} mb-4`}>
      <input type="checkbox" checked={isExpanded} onChange={onToggle} />
      <div className="collapse-title text-xl font-medium flex items-center gap-3">
        <span className={`text-${getColorClass()}`}>{getAgentIcon()}</span>
        <h3>{agent} Agent</h3>
        {data.execution_time && (
          <span className="ml-auto text-sm font-normal opacity-60 font-mono">
            {data.execution_time}s
          </span>
        )}
      </div>
      <div className="collapse-content">
        <div className="pt-4 border-t border-base-300">
          {agent === 'Scanner' && renderScannerContent()}
          {agent === 'Fixer' && renderFixerContent()}
          {agent === 'Validator' && renderValidatorContent()}
        </div>
      </div>
    </div>
  )
}

export default AgentCard
