import { rpc, sign, json, FORMSUBMIT, yn } from "./_lib.mjs";

const SPORTS = ["Basketball", "Wrestling", "Volleyball", "Football", "Flag Football", "Soccer", "Baseball", "Softball"];
const POSITIONS = ["Referee / umpire / game official", "Site supervisor"];
const TRAINING = ["Rules", "Mechanics and positioning", "Game management", "All of the above"];
const HEARD = ["Google search", "Social media", "Friend or referral", "School or league", "Other"];
const MAX_RESUME = 4 * 1024 * 1024;
const EXT = { pdf: "application/pdf", doc: "application/msword", docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" };

const s = (fd, k, max = 500) => String(fd.get(k) ?? "").trim().slice(0, max);
const b = (fd, k) => { const v = s(fd, k, 5).toLowerCase(); return v === "yes" ? true : v === "no" ? false : null; };
const list = (fd, k, allowed) => fd.getAll(k).map(String).filter((v) => allowed.includes(v));

export async function POST(request) {
  let fd;
  try { fd = await request.formData(); } catch { return json({ ok: false, error: "Invalid form." }, 400); }

  // Spam checks: honeypot and minimum fill time. Bots get a quiet fake success.
  const started = Number(s(fd, "_t", 20));
  if (s(fd, "_honey") || !started || Date.now() - started < 3000) return json({ ok: true, id: null, emailed: true });

  const p = {
    full_name: s(fd, "full_name", 120),
    email: s(fd, "email", 160),
    phone: s(fd, "phone", 40),
    city_zip: s(fd, "city_zip", 80),
    is_18_plus: b(fd, "is_18_plus"),
    background_check_ok: b(fd, "background_check_ok"),
    reliable_transportation: b(fd, "reliable_transportation"),
    sports: list(fd, "sports", SPORTS),
    sport_other: s(fd, "sport_other", 120),
    positions: list(fd, "positions", POSITIONS),
    has_experience: b(fd, "has_experience"),
    experience_details: s(fd, "experience_details", 3000),
    certifications: s(fd, "certifications", 500),
    has_references: b(fd, "has_references"),
    references_details: s(fd, "references_details", 2000),
    wants_training: fd.get("wants_training") === "yes" || b(fd, "has_experience") === false,
    training_needs: list(fd, "training_needs", TRAINING),
    training_other: s(fd, "training_other", 300),
    heard_about: HEARD.includes(s(fd, "heard_about")) ? s(fd, "heard_about") : "",
    heard_other: s(fd, "heard_other", 200),
    source_sport: s(fd, "source_sport", 40),
    user_agent: (request.headers.get("user-agent") || "").slice(0, 300),
  };
  if (!p.wants_training) { p.training_needs = []; p.training_other = ""; }

  const missing = [];
  if (!p.full_name) missing.push("full name");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(p.email)) missing.push("a valid email");
  if (p.phone.replace(/\D/g, "").length < 10) missing.push("a phone number");
  if (!p.city_zip) missing.push("city or ZIP");
  for (const [k, label] of [["is_18_plus", "18 or older"], ["background_check_ok", "background check"], ["reliable_transportation", "transportation"], ["has_experience", "previous experience"], ["has_references", "references"]])
    if (p[k] === null) missing.push(label);
  if (!p.sports.length && !p.sport_other) missing.push("at least one sport");
  if (missing.length) return json({ ok: false, error: "Please complete: " + missing.join(", ") + "." }, 400);

  let resumeB64 = null, resumeName = null, resumeType = null;
  const file = fd.get("resume");
  if (file && typeof file === "object" && file.size > 0) {
    const ext = (file.name.split(".").pop() || "").toLowerCase();
    if (!EXT[ext]) return json({ ok: false, error: "Résumé must be a PDF, DOC, or DOCX file." }, 400);
    if (file.size > MAX_RESUME) return json({ ok: false, error: "Résumé must be 4 MB or smaller." }, 400);
    resumeB64 = Buffer.from(await file.arrayBuffer()).toString("base64");
    resumeName = file.name.replace(/[^\w.\- ()]/g, "_").slice(0, 120);
    resumeType = EXT[ext];
  }

  let id;
  try {
    id = await rpc("mho_submit_application", { p, p_resume_b64: resumeB64, p_resume_name: resumeName, p_resume_type: resumeType });
  } catch (e) {
    console.error("save failed", e.message);
    return json({ ok: false, error: "We could not save your application just now. Please try again, or email admin@milehighofficials.com." }, 500);
  }

  const origin = new URL(request.url).origin;
  const sports = [...p.sports, p.sport_other && `Other: ${p.sport_other}`].filter(Boolean).join(", ");
  const email = {
    _subject: `New official application: ${p.full_name}${sports ? " (" + sports + ")" : ""}`,
    _template: "table",
    _captcha: "false",
    name: p.full_name,
    email: p.email,
    phone: p.phone,
    "City or ZIP": p.city_zip,
    "18 or older": yn(p.is_18_plus),
    "OK with background check": yn(p.background_check_ok),
    "Reliable transportation": yn(p.reliable_transportation),
    "Sports": sports,
    "Position": p.positions.join(", ") || "Not specified",
    "Previous officiating experience": yn(p.has_experience),
    "Experience details": p.experience_details || "-",
    "Certifications": p.certifications || "-",
    "Has references": yn(p.has_references),
    "References": p.references_details || "-",
    "Wants training": yn(p.wants_training),
    "Training needed": [...p.training_needs, p.training_other && `Other: ${p.training_other}`].filter(Boolean).join(", ") || "-",
    "Heard about MHO": [p.heard_about, p.heard_other].filter(Boolean).join(": ") || "-",
    "Résumé": resumeName ? `${origin}/api/resume?id=${id}&sig=${sign(id)}` : "None uploaded",
    "Application ID": id,
  };

  let emailed = false;
  try {
    const r = await fetch(FORMSUBMIT, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json", Origin: "https://www.milehighofficials.com", Referer: "https://www.milehighofficials.com/apply/" },
      body: JSON.stringify(email),
    });
    const d = await r.json().catch(() => ({}));
    emailed = r.ok && (d.success === true || d.success === "true");
    if (!emailed) console.error("formsubmit", r.status, JSON.stringify(d).slice(0, 300));
  } catch (e) { console.error("formsubmit error", e.message); }
  if (emailed) { try { await rpc("mho_mark_emailed", { p_id: id }); } catch {} }

  // If the server-side email failed, the browser sends the same email as a fallback.
  return json({ ok: true, id, emailed, email: emailed ? undefined : email });
}
