"use client";

import { useState } from "react";

export default function SemanticPage() {
  const [projectId, setProjectId] = useState("0");
  const [clips, setClips] = useState(`[
  {
    "id": "test-1",
    "transcript": "This is a sample video about fitness mindset and discipline."
  }
]`);
  const [results, setResults] = useState<any>(null);

  const run = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setResults({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/semantic-rank/${projectId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: clips,
    });
    setResults(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Semantic Ranking Test</h1>
      <label>
        Project ID:
        <input value={projectId} onChange={(event) => setProjectId(event.target.value)} style={{ width: 80, marginLeft: 8 }} />
      </label>
      <h3>Clips JSON</h3>
      <textarea value={clips} onChange={(event) => setClips(event.target.value)} style={{ width: "100%", height: 200 }} />
      <button onClick={run}>Run Semantic Rank</button>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(results, null, 2)}</pre>
    </div>
  );
}
