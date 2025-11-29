"use client";

import { useState } from "react";

export default function BrainPage() {
  const [projectId, setProjectId] = useState("0");
  const [clips, setClips] = useState("[]");
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/brain/${projectId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ clips: JSON.parse(clips || "[]") }),
        }
      );
      if (!response.ok) {
        throw new Error(`Brain decision failed with status ${response.status}`);
      }
      setResult(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown brain error");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Unified Agent Brain</h1>
      <p style={{ maxWidth: 720 }}>
        Provide candidate clips to run the full arbitration layer. The brain gathers prioritization, planning,
        deliberation, emotional, and cognitive signals to determine the next action.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID: <input value={projectId} onChange={(e) => setProjectId(e.target.value)} style={{ width: "80px" }} />
      </div>

      <h3>Clips (JSON)</h3>
      <textarea
        style={{ width: "100%", height: "200px", fontFamily: "monospace" }}
        value={clips}
        onChange={(e) => setClips(e.target.value)}
      />

      <button onClick={run} disabled={loading} style={{ marginTop: "0.5rem" }}>
        {loading ? "Evaluating..." : "Run Brain Decision"}
      </button>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Decision</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "160px" }}>
        {result ? JSON.stringify(result, null, 2) : "No decision yet."}
      </pre>
    </div>
  );
}
