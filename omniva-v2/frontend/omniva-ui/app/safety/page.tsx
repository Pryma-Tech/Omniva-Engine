"use client";

import { useState } from "react";

export default function SafetyPage() {
  const [projectId, setProjectId] = useState("0");
  const [crises, setCrises] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setError(null);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/safety/crises/${projectId}`);
      if (!response.ok) {
        throw new Error(`Failed to load crises (status ${response.status})`);
      }
      setCrises(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Safety & Crisis Dashboard</h1>
      <p style={{ maxWidth: 720 }}>
        Review recorded crises triggered by safety guardrails and crisis protocols. Autonomy pauses automatically when a
        crisis occurs; investigate entries below before resuming.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input value={projectId} onChange={(e) => setProjectId(e.target.value)} style={{ width: "80px" }} />
        <button onClick={load} style={{ marginLeft: "0.5rem" }}>
          Load Crises
        </button>
      </div>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "160px" }}>
        {crises ? JSON.stringify(crises, null, 2) : "No crises loaded."}
      </pre>
    </div>
  );
}
