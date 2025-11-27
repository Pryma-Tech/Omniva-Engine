"use client";

import { useState } from "react";

export default function EditingPage() {
  const [analysis, setAnalysis] = useState("");
  const [topN, setTopN] = useState("1");
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async () => {
    const api = process.env.NEXT_PUBLIC_BACKEND_URL;
    const res = await fetch(`${api}/editing/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        analysis_filepath: analysis,
        project_id: 0,
        top_n: Number.parseInt(topN, 10) || 1,
      }),
    });
    setResponse(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Editing Engine Test</h1>
      <p>Render clips directly by pointing to an analysis JSON file.</p>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 420 }}>
        <input
          value={analysis}
          onChange={(event) => setAnalysis(event.target.value)}
          placeholder="/storage/projects/1/analysis/file.mp4.json"
          style={{ padding: 8 }}
        />
        <input
          value={topN}
          onChange={(event) => setTopN(event.target.value)}
          style={{ padding: 8, width: 120 }}
        />
        <button onClick={handleSubmit}>Render Clips</button>
      </div>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
