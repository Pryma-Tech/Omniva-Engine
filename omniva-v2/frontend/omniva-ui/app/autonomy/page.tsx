"use client";

import { useState } from "react";

export default function AutonomyPage() {
  const [projectId, setProjectId] = useState("0");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const call = async (endpoint: "start" | "stop" | "pause" | "resume") => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/autonomy/${endpoint}/${projectId}`,
        { method: "POST" }
      );
      if (!response.ok) {
        throw new Error(`Autonomy ${endpoint} failed (${response.status})`);
      }
      setResult(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown autonomy error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Autonomy Control</h1>
      <p style={{ maxWidth: 720 }}>
        Start, stop, or pause the dual-loop Autonomy Kernel for a project. Loops drive micro (cognitive) and macro
        (brain) cycles with adaptive timing.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input value={projectId} onChange={(e) => setProjectId(e.target.value)} style={{ width: "80px" }} />
      </div>

      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
        <button onClick={() => call("start")} disabled={loading}>
          Start
        </button>
        <button onClick={() => call("stop")} disabled={loading}>
          Stop
        </button>
        <button onClick={() => call("pause")} disabled={loading}>
          Pause
        </button>
        <button onClick={() => call("resume")} disabled={loading}>
          Resume
        </button>
      </div>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Result</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "120px" }}>
        {result ? JSON.stringify(result, null, 2) : "No commands issued yet."}
      </pre>
    </div>
  );
}
