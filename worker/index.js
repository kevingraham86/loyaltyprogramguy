// loyaltyprogramguy.com Worker
//   static site (ASSETS) + A/B test on the calculator CTA + /api/lead + /api/event + /go/<code> + /admin
import { EXPERIMENTS, pickVariant } from "./experiments.js";
import { renderAdmin } from "./admin.js";

const CONSENT_TEXT =
  "I agree to be contacted by Kevin Graham / SMB AI Partners by call or text at the number provided, " +
  "including automated texts, about my results and services. Consent is not a condition of purchase. " +
  "Msg & data rates may apply. Reply STOP to opt out.";
const EVENT_TYPES = new Set(["calculator_start", "calculator_change", "cta_click", "lead_form_view", "lead_form_start"]);
const SHORT_CODE = /^[a-z0-9][a-z0-9-]{0,39}$/;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    // getyourcustomersback.com (+ www): tracked redirect to the calculator.
    //   /        -> src=gycb      /poway -> src=gycb-poway
    if (url.hostname === "getyourcustomersback.com" || url.hostname === "www.getyourcustomersback.com") {
      return handleVanity(request, ctx, env, url, "gycb");
    }
    // Canonical host: https://loyaltyprogramguy.com (workers.dev stays reachable for testing)
    if (url.hostname === "www.loyaltyprogramguy.com" || (url.protocol === "http:" && url.hostname.endsWith("loyaltyprogramguy.com"))) {
      url.hostname = "loyaltyprogramguy.com";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    try {
      if (path === "/api/lead") return await handleLead(request, env);
      if (path === "/api/event") return await handleEvent(request, env);
      if (path.startsWith("/go/")) return await handleGo(request, env, ctx, path.slice(4).replace(/\/$/, ""));
      if (path === "/admin" || path.startsWith("/admin/")) return await renderAdmin(request, env);
      if (path === "/" || path === "/card/") return await servePage(request, env, ctx, url);
      if (path === "/mainstream" || path === "/mainstream/") {
        return await servePage(request, env, ctx, url, { assetPath: "/mainstream/", source: url.searchParams.get("src") || "mainstream" });
      }
      if (path === "/hakumaru" || path === "/hakumaru/") {
        return await servePage(request, env, ctx, url, { assetPath: "/hakumaru/", source: url.searchParams.get("src") || "hakumaru" });
      }
      if (path === "/offer" || path === "/offer/") {
        return await servePage(request, env, ctx, url, { assetPath: "/offer/", source: url.searchParams.get("src") || "offer" });
      }
      if (path === "/adamsave" || path === "/adamsave/") {
        // The street fair offer ends Fri Sept 25 2026 (midnight PT); after that, send people to the evergreen page.
        if (Date.now() > Date.parse("2026-09-26T07:00:00Z")) {
          return Response.redirect(new URL("/offer?src=adamsave", url).toString(), 302);
        }
        return await servePage(request, env, ctx, url, { assetPath: "/adamsave/", source: url.searchParams.get("src") || "adamsave" });
      }
      // Instagram traffic: /insta, or /insta/<tag> to track a single post, reel or story.
      //   /insta -> source "insta"      /insta/reel-sept -> source "insta-reel-sept"
      const insta = path.match(/^\/insta(?:\/([a-z0-9-]{1,30}))?\/?$/i);
      if (insta) {
        const source = insta[1] ? `insta-${insta[1].toLowerCase()}` : "insta";
        return await servePage(request, env, ctx, url, { assetPath: "/offer/", source, eyebrow: "Straight from Instagram \u00b7 Repeat Business Program" });
      }
      const landing = path.match(/^\/gycb(?:\/([a-z0-9-]{1,30}))?\/?$/i);
      if (landing) {
        const source = landing[1] ? `gycb-${landing[1].toLowerCase()}` : "gycb";
        return await servePage(request, env, ctx, url, { assetPath: "/card/", source });
      }
      return env.ASSETS.fetch(request);
    } catch (err) {
      console.error(path, err && err.stack || err);
      if (path.startsWith("/api/")) return json({ ok: false, error: "server_error" }, 500);
      return env.ASSETS.fetch(request);
    }
  },
};

// ---------------------------------------------------------------- pages + A/B
// opts.assetPath: serve a different asset (e.g. /gycb serves /card/); opts.source: tracking source for landing paths
// opts.eyebrow: replace the page's small line above the headline (says where the visitor came from)
async function servePage(request, env, ctx, url, opts = {}) {
  const res = await env.ASSETS.fetch(opts.assetPath ? new Request(new URL(opts.assetPath, url), request) : request);
  const type = res.headers.get("content-type") || "";
  if (!res.ok || !type.includes("text/html")) return res;

  const cookies = parseCookies(request.headers.get("cookie"));
  const setCookies = [];
  let vid = cookies.lpg_vid;
  if (!vid || !/^[a-f0-9-]{36}$/.test(vid)) {
    vid = crypto.randomUUID();
    setCookies.push(cookie("lpg_vid", vid, 60 * 60 * 24 * 365));
  }
  const exp = EXPERIMENTS.calc_cta;
  let variant = cookies[`ab_${exp.id}`];
  if (!exp.variants[variant]) {
    variant = pickVariant(exp);
    setCookies.push(cookie(`ab_${exp.id}`, variant, 60 * 60 * 24 * 90));
  }
  const bot = isBot(request);
  ctx.waitUntil(logEvent(env, request, {
    type: "page_view", experiment: exp.id, variant, source: opts.source || url.searchParams.get("src"),
    path: url.pathname, visitor_id: vid, is_bot: bot,
  }));

  const v = exp.variants[variant];
  const rewritten = new HTMLRewriter()
    .on(`[data-ab="${exp.id}"]`, { element(el) { el.setInnerContent(v.text); el.setAttribute("data-variant", variant); } })
    .on(".eyebrow", { element(el) { if (opts.eyebrow) el.setInnerContent(opts.eyebrow); } })
    .on("[data-turnstile-sitekey]", { element(el) { el.setAttribute("data-sitekey", env.TURNSTILE_SITEKEY || ""); } })
    .on("body", { element(el) { el.setAttribute("data-vid", vid); el.setAttribute(`data-ab-${exp.id}`, variant); if (opts.source) el.setAttribute("data-src", opts.source); } })
    .transform(res);

  const out = new Response(rewritten.body, rewritten);
  out.headers.set("Cache-Control", "private, no-store");
  out.headers.set("X-Robots-Tag", url.pathname === "/" ? "all" : "noindex");
  for (const c of setCookies) out.headers.append("Set-Cookie", c);
  return out;
}

// ---------------------------------------------------------------- /go/<code>
async function handleGo(request, env, ctx, code) {
  code = decodeURIComponent(code || "").toLowerCase();
  const dest = new URL("/card/", request.url);
  if (SHORT_CODE.test(code)) {
    dest.searchParams.set("src", code);
    ctx.waitUntil(logEvent(env, request, { type: "short_link", source: code, path: `/go/${code}`, is_bot: isBot(request, new URL(request.url)) }));
  }
  return new Response(null, { status: 302, headers: { Location: dest.toString(), "Cache-Control": "no-store" } });
}

// ---------------------------------------------------------------- vanity domains
function handleVanity(request, ctx, env, url, prefix) {
  const seg = (url.pathname.split("/").filter(Boolean)[0] || "").toLowerCase().replace(/[^a-z0-9-]/g, "");
  const code = (seg ? `${prefix}-${seg}` : prefix).slice(0, 40);
  // Bare getyourcustomersback.com -> the evergreen offer page.
  const VANITY_ROOT = "/offer?src=gycb";
  const dest = new URL(seg ? `https://loyaltyprogramguy.com/${prefix}/${seg.slice(0, 30)}` : `https://loyaltyprogramguy.com${VANITY_ROOT}`);
  ctx.waitUntil(logEvent(env, request, { type: "short_link", source: code, path: `${url.hostname}${url.pathname}`.slice(0, 100), is_bot: isBot(request, url) }));
  return new Response(null, { status: 302, headers: { Location: dest.toString(), "Cache-Control": "no-store" } });
}

// ---------------------------------------------------------------- /api/event
async function handleEvent(request, env) {
  const url = new URL(request.url);
  if (request.method !== "POST") return json({ ok: false }, 405);
  if (!sameOrigin(request)) return json({ ok: false }, 403);
  const body = await readJson(request, 4000);
  if (!body || !EVENT_TYPES.has(body.type)) return json({ ok: false }, 400);
  const cookies = parseCookies(request.headers.get("cookie"));
  const exp = EXPERIMENTS.calc_cta;
  await logEvent(env, request, {
    type: body.type,
    experiment: exp.id,
    variant: exp.variants[cookies[`ab_${exp.id}`]] ? cookies[`ab_${exp.id}`] : null,
    source: str(body.source, 40),
    path: str(body.path, 100),
    visitor_id: cookies.lpg_vid || null,
    is_bot: isBot(request, url),
    detail: body.detail ? JSON.stringify(body.detail).slice(0, 500) : null,
  });
  return json({ ok: true });
}

// ---------------------------------------------------------------- /api/lead
async function handleLead(request, env) {
  if (request.method !== "POST") return json({ ok: false }, 405);
  if (!sameOrigin(request)) return json({ ok: false, error: "bad_origin" }, 403);
  const body = await readJson(request, 8000);
  if (!body) return json({ ok: false, error: "bad_request" }, 400);
  if (body.website) return json({ ok: true }); // honeypot: pretend success

  const ip = request.headers.get("cf-connecting-ip") || "";
  if (!(await verifyTurnstile(env, body.turnstile, ip))) return json({ ok: false, error: "verification_failed" }, 400);

  const name = str(body.name, 80), business = str(body.business, 120);
  const phoneDigits = String(body.phone || "").replace(/\D/g, "");
  const phone = phoneDigits.length === 11 && phoneDigits.startsWith("1") ? phoneDigits.slice(1) : phoneDigits;
  const email = str(body.email, 120);
  const errors = [];
  if (!name) errors.push("name");
  if (!business) errors.push("business");
  if (phone.length !== 10) errors.push("phone");
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.push("email");
  if (body.consent !== true) errors.push("consent");
  if (errors.length) return json({ ok: false, error: "invalid", fields: errors }, 400);

  const ipHash = await sha256(`${ip}|${new Date().toISOString().slice(0, 10)}`);
  const recent = await env.DB.prepare(
    "SELECT COUNT(*) AS n FROM leads WHERE ip_hash = ? AND created_at > datetime('now', '-10 minutes')"
  ).bind(ipHash).first();
  if (recent && recent.n >= 5) return json({ ok: false, error: "rate_limited" }, 429);

  const cookies = parseCookies(request.headers.get("cookie"));
  const exp = EXPERIMENTS.calc_cta;
  const variant = exp.variants[cookies[`ab_${exp.id}`]] ? cookies[`ab_${exp.id}`] : null;
  const calc = body.calc || {};
  await env.DB.prepare(
    `INSERT INTO leads (name, business, phone, email, consent_text, list_size, avg_ticket, extra_visits,
       monthly_estimate, source, variant, page, visitor_id, country, ip_hash)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(
    name, business, `${phone.slice(0, 3)}-${phone.slice(3, 6)}-${phone.slice(6)}`, email || null, CONSENT_TEXT,
    int(calc.list_size), int(calc.avg_ticket), num(calc.extra_visits), int(calc.monthly_estimate),
    str(body.source, 40), variant, str(body.path, 100), cookies.lpg_vid || null,
    (request.cf && request.cf.country) || null, ipHash
  ).run();

  await notify(env, { business, source: str(body.source, 40), estimate: int(calc.monthly_estimate), adminUrl: new URL("/admin", request.url).toString() });
  return json({ ok: true });
}

async function verifyTurnstile(env, token, ip) {
  if (!env.TURNSTILE_SECRET || !token) return false;
  const form = new FormData();
  form.append("secret", env.TURNSTILE_SECRET);
  form.append("response", String(token).slice(0, 2048));
  if (ip) form.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: form });
  const data = await r.json();
  return data.success === true;
}

// Optional: set NOTIFY_WEBHOOK (wrangler secret) to a Slack incoming-webhook URL (Discord also works).
// The alert never includes the lead's contact details; those stay in /admin.
async function notify(env, { business, source, estimate, adminUrl }) {
  if (!env.NOTIFY_WEBHOOK) return;
  const text = `:tada: New calculator lead: *${business}*` +
    (estimate ? ` (their estimate: $${Number(estimate).toLocaleString("en-US")}/mo)` : "") +
    (source ? `, source: ${source}` : "") + `\n<${adminUrl}|Open the lead dashboard>`;
  const isDiscord = env.NOTIFY_WEBHOOK.includes("discord.com");
  try {
    const r = await fetch(env.NOTIFY_WEBHOOK, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(isDiscord ? { content: text.replace(/<([^|>]+)\|([^>]+)>/g, "$2: $1") } : { text }),
    });
    if (!r.ok) console.error("notify failed", r.status, await r.text());
  } catch (e) { console.error("notify failed", e); }
}

// ---------------------------------------------------------------- helpers
async function logEvent(env, request, e) {
  try {
    await env.DB.prepare(
      "INSERT INTO events (type, experiment, variant, source, path, visitor_id, country, is_bot, detail) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    ).bind(
      e.type, e.experiment || null, e.variant || null, e.source ? String(e.source).slice(0, 40) : null,
      e.path || null, e.visitor_id || null, (request.cf && request.cf.country) || null, e.is_bot ? 1 : 0, e.detail || null
    ).run();
  } catch (err) { console.error("logEvent failed", err); }
}

// Scanners hammer new domains (2,190 hits in 3 days looking for /wp-admin, /.env, /.git ...).
// Anything matching these is never a customer.
const SCANNER_PATH = /wp-admin|wp-login|wp-content|wp-includes|xmlrpc|\.php|\.env|\.git|\.aws|phpmyadmin|myadmin|cgi-bin|vendor\/|autodiscover|owa\/|\.well-known\/traffic|config\.json|backup|shell|eval-stdin/i;

function isBot(request, url) {
  const ua = (request.headers.get("user-agent") || "").toLowerCase();
  const score = request.cf && request.cf.botManagement && request.cf.botManagement.score;
  if (typeof score === "number" && score < 30) return true;
  if (!ua || /bot|crawl|spider|slurp|headless|python|curl|wget|httpclient|scan|monitor|preview|facebookexternalhit/.test(ua)) return true;
  // Real browsers send these; most scanners do not.
  if (!request.headers.get("accept-language") || !request.headers.get("sec-fetch-dest")) return true;
  const path = url ? url.pathname : new URL(request.url).pathname;
  return SCANNER_PATH.test(path);
}

function sameOrigin(request) {
  const origin = request.headers.get("origin");
  return !origin || origin === new URL(request.url).origin;
}

async function readJson(request, maxBytes) {
  const len = Number(request.headers.get("content-length") || 0);
  if (len > maxBytes) return null;
  const text = await request.text();
  if (text.length > maxBytes) return null;
  try { return JSON.parse(text); } catch { return null; }
}

function parseCookies(header) {
  const out = {};
  for (const part of (header || "").split(";")) {
    const i = part.indexOf("=");
    if (i > 0) out[part.slice(0, i).trim()] = decodeURIComponent(part.slice(i + 1).trim());
  }
  return out;
}
const cookie = (k, v, maxAge) => `${k}=${encodeURIComponent(v)}; Path=/; Max-Age=${maxAge}; Secure; SameSite=Lax`;
const str = (v, max) => (typeof v === "string" ? v.trim().slice(0, max) : "");
const int = (v) => (Number.isFinite(Number(v)) ? Math.round(Number(v)) : null);
const num = (v) => (Number.isFinite(Number(v)) ? Number(v) : null);
const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
async function sha256(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
