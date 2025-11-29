"use client";

import { useState } from "react";

type PluginList = Record<string, { version: string; enabled: boolean; path?: string }> | null;
type DiscoverResult = string[] | null;

export default function ForgePage() {
  const [plugins, setPlugins] = useState<PluginList>(null);
  const [discoveries, setDiscoveries] = useState<DiscoverResult>(null);
  const [loadPath, setLoadPath] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = async () => {
    try {
      setBusy(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/forge/list`);
      setPlugins(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setPlugins(null);
    } finally {
      setBusy(false);
    }
  };

  const runDiscover = async () => {
    try {
      setBusy(true);
      setError(null);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/forge/discover`, {
        method: "POST"
      });
      setDiscoveries(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setDiscoveries(null);
    } finally {
      setBusy(false);
    }
  };

  const loadPlugin = async () => {
    if (!loadPath.trim()) {
      setError("Provide a plugin path to load.");
      return;
    }
    try {
      setBusy(true);
      setError(null);
      await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/forge/load`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path: loadPath })
      });
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setBusy(false);
    }
  };

  const enable = async (name: string) => {
    await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/forge/enable/${name}`, {
      method: "POST"
    });
    refresh();
  };

  const disable = async (name: string) => {
    await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/forge/disable/${name}`, {
      method: "POST"
    });
    refresh();
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Forge — Plugin Manager</h1>
      <p>Discover, load, and manage runtime plugins safely.</p>

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <button onClick={refresh} disabled={busy}>Load Plugins</button>
        <button onClick={runDiscover} disabled={busy}>Discover</button>
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <input
          value={loadPath}
          onChange={(e) => setLoadPath(e.target.value)}
          placeholder="plugins/example_plugin"
          style={{ width: 320, marginRight: "0.5rem" }}
        />
        <button onClick={loadPlugin} disabled={busy}>Load Plugin</button>
      </div>

      {error && <p style={{ color: "tomato" }}>Error: {error}</p>}

      <h3>Discovered Paths</h3>
      <pre style={{ background: "#111", color: "#f5f5f5", padding: "1rem" }}>
        {discoveries ? JSON.stringify(discoveries, null, 2) : "No discovery run yet."}
      </pre>

      <h3>Installed Plugins</h3>
      {plugins ? (
        <ul>
          {Object.entries(plugins).map(([name, meta]) => (
            <li key={name} style={{ marginBottom: "0.5rem" }}>
              <strong>{name}</strong> — v{meta.version} — {meta.enabled ? "enabled" : "disabled"}
              {meta.path ? ` (${meta.path})` : ""}
              <span style={{ marginLeft: "0.5rem" }}>
                <button onClick={() => enable(name)} style={{ marginRight: "0.25rem" }}>
                  Enable
                </button>
                <button onClick={() => disable(name)}>Disable</button>
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <p>No plugins loaded.</p>
      )}
    </div>
  );
}
