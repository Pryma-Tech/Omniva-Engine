"use client";

import { useState } from "react";

export default function CognitionPage() {
  const [projectId, setProjectId] = useState("0");
  const [attention, setAttention] = useState("1.0");
  const [memory, setMemory] = useState<any>(null);
  const [updateResult, setUpdateResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const backend = process.env.NEXT_PUBLIC_BACKEND_URL;

  const loadMemory = async () => {
    setError(null);
    try {
      const response = await fetch(`${backend}/intelligence/cognition/memory/${projectId}`);
      setMemory(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load memory");
    }
  };

  const updateAttention = async () => {
    setError(null);
    setLoading(true);
    try {
      await fetch(
        `${backend}/intelligence/cognition/attention/${projectId}/${attention}`,
        { method: "POST" }
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update attention");
    } finally {
      setLoading(false);
    }
  };

  const updateFocus = async () => {
    setError(null);
    setLoading(true);
    try {
      const payload = {
        temperament: "calm",
        trend_score: 0.7,
        drift_detected: true,
      };
      const response = await fetch(
        `${backend}/intelligence/cognition/update_focus/${projectId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }
      );
      setUpdateResult(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update focus");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Cognitive State Engine</h1>
      <p style={{ maxWidth: 720 }}>
        Inspect attention levels, working memory, and focus drift signals that shape short-term prioritization and
        planner decisions.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input value={projectId} onChange={(e) => setProjectId(e.target.value)} style={{ width: "80px" }} />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        Attention:{" "}
        <input value={attention} onChange={(e) => setAttention(e.target.value)} style={{ width: "80px" }} />
        <button onClick={updateAttention} disabled={loading} style={{ marginLeft: "0.5rem" }}>
          Set Attention
        </button>
      </div>

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <button onClick={updateFocus} disabled={loading}>
          Update Focus Drift
        </button>
        <button onClick={loadMemory} disabled={loading}>
          Load Working Memory
        </button>
      </div>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Working Memory</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "120px" }}>
        {memory ? JSON.stringify(memory, null, 2) : "No entries loaded."}
      </pre>

      <h3>Focus Update</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "120px" }}>
        {updateResult ? JSON.stringify(updateResult, null, 2) : "No focus update run."}
      </pre>
    </div>
  );
}
