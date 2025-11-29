"use client";

import { useState } from "react";

export default function DeliberatePage() {
  const [projectId, setProjectId] = useState("0");
  const [input, setInput] = useState("[]");
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/deliberate/${projectId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ scored: JSON.parse(input || "[]") }),
        }
      );
      if (!response.ok) {
        throw new Error(`Deliberation failed with status ${response.status}`);
      }
      setResult(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown deliberation error");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Deliberation Engine</h1>
      <p style={{ maxWidth: 720 }}>
        Simulate the agent's internal dialogue leveraging persona, planner, cognition, and committee signals. Provide a
        scored clip list to preview the reasoning fiber and final decision.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input value={projectId} onChange={(e) => setProjectId(e.target.value)} style={{ width: "80px" }} />
      </div>

      <h3>Scored Clips (JSON)</h3>
      <textarea
        style={{ width: "100%", height: "200px", fontFamily: "monospace" }}
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button onClick={run} disabled={loading} style={{ marginTop: "0.5rem" }}>
        {loading ? "Deliberating..." : "Run Deliberation"}
      </button>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Result</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "140px" }}>
        {result ? JSON.stringify(result, null, 2) : "No deliberation run yet."}
      </pre>
    </div>
  );
}
