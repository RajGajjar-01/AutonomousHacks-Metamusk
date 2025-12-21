import Editor from '@monaco-editor/react'
import { useTheme } from '../contexts/ThemeContext'

export default function CodeEditor({ value, onChange, language, readOnly = false }) {
  const { theme } = useTheme()

  const handleEditorDidMount = (editor, monaco) => {
    // Define custom dark theme with #202020 background
    monaco.editor.defineTheme('custom-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#202020',
      },
    })

    // Apply the custom theme if dark mode is active
    if (theme === 'dark') {
      monaco.editor.setTheme('custom-dark')
    }
  }

  return (
    <div className="flex-1 min-h-[200px] lg:min-h-[400px] rounded-lg overflow-hidden border border-base-content/10">
      <Editor
        height="100%"
        language={language === 'cpp' ? 'cpp' : language}
        value={value}
        onChange={onChange}
        theme={theme === 'dark' ? 'custom-dark' : 'light'}
        onMount={handleEditorDidMount}
        options={{
          minimap: { enabled: false },
          fontSize: 16,
          fontFamily: "'Source Code Pro', 'Courier New', monospace",
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          wordWrap: 'on',
          padding: { top: 8, bottom: 8 },
          folding: true,
          renderLineHighlight: 'all',
          scrollbar: {
            vertical: 'visible',
            horizontal: 'visible',
            useShadows: false,
            verticalScrollbarSize: 8,
            horizontalScrollbarSize: 8,
          },
          readOnly: readOnly,
        }}
        loading={
          <div className="flex items-center justify-center h-full bg-base-200">
            <span className="loading loading-spinner loading-lg text-primary"></span>
          </div>
        }
      />
    </div>
  )
}
