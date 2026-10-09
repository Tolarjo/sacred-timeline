* {
  box-sizing: border-box;
}

:root {
  --bg: #0f172a;
  --bg-soft: #111827;
  --panel: #1f2937;
  --panel-alt: #111827;
  --accent: #7c3aed;
  --accent-soft: #a78bfa;
  --text: #e5e7eb;
  --muted: #9ca3af;
  --border: rgba(255,255,255,0.08);
  --good: #34d399;
}

body {
  margin: 0;
  background: linear-gradient(180deg, var(--bg) 0%, #111827 100%);
  color: var(--text);
  font-family: Arial, sans-serif;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid var(--border);
  background: rgba(17, 24, 39, 0.7);
  position: sticky;
  top: 0;
  backdrop-filter: blur(10px);
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 11px;
  color: var(--muted);
  margin: 0 0 8px;
}

h1, h2, p {
  margin-top: 0;
}

button {
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 16px;
  font-weight: 700;
  cursor: pointer;
}

.layout {
  padding: 24px 32px 48px;
}

.stats-panel {
  display: grid;
  grid-template-columns: repeat(4, minmax(160px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card,
.panel {
  background: rgba(31, 41, 55, 0.9);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-card span {
  color: var(--muted);
  font-size: 14px;
}

.stat-card strong {
  font-size: 30px;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.timeline {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  min-height: 220px;
  padding-top: 16px;
}

.timeline-item {
  flex: 1;
  min-width: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.timeline-bar {
  width: 100%;
  background: linear-gradient(180deg, var(--accent-soft), var(--accent));
  border-radius: 8px 8px 0 0;
  min-height: 20px;
  position: relative;
}

.timeline-item small {
  color: var(--muted);
}

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.breakdown-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.breakdown-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  background: var(--good);
  display: inline-block;
}

.library {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.section-header input {
  flex: 1;
  max-width: 380px;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: rgba(17, 24, 39, 0.8);
  color: var(--text);
}

.document-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}

.document-card {
  background: rgba(17, 24, 39, 0.7);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px;
}

.document-card h3 {
  margin-bottom: 8px;
}

.meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.badge {
  display: inline-block;
  color: var(--text);
  background: rgba(124, 58, 237, 0.2);
  border: 1px solid rgba(124, 58, 237, 0.5);
  border-radius: 999px;
  padding: 4px 8px;
  font-size: 12px;
}

.document-card p {
  color: var(--muted);
  line-height: 1.5;
}

.form-panel {
  margin-top: 12px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

input, textarea {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: rgba(17, 24, 39, 0.8);
  color: var(--text);
}

textarea {
  resize: vertical;
  min-height: 90px;
}

@media (max-width: 768px) {
  .stats-panel,
  .content-grid {
    grid-template-columns: 1fr;
  }

  .topbar,
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
