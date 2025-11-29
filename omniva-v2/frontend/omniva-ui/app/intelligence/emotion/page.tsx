"use client";

import { useState } from "react";

export default function EmotionPage() {
  const [projectId, setProjectId] = useState("0");
  const [emotion, setEmotion] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setError(null);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/emotion/${projectId}`
      );
      if (!response.ok) {
        throw new Error(`Failed to load emotion (status ${response.status})`);
      }
      setEmotion(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Emotional State Dashboard</h1>
      <p style={{ maxWidth: 720 }}>
        Inspect the synthetic affective signals (excitement, stress, curiosity, confidence, stability) that influence
        prioritization, planning, and deliberation.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input value={projectId} onChange={(e) => setProjectId(e.target.value)} style={{ width: "80px" }} />
      </div>

      <button onClick={load}>Load Emotional State</button>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Emotion</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "140px" }}>
        {emotion ? JSON.stringify(emotion, null, 2) : "No emotion data loaded."}
      </pre>
    </div>
  );
}
