"use client";

import { useEffect, useState } from "react";

const apiBase = process.env.NEXT_PUBLIC_BACKEND_URL;

export default function WorkerPage() {
  const [status, setStatus] = useState<any>(null);
  const [heartbeat, setHeartbeat] = useState<any>(null);

  useEffect(() => {
    if (!apiBase) {
      setStatus({ error: "Backend URL not configured" });
      setHeartbeat(null);
      return;
    }
    fetch(`${apiBase}/worker/status`)
      .then((response) => response.json())
      .then(setStatus)
      .catch(() => setStatus({ error: "Failed to load status" }));
    fetch(`${apiBase}/worker/heartbeat`)
      .then((response) => response.json())
      .then(setHeartbeat)
      .catch(() => setHeartbeat({ error: "Failed to load heartbeat" }));
  }, [apiBase]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Worker Engine (Placeholder)</h1>
      <h2>Status</h2>
      <pre>{JSON.stringify(status ?? { status: "loading" }, null, 2)}</pre>
      <h2>Heartbeat</h2>
      <pre>{JSON.stringify(heartbeat ?? { status: "loading" }, null, 2)}</pre>
    </div>
  );
}
