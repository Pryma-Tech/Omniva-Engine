"use client";

import { useEffect, useState } from "react";

export default function IntelligencePage() {
  const [status, setStatus] = useState<any>(null);
  const [mode, setMode] = useState("balanced");
  const [response, setResponse] = useState<any>(null);

  const load = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setStatus({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/status`);
    setStatus(await res.json());
  };

  const changeMode = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setResponse({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/mode/${mode}`, {
      method: "POST",
    });
    setResponse(await res.json());
    load();
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Intelligence Engine</h1>
      <pre>{JSON.stringify(status, null, 2)}</pre>

      <h3>Set Mode</h3>
      <select value={mode} onChange={(event) => setMode(event.target.value)} style={{ marginRight: 8 }}>
        <option value="balanced">Balanced</option>
        <option value="viral">Viral First</option>
        <option value="evergreen">Evergreen</option>
      </select>
      <button onClick={changeMode}>Apply</button>

      <h3>Response</h3>
      <pre>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
