"use client";

import { useState } from "react";

type InfinityData = Record<string, unknown> | null;

export default function InfinityPage() {
  const [data, setData] = useState<InfinityData>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadSnapshot = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/infinity/snapshot`);
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

  const runScale = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/infinity/scale`, {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error(`Scale failed: ${response.status}`);
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
      <h1>Omniva Infinity</h1>
      <p>Elastic compute orchestration and temporal load balancing.</p>
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <button onClick={loadSnapshot} disabled={loading}>
          {loading ? "Loading..." : "Load Snapshot"}
        </button>
        <button onClick={runScale} disabled={loading}>
          {loading ? "Scaling..." : "Run Scale Cycle"}
        </button>
      </div>
      {error && <p style={{ color: "tomato" }}>{error}</p>}
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {data ? JSON.stringify(data, null, 2) : "No data loaded yet."}
      </pre>
    </div>
  );
}
