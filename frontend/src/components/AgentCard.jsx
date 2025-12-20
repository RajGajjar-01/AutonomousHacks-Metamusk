function AgentCard({ agent, data, isExpanded, onToggle }) {
    if (!data) return null

    const getAgentIcon = () => {
        switch (agent) {
            case 'Scanner':
                return (
                    <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="11" cy="11" r="8" />
                        <line x1="21" y1="21" x2="16.65" y2="16.65" />
                    </svg>
                )
            case 'Fixer':
                return (
                    <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                    </svg>
                )
            case 'Validator':
                return (
                    <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
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
            case 'Scanner': return 'primary'
            case 'Fixer': return 'secondary'
            case 'Validator': return 'accent'
            default: return 'neutral'
        }
    }

    const renderScannerContent = () => (
        <div className="grid gap-4">
            <div className="flex flex-wrap gap-2">
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
                <div className="space-y-2">
                    <h4 className="font-bold text-sm uppercase opacity-70">Errors Found</h4>
                    {data.errors.map((error, idx) => (
                        <div key={idx} className="alert alert-error shadow-sm text-sm py-2 px-3 items-start flex-col sm:flex-row gap-2">
                            <div className="flex gap-2 w-full sm:w-auto items-center">
                                <span className="badge badge-sm badge-outline font-mono opacity-75">{error.error_id}</span>
                                <span className="badge badge-sm badge-white font-mono opacity-75">Line {error.line}</span>
                            </div>
                            <div className="flex-1">
                                <p className="font-semibold">{error.type}</p>
                                <p className="opacity-90">{error.description}</p>
                                {error.suggestion && (
                                    <p className="mt-1 text-xs bg-white/10 p-2 rounded">💡 {error.suggestion}</p>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {data.warnings?.length > 0 && (
                <div className="space-y-2 mt-2">
                    <h4 className="font-bold text-sm uppercase opacity-70">Warnings</h4>
                    {data.warnings.map((warning, idx) => (
                        <div key={idx} className="alert alert-warning shadow-sm text-sm py-2 px-3 items-start flex-col gap-1">
                            <div className="flex gap-2 w-full items-center">
                                <span className="badge badge-sm badge-outline font-mono opacity-75">{warning.warning_id}</span>
                                <span className="badge badge-sm font-mono opacity-75">Line {warning.line}</span>
                                <span className="font-bold">{warning.type}</span>
                            </div>
                            <p className="opacity-90">{warning.description}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )

    const renderFixerContent = () => (
        <div className="grid gap-4">
            <div className="flex gap-2">
                <div className="badge badge-success gap-2 p-3">
                    <span className="font-bold">{data.total_changes || 0}</span> Changes applied
                </div>
            </div>

            {data.changes?.length > 0 && (
                <div className="space-y-3">
                    <h4 className="font-bold text-sm uppercase opacity-70">Changes Made</h4>
                    {data.changes.map((change, idx) => (
                        <div key={idx} className="card bg-base-200 compact border border-base-300">
                            <div className="card-body p-3">
                                <div className="flex gap-2 items-center mb-2">
                                    <span className="badge badge-sm badge-outline">{change.change_id}</span>
                                    <span className="badge badge-sm badge-ghost">Line {change.line_number}</span>
                                    <span className="font-semibold text-sm">{change.type}</span>
                                </div>
                                <div className="mockup-code bg-base-300 text-xs p-0 min-w-0">
                                    {change.original_line && (
                                        <pre className="text-error bg-error/10 block px-4 py-1"><code>- {change.original_line}</code></pre>
                                    )}
                                    <pre className="text-success bg-success/10 block px-4 py-1"><code>+ {change.fixed_line}</code></pre>
                                </div>
                                <p className="text-xs mt-2 italic opacity-70">{change.reason}</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {data.explanation && (
                <div className="mt-2">
                    <h4 className="font-bold text-sm uppercase opacity-70 mb-1">Explanation</h4>
                    <p className="text-sm opacity-90 leading-relaxed bg-base-200 p-3 rounded-lg">{data.explanation}</p>
                </div>
            )}
        </div>
    )

    const renderValidatorContent = () => (
        <div className="grid gap-4">
            <div className="flex gap-2">
                <div className={`badge ${data.validation_status === 'approved' ? 'badge-success' : 'badge-warning'} gap-2 p-3`}>
                    <span className="font-bold">{(data.confidence_score * 100).toFixed(0)}%</span> Confidence
                </div>
                <div className={`badge ${data.validation_status === 'approved' ? 'badge-success' : 'badge-warning'} badge-outline p-3 uppercase font-bold`}>
                    {data.validation_status}
                </div>
            </div>

            {data.checks_performed?.length > 0 && (
                <div className="space-y-2">
                    <h4 className="font-bold text-sm uppercase opacity-70">Checks Performed</h4>
                    {data.checks_performed.map((check, idx) => (
                        <div key={idx} className={`alert ${check.status === 'passed' ? 'alert-success' : check.status === 'failed' ? 'alert-error' : 'alert-warning'} text-sm py-2 px-3 flex-row items-center gap-2 shadow-sm`}>
                            <span className="font-bold text-lg">
                                {check.status === 'passed' ? '✓' : check.status === 'failed' ? '✗' : '⚠'}
                            </span>
                            <div className="flex-1">
                                <span className="font-bold uppercase text-xs opacity-80 mr-2">{check.check_type?.replace(/_/g, ' ')}:</span>
                                <span>{check.message}</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {data.recommendations?.length > 0 && (
                <div className="mt-2">
                    <h4 className="font-bold text-sm uppercase opacity-70 mb-2">Recommendations</h4>
                    <ul className="menu bg-base-200 rounded-box p-2 text-sm">
                        {data.recommendations.map((rec, idx) => (
                            <li key={idx}><a>• {rec}</a></li>
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
                    <span className="ml-auto text-sm font-normal opacity-60 font-mono">{data.execution_time}s</span>
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
