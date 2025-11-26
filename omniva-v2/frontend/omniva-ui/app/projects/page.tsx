"use client";

import { useEffect, useState } from "react";

const apiBase = process.env.NEXT_PUBLIC_BACKEND_URL;

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[]>([]);

  useEffect(() => {
    if (!apiBase) {
      setProjects([]);
      return;
    }
    fetch(`${apiBase}/projects`)
      .then((response) => response.json())
      .then(setProjects)
      .catch(() => setProjects([]));
  }, [apiBase]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Projects (Placeholder)</h1>
      <pre>{JSON.stringify(projects ?? [], null, 2)}</pre>
    </div>
  );
}
