"use client";

import { useState } from "react";

export default function GovernancePage() {
  const [projectId, setProjectId] = useState("0");
  const [policy, setPolicy] = useState<any>(null);
  const [input, setInput] = useState("{}");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/governance/policy/${projectId}`);
      if (!response.ok) {
        throw new Error(`Failed to load policy (${response.status})`);
      }
      setPolicy(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const update = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/governance/policy/${projectId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: input,
      });
      if (!response.ok) {
        throw new Error(`Update failed (${response.status})`);
      }
      setPolicy(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Project Governance</h1>
      <p style={{ maxWidth: 720 }}>
        Configure allowed platforms, creators, posting cadence, and manual review requirements. The governance engine
        verifies these rules before the unified brain executes decisions.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input value={projectId} onChange={(e) => setProjectId(e.target.value)} style={{ width: "80px" }} />
        <button onClick={load} disabled={loading} style={{ marginLeft: "0.5rem" }}>
          Load Policy
        </button>
      </div>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Current Policy</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "160px" }}>
        {policy ? JSON.stringify(policy, null, 2) : "No policy loaded."}
      </pre>

      <h3>Update Payload (JSON)</h3>
      <textarea
        style={{ width: "100%", height: 200, fontFamily: "monospace" }}
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button onClick={update} disabled={loading} style={{ marginTop: "0.5rem" }}>
        Apply Changes
      </button>
    </div>
  );
}
