"use client";

import { useState } from "react";

type StrategyPayload = Record<string, unknown> | null;

export default function StrategyPage() {
  const [projectId, setProjectId] = useState("0");
  const [projData, setProjData] = useState<StrategyPayload>(null);
  const [map, setMap] = useState<StrategyPayload>(null);
  const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  const loadProj = async () => {
    if (!baseUrl) {
      console.warn("Backend URL not configured");
      return;
    }
    const r = await fetch(`${baseUrl}/strategy/project/${projectId}`);
    setProjData(await r.json());
  };

  const loadMap = async () => {
    if (!baseUrl) {
      console.warn("Backend URL not configured");
      return;
    }
    const r = await fetch(`${baseUrl}/strategy/map`);
    setMap(await r.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Emergent Strategy</h1>

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <input value={projectId} onChange={(e) => setProjectId(e.target.value)} />
        <button onClick={loadProj}>Generate Project Strategy</button>
      </div>

      <button onClick={loadMap} style={{ marginBottom: "1rem" }}>
        Load Global Strategy Map
      </button>

      <h3>Project Strategy</h3>
      <pre>{projData ? JSON.stringify(projData, null, 2) : "No data yet"}</pre>

      <h3>Global Strategy Map</h3>
      <pre>{map ? JSON.stringify(map, null, 2) : "No data yet"}</pre>
    </div>
  );
}
