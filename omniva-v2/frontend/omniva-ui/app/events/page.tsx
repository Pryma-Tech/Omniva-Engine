"use client";

import { useEffect, useState } from "react";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export default function EventsPage() {
  const [status, setStatus] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${backendUrl}/events/status`).then((r) => r.json()).then(setStatus);
    fetch(`${backendUrl}/events/history`).then((r) => r.json()).then(setHistory);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>EventBus Inspector (Placeholder)</h1>
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <h2>Event History</h2>
      <pre>{JSON.stringify(history, null, 2)}</pre>
    </div>
  );
}
