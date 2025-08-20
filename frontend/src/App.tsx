import React, { useState } from 'react'

const API = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

export default function App() {
  const [ticker, setTicker] = useState('AAPL')
  const [log, setLog] = useState<string>('Ready.')
  const [loading, setLoading] = useState(false)

  async function call(path: string, body: any) {
    setLoading(true)
    setLog(`POST ${API}${path} ...`)
    try {
      const res = await fetch(`${API}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      const data = await res.json()
      setLog(JSON.stringify(data, null, 2))
    } catch (e: any) {
      setLog('ERROR: ' + (e?.message || String(e)))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow p-6 space-y-4">
        <h1 className="text-2xl font-bold">QuantVestor Frontend ✅</h1>
        <p className="text-sm text-slate-500">Tailwind + Vite are working.</p>

        <div className="flex gap-3 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium mb-1">Ticker</label>
            <input
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring"
              placeholder="AAPL"
            />
          </div>

          <button
            className="px-4 py-2 rounded-lg bg-black text-white disabled:opacity-50"
            disabled={loading}
            onClick={() => call('/valuation', { ticker })}
          >
            Run Valuation
          </button>

          <button
            className="px-4 py-2 rounded-lg bg-indigo-600 text-white disabled:opacity-50"
            disabled={loading}
            onClick={() => call('/sentiment', { query: ticker })}
          >
            Run Sentiment
          </button>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Response</label>
          <pre className="bg-slate-900 text-slate-100 p-3 rounded-lg overflow-auto text-xs max-h-80">
{log}
          </pre>
        </div>

        <p className="text-xs text-slate-400">
          Using API base: <code>{API}</code>
        </p>
      </div>
    </div>
  )
}
