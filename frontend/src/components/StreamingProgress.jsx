import { useRef, useEffect } from 'react'

function StreamingProgress({ status, agentResults }) {
    const agents = [
        {
            name: 'Scanner',
            icon: '🔍',
            color: 'primary',
            description: 'Analyzing code for errors'
        },
        {
            name: 'Fixer',
            icon: '🔧',
            color: 'secondary',
            description: 'Applying fixes'
        },
        {
            name: 'Validator',
            icon: '✓',
            color: 'accent',
            description: 'Validating changes'
        }
    ]

    const getAgentStatus = (agentName) => {
        if (agentResults && agentResults[agentName]) return 'complete'
        if (status?.agent === agentName && status?.status === 'working') return 'working'
        if (status?.agent === agentName && status?.status === 'complete') return 'complete'
        return 'pending'
    }

    return (
        <div className="card bg-base-100 shadow-lg border border-base-200">
            <div className="card-body">
                <div className="flex items-center gap-2 mb-6">
                    <span className="loading loading-pulse loading-sm text-primary"></span>
                    <h3 className="card-title text-base font-bold uppercase tracking-wider text-base-content/70">Processing Pipeline</h3>
                </div>

                <ul className="steps steps-vertical lg:steps-horizontal w-full">
                    {agents.map((agent) => {
                        const agentStatus = getAgentStatus(agent.name)
                        const result = agentResults[agent.name]

                        let stepClass = "step"
                        if (agentStatus === 'complete') stepClass += ` step-${agent.color}`
                        if (agentStatus === 'working') stepClass += ` step-${agent.color}`

                        return (
                            <li key={agent.name} className={stepClass} data-content={agentStatus === 'complete' ? "✓" : agentStatus === 'working' ? "●" : ""}>
                                <div className="flex flex-col items-start lg:items-center text-left lg:text-center w-full p-2 gap-1">
                                    <span className="font-bold text-lg">{agent.name}</span>

                                    <div className="text-sm min-h-[1.5em]">
                                        {agentStatus === 'working' ? (
                                            <span className="badge badge-ghost gap-2">
                                                <span className="loading loading-dots loading-xs"></span>
                                                Working
                                            </span>
                                        ) : agentStatus === 'complete' ? (
                                            <span className={`badge badge-${agent.color} badge-outline`}>Complete</span>
                                        ) : (
                                            <span className="text-base-content/50">Pending</span>
                                        )}
                                    </div>

                                    <div className="text-xs text-base-content/70 max-w-[200px] mt-1">
                                        {agentStatus === 'working' && status?.message ? (
                                            <span className="animate-pulse">{status.message}</span>
                                        ) : result ? (
                                            <span className="font-medium">
                                                {agent.name === 'Scanner' && `${result.total_errors || 0} errors`}
                                                {agent.name === 'Fixer' && `${result.total_changes || 0} fixes`}
                                                {agent.name === 'Validator' && `${((result.confidence_score || 0) * 100).toFixed(0)}% conf.`}
                                            </span>
                                        ) : (
                                            agent.description
                                        )}
                                    </div>
                                </div>
                            </li>
                        )
                    })}
                </ul>

                {status && (
                    <div className="alert alert-info bg-base-200/50 mt-6 text-sm py-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="stroke-current shrink-0 w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <span>{status.message}</span>
                    </div>
                )}
            </div>
        </div>
    )
}

export default StreamingProgress
