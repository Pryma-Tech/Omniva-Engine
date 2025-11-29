"use client";

import { useState } from "react";

type ObservatoryData = Record<string, unknown> | null;

export default function ObservatoryPage() {
  const [data, setData] = useState<ObservatoryData>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/observatory/insights`);
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Observatory</h1>
      <p>Global insight layer combining emotion, drift, federation, identity, and archival history.</p>
      <button onClick={load} disabled={loading}>
        {loading ? "Loading..." : "Load Insights"}
      </button>
      {error && (
        <p style={{ color: "tomato" }}>
          Failed to load insights: {error}
        </p>
      )}
      <h3>Global Insights</h3>
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {data ? JSON.stringify(data, null, 2) : "No data loaded yet."}
      </pre>
    </div>
  );
}
