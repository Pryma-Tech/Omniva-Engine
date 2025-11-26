"use client";

import { useEffect, useState } from "react";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export default function SchedulerPage() {
  const [status, setStatus] = useState<any>(null);
  const [rules, setRules] = useState<any>([]);

  useEffect(() => {
    fetch(`${backendUrl}/scheduler/status`).then((r) => r.json()).then(setStatus);
    fetch(`${backendUrl}/scheduler/rules`).then((r) => r.json()).then(setRules);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Scheduler Engine (Placeholder)</h1>
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <h2>Rules</h2>
      <pre>{JSON.stringify(rules, null, 2)}</pre>
    </div>
  );
}
