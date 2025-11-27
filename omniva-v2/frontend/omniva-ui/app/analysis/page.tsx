"use client";

import { useState } from "react";

export default function AnalysisPage() {
  const [filepath, setFilepath] = useState("");
  const [keywords, setKeywords] = useState("");
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async () => {
    const api = process.env.NEXT_PUBLIC_BACKEND_URL;
    const res = await fetch(`${api}/analysis/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filepath,
        project_id: 0,
        keywords: keywords
          .split(",")
          .map((entry) => entry.trim())
          .filter(Boolean),
      }),
    });
    setResponse(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Analysis Engine Test</h1>
      <p>Queue the analysis engine for a transcript JSON file.</p>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 420 }}>
        <input
          value={filepath}
          onChange={(event) => setFilepath(event.target.value)}
          placeholder="/storage/projects/1/transcripts/file.mp4.json"
          style={{ padding: 8 }}
        />
        <input
          value={keywords}
          onChange={(event) => setKeywords(event.target.value)}
          placeholder="motivation, hustle"
          style={{ padding: 8 }}
        />
        <button onClick={handleSubmit}>Analyze</button>
      </div>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
