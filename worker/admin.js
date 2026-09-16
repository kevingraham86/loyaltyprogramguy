// Password-protected dashboard. Set the password once with:  npx wrangler secret put ADMIN_PASSWORD
import { EXPERIMENTS } from "./experiments.js";

export async function renderAdmin(request, env) {
  if (!env.ADMIN_PASSWORD) return new Response("Admin is not configured.", { status: 503 });
  if (!(await authorized(request, env.ADMIN_PASSWORD))) {
    return new Response("Authentication required.", {
      status: 401,
      headers: { "WWW-Authenticate": 'Basic realm="Loyalty Program Guy admin", charset="UTF-8"', "Cache-Control": "no-store" },
    });
  }
  const days = Math.min(Math.max(Number(new URL(request.url).searchParams.get("days")) || 30, 1), 365);
  const since = `-${days} days`;
  const q = (sql, ...b) => env.DB.prepare(sql).bind(...b).all().then((r) => r.results);

  const [leads, ab, sources, links, daily] = await Promise.all([
    q("SELECT * FROM leads WHERE status != 'test' AND created_at > datetime('now', ?) ORDER BY id DESC LIMIT 200", since),
    q(`SELECT variant,
         COUNT(DISTINCT CASE WHEN type='page_view' THEN visitor_id END) AS visitors,
         COUNT(DISTINCT CASE WHEN type='calculator_start' THEN visitor_id END) AS calc_users,
         COUNT(DISTINCT CASE WHEN type='cta_click' THEN visitor_id END) AS cta_clickers
       FROM events WHERE experiment='calc_cta' AND is_bot=0 AND variant IS NOT NULL AND ts > datetime('now', ?)
       GROUP BY variant ORDER BY variant`, since),
    q(`SELECT COALESCE(source,'(none)') AS source, COUNT(DISTINCT visitor_id) AS visitors
       FROM events WHERE type='page_view' AND is_bot=0 AND ts > datetime('now', ?) GROUP BY 1 ORDER BY 2 DESC LIMIT 20`, since),
    q(`SELECT source AS code, SUM(is_bot=0) AS scans, SUM(is_bot=1) AS bot_hits
       FROM events WHERE type='short_link' AND ts > datetime('now', ?) GROUP BY 1 ORDER BY 2 DESC`, since),
    q(`SELECT date(ts) AS day, COUNT(DISTINCT CASE WHEN is_bot=0 THEN visitor_id END) AS visitors,
         SUM(type='calculator_start' AND is_bot=0) AS calc_starts, SUM(is_bot=1) AS bot_hits
       FROM events WHERE ts > datetime('now', ?) GROUP BY 1 ORDER BY 1 DESC LIMIT 60`, since),
  ]);
  const leadsByVariant = {};
  for (const l of leads) if (l.variant) leadsByVariant[l.variant] = (leadsByVariant[l.variant] || 0) + 1;

  const e = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const table = (rows, cols) => rows.length
    ? `<table><tr>${cols.map(([, h]) => `<th>${h}</th>`).join("")}</tr>${rows.map((r) => `<tr>${cols.map(([k]) => `<td>${e(typeof k === "function" ? k(r) : r[k])}</td>`).join("")}</tr>`).join("")}</table>`
    : `<p class="muted">Nothing yet.</p>`;
  const pct = (a, b) => (b ? `${((100 * a) / b).toFixed(1)}%` : "–");
  const exp = EXPERIMENTS.calc_cta;

  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Leads & insights | Loyalty Program Guy</title>
<style>body{font:15px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;margin:0;background:#f3f4f6;color:#111827}
main{max-width:1100px;margin:0 auto;padding:20px}h1{margin:0 0 4px}h2{margin:28px 0 8px;font-size:19px}
.card{background:#fff;border-radius:12px;padding:14px 16px;box-shadow:0 1px 2px rgba(0,0,0,.06);overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:6px 8px;border-bottom:1px solid #e5e7eb;white-space:nowrap}
th{background:#f9fafb}.muted{color:#6b7280}a{color:#2563eb}</style></head><body><main>
<h1>Leads &amp; insights</h1><p class="muted">Last ${days} days · bots excluded where noted · <a href="?days=7">7d</a> · <a href="?days=30">30d</a> · <a href="?days=90">90d</a></p>
<h2>Leads (${leads.length})</h2><div class="card">${table(leads, [
    ["created_at", "When (UTC)"], ["name", "Name"], ["business", "Business"], ["phone", "Phone"], ["email", "Email"],
    [(r) => r.monthly_estimate ? `$${Number(r.monthly_estimate).toLocaleString()}/mo` : "", "Their estimate"],
    [(r) => [r.list_size, r.avg_ticket && `$${r.avg_ticket}`, r.extra_visits].filter(Boolean).join(" × "), "Inputs"],
    ["source", "Source"], ["variant", "CTA variant"], ["status", "Status"]])}</div>
<h2>A/B test: ${e(exp.description)}</h2><div class="card">${table(ab.map((r) => ({ ...r,
    text: exp.variants[r.variant]?.text, leads: leadsByVariant[r.variant] || 0 })), [
    ["variant", "Variant"], ["text", "Button text"], ["visitors", "Visitors"], ["calc_users", "Used calculator"],
    ["cta_clickers", "Clicked button"], [(r) => pct(r.cta_clickers, r.visitors), "Click rate"],
    ["leads", "Form leads"], [(r) => pct(r.leads, r.visitors), "Lead rate"]])}
<p class="muted">Rule of thumb: wait for at least ~100 visitors per variant before calling a winner.</p></div>
<h2>Traffic sources (human visitors)</h2><div class="card">${table(sources, [["source", "Source (?src=)"], ["visitors", "Visitors"]])}</div>
<h2>Short links (/go/…)</h2><div class="card">${table(links, [["code", "Code"], ["scans", "Scans"], ["bot_hits", "Bot hits"]])}</div>
<h2>Daily</h2><div class="card">${table(daily, [["day", "Day"], ["visitors", "Visitors"], ["calc_starts", "Calculator starts"], ["bot_hits", "Bot hits (filtered)"]])}</div>
</main></body></html>`;
  return new Response(html, { headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex" } });
}

async function authorized(request, password) {
  const h = request.headers.get("authorization") || "";
  if (!h.startsWith("Basic ")) return false;
  let decoded = "";
  try { decoded = atob(h.slice(6)); } catch { return false; }
  const given = decoded.slice(decoded.indexOf(":") + 1);
  const enc = new TextEncoder();
  const [a, b] = await Promise.all([crypto.subtle.digest("SHA-256", enc.encode(given)), crypto.subtle.digest("SHA-256", enc.encode(password))]);
  return crypto.subtle.timingSafeEqual ? crypto.subtle.timingSafeEqual(a, b) : btoa(String.fromCharCode(...new Uint8Array(a))) === btoa(String.fromCharCode(...new Uint8Array(b)));
}
