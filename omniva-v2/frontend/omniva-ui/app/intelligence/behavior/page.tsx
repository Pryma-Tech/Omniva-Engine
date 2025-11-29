"use client";

import { useState } from "react";

const defaultPayload = `{
  "project": {
    "id": 0,
    "autonomous": true,
    "seed_links": [
      "https://example.com/post-1",
      "https://example.com/post-2"
    ]
  }
}`;

export default function BehaviorPage() {
  const [projectId, setProjectId] = useState("0");
  const [payload, setPayload] = useState(defaultPayload);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/behavior/run/${projectId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: payload,
        }
      );
      if (!response.ok) {
        const detail = await response.text();
        throw new Error(detail || `Request failed with status ${response.status}`);
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
      <h1>Behavior Tree Simulator</h1>
      <p style={{ maxWidth: 720 }}>
        Run the project-specific behavior tree to see how Omniva sequences discovery, downloads, scoring, and
        personality-driven decisions. Customize the payload to spoof links or simulated project metadata.
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
        style={{ width: "100%", height: "200px", fontFamily: "monospace" }}
      />

      <button onClick={run} disabled={loading} style={{ marginTop: "0.5rem" }}>
        {loading ? "Running..." : "Run Behavior Tree"}
      </button>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Result</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", overflowX: "auto" }}>
        {result ? JSON.stringify(result, null, 2) : "No run yet."}
      </pre>

      {result?.context?.trace && (
        <>
          <h3>Node Trace</h3>
          <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", overflowX: "auto" }}>
            {JSON.stringify(result.context.trace, null, 2)}
          </pre>
        </>
      )}
    </div>
  );
}
