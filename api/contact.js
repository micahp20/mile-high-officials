const TO_EMAIL = process.env.CONTACT_TO_EMAIL || "admin@milehighofficials.com";
const FROM_EMAIL =
  process.env.RESEND_FROM || "Mile High Officials <beth.t@example.com>";

function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") {
    try {
      return JSON.parse(req.body);
    } catch {
      return {};
    }
  }
  return {};
}

function clean(value, max) {
  return String(value || "")
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "")
    .trim()
    .slice(0, max);
}

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed." });
  }

  const body = readBody(req);
  if (body.company) {
    return res.status(200).json({ ok: true, message: "Thanks. We received your message." });
  }

  const name = clean(body.name, 120);
  const email = clean(body.email, 160).toLowerCase();
  const phone = clean(body.phone, 40);
  const message = clean(body.message, 4000);

  if (!name || !email || !message) {
    return res.status(400).json({
      ok: false,
      error: "Please enter your name, email, and a message.",
    });
  }
  if (!isEmail(email)) {
    return res.status(400).json({ ok: false, error: "Please enter a valid email address." });
  }

  const submission = {
    name,
    email,
    phone: phone || "(not provided)",
    message,
    receivedAt: new Date().toISOString(),
  };

  const key = process.env.RESEND_API_KEY;
  if (!key) {
    console.log("Contact submission (email not sent — RESEND_API_KEY is not set):", submission);
    return res.status(200).json({
      ok: false,
      queued: true,
      error:
        "Email delivery is not configured yet, so this message was saved in the server log but was not emailed. Please call 720-432-0354 or email admin@milehighofficials.com, and we will set up email delivery next.",
    });
  }

  try {
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + key,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: FROM_EMAIL,
        to: [TO_EMAIL],
        reply_to: email,
        subject: "Website contact from " + name,
        text: [
          "New message from the Mile High Officials website.",
          "",
          "Name: " + name,
          "Email: " + email,
          "Phone: " + (phone || "(not provided)"),
          "",
          message,
        ].join("\n"),
      }),
    });

    if (!response.ok) {
      const detail = await response.text();
      console.error("Resend error:", response.status, detail);
      return res.status(502).json({
        ok: false,
        error:
          "We could not deliver your message by email just now. Please call 720-432-0354 or email admin@milehighofficials.com.",
      });
    }

    return res.status(200).json({
      ok: true,
      message: "Thanks. We received your message and will get back to you.",
    });
  } catch (err) {
    console.error("Contact form error:", err);
    return res.status(500).json({
      ok: false,
      error:
        "We could not send your message just now. Please call 720-432-0354 or email admin@milehighofficials.com.",
    });
  }
}
