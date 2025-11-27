"use client";

import { useEffect, useState } from "react";

export default function TemplatesPage() {
  const [templates, setTemplates] = useState<any[]>([]);
  const [resp, setResp] = useState<any>(null);
  const [form, setForm] = useState({
    name: "default",
    font: "Arial",
    font_size: 48,
    text_color: "white",
    outline_color: "black",
    outline_width: 2,
    watermark_path: "",
  });

  const load = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/templates/`);
    setTemplates(await res.json());
  };

  const save = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/templates/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    setResp(await res.json());
    load();
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Template Management</h1>
      <section style={{ marginBottom: 20 }}>
        <h3>Create / Update Template</h3>
        {Object.keys(form).map((key) => (
          <div key={key} style={{ marginBottom: 8 }}>
            <label style={{ width: 150, display: "inline-block" }}>{key}</label>
            <input
              value={(form as any)[key]}
              onChange={(event) => setForm({ ...form, [key]: event.target.value })}
            />
          </div>
        ))}
        <button onClick={save}>Save Template</button>
      </section>

      <section>
        <h3>Existing Templates</h3>
        <pre>{JSON.stringify(templates, null, 2)}</pre>
      </section>

      <section>
        <h3>Response</h3>
        <pre>{JSON.stringify(resp, null, 2)}</pre>
      </section>
    </div>
  );
}
