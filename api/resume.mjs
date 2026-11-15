import { rpc, sign, safeEqual } from "./_lib.mjs";

export async function GET(request) {
  const u = new URL(request.url);
  const id = u.searchParams.get("id") || "";
  if (!/^[0-9a-f-]{36}$/.test(id) || !safeEqual(u.searchParams.get("sig"), sign(id))) return new Response("Not found", { status: 404 });
  const rows = await rpc("mho_get_resume", { p_id: id }).catch(() => null);
  if (!rows || !rows.length) return new Response("Not found", { status: 404 });
  const r = rows[0];
  return new Response(Buffer.from(r.data_b64, "base64"), {
    headers: {
      "Content-Type": r.content_type,
      "Content-Disposition": `attachment; filename="${r.filename.replace(/"/g, "")}"`,
      "Cache-Control": "private, no-store",
      "X-Robots-Tag": "noindex",
    },
  });
}
