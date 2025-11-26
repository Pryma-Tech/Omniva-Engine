export default function SubsystemsPage() {
  const subsystems = ["downloader", "scraper", "transcription", "analysis", "editing", "uploader"];
  return (
    <section>
      <h1>Subsystem Registry (Placeholder)</h1>
      <ul>
        {subsystems.map(name => (
          <li key={name}>{name} subsystem status pending</li>
        ))}
      </ul>
    </section>
  );
}
