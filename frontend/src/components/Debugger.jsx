import { useState } from 'react'
import { useTheme } from '../contexts/ThemeContext'
import Navbar from './Navbar'
import AgentCard from './AgentCard'
import ResultsPanel from './ResultsPanel'
import StreamingProgress from './StreamingProgress'
import CodeEditor from './Editor'

const API_URL = 'http://localhost:8000'

const LANGUAGES = ['python', 'javascript', 'java', 'cpp', 'go']
const LANGUAGE_LABELS = {
  python: 'Python',
  javascript: 'JavaScript',
  java: 'Java',
  cpp: 'C++',
  go: 'Go',
}

export default function Debugger() {
  const { theme } = useTheme()
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [context, setContext] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [streamingStatus, setStreamingStatus] = useState(null)
  const [agentResults, setAgentResults] = useState({})

  const handleDebug = async () => {
    if (!code.trim()) {
      setError('Please enter some code to debug')
      return
    }

    setIsLoading(true)
    setError(null)
    setResult(null)
    setStreamingStatus({ message: 'Connecting to server...' })
    setAgentResults({})

    try {
      const response = await fetch(`${API_URL}/debug/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code,
          language,
          context: context || null,
        }),
      })

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              handleStreamEvent(JSON.parse(line.slice(6)))
            } catch (e) {
              console.error('Error parsing SSE data:', e)
            }
          }
        }
      }
    } catch (err) {
      setError(err.message || 'Failed to connect to debug server')
      setStreamingStatus(null)
    } finally {
      setIsLoading(false)
    }
  }

  const handleStreamEvent = event => {
    switch (event.type) {
      case 'agent_start':
        setStreamingStatus({ agent: event.agent, message: event.message, status: 'working' })
        break
      case 'agent_complete':
        setAgentResults(prev => ({ ...prev, [event.agent]: event.result }))
        setStreamingStatus({ agent: event.agent, message: event.message, status: 'complete' })
        break
      case 'workflow_complete':
        setResult(event.result)
        setStreamingStatus(null)
        break
      case 'error':
        setError(event.message)
        setStreamingStatus(null)
        break
    }
  }

  const hasResults = Object.keys(agentResults).length > 0

  return (
    <div className="h-screen flex flex-col bg-base-100 overflow-hidden">
      <Navbar />

      <div className="flex-1 flex flex-col lg:grid lg:grid-cols-2 gap-2 lg:gap-4 p-2 lg:p-4 max-w-[2000px] mx-auto w-full overflow-hidden">
        {/* Left Panel - Input */}
        <div className="flex flex-col min-h-0 h-full lg:h-full">
          <div className="card bg-base-100 shadow-xl border border-base-300 flex flex-col h-full">
            <div className="card-body p-2.5 lg:p-4 flex flex-col h-full">
              {/* Header */}
              <div className="flex items-center justify-between mb-2 lg:mb-3">
                <h2 className="card-title text-primary text-sm lg:text-lg">Code Editor</h2>
                <div className="badge badge-primary badge-sm lg:badge-lg">
                  {language.toUpperCase()}
                </div>
              </div>

              {/* Language Selector */}
              <div className="flex gap-1.5 lg:gap-2 mb-2 lg:mb-3 flex-wrap">
                {LANGUAGES.map(lang => (
                  <button
                    key={lang}
                    className={`btn btn-xs lg:btn-sm ${language === lang ? 'btn-primary' : 'btn-ghost'}`}
                    onClick={() => setLanguage(lang)}
                  >
                    {LANGUAGE_LABELS[lang]}
                  </button>
                ))}
              </div>

              {/* Code Editor */}
              <CodeEditor
                value={code}
                onChange={value => setCode(value || '')}
                language={language}
              />

              {/* Context Input - Improved Layout */}
              <div className="mt-2 lg:mt-3">
                <label className="text-xs font-semibold uppercase tracking-wide opacity-70 mb-1.5 lg:mb-2 block">
                  Additional Context (Optional)
                </label>
                <textarea
                  className="textarea textarea-bordered w-full h-14 lg:h-20 text-xs lg:text-sm resize-none"
                  placeholder="Describe what the code should do, error messages, or any other context..."
                  value={context}
                  onChange={e => setContext(e.target.value)}
                />
              </div>

              {/* Action Button */}
              <button
                className="btn btn-primary btn-block mt-2 lg:mt-3 btn-sm lg:btn-md"
                onClick={handleDebug}
                disabled={isLoading || !code.trim()}
              >
                {isLoading ? (
                  <>
                    <span className="loading loading-spinner"></span>
                    Processing...
                  </>
                ) : (
                  'Debug Code'
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Right Panel - Results */}
        <div className="flex flex-col min-h-0 flex-1 lg:h-full overflow-y-auto space-y-3 lg:space-y-4">
          {error && (
            <div className="alert alert-error shadow-lg text-xs lg:text-sm">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="stroke-current shrink-0 h-5 w-5 lg:h-6 lg:w-6"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span className="text-sm lg:text-base">{error}</span>
            </div>
          )}

          {streamingStatus && (
            <StreamingProgress status={streamingStatus} agentResults={agentResults} />
          )}

          {hasResults && !result && (
            <div className="space-y-3 lg:space-y-4">
              {['Scanner', 'Fixer', 'Validator'].map(
                agent =>
                  agentResults[agent] && (
                    <AgentCard key={agent} agent={agent} data={agentResults[agent]} />
                  )
              )}
            </div>
          )}

          {result && !isLoading && <ResultsPanel result={result} language={language} />}

          {!isLoading && !result && !error && !streamingStatus && (
            <div className="card bg-base-200 shadow-xl flex-1 flex min-h-[200px]">
              <div className="card-body items-center justify-center text-center p-4 lg:p-8">
                <div className="mb-3 lg:mb-4 p-3 lg:p-6 rounded-full bg-base-300">
                  <svg
                    className="w-10 h-10 lg:w-16 lg:h-16 text-primary"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                </div>
                <h3 className="text-lg lg:text-2xl font-bold text-base-content mb-1 lg:mb-2">
                  Ready to Debug
                </h3>
                <p className="text-xs lg:text-base text-base-content/60 max-w-md">
                  Enter your code in the editor and click "Debug Code" to analyze and fix issues
                  automatically
                </p>
                <div className="mt-3 lg:mt-6 space-y-1.5 lg:space-y-2">
                  {['Automatic bug detection', 'Smart code fixes', 'Validation & testing'].map(
                    feature => (
                      <div
                        key={feature}
                        className="flex items-center gap-2 text-xs lg:text-sm text-base-content/50"
                      >
                        <svg
                          className="w-3 h-3 lg:w-4 lg:h-4"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                        >
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                        <span>{feature}</span>
                      </div>
                    )
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
