"use client";

import { useEffect, useState } from "react";

const apiBase = process.env.NEXT_PUBLIC_BACKEND_URL;

export default function UploaderPage() {
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    if (!apiBase) {
      setStatus({ error: "Backend URL not configured" });
      return;
    }
    fetch(`${apiBase}/uploader/status`)
      .then((response) => response.json())
      .then(setStatus)
      .catch(() => setStatus({ error: "Failed to load status" }));
  }, [apiBase]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Uploader Engine (Placeholder)</h1>
      <pre>{JSON.stringify(status ?? { status: "loading" }, null, 2)}</pre>
    </div>
  );
}
