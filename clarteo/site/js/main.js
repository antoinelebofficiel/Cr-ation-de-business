(function () {
  const C = window.CLARTEO || {};
  const tel = (C.tel || "").replace(/\s/g, "");
  const wa = (C.wa || "").replace(/\D/g, "");
  const params = new URLSearchParams(location.search);
  const angle = params.get("a") || "";

  if (C.pixelId) {
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", C.pixelId);
    window.fbq("track", "PageView");
  }

  const adsPack = ((window.CLARTEO_ADS && window.CLARTEO_ADS.angles) || []).reduce((m, a) => {
    m[a.id] = { echo: "Suite de la pub Meta", h1: a.h1, lede: a.lede };
    return m;
  }, {});
  const angles = {
    vitres: adsPack,
    menage: {
      samedi: {
        echo: "Suite de la pub Meta",
        h1: "Deux heures de votre week-end. Rendues.",
        lede: "Première vacation sous 48 h. Si le niveau est là, on cale un jour fixe.",
      },
      vitres: {
        echo: "Suite de la pub Meta",
        h1: "Les vitres, on sait.",
        lede: "Baies, vérandas, velux. Le ménage suit si vous voulez un rythme.",
      },
      jourfixe: {
        echo: "Suite de la pub Meta",
        h1: "Un jour fixe. C’est fait.",
        lede: "Toutes les deux semaines. Vous rentrez, c’est fait. Première vacation pour juger.",
      },
    },
  };

  const page = document.body.getAttribute("data-lead");
  const pack = (angles[page] || {})[angle];
  if (pack) {
    const echo = document.querySelector("[data-echo]");
    const h1 = document.querySelector("[data-h1]");
    const lede = document.querySelector("[data-lede]");
    if (echo) { echo.hidden = false; echo.textContent = pack.echo; }
    if (h1) h1.textContent = pack.h1;
    if (lede) lede.textContent = pack.lede;
    document.title = pack.h1 + " — Clartéo";
  }

  if (window.fbq && page) {
    window.fbq("track", "ViewContent", {
      content_name: (page || "site") + (angle ? "-" + angle : ""),
      content_category: "vitrines",
    });
  }

  document.querySelectorAll("[data-tel-href]").forEach((el) => {
    if (tel) {
      el.href = "tel:" + tel;
      if (C.telDisplay && el.hasAttribute("data-tel-label")) el.textContent = C.telDisplay;
    } else if (!el.getAttribute("href") || el.getAttribute("href") === "#") {
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

  if (location.pathname.indexOf("merci") !== -1 && window.fbq) {
    window.fbq("track", "Lead");
  }

  const form = document.querySelector("form[data-lead]");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const err = form.querySelector(".form-err");
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
      angle ? "Angle pub : " + angle : "",
      "Prénom : " + data.prenom,
      "Tél : " + data.tel,
      data.ville ? "Ville : " + data.ville : "",
      data.type ? "Type : " + data.type : "",
      data.baies ? "Baies : " + data.baies : "",
      data.besoin ? "Besoin : " + data.besoin : "",
      data.consent ? "Consentement : oui" : "",
    ].filter(Boolean);
    const body = lines.join("\n");

    try {
      localStorage.setItem("clarteo_lead", JSON.stringify({ prenom: data.prenom, tel: data.tel, kind: kind }));
    } catch (x) {}

    if (window.fbq) window.fbq("track", "Lead");

    if (wa) {
      window.open("https://wa.me/" + wa + "?text=" + encodeURIComponent(body), "_blank");
    } else {
      const subject = encodeURIComponent("Lead Clartéo " + kind + " — " + data.prenom);
      window.open("mailto:" + C.email + "?subject=" + subject + "&body=" + encodeURIComponent(body), "_self");
    }

    location.href = "merci.html?lead=" + encodeURIComponent(kind);
  });
})();
