"use client";

import { useState } from "react";

type EclipseData = Record<string, unknown> | null;

export default function EclipsePage() {
  const [data, setData] = useState<EclipseData>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/eclipse/snapshot`);
      if (!response.ok) {
        throw new Error(`Snapshot failed: ${response.status}`);
      }
      setData(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const resolve = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/eclipse/resolve`, {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error(`Resolve failed: ${response.status}`);
      }
      setData(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Eclipse</h1>
      <p>Crisis detection, recovery rituals, and failsafe orchestration.</p>
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <button onClick={load} disabled={loading}>
          {loading ? "Loading..." : "Load Crisis Snapshot"}
        </button>
        <button onClick={resolve} disabled={loading}>
          {loading ? "Resolving..." : "Resolve Crisis"}
        </button>
      </div>
      {error && <p style={{ color: "tomato" }}>{error}</p>}
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {data ? JSON.stringify(data, null, 2) : "No data loaded yet."}
      </pre>
    </div>
  );
}
