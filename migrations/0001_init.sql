-- Leads submitted from the calculator form
CREATE TABLE leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  name TEXT NOT NULL,
  business TEXT NOT NULL,
  phone TEXT NOT NULL,
  email TEXT,
  consent_text TEXT NOT NULL,
  list_size INTEGER,
  avg_ticket INTEGER,
  extra_visits REAL,
  monthly_estimate INTEGER,
  source TEXT,
  variant TEXT,
  page TEXT,
  visitor_id TEXT,
  country TEXT,
  ip_hash TEXT,
  status TEXT NOT NULL DEFAULT 'new'
);
CREATE INDEX leads_created ON leads(created_at);
CREATE INDEX leads_ip ON leads(ip_hash, created_at);

-- Lightweight first-party events: page views of tested pages, calculator use, CTA clicks, short-link scans
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL DEFAULT (datetime('now')),
  type TEXT NOT NULL,
  experiment TEXT,
  variant TEXT,
  source TEXT,
  path TEXT,
  visitor_id TEXT,
  country TEXT,
  is_bot INTEGER NOT NULL DEFAULT 0,
  detail TEXT
);
CREATE INDEX events_type_ts ON events(type, ts);
CREATE INDEX events_exp ON events(experiment, variant, type);
