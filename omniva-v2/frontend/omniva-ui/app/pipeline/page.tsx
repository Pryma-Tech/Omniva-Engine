"use client";

import { useState } from "react";
import PipelineGraph from "./PipelineGraph";

export default function PipelinePage() {
  const [project, setProject] = useState("0");
  const [response, setResponse] = useState<any>(null);

  const run = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setResponse({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/pipeline/run/${project}`, {
      method: "POST",
    });
    setResponse(await res.json());
  };

  return (
    <section style={{ padding: 20 }}>
      <h1>Pipeline Control</h1>
      <div style={{ marginBottom: 16 }}>
        <input value={project} onChange={(event) => setProject(event.target.value)} style={{ width: 80, marginRight: 8 }} />
        <button onClick={run}>Start Pipeline</button>
      </div>
      <pre>{JSON.stringify(response, null, 2)}</pre>
      <h2>Visualization</h2>
      <PipelineGraph />
    </section>
  );
}
