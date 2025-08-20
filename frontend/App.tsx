import React, { useState } from 'react'
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend
} from 'recharts'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

type Val = { value: number; explanation: string }
type ValRes = { DCF: Val; PE: Val; Graham: Val }
type SentRes = { score: number; headlines: string[]; explanation: string }

export default function App() {
  const [tickerOrUrl, setTickerOrUrl] = useState('')
  const [peers, setPeers] = useState('')
  const [val, setVal] = useState<ValRes | null>(null)
  const [peerVals, setPeerVals] = useState<{ticker:string; valuation:ValRes}[]>([])
  const [sent, setSent] = useState<SentRes | null>(null)
  const [expanded, setExpanded] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')

  const colorBy = (score:number) => {
    const hue = (score + 1) * 60 // -1..1 => 0..120
    return `hsl(${hue},70%,50%)`
  }

  function toYahooUrl(input: string) {
    if (!input) return ''
    if (input.toLowerCase().startsWith('http')) return input
    const t = input.split('?')[0].toUpperCase().trim()
    return `https://finance.yahoo.com/quote/${t}`
  }

  async function go() {
    setLoading(true); setErr(''); setVal(null); setPeerVals([]); setSent(null)
    try {
      const primaryTicker = (tickerOrUrl.startsWith('http')
        ? tickerOrUrl.split('/').pop()!
        : tickerOrUrl).split('?')[0].toUpperCase()

      if (!primaryTicker) throw new Error('Enter a ticker or Yahoo Finance URL')

      const peerTickers = peers
        .split(',')
        .map(t => t.trim().toUpperCase())
        .filter(Boolean)

      const urls = [toYahooUrl(primaryTicker), ...peerTickers.map(toYahooUrl)]

      // --- bulk valuation ---
      const bulkRes = await fetch(`${API}/bulk-valuation`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ urls })
      })
      if (!bulkRes.ok) throw new Error(`Bulk valuation HTTP ${bulkRes.status}`)
      const bulk = await bulkRes.json()

      if (!bulk.success) throw new Error('Bulk valuation failed')
      const primaryVal: ValRes = bulk.data[primaryTicker] || bulk.data[primaryTicker.toUpperCase()]
      if (!primaryVal) throw new Error('Primary ticker valuation not found')

      setVal(primaryVal)
      const pv = Object.entries(bulk.data)
        .filter(([k]) => k !== primaryTicker)
        .map(([ticker, valuation]) => ({ ticker, valuation: valuation as ValRes }))
      setPeerVals(pv)

      // --- sentiment ---
      const sRes = await fetch(`${API}/sentiment`, {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ query: primaryTicker })
      })
      if (sRes.ok) {
        const s = await sRes.json()
        if (s.success) setSent(s.data as SentRes)
      }
    } catch (e:any) {
      setErr(e.message || 'Failed to fetch')
    } finally {
      setLoading(false)
    }
  }

  const chartData = (() => {
    const rows:any[] = []
    if (val) rows.push({
      name: (tickerOrUrl.split('/').pop() || tickerOrUrl).toUpperCase(),
      DCF: val.DCF.value, PE: val.PE.value, Graham: val.Graham.value
    })
    peerVals.forEach(p => rows.push({
      name: p.ticker,
      DCF: p.valuation.DCF.value,
      PE: p.valuation.PE.value,
      Graham: p.valuation.Graham.value
    }))
    return rows
  })()

  return (
    <div className="min-h-screen p-6 bg-gray-100 text-gray-800">
      <div className="max-w-3xl mx-auto space-y-4">
        <h1 className="text-3xl font-bold">QuantVestor</h1>

        <div className="grid md:grid-cols-3 gap-3">
          <input
            className="md:col-span-2 w-full p-3 border rounded"
            placeholder="Ticker or Yahoo URL (e.g., AAPL or https://finance.yahoo.com/quote/AAPL)"
            value={tickerOrUrl}
            onChange={e=>setTickerOrUrl(e.target.value)}
          />
          <input
            className="w-full p-3 border rounded"
            placeholder="Peers (comma-separated, e.g., MSFT, GOOGL)"
            value={peers}
            onChange={e=>setPeers(e.target.value)}
          />
        </div>

        <button
          className="w-full bg-blue-600 text-white py-2 rounded disabled:opacity-60"
          onClick={go}
          disabled={loading}
        >
          {loading ? 'Analyzing…' : 'Analyze'}
        </button>

        {err && <p className="text-red-600">{err}</p>}

        {/* Valuation cards */}
        {val && (['DCF','PE','Graham'] as const).map(k => (
          <div key={k} className="bg-white rounded shadow p-4">
            <div
              className="flex justify-between cursor-pointer"
              onClick={()=>setExpanded(expanded===k?null:k)}
            >
              <div className="font-semibold">{k} Valuation</div>
              <div className="font-semibold">{val[k].value}</div>
            </div>
            {expanded===k && <p className="mt-2 text-sm">{val[k].explanation}</p>}
          </div>
        ))}

        {/* Peer chart */}
        {chartData.length>1 && (
          <div className="bg-white rounded shadow p-4">
            <h2 className="text-lg font-semibold mb-2">Peer Comparison</h2>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={chartData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="DCF" />
                <Bar dataKey="PE" />
                <Bar dataKey="Graham" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Sentiment */}
        {sent && (
          <div className="bg-white rounded shadow p-4">
            <h2 className="text-lg font-semibold mb-2">Market Sentiment</h2>
            <div className="h-3 w-full bg-gray-200 rounded overflow-hidden">
              <div
                className="h-full"
                style={{ width: `${(sent.score + 1) * 50}%`, background: colorBy(sent.score) }}
              />
            </div>
            <p className="mt-2 text-sm">{sent.explanation}</p>
            <ul className="list-disc pl-5 mt-1 text-sm">
              {sent.headlines.map((h,i)=><li key={i}>{h}</li>)}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
