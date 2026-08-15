const form = document.getElementById("formulaire");
const thanks = document.querySelector(".thanks");
const thanksCopy = document.querySelector(".thanks-copy");
const errorEl = document.querySelector(".form-error");

function phoneOk(value) {
  const digits = value.replace(/\D/g, "");
  return digits.length >= 10 && digits.length <= 14;
}

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorEl.hidden = true;

  const data = new FormData(form);
  const offre = event.submitter?.value || String(data.get("offre") || "");
  const tel = String(data.get("telephone") || "");
  data.set("offre", offre);

  if (!offre) {
    errorEl.textContent = "Cliquez sur un des deux boutons de devis.";
    errorEl.hidden = false;
    return;
  }
  if (!phoneOk(tel)) {
    errorEl.textContent = "Indiquez un téléphone joignable.";
    errorEl.hidden = false;
    return;
  }

  const payload = Object.fromEntries(data.entries());
  delete payload["bot-field"];
  payload.date = new Date().toISOString();

  try {
    const endpoint = form.getAttribute("action");
    if (endpoint) {
      await fetch(endpoint, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: data,
      });
    } else {
      const leads = JSON.parse(localStorage.getItem("leads-vitres") || "[]");
      leads.push(payload);
      localStorage.setItem("leads-vitres", JSON.stringify(leads));
    }
  } catch (err) {
    errorEl.textContent = "Envoi incomplet. Renvoyez le formulaire.";
    errorEl.hidden = false;
    return;
  }

  const combo = offre === "nettoyage de vitres plus ménage";
  thanksCopy.textContent = combo
    ? "Offre notée : nettoyage de vitres plus ménage. On vous appelle dans les 5 minutes."
    : "Offre notée : nettoyage de vitres. On vous appelle dans les 5 minutes.";
  form.hidden = true;
  thanks.hidden = false;
});
