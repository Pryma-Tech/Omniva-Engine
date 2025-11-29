"use client";

import { useState } from "react";

const defaultPayload = `{
  "clips": [
    { "id": "c1", "transcript": "Discipline builds strength", "meta": {} },
    { "id": "c2", "transcript": "Entrepreneurship requires vision", "meta": {} }
  ],
  "rounds": 5,
  "ghost_rounds": 5
}`;

export default function OptimizerPage() {
  const [projectId, setProjectId] = useState("0");
  const [payload, setPayload] = useState(defaultPayload);
  const [result, setResult] = useState<unknown>(null);
  const [history, setHistory] = useState<unknown>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/self-opt/${projectId}`,
        { method: "POST", headers: { "Content-Type": "application/json" }, body: payload }
      );
      if (!response.ok) {
        throw new Error(`Run failed with status ${response.status}`);
      }
      setResult(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown run error");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = async () => {
    setError(null);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/self-opt/history/${projectId}`
      );
      if (!response.ok) {
        throw new Error(`History failed with status ${response.status}`);
      }
      setHistory(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown history error");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Self-Optimization Engine</h1>
      <p style={{ maxWidth: 640 }}>
        Batch ghost simulations, evaluate recommendation score distributions, and automatically tune
        prioritizer weights. Nothing touches live storage, making this safe for offline experimentation.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          style={{ width: "80px", marginLeft: "0.5rem" }}
        />
      </div>

      <h3>Payload</h3>
      <textarea
        value={payload}
        onChange={(e) => setPayload(e.target.value)}
        style={{ width: "100%", height: "200px" }}
      />

      <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.5rem" }}>
        <button onClick={run} disabled={loading}>
          {loading ? "Optimizing..." : "Run Self-Optimization"}
        </button>
        <button onClick={loadHistory}>Load History</button>
      </div>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Result</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px" }}>
        {result ? JSON.stringify(result, null, 2) : "No run yet."}
      </pre>

      <h3>History</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px" }}>
        {history ? JSON.stringify(history, null, 2) : "No history loaded."}
      </pre>
    </div>
  );
}
