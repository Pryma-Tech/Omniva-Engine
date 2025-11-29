"use client";

import { useState } from "react";

type GraphData = Record<string, unknown> | null;

export default function StardustPage() {
  const [data, setData] = useState<GraphData>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/stardust/graph`);
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      setData(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Stardust</h1>
      <p>Metadata cosmos and provenance graph explorer.</p>
      <button onClick={load} disabled={loading}>
        {loading ? "Loading..." : "Load Metadata Graph"}
      </button>
      {error && <p style={{ color: "tomato" }}>{error}</p>}
      <h3>Graph Snapshot</h3>
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {data ? JSON.stringify(data, null, 2) : "No data loaded yet."}
      </pre>
    </div>
  );
}
