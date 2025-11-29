const links = [
  { href: "/", label: "Home" },
  { href: "/projects", label: "Projects" },
  { href: "/pipeline", label: "Pipeline" },
  { href: "/analysis", label: "Analysis" },
  { href: "/editing", label: "Editing" },
  { href: "/download", label: "Download" },
  { href: "/transcription", label: "Transcription" },
  { href: "/discovery", label: "Discovery" },
  { href: "/templates", label: "Templates" },
  { href: "/scheduler", label: "Scheduler" },
  { href: "/uploader", label: "Uploader" },
  { href: "/autonomous", label: "Autonomous" },
  { href: "/intelligence", label: "Intelligence" },
  { href: "/intelligence/trending", label: "Trending" },
  { href: "/intelligence/semantic", label: "Semantic" },
  { href: "/intelligence/audio", label: "Audio" },
  { href: "/intelligence/prioritizer", label: "Prioritizer" },
  { href: "/intelligence/ghost", label: "Ghost Run" },
  { href: "/intelligence/optimizer", label: "Optimizer" },
  { href: "/intelligence/ltm", label: "LTM (Memory)" },
  { href: "/intelligence/behavior", label: "Behavior Trees" },
  { href: "/intelligence/planner", label: "Planner" },
  { href: "/intelligence/cognition", label: "Cognition" },
  { href: "/intelligence/emotion", label: "Emotion" },
  { href: "/intelligence/deliberate", label: "Deliberation" },
  { href: "/intelligence/persona", label: "Persona" },
  { href: "/intelligence/personality", label: "Personality" },
  { href: "/health", label: "Health" },
  { href: "/events", label: "Events" },
  { href: "/worker", label: "Worker" },
  { href: "/workers", label: "Workers" }
];

export default function Nav() {
  return (
    <nav style={{ background: "#111", padding: "0.5rem 1rem" }}>
      <ul style={{ listStyle: "none", display: "flex", gap: "1rem", margin: 0, padding: 0 }}>
        {links.map((link) => (
          <li key={link.href}>
            <a href={link.href} style={{ color: "#f5f5f5", textDecoration: "none" }}>
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
