import crypto from "node:crypto";

export const SB_URL = process.env.MHO_SUPABASE_URL;
export const SB_KEY = process.env.MHO_SUPABASE_KEY;
export const DB_TOKEN = process.env.MHO_DB_TOKEN;
export const LINK_SECRET = process.env.MHO_LINK_SECRET;
export const VIEW_KEY = process.env.MHO_VIEW_KEY;
export const FORMSUBMIT = "https://formsubmit.co/ajax/715cffcfd4b9afa81b063f18821de910";

export async function rpc(name, args) {
  const res = await fetch(`${SB_URL}/rest/v1/rpc/${name}`, {
    method: "POST",
    headers: { apikey: SB_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({ p_token: DB_TOKEN, ...args }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`rpc ${name} ${res.status}: ${text.slice(0, 300)}`);
  return text ? JSON.parse(text) : null;
}

export function sign(id) {
  return crypto.createHmac("sha256", LINK_SECRET).update(String(id)).digest("hex").slice(0, 32);
}

export function safeEqual(a, b) {
  const x = Buffer.from(String(a || "")), y = Buffer.from(String(b || ""));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}

export function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

export const yn = (v) => (v === true ? "Yes" : v === false ? "No" : "");
