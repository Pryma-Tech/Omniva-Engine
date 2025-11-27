"use client";

import { useState } from "react";

export default function TrendingPage() {
  const [projectId, setProjectId] = useState("0");
  const [data, setData] = useState<any>(null);

  const load = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setData({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/trending/${projectId}`);
    setData(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Trending Keywords</h1>
      <input value={projectId} onChange={(event) => setProjectId(event.target.value)} style={{ width: 80, marginRight: 8 }} />
      <button onClick={load}>Load</button>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
