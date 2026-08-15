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

  const submitter = event.submitter;
  const offre = submitter?.getAttribute("value") || "";
  const data = new FormData(form);
  data.set("offre", offre);

  const tel = String(data.get("telephone") || "");
  if (!phoneOk(tel)) {
    errorEl.textContent = "Indiquez un téléphone joignable.";
    errorEl.hidden = false;
    return;
  }
  if (!offre) {
    errorEl.textContent = "Cliquez sur un des deux boutons.";
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
    errorEl.textContent = "Envoi incomplet. Cliquez à nouveau sur le bouton.";
    errorEl.hidden = false;
    return;
  }

  const combo = offre === "nettoyage de vitres plus ménage";
  thanksCopy.textContent = combo
    ? "Demande notée : devis nettoyage de vitres et ménage / locaux. Téléphone en main."
    : "Demande notée : devis nettoyage de vitres. Téléphone en main.";
  form.hidden = true;
  thanks.hidden = false;
  thanks.scrollIntoView({ behavior: "smooth", block: "start" });
});
