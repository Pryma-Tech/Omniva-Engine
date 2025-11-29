"use client";

import { useState } from "react";

type EtherlinkState = Record<string, unknown> | null;

export default function EtherlinkPage() {
  const [state, setState] = useState<EtherlinkState>(null);
  const [token, setToken] = useState("CHANGE_ME");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const loadNodes = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/etherlink/state?token=${encodeURIComponent(token)}`
      );
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      setState(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setState(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Etherlink</h1>
      <p>Distributed Node Overview</p>
      <div style={{ display: "flex", gap: "0.5rem", alignItems: "center", marginBottom: "1rem" }}>
        <label>
          Auth Token:
          <input
            value={token}
            onChange={(e) => setToken(e.target.value)}
            style={{ marginLeft: "0.5rem" }}
          />
        </label>
        <button onClick={loadNodes} disabled={loading}>
          {loading ? "Loading..." : "Load Local Node State"}
        </button>
      </div>
      {error && <p style={{ color: "tomato" }}>Error: {error}</p>}
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {state ? JSON.stringify(state, null, 2) : "No state loaded yet."}
      </pre>
    </div>
  );
}
