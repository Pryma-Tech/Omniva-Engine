"use client";

import Card from "../components/Card";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export default function HomePage() {
  const summary = [
    { title: "Backend", detail: backendUrl },
    { title: "Pipeline", detail: "Placeholder pipeline summary" },
    { title: "Subsystems", detail: "Modules registered via plugin system" }
  ];

  return (
    <section>
      <h1>Omniva Engine v2 Dashboard</h1>
      <p>This is a placeholder UI for monitoring the Omniva Engine subsystems.</p>
      <div style={{ display: "grid", gap: "1rem", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))" }}>
        {summary.map(item => (
          <Card key={item.title} title={item.title}>
            <p>{item.detail}</p>
          </Card>
        ))}
      </div>
    </section>
  );
}
