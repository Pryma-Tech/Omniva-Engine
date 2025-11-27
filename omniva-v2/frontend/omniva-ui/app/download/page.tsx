"use client";

import { useState } from "react";

export default function DownloadPage() {
  const [url, setUrl] = useState("");
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async () => {
    const api = process.env.NEXT_PUBLIC_BACKEND_URL;
    const res = await fetch(`${api}/download/url`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, project_id: 0 }),
    });
    setResponse(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Download Engine Test</h1>
      <p>Enter a TikTok, Instagram, or YouTube URL to queue a download.</p>
      <input
        style={{ width: 320, marginRight: 12 }}
        value={url}
        onChange={(event) => setUrl(event.target.value)}
        placeholder="https://www.tiktok.com/@..."
      />
      <button onClick={handleSubmit}>Queue Download</button>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
