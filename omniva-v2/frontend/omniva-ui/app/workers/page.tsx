"use client";

import { useState } from "react";

export default function WorkersPage() {
  const [response, setResponse] = useState<any>(null);

  const send = async (path: string) => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/workers/${path}`, {
      method: "POST",
    });
    setResponse(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Worker Engine Control</h1>
      <button onClick={() => send("start")} style={{ marginRight: 12 }}>
        Start Workers
      </button>
      <button onClick={() => send("stop")}>Stop Workers</button>
      <pre style={{ marginTop: 16 }}>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
