"use client";

import { useState } from "react";

export default function UploaderPage() {
  const [clips, setClips] = useState("");
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async () => {
    const api = process.env.NEXT_PUBLIC_BACKEND_URL;
    const payload = {
      clips: clips
        .split(",")
        .map((entry) => entry.trim())
        .filter(Boolean),
      project_id: 0,
    };

    const res = await fetch(`${api}/uploader/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    setResponse(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Uploader Engine Test</h1>
      <p>Provide one or more clip paths to queue a YouTube upload job.</p>
      <textarea
        value={clips}
        onChange={(event) => setClips(event.target.value)}
        placeholder="/storage/projects/1/clips/clip_0_final.mp4, /storage/projects/1/clips/clip_1_final.mp4"
        style={{ width: 420, height: 120, marginBottom: 12 }}
      />
      <div>
        <button onClick={handleSubmit}>Upload Clips</button>
      </div>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
