"use client";

import { useState } from "react";

export default function OrchestratorPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const call = async (endpoint: string, method: "GET" | "POST") => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/orchestrator/${endpoint}`, { method });
      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
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
      <h1>Omniva Master Orchestrator</h1>
      <p style={{ maxWidth: 720 }}>
        Coordinate every subsystem: start/stop autonomy for all projects, run a global cycle, or fetch the aggregated
        health report.
      </p>
      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "1rem" }}>
        <button onClick={() => call("start_all", "POST")} disabled={loading}>
          Start All Projects
        </button>
        <button onClick={() => call("stop_all", "POST")} disabled={loading}>
          Stop All Projects
        </button>
        <button onClick={() => call("cycle", "GET")} disabled={loading}>
          Run Global Cycle
        </button>
        <button onClick={() => call("health", "GET")} disabled={loading}>
          System Health
        </button>
      </div>
      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "160px" }}>
        {data ? JSON.stringify(data, null, 2) : "No orchestration actions yet."}
      </pre>
    </div>
  );
}
