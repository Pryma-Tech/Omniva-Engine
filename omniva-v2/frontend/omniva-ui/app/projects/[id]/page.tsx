"use client";

import { useEffect, useState } from "react";

export default function ProjectPage({ params }: { params: { id: string } }) {
  const projectId = params.id;
  const [data, setData] = useState<any>(null);
  const [creators, setCreators] = useState("");
  const [keywords, setKeywords] = useState("");
  const [resp, setResp] = useState<any>(null);

  const load = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/projects/${projectId}`);
    const json = await res.json();
    setData(json);
    setCreators((json.creators ?? []).join(", "));
    setKeywords((json.keywords ?? []).join(", "));
  };

  const save = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/projects/${projectId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        creators: creators.split(",").map((s) => s.trim()).filter(Boolean),
        keywords: keywords.split(",").map((s) => s.trim()).filter(Boolean),
      }),
    });
    setResp(await res.json());
  };

  useEffect(() => {
    load();
  }, [projectId]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Project #{projectId}</h1>
      <button onClick={load} style={{ marginBottom: 12 }}>
        Reload
      </button>

      <h3>Creators</h3>
      <textarea value={creators} onChange={(event) => setCreators(event.target.value)} style={{ width: 400, height: 120 }} />

      <h3>Keywords</h3>
      <textarea value={keywords} onChange={(event) => setKeywords(event.target.value)} style={{ width: 400, height: 80 }} />

      <div style={{ marginTop: 12 }}>
        <button onClick={save}>Save</button>
      </div>

      <h3 style={{ marginTop: 20 }}>Current Data</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>

      <h3>Response</h3>
      <pre>{JSON.stringify(resp, null, 2)}</pre>
    </div>
  );
}
