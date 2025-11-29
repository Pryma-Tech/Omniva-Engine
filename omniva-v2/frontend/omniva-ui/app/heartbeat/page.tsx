"use client";

import { useState } from "react";

export default function HeartbeatPage() {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const call = async (endpoint: string, method: "GET" | "POST") => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/heartbeat/${endpoint}`, { method });
      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
      }
      setStatus(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Heartbeat</h1>
      <p style={{ maxWidth: 720 }}>
        Start or stop the global heartbeat loop, or query the current status. The heartbeat drives scheduled resets,
        orchestrator cycles, and agent keepalives.
      </p>
      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "1rem" }}>
        <button onClick={() => call("start", "POST")} disabled={loading}>
          Start Heartbeat
        </button>
        <button onClick={() => call("stop", "POST")} disabled={loading}>
          Stop Heartbeat
        </button>
        <button onClick={() => call("status", "GET")} disabled={loading}>
          Status
        </button>
      </div>
      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "140px" }}>
        {status ? JSON.stringify(status, null, 2) : "No heartbeat command issued yet."}
      </pre>
    </div>
  );
}
