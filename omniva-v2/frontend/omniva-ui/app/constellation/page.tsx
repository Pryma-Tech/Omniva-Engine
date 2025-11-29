"use client";

import { useState } from "react";

export default function ConstellationPage() {
  const [projectId, setProjectId] = useState("0");
  const [consensus, setConsensus] = useState<any>(null);
  const [similarity, setSimilarity] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const loadConsensus = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/constellation/consensus/${projectId}`
      );
      if (!response.ok) {
        throw new Error(`Consensus fetch failed (${response.status})`);
      }
      setConsensus(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const loadSimilarity = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/constellation/similarity`
      );
      if (!response.ok) {
        throw new Error(`Similarity fetch failed (${response.status})`);
      }
      setSimilarity(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Omniva Constellation</h1>
      <p style={{ maxWidth: 720 }}>
        Coordinate editor, trend, and risk agents per project, or view cross-project niche similarity recommendations.
      </p>
      <div style={{ marginBottom: "1rem" }}>
        <input value={projectId} onChange={(e) => setProjectId(e.target.value)} style={{ width: "80px" }} />
        <button onClick={loadConsensus} disabled={loading} style={{ marginLeft: "0.5rem" }}>
          Load Consensus
        </button>
      </div>
      <button onClick={loadSimilarity} disabled={loading}>
        Load Niche Similarity
      </button>
      {error && (
        <p style={{ color: "tomato" }}>
          Error: {error}
        </p>
      )}
      <h3>Consensus</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "140px" }}>
        {consensus ? JSON.stringify(consensus, null, 2) : "No consensus data."}
      </pre>
      <h3>Niche Similarity</h3>
      <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "4px", minHeight: "140px" }}>
        {similarity ? JSON.stringify(similarity, null, 2) : "No similarity data."}
      </pre>
    </div>
  );
}
