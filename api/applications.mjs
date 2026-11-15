import { rpc, sign, safeEqual, esc, yn, VIEW_KEY } from "./_lib.mjs";

const COLS = [
  ["created_at", "Submitted"], ["full_name", "Name"], ["email", "Email"], ["phone", "Phone"], ["city_zip", "City/ZIP"],
  ["is_18_plus", "18+"], ["background_check_ok", "Background check OK"], ["reliable_transportation", "Transportation"],
  ["sports", "Sports"], ["sport_other", "Other sport"], ["has_experience", "Experience"],
  ["experience_details", "Experience details"], ["certifications", "Certifications"], ["has_references", "References"],
  ["reference_list", "Reference list"], ["wants_training", "Wants training"], ["training_sports", "Training in sports"],
  ["heard_about", "Heard about MHO"], ["heard_other", "Heard (other)"],
  ["status", "Status"], ["notes", "Notes"],
];

function val(row, k) {
  const v = row[k];
  if (typeof v === "boolean") return yn(v);
  if (k === "reference_list") return (v || []).map((r, i) => `${i + 1}) ${r.first_name} ${r.last_name}, ${r.phone}, ${r.relationship}`).join("\n");
  if (Array.isArray(v)) return v.join(", ");
  if (k === "created_at") return new Date(v).toLocaleString("en-US", { timeZone: "America/Denver", dateStyle: "medium", timeStyle: "short" }) + " MT";
  return v ?? "";
}

export async function GET(request) {
  const u = new URL(request.url);
  if (!VIEW_KEY || !safeEqual(u.searchParams.get("key"), VIEW_KEY)) return new Response("Not found", { status: 404 });
  const rows = await rpc("mho_list_applications", {});
  const resumeUrl = (r) => (r.has_resume ? `${u.origin}/api/resume?id=${r.id}&sig=${sign(r.id)}` : "");
  const headers = { "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" };

  if (u.searchParams.get("format") === "csv") {
    const q = (x) => `"${String(x).replace(/"/g, '""')}"`;
    const lines = [[...COLS.map((c) => c[1]), "Résumé", "ID"].map(q).join(",")];
    for (const r of rows) lines.push([...COLS.map((c) => val(r, c[0])), resumeUrl(r), r.id].map(q).join(","));
    return new Response("\ufeff" + lines.join("\r\n"), {
      headers: { ...headers, "Content-Type": "text/csv; charset=utf-8", "Content-Disposition": `attachment; filename="mho-applications.csv"` },
    });
  }

  const cards = rows.map((r) => `<article><h2>${esc(r.full_name)}</h2>
<p class="meta">${esc(val(r, "created_at"))} · ${esc(r.status)}</p>
<dl>${COLS.slice(2).filter(([k]) => val(r, k) !== "").map(([k, l]) => `<dt>${esc(l)}</dt><dd>${k === "email" ? `<a href="mailto:${esc(r.email)}">${esc(r.email)}</a>` : k === "phone" ? `<a href="tel:${esc(r.phone.replace(/[^\d+]/g, ""))}">${esc(r.phone)}</a>` : esc(val(r, k))}</dd>`).join("")}
<dt>Résumé</dt><dd>${r.has_resume ? `<a href="${esc(resumeUrl(r))}">Download ${esc(r.resume_filename)}</a>` : "None"}</dd></dl></article>`).join("\n");
  const csvHref = `?key=${encodeURIComponent(u.searchParams.get("key"))}&format=csv`;
  return new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>MHO applications</title>
<style>body{font-family:-apple-system,system-ui,sans-serif;margin:0;padding:16px;background:#f6f4f1;color:#1b1b1b}h1{font-size:1.4rem;margin:0 0 4px}.top a{display:inline-block;margin:8px 0 16px;padding:10px 14px;background:#d4690f;color:#fff;border-radius:8px;text-decoration:none;font-weight:600}article{background:#fff;border-radius:12px;padding:14px 16px;margin:0 0 14px;box-shadow:0 1px 3px rgba(0,0,0,.08)}article h2{margin:0;font-size:1.15rem}.meta{color:#666;margin:2px 0 10px;font-size:.9rem}dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 12px;margin:0;font-size:.95rem}dt{color:#666}dd{margin:0;white-space:pre-wrap;word-break:break-word}</style></head>
<body><div class="top"><h1>Mile High Officials applications (${rows.length})</h1><a href="${esc(csvHref)}">Download as spreadsheet (CSV)</a></div>
${cards || "<p>No applications yet.</p>"}</body></html>`, { headers: { ...headers, "Content-Type": "text/html; charset=utf-8" } });
}
