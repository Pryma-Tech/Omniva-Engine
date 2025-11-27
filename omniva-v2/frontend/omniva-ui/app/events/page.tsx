"use client";

import { useEffect, useState } from "react";

export default function EventsPage() {
  const [events, setEvents] = useState<any[]>([]);

  const load = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/events/log`);
    setEvents(await res.json());
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Event Log</h1>
      <pre>{JSON.stringify(events, null, 2)}</pre>
    </div>
  );
}
