import './AgentCard.css'

function AgentCard({ agent, data, isExpanded, onToggle }) {
    if (!data) return null

    const getAgentIcon = () => {
        switch (agent) {
            case 'Scanner':
                return (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="11" cy="11" r="8" />
                        <line x1="21" y1="21" x2="16.65" y2="16.65" />
                    </svg>
                )
            case 'Fixer':
                return (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                    </svg>
                )
            case 'Validator':
                return (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                        <polyline points="9,12 12,15 16,10" />
                    </svg>
                )
            default:
                return null
        }
    }

    const getAgentColor = () => {
        switch (agent) {
            case 'Scanner': return 'var(--accent-blue)'
            case 'Fixer': return 'var(--accent-purple)'
            case 'Validator': return 'var(--accent-green)'
            default: return 'var(--accent-blue)'
        }
    }

    const renderScannerContent = () => (
        <>
            <div className="agent-stats">
                <div className="stat-box error">
                    <span className="stat-number">{data.total_errors || 0}</span>
                    <span className="stat-text">Errors</span>
                </div>
                <div className="stat-box warning">
                    <span className="stat-number">{data.total_warnings || 0}</span>
                    <span className="stat-text">Warnings</span>
                </div>
                <div className="stat-box info">
                    <span className="stat-number">{data.code_quality_score?.toFixed(1) || 'N/A'}</span>
                    <span className="stat-text">Quality</span>
                </div>
            </div>

            {data.errors?.length > 0 && (
                <div className="agent-section">
                    <h4 className="section-heading">Errors Found</h4>
                    {data.errors.map((error, idx) => (
                        <div key={idx} className="issue-item error">
                            <div className="issue-header">
                                <span className="issue-id">{error.error_id}</span>
                                <span className="issue-type">{error.type}</span>
                                <span className="issue-line">Line {error.line}</span>
                            </div>
                            <p className="issue-description">{error.description}</p>
                            {error.suggestion && (
                                <p className="issue-suggestion">💡 {error.suggestion}</p>
                            )}
                        </div>
                    ))}
                </div>
            )}

            {data.warnings?.length > 0 && (
                <div className="agent-section">
                    <h4 className="section-heading">Warnings</h4>
                    {data.warnings.map((warning, idx) => (
                        <div key={idx} className="issue-item warning">
                            <div className="issue-header">
                                <span className="issue-id">{warning.warning_id}</span>
                                <span className="issue-type">{warning.type}</span>
                                <span className="issue-line">Line {warning.line}</span>
                            </div>
                            <p className="issue-description">{warning.description}</p>
                        </div>
                    ))}
                </div>
            )}
        </>
    )

    const renderFixerContent = () => (
        <>
            <div className="agent-stats">
                <div className="stat-box success">
                    <span className="stat-number">{data.total_changes || 0}</span>
                    <span className="stat-text">Changes</span>
                </div>
            </div>

            {data.changes?.length > 0 && (
                <div className="agent-section">
                    <h4 className="section-heading">Changes Made</h4>
                    {data.changes.map((change, idx) => (
                        <div key={idx} className="change-item">
                            <div className="change-header">
                                <span className="change-id">{change.change_id}</span>
                                <span className="change-type">{change.type}</span>
                                <span className="change-line">Line {change.line_number}</span>
                            </div>
                            <div className="change-diff">
                                {change.original_line && (
                                    <div className="diff-line removed">- {change.original_line}</div>
                                )}
                                <div className="diff-line added">+ {change.fixed_line}</div>
                            </div>
                            <p className="change-reason">{change.reason}</p>
                        </div>
                    ))}
                </div>
            )}

            {data.explanation && (
                <div className="agent-section">
                    <h4 className="section-heading">Explanation</h4>
                    <p className="explanation-text">{data.explanation}</p>
                </div>
            )}
        </>
    )

    const renderValidatorContent = () => (
        <>
            <div className="agent-stats">
                <div className={`stat-box ${data.validation_status === 'approved' ? 'success' : 'warning'}`}>
                    <span className="stat-number">{(data.confidence_score * 100).toFixed(0)}%</span>
                    <span className="stat-text">Confidence</span>
                </div>
                <div className={`stat-box ${data.validation_status === 'approved' ? 'success' : 'warning'}`}>
                    <span className="stat-text" style={{ fontSize: '0.9rem' }}>{data.validation_status?.toUpperCase()}</span>
                </div>
            </div>

            {data.checks_performed?.length > 0 && (
                <div className="agent-section">
                    <h4 className="section-heading">Checks Performed</h4>
                    {data.checks_performed.map((check, idx) => (
                        <div key={idx} className={`check-item ${check.status}`}>
                            <div className="check-header">
                                <span className={`check-status ${check.status}`}>
                                    {check.status === 'passed' ? '✓' : check.status === 'failed' ? '✗' : '⚠'}
                                </span>
                                <span className="check-type">{check.check_type?.replace(/_/g, ' ')}</span>
                            </div>
                            <p className="check-message">{check.message}</p>
                        </div>
                    ))}
                </div>
            )}

            {data.recommendations?.length > 0 && (
                <div className="agent-section">
                    <h4 className="section-heading">Recommendations</h4>
                    <ul className="recommendations-list">
                        {data.recommendations.map((rec, idx) => (
                            <li key={idx}>{rec}</li>
                        ))}
                    </ul>
                </div>
            )}
        </>
    )

    return (
        <div className={`agent-card ${isExpanded ? 'expanded' : ''}`} style={{ '--agent-color': getAgentColor() }}>
            <div className="agent-header" onClick={onToggle}>
                <div className="agent-title">
                    <div className="agent-icon">{getAgentIcon()}</div>
                    <h3>{agent} Agent</h3>
                </div>
                <div className="agent-meta">
                    {data.execution_time && (
                        <span className="execution-time">{data.execution_time}s</span>
                    )}
                    <svg
                        className={`expand-icon ${isExpanded ? 'rotated' : ''}`}
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                    >
                        <polyline points="6 9 12 15 18 9" />
                    </svg>
                </div>
            </div>

            {isExpanded && (
                <div className="agent-content animate-fadeIn">
                    {agent === 'Scanner' && renderScannerContent()}
                    {agent === 'Fixer' && renderFixerContent()}
                    {agent === 'Validator' && renderValidatorContent()}
                </div>
            )}
        </div>
    )
}

export default AgentCard
