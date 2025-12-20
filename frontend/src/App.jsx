import { useState } from 'react'
import './App.css'
import AgentCard from './components/AgentCard'
import ResultsPanel from './components/ResultsPanel'
import StreamingProgress from './components/StreamingProgress'

const API_URL = 'http://localhost:8000'

function App() {
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [context, setContext] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  // Streaming state
  const [streamingStatus, setStreamingStatus] = useState(null)
  const [agentResults, setAgentResults] = useState({
    Scanner: null,
    Fixer: null,
    Validator: null
  })

  const handleDebug = async () => {
    if (!code.trim()) {
      setError('Please enter some code to debug')
      return
    }

    setIsLoading(true)
    setError(null)
    setResult(null)
    setStreamingStatus({ agent: null, message: 'Connecting to server...' })
    setAgentResults({ Scanner: null, Fixer: null, Validator: null })

    try {
      // First try streaming endpoint
      const response = await fetch(`${API_URL}/debug/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code,
          language: language,
          context: context || null
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // Check if we got a streaming response
      if (!response.body) {
        throw new Error('Streaming not supported')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              handleStreamEvent(data)
            } catch (e) {
              console.error('Parse error:', e, line)
            }
          }
        }
      }
    } catch (err) {
      console.error('Stream error:', err)
      // Fallback to non-streaming endpoint
      try {
        setStreamingStatus({ agent: 'Scanner', message: 'Processing (fallback mode)...', status: 'working' })
        const response = await fetch(`${API_URL}/debug`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code, language, context: context || null }),
        })
        if (response.ok) {
          const data = await response.json()
          setResult(data)
          setStreamingStatus(null)
        } else {
          throw new Error(`Fallback failed: ${response.status}`)
        }
      } catch (fallbackErr) {
        setError(`Connection failed: ${err.message}. Fallback: ${fallbackErr.message}`)
        setStreamingStatus(null)
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleStreamEvent = (event) => {
    switch (event.type) {
      case 'agent_start':
        setStreamingStatus({
          agent: event.agent,
          message: event.message,
          status: 'working'
        })
        break

      case 'agent_complete':
        setAgentResults(prev => ({
          ...prev,
          [event.agent]: event.result
        }))
        setStreamingStatus({
          agent: event.agent,
          message: event.message,
          status: 'complete'
        })
        break

      case 'workflow_complete':
        setResult(event.result)
        setStreamingStatus(null)
        break

      case 'error':
        setError(event.message)
        setStreamingStatus(null)
        break

      default:
        console.log('Unknown event:', event)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">🔍 Multi-Agent Debugger</h1>
        <p className="app-subtitle">AI-powered code debugging with Scanner → Fixer → Validator pipeline</p>
      </header>

      <main className="main-content">
        {/* Input Section */}
        <section className="input-section">
          <h2 className="section-title">
            <svg className="section-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M16 18l6-6-6-6M8 6l-6 6 6 6" />
            </svg>
            Code Input
          </h2>

          <div className="editor-card">
            <div className="editor-header">
              <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Enter code to debug</span>
              <select
                className="language-select"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="typescript">TypeScript</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
                <option value="go">Go</option>
              </select>
            </div>
            <textarea
              className="code-textarea"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder={`# Paste your ${language} code here...\n\ndef calculate(a, b)\n    return a + b`}
              spellCheck={false}
            />
          </div>

          <div className="context-card">
            <span className="context-label">Context (optional)</span>
            <input
              type="text"
              className="context-input"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Describe what this code should do..."
            />
          </div>

          <button
            className="debug-button"
            onClick={handleDebug}
            disabled={isLoading || !code.trim()}
          >
            {isLoading ? (
              <>
                <div className="spinner"></div>
                Processing...
              </>
            ) : (
              <>
                <svg className="button-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polygon points="5 3 19 12 5 21 5 3" />
                </svg>
                Debug Code
              </>
            )}
          </button>

          {error && (
            <div className="status-badge error">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="15" y1="9" x2="9" y2="15" />
                <line x1="9" y1="9" x2="15" y2="15" />
              </svg>
              {error}
            </div>
          )}
        </section>

        {/* Results Section */}
        <section className="results-section">
          <h2 className="section-title">
            <svg className="section-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 11l3 3L22 4" />
              <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
            </svg>
            Results
          </h2>

          <div className="results-scroll">
            {isLoading ? (
              <StreamingProgress
                status={streamingStatus}
                agentResults={agentResults}
              />
            ) : result ? (
              <ResultsPanel result={result} />
            ) : (
              <div className="empty-state">
                <svg className="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <rect x="2" y="3" width="20" height="14" rx="2" />
                  <line x1="8" y1="21" x2="16" y2="21" />
                  <line x1="12" y1="17" x2="12" y2="21" />
                </svg>
                <h3 className="empty-title">Ready to debug</h3>
                <p className="empty-text">Enter code and click Debug</p>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
