"use client";

import { useEffect, useState } from "react";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export default function UploaderPage() {
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    fetch(`${backendUrl}/uploader/status`)
      .then((r) => r.json())
      .then(setStatus)
      .catch(() => setStatus({ error: "Failed to load status" }));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Uploader Engine (Placeholder)</h1>
      <pre>{JSON.stringify(status, null, 2)}</pre>
    </div>
  );
}
