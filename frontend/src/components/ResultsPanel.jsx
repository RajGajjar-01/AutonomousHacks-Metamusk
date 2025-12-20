import { useState } from 'react'
import AgentCard from './AgentCard'
import './ResultsPanel.css'

function ResultsPanel({ result }) {
    const [expandedAgents, setExpandedAgents] = useState({
        Scanner: false,
        Fixer: true,
        Validator: false
    })

    const toggleAgent = (agent) => {
        setExpandedAgents(prev => ({
            ...prev,
            [agent]: !prev[agent]
        }))
    }

    if (!result) return null

    return (
        <div className="results-panel">
            {/* Status Header */}
            <div className={`results-header ${result.success ? 'success' : 'error'}`}>
                <div className="results-status">
                    {result.success ? (
                        <svg className="status-icon success" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                            <polyline points="22 4 12 14.01 9 11.01" />
                        </svg>
                    ) : (
                        <svg className="status-icon error" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="10" />
                            <line x1="12" y1="8" x2="12" y2="12" />
                            <line x1="12" y1="16" x2="12.01" y2="16" />
                        </svg>
                    )}
                    <div>
                        <h3 className="status-title">{result.success ? 'Success' : 'Failed'}</h3>
                        <p className="status-message">{result.message}</p>
                    </div>
                </div>
                <div className="time-badge">{result.workflow_metadata?.total_time}s</div>
            </div>

            {/* Summary Stats */}
            {result.summary && (
                <div className="summary-stats">
                    <div className="stat-item">
                        <span className="stat-value">{result.summary.errors_found || 0}</span>
                        <span className="stat-label">Errors</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-value">{result.summary.errors_fixed || 0}</span>
                        <span className="stat-label">Fixed</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-value">{((result.summary.validation_score || 0) * 100).toFixed(0)}%</span>
                        <span className="stat-label">Confidence</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-value">{result.workflow_metadata?.iterations || 1}</span>
                        <span className="stat-label">Iterations</span>
                    </div>
                </div>
            )}

            {/* Fixed Code Display */}
            {result.final_code && result.final_code !== result.original_code && (
                <div className="code-card">
                    <div className="code-card-header">
                        <span className="code-card-title">✨ Fixed Code</span>
                        <button
                            className="copy-button"
                            onClick={() => navigator.clipboard.writeText(result.final_code)}
                        >
                            Copy
                        </button>
                    </div>
                    <div className="code-display">
                        <pre>{result.final_code}</pre>
                    </div>
                </div>
            )}

            {/* Agent Cards */}
            <div className="agents-container">
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
