"use client";

import { useState } from "react";

type IdentityPayload = {
  state: Record<string, unknown>;
  history: Array<Record<string, unknown>>;
};

export default function IdentityPage() {
  const [data, setData] = useState<IdentityPayload | null>(null);
  const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  const load = async () => {
    if (!baseUrl) {
      console.warn("Backend URL not configured");
      return;
    }
    const r = await fetch(`${baseUrl}/identity/`);
    setData(await r.json());
  };

  const recompute = async () => {
    if (!baseUrl) {
      console.warn("Backend URL not configured");
      return;
    }
    const r = await fetch(`${baseUrl}/identity/recompute`, { method: "POST" });
    setData(await r.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Agent Identity</h1>

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <button onClick={load}>Load Identity</button>
        <button onClick={recompute}>Recompute Identity</button>
      </div>

      <h3>Current Identity State</h3>
      <pre>{data ? JSON.stringify(data, null, 2) : "No data yet"}</pre>
    </div>
  );
}
