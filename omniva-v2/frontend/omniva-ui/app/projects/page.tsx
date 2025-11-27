"use client";

import { useEffect, useState } from "react";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [projectId, setProjectId] = useState("0");

  const load = async () => {
    if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
      setProjects([]);
      return;
    }
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/projects`);
      setProjects(await res.json());
    } catch {
      setProjects([]);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Projects</h1>
      <div style={{ marginBottom: 12 }}>
        <label>
          Open Project ID:{" "}
          <input
            value={projectId}
            onChange={(event) => setProjectId(event.target.value)}
            style={{ width: 80, marginRight: 8 }}
          />
        </label>
        <a href={`/projects/${projectId}`} style={{ marginRight: 8 }}>
          Manage Project
        </a>
        <button onClick={load}>Reload List</button>
      </div>
      <pre>{JSON.stringify(projects ?? [], null, 2)}</pre>
    </div>
  );
}
