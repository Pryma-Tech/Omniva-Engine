"use client";

import { useEffect, useState } from "react";

export default function IntelligencePage() {
  const [status, setStatus] = useState<any>(null);
  const [mode, setMode] = useState("balanced");
  const [modeResp, setModeResp] = useState<any>(null);
  const [projectId, setProjectId] = useState("0");
  const [posting, setPosting] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [applyResp, setApplyResp] = useState<any>(null);

  const loadStatus = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setStatus({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/status`);
    setStatus(await res.json());
  };

  const changeMode = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setModeResp({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/mode/${mode}`, {
      method: "POST",
    });
    setModeResp(await res.json());
    loadStatus();
  };

  const loadPosting = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setPosting({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/posting-time/${projectId}`);
    setPosting(await res.json());
  };

  const loadStats = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setStats({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/posting-stats/${projectId}`);
    setStats(await res.json());
  };

  const applySchedule = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setApplyResp({ error: "Backend URL not configured" });
      return;
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/apply-schedule/${projectId}`, {
      method: "POST",
    });
    setApplyResp(await res.json());
  };

  useEffect(() => {
    loadStatus();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Intelligence Engine</h1>

      <h3>Status</h3>
      <pre>{JSON.stringify(status, null, 2)}</pre>

      <h3>Set Mode</h3>
      <select value={mode} onChange={(event) => setMode(event.target.value)}>
        <option value="balanced">Balanced</option>
        <option value="viral">Viral First</option>
        <option value="evergreen">Evergreen</option>
      </select>
      <button onClick={changeMode} style={{ marginLeft: 8 }}>
        Apply Mode
      </button>
      <pre>{JSON.stringify(modeResp, null, 2)}</pre>

      <hr />

      <h3>Smart Posting Time</h3>
      <label>
        Project ID:
        <input value={projectId} onChange={(event) => setProjectId(event.target.value)} style={{ width: 80, marginLeft: 8 }} />
      </label>
      <div style={{ marginTop: 8 }}>
        <button onClick={loadPosting}>Get Recommendation</button>
        <button onClick={loadStats} style={{ marginLeft: 8 }}>
          Load Stats
        </button>
        <button onClick={applySchedule} style={{ marginLeft: 8 }}>
          Apply Schedule
        </button>
      </div>

      <h4>Recommended Posting Time</h4>
      <pre>{JSON.stringify(posting, null, 2)}</pre>

      <h4>Posting Stats</h4>
      <pre>{JSON.stringify(stats, null, 2)}</pre>

      <h4>Apply Schedule Response</h4>
      <pre>{JSON.stringify(applyResp, null, 2)}</pre>
    </div>
  );
}
