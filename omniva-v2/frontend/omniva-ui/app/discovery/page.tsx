"use client";

import { useState } from "react";

export default function DiscoveryPage() {
  const [projectId, setProjectId] = useState("0");
  const [response, setResponse] = useState<any>(null);

  const run = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setResponse({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/discover/project/${projectId}`);
    setResponse(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Discovery Debugger</h1>
      <input value={projectId} onChange={(event) => setProjectId(event.target.value)} style={{ width: 80, marginRight: 8 }} />
      <button onClick={run}>Discover</button>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
