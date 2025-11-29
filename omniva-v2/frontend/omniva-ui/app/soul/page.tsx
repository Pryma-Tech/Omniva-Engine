"use client";

import { useState } from "react";

type CodexPayload = Record<string, unknown> | null;

export default function SoulPage() {
  const [data, setData] = useState<CodexPayload>(null);
  const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  const load = async () => {
    if (!baseUrl) {
      console.warn("Backend URL not configured");
      return;
    }
    const r = await fetch(`${baseUrl}/soul/codex`);
    setData(await r.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva — The Codex of Lore</h1>
      <button onClick={load}>Reveal Codex</button>

      <pre style={{ marginTop: 20 }}>{data ? JSON.stringify(data, null, 2) : "No lore revealed yet."}</pre>
    </div>
  );
}
