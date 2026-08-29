export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "method" });
    return;
  }

  const body = typeof req.body === "string" ? JSON.parse(req.body || "{}") : req.body || {};
  const prenom = String(body.prenom || "").trim();
  const tel = String(body.tel || "").trim();
  const ville = String(body.ville || "").trim();
  const angle = String(body.angle || "").trim();

  if (!prenom || !tel) {
    res.status(400).json({ error: "missing" });
    return;
  }

  const message = [
    "Demande Clartéo. Vitrines commerce",
    "Prénom : " + prenom,
    "Tél : " + tel,
    ville ? "Ville : " + ville : "",
    angle ? "Angle pub : " + angle : "",
  ]
    .filter(Boolean)
    .join("\n");

  const payload = { prenom, tel, ville, angle, message };

  const hook = process.env.LEAD_WEBHOOK;
  if (hook) {
    const r = await fetch(hook, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!r.ok) {
      res.status(502).json({ error: "notify" });
      return;
    }
  }

  const resend = process.env.RESEND_API_KEY;
  if (resend) {
    await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + resend,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: "Clartéo <beth.t@example.com>",
        to: [process.env.LEAD_EMAIL || "antoinebch.pro@gmail.com"],
        subject: "Demande Clartéo. Vitrines commerce",
        text: message,
      }),
    });
  }

  res.status(200).json({ ok: true });
}
