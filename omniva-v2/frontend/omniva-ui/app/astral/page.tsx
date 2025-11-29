"use client";

import { useState } from "react";

type AstralSnapshot = Record<string, unknown> | null;

export default function AstralPage() {
  const [data, setData] = useState<AstralSnapshot>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/astral/snapshot`);
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
      <h1>Omniva Astral</h1>
      <p>Counterfactual multi-world futures for every project.</p>
      <button onClick={load} disabled={loading}>
        {loading ? "Loading..." : "Load Multi-World Snapshot"}
      </button>
      {error && <p style={{ color: "tomato" }}>{error}</p>}
      <h3>Data</h3>
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {data ? JSON.stringify(data, null, 2) : "No data loaded yet."}
      </pre>
    </div>
  );
}
