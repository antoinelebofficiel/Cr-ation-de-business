const form = document.getElementById("formulaire");
const thanks = document.querySelector(".thanks");
const thanksCopy = document.querySelector(".thanks-copy");
const errorEl = document.querySelector(".form-error");
const offers = document.querySelectorAll(".offer");

function markOffer() {
  offers.forEach((label) => {
    const on = label.querySelector("input")?.checked;
    label.classList.toggle("is-on", Boolean(on));
  });
}

offers.forEach((label) => {
  label.addEventListener("change", markOffer);
});
markOffer();

function phoneOk(value) {
  const digits = value.replace(/\D/g, "");
  return digits.length >= 10 && digits.length <= 14;
}

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorEl.hidden = true;

  const data = new FormData(form);
  const offre = String(data.get("offre") || "");
  const tel = String(data.get("telephone") || "");
  const etage = String(data.get("etage") || "");

  if (!offre) {
    errorEl.textContent = "Choisissez une offre.";
    errorEl.hidden = false;
    return;
  }
  if (!phoneOk(tel)) {
    errorEl.textContent = "Indiquez un téléphone joignable.";
    errorEl.hidden = false;
    return;
  }
  if (etage === "plus haut") {
    errorEl.textContent = "Au-dessus du R+2, hors forfait. On ne prend pas.";
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
    errorEl.textContent = "Envoi incomplet. Envoyez le formulaire à nouveau ou appelez-nous.";
    errorEl.hidden = false;
    return;
  }

  const combo = offre === "nettoyage de vitres plus ménage";
  thanksCopy.textContent = combo
    ? "Offre retenue : nettoyage de vitres plus ménage (690 €). On confirme le créneau au téléphone."
    : "Offre retenue : nettoyage de vitres (390 €). On confirme le créneau au téléphone.";
  form.hidden = true;
  thanks.hidden = false;
});
