:root {
  --bg: #0b1020;
  --panel: rgba(19, 27, 43, 0.9);
  --panel-alt: rgba(10, 17, 31, 0.8);
  --card: rgba(17, 24, 39, 0.9);
  --text: #edf3ff;
  --muted: #a7b4c9;
  --accent: #8b5cf6;
  --accent-2: #3b82f6;
  --accent-3: #34d399;
  --border: rgba(148, 163, 184, 0.18);
  --shadow: rgba(0, 0, 0, 0.24);
}

* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  background: linear-gradient(180deg, var(--bg) 0%, #111827 100%);
  color: var(--text);
  font-family: Inter, Arial, sans-serif;
}

button, input, textarea, select {
  font: inherit;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 32px 20px;
  border-bottom: 1px solid var(--border);
  background: rgba(15, 23, 42, 0.7);
  position: sticky;
  top: 0;
  backdrop-filter: blur(10px);
}

.eyebrow {
  margin: 0 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 11px;
  color: var(--muted);
}

h1, h2, h3, p {
  margin-top: 0;
}

button {
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: white;
  padding: 10px 16px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(139, 92, 246, 0.3);
}

.layout {
  padding: 24px 32px 60px;
}

.stats-panel {
  display: grid;
  grid-template-columns: repeat(4, minmax(180px, 1fr));
  gap: 18px;
  margin-bottom: 22px;
}

.stat-card,
.panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  box-shadow: 0 18px 32px var(--shadow);
}

.stat-card {
  padding: 20px 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-card span {
  color: var(--muted);
  font-size: 14px;
}

.stat-card strong {
  font-size: 28px;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.details-grid {
  grid-template-columns: 1.3fr 1fr;
}

.panel {
  padding: 20px;
}

.panel-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.timeline {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  min-height: 220px;
  padding-top: 16px;
}

.timeline-item {
  flex: 1;
  min-width: 70px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.timeline-bar {
  width: 100%;
  border-radius: 10px 10px 0 0;
  min-height: 20px;
  background: linear-gradient(180deg, #8b5cf6 0%, #3b82f6 100%);
}

.timeline-item small {
  color: var(--muted);
  font-size: 10px;
  text-align: center;
}

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.breakdown-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid var(--border);
  border-radius: 12px;
}

.breakdown-label {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  display: inline-block;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
  gap: 12px;
}

.library-filters {
  display: flex;
  align-items: center;
  gap: 12px;
  width: min(100%, 520px);
}

.library-filters select,
.library-filters input {
  flex: 1;
}

.document-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}

.document-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px;
  transition: transform 0.15s ease, border-color 0.15s ease;
}

.document-card.selected {
  border-color: rgba(59, 130, 246, 0.8);
  transform: translateY(-1px);
}

.document-card button {
  margin-top: 12px;
  font-size: 12px;
  padding: 8px 12px;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 999px;
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.4);
  font-size: 11px;
}

.document-card h3 {
  font-size: 18px;
  margin-bottom: 8px;
}

.document-card p {
  color: var(--muted);
  line-height: 1.5;
}

.selected-document,
.comparison-panel,
.empty-state {
  color: var(--muted);
  line-height: 1.6;
}

.detail-card,
.compare-box {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  margin-top: 14px;
}

.compare-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.compare-box h4 {
  margin: 0 0 10px;
}

.document-text {
  margin-top: 18px;
  max-height: 240px;
  overflow: auto;
  padding: 12px;
  background: rgba(2, 6, 23, 0.55);
  border: 1px solid var(--border);
  border-radius: 12px;
  white-space: pre-wrap;
  line-height: 1.6;
  color: var(--text);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

input, textarea, select {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: rgba(15, 23, 42, 0.7);
  color: var(--text);
}

textarea {
  resize: vertical;
  min-height: 90px;
}

.ingest-form {
  margin-top: 8px;
}

@media (max-width: 768px) {
  .topbar,
  .section-header,
  .library-filters {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-panel,
  .content-grid,
  .compare-grid,
  .details-grid {
    grid-template-columns: 1fr;
  }
}
