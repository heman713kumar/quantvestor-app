import React, { useState } from "react";

type ValuationRow = { model: string; target: number; entry?: number; note?: string };

const demoData: { valuations: ValuationRow[]; sentiment: { scorePct: number; label: string } } = {
  valuations: [
    { model: "DCF", target: 388.14, entry: 258.76, note: "10y FCF, 7.3% discount" },
    { model: "PE (7Y Avg)", target: 230.85, entry: 153.75, note: "Forward EPS × historical PE" },
    { model: "EV/EBITDA", target: 214.79, entry: 143.19, note: "EV/EBITDA multiple approach" },
    { model: "Graham (old)", target: 150.88, note: "EPS × (8.5 + 2g)" },
  ],
  sentiment: { scorePct: 62, label: "Positive" },
};

const API_BASE = import.meta.env.VITE_API_BASE as string | undefined;

export default function App() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<typeof demoData | null>(null);

  async function runAnalysis(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setData(null);

    // If no backend yet, fall back to demo so the UI works now
    if (!API_BASE) {
      await new Promise(r => setTimeout(r, 600));
      setData(demoData);
      setLoading(false);
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/valuation?url=${encodeURIComponent(url)}`);
      if (!res.ok) throw new Error(`API ${res.status}`);
      const json = await res.json();
      setData(json);
    } catch (err: any) {
      setError(err?.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold">Welcome to QuantVestor 📊</h1>
      <p className="mt-2 text-gray-600">Your personal stock analysis dashboard.</p>

      <form onSubmit={runAnalysis} className="mt-6 flex gap-2">
        <input
          className="border rounded-md px-3 py-2 flex-1"
          placeholder="Paste a Yahoo Finance URL, e.g. https://finance.yahoo.com/quote/EMUDHRA.NS"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 rounded-md bg-black text-white disabled:opacity-60"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && <div className="mt-4 text-red-600">Error: {error}</div>}

      {data && (
        <div className="mt-8 space-y-6">
          {/* Sentiment */}
          <section>
            <h2 className="font-semibold">Sentiment (3 months)</h2>
            <div className="mt-2 flex items-center gap-3">
              <div className="w-64 h-3 bg-red-200 rounded-full overflow-hidden">
                <div
                  className="h-3 bg-green-500"
                  style={{ width: `${Math.max(0, Math.min(100, data.sentiment.scorePct))}%` }}
                />
              </div>
              <span className="text-sm text-gray-700">
                {data.sentiment.scorePct}% — {data.sentiment.label}
              </span>
            </div>
          </section>

          {/* Valuations */}
          <section>
            <h2 className="font-semibold mb-2">Valuation Models</h2>
            <div className="overflow-x-auto border rounded-lg">
              <table className="min-w-full text-sm">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="text-left p-3">Model</th>
                    <th className="text-right p-3">Target</th>
                    <th className="text-right p-3">Entry</th>
                    <th className="text-left p-3">Why?</th>
                  </tr>
                </thead>
                <tbody>
                  {data.valuations.map((v, i) => (
                    <tr key={i} className="border-t">
                      <td className="p-3">{v.model}</td>
                      <td className="p-3 text-right">₹{v.target.toFixed(2)}</td>
                      <td className="p-3 text-right">{v.entry ? `₹${v.entry.toFixed(2)}` : "—"}</td>
                      <td className="p-3">
                        <details>
                          <summary className="cursor-pointer text-blue-600">Explain</summary>
                          <div className="mt-2 text-gray-700">
                            {v.note || "Formula details coming from backend explanation."}
                          </div>
                        </details>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
