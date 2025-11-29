"use client";

import { useState } from "react";

const goals = [
  { value: "improve_growth", label: "Improve Growth" },
  { value: "recover_drift", label: "Recover Drift" },
  { value: "chase_trend", label: "Chase Trend" },
  { value: "increase_consistency", label: "Increase Consistency" },
];

export default function PlannerPage() {
  const [projectId, setProjectId] = useState("0");
  const [goal, setGoal] = useState(goals[0].value);
  const [planResult, setPlanResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const runPlanner = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/intelligence/planner/${projectId}/${goal}`
      );
      if (!response.ok) {
        throw new Error(`Planner failed with status ${response.status}`);
      }
      setPlanResult(await response.json());
    } catch (err) {
      setPlanResult(null);
      setError(err instanceof Error ? err.message : "Unknown planner error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Agent Hierarchical Planning</h1>
      <p style={{ maxWidth: 720 }}>
        Generate medium-term strategies (HTN) that complement behavior trees. Plans blend personality, long-term memory,
        and optimizer signals to decide the next set of actions.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          style={{ width: "80px", marginLeft: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        Goal:{" "}
        <select value={goal} onChange={(e) => setGoal(e.target.value)}>
          {goals.map((g) => (
            <option value={g.value} key={g.value}>
              {g.label}
            </option>
          ))}
        </select>
      </div>

      <button onClick={runPlanner} disabled={loading}>
        {loading ? "Planning..." : "Generate Plan"}
      </button>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Plan</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", overflowX: "auto" }}>
        {planResult ? JSON.stringify(planResult, null, 2) : "No plan generated yet."}
      </pre>
    </div>
  );
}
