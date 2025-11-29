"use client";

import { useState } from "react";

const defaultPayload = `{
  "temperament": "calm",
  "voice": "minimal",
  "committee": []
}`;

export default function PersonaPage() {
  const [projectId, setProjectId] = useState("0");
  const [payload, setPayload] = useState(defaultPayload);
  const [persona, setPersona] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/persona/${projectId}`
      );
      if (!response.ok) {
        throw new Error(`Load failed with status ${response.status}`);
      }
      setPersona(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown load error");
    } finally {
      setLoading(false);
    }
  };

  const update = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/persona/${projectId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: payload,
        }
      );
      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Update failed with status ${response.status}`);
      }
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown update error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Persona System</h1>
      <p style={{ maxWidth: 720 }}>
        Configure temperament, voice, and committee voters to guide internal explanations, planner summaries, and
        behavior tree debug voice.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          style={{ width: "80px", marginLeft: "0.5rem" }}
        />
      </div>

      <h3>Persona Payload</h3>
      <textarea
        style={{ width: "100%", height: "200px", fontFamily: "monospace" }}
        value={payload}
        onChange={(e) => setPayload(e.target.value)}
      />

      <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.5rem" }}>
        <button onClick={update} disabled={loading}>
          {loading ? "Saving..." : "Apply Persona"}
        </button>
        <button onClick={load} disabled={loading}>
          Load Persona
        </button>
      </div>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Active Persona</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "150px" }}>
        {persona ? JSON.stringify(persona, null, 2) : "No persona loaded yet."}
      </pre>
    </div>
  );
}
