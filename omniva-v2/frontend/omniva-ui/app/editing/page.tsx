"use client";

import { useEffect, useState } from "react";

const apiBase = process.env.NEXT_PUBLIC_BACKEND_URL;

export default function EditingPage() {
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    if (!apiBase) {
      setStatus({ error: "Backend URL not configured" });
      return;
    }
    fetch(`${apiBase}/editing/status`)
      .then((response) => response.json())
      .then(setStatus)
      .catch(() => setStatus({ error: "Failed to load status" }));
  }, [apiBase]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Editing Engine (Placeholder)</h1>
      <pre>{JSON.stringify(status ?? { status: "loading" }, null, 2)}</pre>
    </div>
  );
}
