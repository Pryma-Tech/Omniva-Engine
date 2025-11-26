"use client";

import { useEffect, useState } from "react";

const apiBase = process.env.NEXT_PUBLIC_BACKEND_URL;

export default function TemplatesPage() {
  const [status, setStatus] = useState<any>(null);
  const [templates, setTemplates] = useState<any[]>([]);

  useEffect(() => {
    if (!apiBase) {
      setStatus({ error: "Backend URL not configured" });
      setTemplates([]);
      return;
    }
    fetch(`${apiBase}/templates/status`)
      .then((response) => response.json())
      .then(setStatus)
      .catch(() => setStatus({ error: "Failed to load status" }));
    fetch(`${apiBase}/templates/list`)
      .then((response) => response.json())
      .then(setTemplates)
      .catch(() => setTemplates([]));
  }, [apiBase]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Style & Template Engine (Placeholder)</h1>
      <h2>Status</h2>
      <pre>{JSON.stringify(status ?? { status: "loading" }, null, 2)}</pre>
      <h2>Templates</h2>
      <pre>{JSON.stringify(templates ?? [], null, 2)}</pre>
    </div>
  );
}
