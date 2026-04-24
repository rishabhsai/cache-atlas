import { type CSSProperties, useMemo, useState } from "react";

export default function CacheBudgetDemo() {
  const [layers, setLayers] = useState(24);
  const [prefix, setPrefix] = useState(256);
  const [tokenCost, setTokenCost] = useState(2.4);

  const totalMb = useMemo(() => {
    return (layers * prefix * tokenCost) / 1024;
  }, [layers, prefix, tokenCost]);

  return (
    <div style={styles.card}>
      <div style={styles.label}>inline demo</div>
      <p style={styles.copy}>
        Tiny proxy for why cache-budget papers exist at all. Push layer count, kept prefix length, or per-token memory cost,
        and the memory bill climbs fast.
      </p>

      <div style={styles.grid}>
        <label style={styles.control}>
          <span>layers</span>
          <strong>{layers}</strong>
          <input type="range" min="8" max="48" step="4" value={layers} onChange={(e) => setLayers(Number(e.target.value))} />
        </label>
        <label style={styles.control}>
          <span>kept prefix</span>
          <strong>{prefix}</strong>
          <input type="range" min="64" max="1024" step="64" value={prefix} onChange={(e) => setPrefix(Number(e.target.value))} />
        </label>
        <label style={styles.control}>
          <span>mb / token / layer</span>
          <strong>{tokenCost.toFixed(1)}</strong>
          <input type="range" min="0.5" max="4" step="0.1" value={tokenCost} onChange={(e) => setTokenCost(Number(e.target.value))} />
        </label>
      </div>

      <div style={styles.result}>
        <span>estimated cache memory</span>
        <strong>{totalMb.toFixed(1)} MB</strong>
      </div>
    </div>
  );
}

const styles: Record<string, CSSProperties> = {
  card: {
    border: "1px solid rgba(231,237,244,0.14)",
    background: "rgba(11,14,18,0.92)",
    padding: "18px",
    margin: "24px 0",
  },
  label: {
    color: "#9aa6b2",
    fontSize: "12px",
    textTransform: "uppercase",
  },
  copy: {
    color: "#9aa6b2",
    lineHeight: 1.8,
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "12px",
    marginTop: "12px",
  },
  control: {
    display: "grid",
    gap: "8px",
    border: "1px solid rgba(231,237,244,0.14)",
    padding: "12px",
    background: "rgba(8,10,12,0.92)",
    color: "#e7edf4",
  },
  result: {
    display: "grid",
    gap: "6px",
    marginTop: "14px",
    padding: "12px",
    border: "1px solid rgba(231,237,244,0.14)",
    background: "rgba(8,10,12,0.92)",
    color: "#e7edf4",
  },
};
