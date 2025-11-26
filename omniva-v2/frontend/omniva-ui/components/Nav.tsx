import Link from "next/link";

const links = [
  { href: "/", label: "Dashboard" },
  { href: "/pipeline", label: "Pipeline" },
  { href: "/analysis", label: "Analysis" },
  { href: "/editing", label: "Editing" },
  { href: "/uploader", label: "Uploader" },
  { href: "/subsystems", label: "Subsystems" }
];

export default function Nav() {
  return (
    <nav style={{ background: "#111", padding: "0.5rem 1rem", display: "flex", gap: "1rem" }}>
      {links.map(link => (
        <Link key={link.href} href={link.href} style={{ color: "#f5f5f5" }}>
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
