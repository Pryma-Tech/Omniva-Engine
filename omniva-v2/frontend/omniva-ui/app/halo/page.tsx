"use client";

import { useState } from "react";

type TokenMap = Record<string, string>;

export default function HaloPage() {
  const [authToken, setAuthToken] = useState("");
  const [tokens, setTokens] = useState<TokenMap | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [scope, setScope] = useState("nexus");

  const loadTokens = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/halo/tokens`, {
        headers: { "X-Omniva-Token": authToken || "" }
      });
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      const data = await response.json();
      setTokens(data.tokens);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setTokens(null);
    } finally {
      setLoading(false);
    }
  };

  const rotateToken = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/halo/rotate/${scope}`, {
        method: "POST",
        headers: { "X-Omniva-Token": authToken || "" }
      });
      if (!response.ok) {
        throw new Error(`Rotate failed: ${response.status}`);
      }
      await loadTokens();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Halo — Security Panel</h1>
      <p>View and rotate subsystem tokens (requires Sanctum-level authorization).</p>
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem", alignItems: "center" }}>
        <label>
          Admin Token:
          <input
            value={authToken}
            onChange={(e) => setAuthToken(e.target.value)}
            style={{ marginLeft: "0.5rem" }}
            placeholder="Sanctum token"
          />
        </label>
        <button onClick={loadTokens} disabled={loading}>
          {loading ? "Loading..." : "Load Tokens"}
        </button>
      </div>
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem", alignItems: "center" }}>
        <label>
          Scope:
          <select value={scope} onChange={(e) => setScope(e.target.value)} style={{ marginLeft: "0.5rem" }}>
            <option value="nexus">nexus</option>
            <option value="sanctum">sanctum</option>
            <option value="plugin">plugin</option>
            <option value="etherlink">etherlink</option>
          </select>
        </label>
        <button onClick={rotateToken} disabled={loading}>
          Rotate Token
        </button>
      </div>
      {error && <p style={{ color: "tomato" }}>{error}</p>}
      <h3>Core Tokens</h3>
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {tokens ? JSON.stringify(tokens, null, 2) : "No tokens loaded."}
      </pre>
    </div>
  );
}
