"use client";

import { useState } from "react";

type SanctumResponse = Record<string, unknown> | null;

export default function SanctumPage() {
  const [command, setCommand] = useState("");
  const [output, setOutput] = useState<SanctumResponse>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runCommand = async () => {
    if (!command.trim()) {
      setError("Enter a command before executing.");
      return;
    }
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/sanctum/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command }),
      });
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      const json = await response.json();
      setOutput(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setOutput(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Sanctum</h1>
      <p>Root Operator Console — execute approved commands only.</p>
      <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
        <input
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          style={{ width: 400 }}
          placeholder="identity.show"
        />
        <button onClick={runCommand} disabled={loading}>
          {loading ? "Running..." : "Execute"}
        </button>
      </div>
      {error && <p style={{ color: "tomato" }}>Error: {error}</p>}
      <h3>Output</h3>
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem", borderRadius: 8 }}>
        {output ? JSON.stringify(output, null, 2) : "No output yet."}
      </pre>
    </div>
  );
}
