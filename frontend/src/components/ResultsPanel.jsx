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
                className={`alert ${result.success ? 'alert-success/10 border-success/20' : 'alert-error/10 border-error/20'} shadow-sm backdrop-blur-md border border-l-4 ${result.success ? 'border-l-success' : 'border-l-error'}`}
            >
                {result.success ? (
                    <div className="p-2 bg-success/20 rounded-full">
                        <svg className="w-6 h-6 stroke-success" viewBox="0 0 24 24" fill="none" strokeWidth="2.5">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                            <polyline points="22 4 12 14.01 9 11.01" />
                        </svg>
                    </div>
                ) : (
                    <div className="p-2 bg-error/20 rounded-full">
                        <svg className="w-6 h-6 stroke-error" viewBox="0 0 24 24" fill="none" strokeWidth="2.5">
                            <circle cx="12" cy="12" r="10" />
                            <line x1="12" y1="8" x2="12" y2="12" />
                            <line x1="12" y1="16" x2="12.01" y2="16" />
                        </svg>
                    </div>
                )}
                <div>
                    <h3 className={`font-bold text-lg ${result.success ? 'text-success' : 'text-error'}`}>
                        {result.success ? 'Success' : 'Failed'}
                    </h3>
                    <div className="text-sm opacity-80">{result.message}</div>
                </div>
                <div className="badge badge-lg bg-base-100/50 backdrop-blur border border-base-content/10 text-base-content font-mono shadow-sm">
                    {result.workflow_metadata?.total_time}s
                </div>
            </div>

            {/* Summary Stats */}
            {result.summary && (
                <div className="stats stats-vertical lg:stats-horizontal shadow-sm w-full bg-base-100/50 backdrop-blur-md border border-base-content/5 rounded-2xl overflow-hidden">
                    <div className="stat place-items-center lg:place-items-start hover:bg-base-200/50 transition-colors duration-200">
                        <div className="stat-figure text-error p-2 bg-error/10 rounded-xl">
                            <svg
                                className="inline-block w-6 h-6 stroke-current"
                                viewBox="0 0 24 24"
                                fill="none"
                                strokeWidth="2.5"
                            >
                                <circle cx="12" cy="12" r="10" />
                                <line x1="12" y1="8" x2="12" y2="12" />
                                <line x1="12" y1="16" x2="12.01" y2="16" />
                            </svg>
                        </div>
                        <div className="stat-title font-medium opacity-70">Errors Found</div>
                        <div className="stat-value text-error text-3xl font-bold tracking-tight">{result.summary.errors_found || 0}</div>
                        <div className="stat-desc font-medium">Issues detected</div>
                    </div>

                    <div className="stat place-items-center lg:place-items-start hover:bg-base-200/50 transition-colors duration-200">
                        <div className="stat-figure text-success p-2 bg-success/10 rounded-xl">
                            <svg
                                className="inline-block w-6 h-6 stroke-current"
                                viewBox="0 0 24 24"
                                fill="none"
                                strokeWidth="2.5"
                            >
                                <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                            </svg>
                        </div>
                        <div className="stat-title font-medium opacity-70">Fixed</div>
                        <div className="stat-value text-success text-3xl font-bold tracking-tight">{result.summary.errors_fixed || 0}</div>
                        <div className="stat-desc font-medium">Auto-corrected</div>
                    </div>

                    <div className="stat place-items-center lg:place-items-start hover:bg-base-200/50 transition-colors duration-200">
                        <div className="stat-figure text-primary p-2 bg-primary/10 rounded-xl">
                            <svg className="inline-block w-6 h-6 stroke-current" fill="none" viewBox="0 0 24 24" strokeWidth="2.5">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <div className="stat-title font-medium opacity-70">Confidence</div>
                        <div className="stat-value text-primary text-3xl font-bold tracking-tight">
                            {((result.summary.validation_score || 0) * 100).toFixed(0)}%
                        </div>
                        <div className="stat-desc font-medium">Validation Score</div>
                    </div>

                    <div className="stat place-items-center lg:place-items-start hover:bg-base-200/50 transition-colors duration-200">
                        <div className="stat-figure text-secondary p-2 bg-secondary/10 rounded-xl">
                            <svg className="inline-block w-6 h-6 stroke-current" fill="none" viewBox="0 0 24 24" strokeWidth="2.5">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                        </div>
                        <div className="stat-title font-medium opacity-70">Iterations</div>
                        <div className="stat-value text-secondary text-3xl font-bold tracking-tight">{result.workflow_metadata?.iterations || 1}</div>
                        <div className="stat-desc font-medium">Refinement loops</div>
                    </div>
                </div>
            )}

            {/* Fixed Code Display */}
            {result.final_code && (
                <div className="card bg-base-100 shadow-xl border border-base-content/5 overflow-hidden">
                    <div className="card-body p-0">
                        <div className="flex justify-between items-center p-4 bg-base-200/50 border-b border-base-content/5 backdrop-blur-sm">
                            <span className="font-bold text-lg flex items-center gap-3">
                                <div className="p-2 bg-success/10 rounded-lg">
                                    <svg className="w-5 h-5 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                                    </svg>
                                </div>
                                Fixed Code
                            </span>
                            <button
                                className="btn btn-sm btn-ghost hover:bg-base-300 gap-2 font-normal"
                                onClick={() => navigator.clipboard.writeText(result.final_code)}
                            >
                                <svg className="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth="2"
                                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                                    />
                                </svg>
                                Copy Code
                            </button>
                        </div>
                        <div className="relative group">
                            <pre className="min-h-[400px] max-h-[600px] overflow-auto p-6 font-mono text-sm leading-relaxed whitespace-pre bg-base-300 text-base-content scrollbar-thin scrollbar-thumb-base-content/20 scrollbar-track-transparent rounded-b-xl">
                                <code>{result.final_code}</code>
                            </pre>
                            <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                <div className="badge badge-sm badge-ghost opacity-70">Read-only</div>
                            </div>
                        </div>
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
