import "./globals.css";
import type { ReactNode } from "react";
import Nav from "../components/Nav";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Nav />
        <main style={{ padding: "1rem" }}>{children}</main>
      </body>
    </html>
  );
}
