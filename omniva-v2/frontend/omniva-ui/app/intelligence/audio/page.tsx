"use client";

import { useState } from "react";

export default function AudioTrendsPage() {
  const [projectId, setProjectId] = useState("0");
  const [payload, setPayload] = useState(`{
  "id": "example-clip",
  "audio_id": "sound_xyz"
}`);
  const [trends, setTrends] = useState<any>(null);
  const [match, setMatch] = useState<any>(null);

  const loadTrends = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setTrends({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/audio-trends/${projectId}`);
    setTrends(await res.json());
  };

  const runMatch = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setMatch({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/audio-match/${projectId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: payload,
    });
    setMatch(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Audio Trend Intelligence</h1>
      <div>
        Project ID:
        <input value={projectId} onChange={(event) => setProjectId(event.target.value)} style={{ width: 80, marginLeft: 8 }} />
      </div>
      <h3>Clip Meta JSON</h3>
      <textarea value={payload} onChange={(event) => setPayload(event.target.value)} style={{ width: "100%", height: 200 }} />
      <button onClick={loadTrends}>Load Trends</button>
      <button onClick={runMatch} style={{ marginLeft: 8 }}>
        Match Audio
      </button>
      <h3>Trending Audio</h3>
      <pre>{JSON.stringify(trends, null, 2)}</pre>
      <h3>Match Result</h3>
      <pre>{JSON.stringify(match, null, 2)}</pre>
    </div>
  );
}
