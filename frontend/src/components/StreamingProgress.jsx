import './StreamingProgress.css'

function StreamingProgress({ status, agentResults }) {
    const agents = [
        {
            name: 'Scanner',
            icon: '🔍',
            color: '#3b82f6',
            description: 'Analyzing code for errors'
        },
        {
            name: 'Fixer',
            icon: '🔧',
            color: '#8b5cf6',
            description: 'Applying fixes'
        },
        {
            name: 'Validator',
            icon: '✓',
            color: '#10b981',
            description: 'Validating changes'
        }
    ]

    const getAgentStatus = (agentName) => {
        if (agentResults[agentName]) return 'complete'
        if (status?.agent === agentName && status?.status === 'working') return 'working'
        if (status?.agent === agentName && status?.status === 'complete') return 'complete'
        return 'pending'
    }

    return (
        <div className="streaming-progress">
            <div className="progress-header">
                <div className="pulse-dot"></div>
                <span className="progress-title">Processing Pipeline</span>
            </div>

            <div className="agents-pipeline">
                {agents.map((agent, index) => {
                    const agentStatus = getAgentStatus(agent.name)
                    const result = agentResults[agent.name]

                    return (
                        <div key={agent.name} className="pipeline-item">
                            {/* Connector Line */}
                            {index > 0 && (
                                <div className={`connector ${agentStatus !== 'pending' ? 'active' : ''}`}>
                                    <div className="connector-line"></div>
                                    <div className="connector-arrow">→</div>
                                </div>
                            )}

                            {/* Agent Card */}
                            <div
                                className={`agent-step ${agentStatus}`}
                                style={{ '--agent-color': agent.color }}
                            >
                                <div className="step-icon">
                                    {agentStatus === 'working' ? (
                                        <div className="working-spinner"></div>
                                    ) : agentStatus === 'complete' ? (
                                        <span className="complete-check">✓</span>
                                    ) : (
                                        <span className="pending-icon">{agent.icon}</span>
                                    )}
                                </div>

                                <div className="step-content">
                                    <div className="step-header">
                                        <span className="step-name">{agent.name}</span>
                                        <span className={`step-status ${agentStatus}`}>
                                            {agentStatus === 'working' ? 'Working...' :
                                                agentStatus === 'complete' ? 'Done' : 'Pending'}
                                        </span>
                                    </div>

                                    <div className="step-description">
                                        {agentStatus === 'working' && status?.message ? (
                                            <span className="working-message">{status.message}</span>
                                        ) : result ? (
                                            <span className="result-preview">
                                                {agent.name === 'Scanner' && `${result.total_errors || 0} errors, ${result.total_warnings || 0} warnings`}
                                                {agent.name === 'Fixer' && `${result.total_changes || 0} changes applied`}
                                                {agent.name === 'Validator' && `${result.validation_status || 'checking'} (${((result.confidence_score || 0) * 100).toFixed(0)}%)`}
                                            </span>
                                        ) : (
                                            <span className="pending-message">{agent.description}</span>
                                        )}
                                    </div>
                                </div>

                                {/* Progress bar for working state */}
                                {agentStatus === 'working' && (
                                    <div className="step-progress-bar">
                                        <div className="progress-fill"></div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )
                })}
            </div>

            {/* Live status message */}
            {status && (
                <div className="live-status">
                    <div className="status-indicator"></div>
                    <span>{status.message}</span>
                </div>
            )}
        </div>
    )
}

export default StreamingProgress
