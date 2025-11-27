"use client";

import { useState } from "react";

export default function AutonomousPage() {
  const [projectId, setProjectId] = useState("0");
  const [state, setState] = useState<any>(null);
  const [resp, setResp] = useState<any>(null);

  const load = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setState({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/autonomous/state/${projectId}`);
    setState(await res.json());
  };

  const save = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setResp({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/autonomous/state/${projectId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state),
    });
    setResp(await res.json());
  };

  const control = async (action: "start" | "stop") => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setResp({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/autonomous/${action}`, {
      method: "POST",
    });
    setResp(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Autonomous Mode</h1>
      <div style={{ marginBottom: 12 }}>
        <input value={projectId} onChange={(event) => setProjectId(event.target.value)} style={{ width: 80 }} />
        <button onClick={load} style={{ marginLeft: 8 }}>
          Load State
        </button>
      </div>

      {state && (
        <div style={{ marginBottom: 12 }}>
          <label style={{ display: "block", marginBottom: 8 }}>
            <input
              type="checkbox"
              checked={Boolean(state.auto_enabled)}
              onChange={(event) => setState({ ...state, auto_enabled: event.target.checked })}
            />
            Auto Enabled
          </label>
          <label>
            Daily Quota:
            <input
              type="number"
              value={state.daily_quota}
              onChange={(event) => setState({ ...state, daily_quota: Number.parseInt(event.target.value, 10) || 0 })}
              style={{ marginLeft: 8, width: 80 }}
            />
          </label>
          <div style={{ marginTop: 8 }}>
            <button onClick={save}>Save State</button>
          </div>
        </div>
      )}

      <div style={{ marginTop: 16 }}>
        <button onClick={() => control("start")} style={{ marginRight: 8 }}>
          Start Auto Mode
        </button>
        <button onClick={() => control("stop")}>Stop Auto Mode</button>
      </div>

      <h3 style={{ marginTop: 16 }}>Current State</h3>
      <pre>{JSON.stringify(state, null, 2)}</pre>

      <h3>Response</h3>
      <pre>{JSON.stringify(resp, null, 2)}</pre>
    </div>
  );
}
