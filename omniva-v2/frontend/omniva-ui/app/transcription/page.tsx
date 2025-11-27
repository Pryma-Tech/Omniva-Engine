"use client";

import { useState } from "react";

export default function TranscriptionPage() {
  const [filepath, setFilepath] = useState("");
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async () => {
    const api = process.env.NEXT_PUBLIC_BACKEND_URL;
    const res = await fetch(`${api}/transcription/file`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filepath, project_id: 0 }),
    });
    setResponse(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Transcription Engine Test</h1>
      <p>Enter a local media filepath to queue a Whisper transcription job.</p>
      <input
        value={filepath}
        onChange={(event) => setFilepath(event.target.value)}
        placeholder="/path/to/video.mp4"
        style={{ width: 320, marginRight: 12 }}
      />
      <button onClick={handleSubmit}>Transcribe</button>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
