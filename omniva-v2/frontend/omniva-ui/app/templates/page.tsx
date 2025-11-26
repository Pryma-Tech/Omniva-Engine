"use client";

import { useEffect, useState } from "react";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export default function TemplatesPage() {
  const [status, setStatus] = useState<any>(null);
  const [templates, setTemplates] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${backendUrl}/templates/status`).then((r) => r.json()).then(setStatus);
    fetch(`${backendUrl}/templates/list`).then((r) => r.json()).then(setTemplates);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Style & Template Engine (Placeholder)</h1>
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <h2>Templates</h2>
      <pre>{JSON.stringify(templates, null, 2)}</pre>
    </div>
  );
}
