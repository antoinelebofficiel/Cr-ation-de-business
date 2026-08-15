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

  if (!offre) {
    errorEl.textContent = "Choisissez une intervention.";
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
  const high = String(data.get("etage") || "") === "plus haut";
  thanksCopy.textContent = high
    ? "On vous appelle dans les 5 minutes. Si c’est au-dessus du R+2, on vous le dira tout de suite."
    : combo
      ? "Offre notée : nettoyage de vitres plus ménage. On vous appelle dans les 5 minutes."
      : "Offre notée : nettoyage de vitres. On vous appelle dans les 5 minutes.";
  form.hidden = true;
  thanks.hidden = false;
});
