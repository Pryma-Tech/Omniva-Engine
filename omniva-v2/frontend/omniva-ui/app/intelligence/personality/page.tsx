"use client";

import { useEffect, useState } from "react";

interface PersonalityProfile {
  description: string;
  prio_mod: Record<string, number>;
  post_aggression: number;
  niche_strictness: number;
  drift_tolerance: number;
  editorial_style?: string;
  adaptive?: boolean;
}

export default function PersonalityPage() {
  const [projectId, setProjectId] = useState("0");
  const [profiles, setProfiles] = useState<Record<string, PersonalityProfile>>({});
  const [selected, setSelected] = useState("balanced");
  const [current, setCurrent] = useState<Record<string, any> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const backend = process.env.NEXT_PUBLIC_BACKEND_URL;

  const loadProfiles = async () => {
    try {
      const response = await fetch(`${backend}/intelligence/personality/profiles`);
      setProfiles(await response.json());
    } catch (err) {
      console.error(err);
      setError("Failed to load profiles");
    }
  };

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadCurrent = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(`${backend}/intelligence/personality/${projectId}`);
      if (!response.ok) {
        throw new Error(`Load failed with status ${response.status}`);
      }
      const json = await response.json();
      setCurrent(json);
      setSelected(json.key || "balanced");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown load error");
      setCurrent(null);
    } finally {
      setLoading(false);
    }
  };

  const update = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch(
        `${backend}/intelligence/personality/${projectId}/${selected}`,
        { method: "POST" }
      );
      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.detail || `Update failed with status ${response.status}`);
      }
      await loadCurrent();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown update error");
    } finally {
      setLoading(false);
    }
  };

  const profileEntries = Object.entries(profiles);
  const fallbackKeys = ["balanced", "viral_hunter", "evergreen", "brand_guardian", "growth_spiral"];

  return (
    <div style={{ padding: 20 }}>
      <h1>Agent Personality & Strategy Profiles</h1>
      <p style={{ maxWidth: 720 }}>
        Personalities tune prioritizer weights, posting aggression, and drift tolerance. Select a profile per project
        to steer the intelligence engine toward viral hunting, evergreen stability, or adaptive experimentation.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        Project ID:{" "}
        <input
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          style={{ width: "80px", marginLeft: "0.5rem" }}
        />
      </div>

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem", flexWrap: "wrap" }}>
        <button onClick={loadCurrent} disabled={loading}>
          {loading ? "Loading..." : "Load Personality"}
        </button>
        <button onClick={update} disabled={loading}>
          Apply Personality
        </button>
      </div>

      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}

      <h3>Select Personality</h3>
      <select value={selected} onChange={(e) => setSelected(e.target.value)}>
        {profileEntries.length > 0
          ? profileEntries.map(([key, profile]) => (
              <option value={key} key={key}>
                {key} — {profile.description}
              </option>
            ))
          : fallbackKeys.map((key) => (
              <option value={key} key={key}>
                {key}
              </option>
            ))}
      </select>

      <h3>Current Personality</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px" }}>
        {current ? JSON.stringify(current, null, 2) : "Not loaded yet."}
      </pre>

      <h3>Profiles</h3>
      {profileEntries.length > 0 ? (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "1rem" }}>
          {profileEntries.map(([key, profile]) => (
            <div key={key} style={{ border: "1px solid #ddd", padding: "1rem", borderRadius: "6px" }}>
              <h4 style={{ margin: "0 0 0.5rem 0" }}>{key}</h4>
              <p style={{ marginTop: 0 }}>{profile.description}</p>
              <small>
                Aggression: {profile.post_aggression.toFixed(2)} | Niche strictness: {profile.niche_strictness}
                <br /> Drift tolerance: {profile.drift_tolerance.toFixed(2)}
                <br /> Editorial style: {profile.editorial_style || "neutral"}
              </small>
            </div>
          ))}
        </div>
      ) : (
        <p style={{ color: "#666" }}>Profile metadata will appear once the backend responds.</p>
      )}
    </div>
  );
}
