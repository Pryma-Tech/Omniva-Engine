"use client";

import { useState } from "react";

type ArchivePayload = Record<string, unknown> | null;

export default function ArchivePage() {
  const [data, setData] = useState<ArchivePayload>(null);
  const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  const load = async (endpoint: "summary" | "timeline" | "epochs") => {
    if (!baseUrl) {
      console.warn("Backend URL not configured");
      return;
    }
    const r = await fetch(`${baseUrl}/archive/${endpoint}`);
    setData(await r.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Archive</h1>

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <button onClick={() => load("summary")}>Load Summary</button>
        <button onClick={() => load("timeline")}>Load Timeline</button>
        <button onClick={() => load("epochs")}>Load Epochs</button>
      </div>

      <h3>Data</h3>
      <pre>{data ? JSON.stringify(data, null, 2) : "No archive data yet."}</pre>
    </div>
  );
}
