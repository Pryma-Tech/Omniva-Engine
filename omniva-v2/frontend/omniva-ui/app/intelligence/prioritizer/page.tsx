"use client";

import { useState } from "react";

export default function PrioritizerPage() {
  const [projectId, setProjectId] = useState("0");
  const [payload, setPayload] = useState(`{
  "semantic": [
    { "clip_id": "a", "semantic_similarity": 0.92 },
    { "clip_id": "b", "semantic_similarity": 0.54 }
  ],
  "keyword": [
    { "clip_id": "a", "niche_score": 4, "trend_score": 8, "total_score": 6 },
    { "clip_id": "b", "niche_score": 1, "trend_score": 2, "total_score": 1.4 }
  ],
  "audio": [
    { "clip_id": "a", "audio_score": 3 },
    { "clip_id": "b", "audio_score": 1 }
  ]
}`);
  const [result, setResult] = useState<any>(null);
  const [weights, setWeights] = useState<any>(null);

  const run = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setResult({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/prioritize/${projectId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: payload,
    });
    setResult(await res.json());
  };

  const loadWeights = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setWeights({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/prioritizer/weights`);
    setWeights(await res.json());
  };

  const updateWeights = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      return;
    }
    const newWeights = prompt("Enter JSON weights object", JSON.stringify(weights, null, 2));
    if (!newWeights) return;
    await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/prioritizer/weights`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: newWeights,
    });
    loadWeights();
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Clip Prioritization Engine</h1>
      <div>
        Project ID:
        <input value={projectId} onChange={(event) => setProjectId(event.target.value)} style={{ width: 80, marginLeft: 8 }} />
      </div>
      <h3>Payload JSON</h3>
      <textarea value={payload} onChange={(event) => setPayload(event.target.value)} style={{ width: "100%", height: 220 }} />
      <button onClick={run}>Run Prioritization</button>
      <h3>Weights</h3>
      <button onClick={loadWeights}>Load Weights</button>
      <button onClick={updateWeights} style={{ marginLeft: 8 }}>
        Update Weights
      </button>
      <pre>{JSON.stringify(weights, null, 2)}</pre>
      <h3>Results</h3>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}
