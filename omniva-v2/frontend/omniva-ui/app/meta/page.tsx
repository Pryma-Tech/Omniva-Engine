"use client";

import { useState } from "react";

export default function MetaPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/meta/run`);
      if (!response.ok) {
        throw new Error(`Meta cycle failed (${response.status})`);
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
      <h1>Strategic Meta-Learning</h1>
      <p style={{ maxWidth: 720 }}>
        Execute the meta-learning engine to evolve governance policies, persona temperaments, and federated heuristics
        based on cross-project observations.
      </p>
      <button onClick={run} disabled={loading}>
        {loading ? "Running..." : "Run Meta-Learning Cycle"}
      </button>
      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "160px", marginTop: "1rem" }}>
        {data ? JSON.stringify(data, null, 2) : "No meta-learning run yet."}
      </pre>
    </div>
  );
}
