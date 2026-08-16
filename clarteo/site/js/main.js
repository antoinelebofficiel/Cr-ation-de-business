(function () {
  const C = window.CLARTEO || {};
  const tel = (C.tel || "").replace(/\s/g, "");
  const wa = (C.wa || "").replace(/\D/g, "");

  document.querySelectorAll("[data-tel-href]").forEach((el) => {
    if (tel) {
      el.href = "tel:" + tel;
      if (C.telDisplay) el.textContent = C.telDisplay;
    } else {
      el.href = "#form";
    }
  });

  document.querySelectorAll("[data-wa-href]").forEach((el) => {
    if (wa) el.href = "https://wa.me/" + wa;
    else el.hidden = true;
  });

  document.querySelectorAll("[data-email]").forEach((el) => {
    el.textContent = C.email;
    if (el.tagName === "A") el.href = "mailto:" + C.email;
  });
  document.querySelectorAll("[data-responsable]").forEach((el) => {
    el.textContent = C.responsable;
  });

  const form = document.querySelector("form[data-lead]");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const err = form.querySelector(".form-err");
    const ok = document.querySelector(".form-ok");
    err?.classList.remove("show");

    if (form.querySelector(".hp")?.value) return;

    const data = Object.fromEntries(new FormData(form).entries());
    if (!data.prenom || !data.tel) {
      if (err) {
        err.textContent = "Prénom et téléphone sont obligatoires.";
        err.classList.add("show");
      }
      return;
    }

    const kind = form.getAttribute("data-lead");
    const lines = [
      "Demande Clartéo — " + (kind === "menage" ? "ménage / vitres maison" : "vitrines commerce"),
      "Prénom : " + data.prenom,
      "Tél : " + data.tel,
      data.ville ? "Ville : " + data.ville : "",
      data.type ? "Type : " + data.type : "",
      data.baies ? "Baies : " + data.baies : "",
      data.situation ? "Situation : " + data.situation : "",
      data.besoin ? "Besoin : " + data.besoin : "",
      data.surface ? "Surface : " + data.surface : "",
      data.consent ? "Consentement : oui" : "",
    ].filter(Boolean);

    const body = lines.join("\n");
    if (wa) {
      window.open("https://wa.me/" + wa + "?text=" + encodeURIComponent(body), "_blank");
    } else {
      const subject = encodeURIComponent("Lead Clartéo " + kind + " — " + data.prenom);
      window.location.href = "mailto:" + C.email + "?subject=" + subject + "&body=" + encodeURIComponent(body);
    }

    form.hidden = true;
    if (ok) ok.classList.add("show");
  });
})();
