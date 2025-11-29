"use client";

import { useState } from "react";

export default function FederationPage() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/federation/shared`);
      if (!response.ok) {
        throw new Error(`Failed to load shared heuristics (${response.status})`);
      }
      setData(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Federated Intelligence</h1>
      <p style={{ maxWidth: 720 }}>
        View cross-project heuristics such as niche similarity, global trend baselines, and aggregated emotional/drift
        signals shared across agents.
      </p>
      <button onClick={load} disabled={loading}>
        {loading ? "Loading..." : "Load Shared Heuristics"}
      </button>
      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "160px", marginTop: "1rem" }}>
        {data ? JSON.stringify(data, null, 2) : "No data loaded."}
      </pre>
    </div>
  );
}
