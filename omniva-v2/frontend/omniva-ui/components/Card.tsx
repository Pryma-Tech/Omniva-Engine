import type { ReactNode } from "react";

interface CardProps {
  title: string;
  children: ReactNode;
}

export default function Card({ title, children }: CardProps) {
  return (
    <div style={{ background: "#1f1f1f", padding: "1rem", borderRadius: 8 }}>
      <h3>{title}</h3>
      {children}
    </div>
  );
}
