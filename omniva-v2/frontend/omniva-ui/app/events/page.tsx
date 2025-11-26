"use client";

import { useEffect, useState } from "react";

const apiBase = process.env.NEXT_PUBLIC_BACKEND_URL;

export default function EventsPage() {
  const [status, setStatus] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    if (!apiBase) {
      setStatus({ error: "Backend URL not configured" });
      setHistory([]);
      return;
    }
    fetch(`${apiBase}/events/status`)
      .then((response) => response.json())
      .then(setStatus)
      .catch(() => setStatus({ error: "Failed to load status" }));
    fetch(`${apiBase}/events/history`)
      .then((response) => response.json())
      .then(setHistory)
      .catch(() => setHistory([]));
  }, [apiBase]);

  return (
    <div style={{ padding: 20 }}>
      <h1>EventBus Inspector (Placeholder)</h1>
      <h2>Status</h2>
      <pre>{JSON.stringify(status ?? { status: "loading" }, null, 2)}</pre>
      <h2>Event History</h2>
      <pre>{JSON.stringify(history ?? [], null, 2)}</pre>
    </div>
  );
}
