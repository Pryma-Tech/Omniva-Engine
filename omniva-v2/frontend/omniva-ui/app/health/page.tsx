"use client";

import { useEffect, useState } from "react";

export default function HealthPage() {
  const [data, setData] = useState<any>(null);

  const load = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setData({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/health`);
    setData(await res.json());
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>System Health</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
