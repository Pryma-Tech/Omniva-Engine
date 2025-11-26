"use client";

import { useEffect, useState } from "react";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export default function WorkerPage() {
  const [status, setStatus] = useState<any>(null);
  const [heartbeat, setHeartbeat] = useState<any>(null);

  useEffect(() => {
    fetch(`${backendUrl}/worker/status`).then((r) => r.json()).then(setStatus);
    fetch(`${backendUrl}/worker/heartbeat`).then((r) => r.json()).then(setHeartbeat);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Worker Engine (Placeholder)</h1>
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <h2>Heartbeat</h2>
      <pre>{JSON.stringify(heartbeat, null, 2)}</pre>
    </div>
  );
}
