"use client";

import { useState } from "react";

export default function GhostRunPage() {
  const [projectId, setProjectId] = useState("0");
  const [payload, setPayload] = useState(`{
  "clips": [
    {
      "id": "test-1",
      "transcript": "Discipline and fitness mindset makes success.",
      "meta": {"link": "x", "local": "y"}
    },
    {
      "id": "test-2",
      "transcript": "Entrepreneurship requires resilience and patience.",
      "meta": {"link": "x", "local": "y"}
    }
  ],
  "rounds": 5
}`);
  const [result, setResult] = useState<unknown>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/ghost-run/${projectId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: payload,
        }
      );
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }
      const json = await response.json();
      setResult(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Ghost-Run Simulation Engine</h1>
      <p style={{ maxWidth: 640 }}>
        Simulate end-to-end intelligence runs using cached or synthetic data. No files are downloaded,
        uploaded, or modified—ideal for offline training and strategy experiments.
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

      <button onClick={run} disabled={loading} style={{ marginTop: "0.5rem" }}>
        {loading ? "Running..." : "Run Ghost Simulation"}
      </button>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Simulation Result</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px" }}>
        {result ? JSON.stringify(result, null, 2) : "No runs yet."}
      </pre>
    </div>
  );
}
