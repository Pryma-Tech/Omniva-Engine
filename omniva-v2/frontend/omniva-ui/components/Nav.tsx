const links = [
  { href: "/", label: "Home" },
  { href: "/projects", label: "Projects" },
  { href: "/pipeline", label: "Pipeline" },
  { href: "/analysis", label: "Analysis" },
  { href: "/editing", label: "Editing" },
  { href: "/download", label: "Download" },
  { href: "/transcription", label: "Transcription" },
  { href: "/templates", label: "Templates" },
  { href: "/scheduler", label: "Scheduler" },
  { href: "/uploader", label: "Uploader" },
  { href: "/autonomous", label: "Autonomous" },
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
