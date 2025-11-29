"use client";

import { useState } from "react";

export default function LTMPage() {
  const [projectId, setProjectId] = useState("0");
  const [report, setReport] = useState<unknown>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/ltm/report/${projectId}`
      );
      if (!response.ok) {
        throw new Error(`Report failed with status ${response.status}`);
      }
      setReport(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown report error");
    } finally {
      setLoading(false);
    }
  };

  const run = async (cmd: string) => {
    setError(null);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/ltm/${cmd}/${projectId}`,
        { method: "POST" }
      );
      if (!response.ok) {
        throw new Error(`${cmd} failed with status ${response.status}`);
      }
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown action error");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Long-Term Memory Engine</h1>
      <p style={{ maxWidth: 640 }}>
        Archive snapshots, detect drift across keywords/weights/audio, and consolidate optimizer history into a
        single memory health report for each project.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          style={{ width: "80px", marginLeft: "0.5rem" }}
        />
      </div>

      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "1rem" }}>
        <button onClick={load} disabled={loading}>
          {loading ? "Loading..." : "Load Memory Report"}
        </button>
        <button onClick={() => run("snapshot")}>Take Snapshot</button>
        <button onClick={() => run("drift")}>Check Drift</button>
        <button onClick={() => run("consolidate")}>Consolidate Memory</button>
      </div>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Report</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px" }}>
        {report ? JSON.stringify(report, null, 2) : "No report loaded."}
      </pre>
    </div>
  );
}
