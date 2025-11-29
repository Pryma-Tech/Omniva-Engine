"use client";

import { useState } from "react";

type Snapshot = Record<string, unknown> | null;

export default function ParadoxPage() {
  const [data, setData] = useState<Snapshot>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/paradox/snapshot`);
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
      <h1>Omniva Paradox</h1>
      <p>Temporal anomaly detection and reconciliation overview.</p>
      <button onClick={load} disabled={loading}>
        {loading ? "Loading..." : "Load Paradox Snapshot"}
      </button>
      {error && <p style={{ color: "tomato" }}>{error}</p>}
      <h3>Anomalies</h3>
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {data ? JSON.stringify(data, null, 2) : "No data loaded yet."}
      </pre>
    </div>
  );
}
