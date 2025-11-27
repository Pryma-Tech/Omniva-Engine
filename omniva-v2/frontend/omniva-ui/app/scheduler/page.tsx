"use client";

import { useEffect, useState } from "react";

export default function SchedulerPage() {
  const [projectId, setProjectId] = useState("0");
  const [cron, setCron] = useState("");
  const [enabled, setEnabled] = useState(false);
  const [response, setResponse] = useState<any>(null);

  const load = async () => {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/scheduler/project/${projectId}`
    );
    const data = await res.json();
    setCron(data.cron);
    setEnabled(Boolean(data.enabled));
  };

  const save = async () => {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/scheduler/project/${projectId}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cron,
          enabled,
        }),
      }
    );
    setResponse(await res.json());
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Scheduler</h1>
      <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 12 }}>
        <label>
          Project ID:
          <input
            value={projectId}
            onChange={(event) => setProjectId(event.target.value)}
            style={{ width: 80, marginLeft: 8 }}
          />
        </label>
        <label>
          Cron:
          <input
            value={cron}
            onChange={(event) => setCron(event.target.value)}
            placeholder="0 */6 * * *"
            style={{ width: 180, marginLeft: 8 }}
          />
        </label>
        <label style={{ display: "flex", alignItems: "center", gap: 4 }}>
          <input
            type="checkbox"
            checked={enabled}
            onChange={(event) => setEnabled(event.target.checked)}
          />
          Enabled
        </label>
        <button onClick={save}>Save</button>
      </div>
      <button onClick={load}>Load</button>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
