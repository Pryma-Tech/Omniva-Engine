"use client";

import { useState } from "react";

type Snapshot = Record<string, unknown> | null;
type Brief = Record<string, unknown> | null;

export default function NexusPage() {
  const [snapshot, setSnapshot] = useState<Snapshot>(null);
  const [projectId, setProjectId] = useState("0");
  const [brief, setBrief] = useState<Brief>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadSnapshot = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/nexus/snapshot`);
      if (!response.ok) {
        throw new Error(`Snapshot failed: ${response.status}`);
      }
      setSnapshot(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setSnapshot(null);
    } finally {
      setLoading(false);
    }
  };

  const loadBrief = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/nexus/project/${projectId}`);
      if (!response.ok) {
        throw new Error(`Brief failed: ${response.status}`);
      }
      setBrief(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setBrief(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Nexus</h1>
      <p>Unified gateway for global insight snapshots and composed project briefs.</p>
      <div style={{ display: "flex", gap: "1rem", alignItems: "center", marginBottom: "1rem" }}>
        <button onClick={loadSnapshot} disabled={loading}>
          {loading ? "Loading..." : "Load Full Snapshot"}
        </button>
        <label>
          Project ID:
          <input
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
            style={{ marginLeft: "0.5rem" }}
          />
        </label>
        <button onClick={loadBrief} disabled={loading}>
          {loading ? "Loading..." : "Load Brief"}
        </button>
      </div>
      {error && <p style={{ color: "tomato" }}>Error: {error}</p>}
      <h3>Snapshot</h3>
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {snapshot ? JSON.stringify(snapshot, null, 2) : "No snapshot loaded."}
      </pre>
      <h3>Project Brief</h3>
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {brief ? JSON.stringify(brief, null, 2) : "No project brief loaded."}
      </pre>
    </div>
  );
}
