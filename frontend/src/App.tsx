import { useState } from "react";

function App() {
  const [health, setHealth] = useState<string | null>(null);

  const checkBackend = async () => {
    try {
      const res = await fetch("/api/v1/health");
      const data = await res.json();
      setHealth(data.status);
    } catch {
      setHealth("backend unreachable");
    }
  };

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem", maxWidth: "480px", margin: "0 auto" }}>
      <h1>🐉 D&D Campaign Manager</h1>
      <p>Welcome! The frontend is up and running.</p>

      <section>
        <h2>Backend Connection</h2>
        <button onClick={checkBackend}>Check Backend Health</button>
        {health !== null && (
          <p>
            Status: <strong>{health}</strong>
          </p>
        )}
      </section>
    </div>
  );
}

export default App;
