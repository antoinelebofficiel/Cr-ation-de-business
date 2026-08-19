(function () {
  const C = window.CLARTEO || {};
  const telDigits = (C.tel || "").replace(/\D/g, "");
  const wa = (C.wa || "").replace(/\D/g, "");
  const telHref = telDigits
    ? "tel:+" + (telDigits.indexOf("33") === 0 ? telDigits : "33" + telDigits.replace(/^0/, ""))
    : "";
  const params = new URLSearchParams(location.search);
  const angle = params.get("a") || "";

  if (C.pixelId) {
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = !0;
      n.version = "2.0";
      n.queue = [];
      t = b.createElement(e);
      t.async = !0;
      t.src = v;
      s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", C.pixelId);
    window.fbq("track", "PageView");
  }

  const pack = ((window.CLARTEO_ADS && window.CLARTEO_ADS.angles) || []).find((a) => a.id === angle);
  if (pack) {
    const h1 = document.querySelector("[data-h1]");
    const letter = document.querySelector("[data-letter]");
    if (h1) h1.textContent = pack.h1;
    if (letter) {
      letter.innerHTML = "";
      pack.primary.split(/\n\n+/).forEach((block) => {
        const p = document.createElement("p");
        p.textContent = block.trim();
        letter.appendChild(p);
      });
    }
    document.title = pack.h1 + " — Clartéo";
  }

  if (window.fbq && document.body.classList.contains("ad")) {
    window.fbq("track", "ViewContent", {
      content_name: "vitrines" + (angle ? "-" + angle : ""),
      content_category: "vitrines",
    });
  }

  document.querySelectorAll("[data-tel-href]").forEach((el) => {
    if (telHref) {
      el.href = telHref;
      if (C.telDisplay && el.hasAttribute("data-tel-label")) el.textContent = C.telDisplay;
    } else if (!el.getAttribute("href") || el.getAttribute("href") === "#") {
      el.href = "#form";
    }
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
    const err = form.querySelector(".err");
    err?.classList.remove("show");
    if (form.querySelector(".hp")?.value) return;

    const data = Object.fromEntries(new FormData(form).entries());
    if (!data.prenom || !data.tel) {
      if (err) {
        err.textContent = "Il faut le prénom et le téléphone.";
        err.classList.add("show");
      }
      return;
    }

    const lines = [
      "Demande Clartéo — vitrines commerce",
      angle ? "Angle pub : " + angle : "",
      "Prénom : " + data.prenom,
      "Tél : " + data.tel,
      data.ville ? "Ville : " + data.ville : "",
      data.baies ? "Baies : " + data.baies : "",
      data.consent ? "Consentement : oui" : "",
    ].filter(Boolean);
    const body = lines.join("\n");

    try {
      localStorage.setItem("clarteo_lead", JSON.stringify({ prenom: data.prenom, tel: data.tel }));
    } catch (x) {}

    if (window.fbq) window.fbq("track", "Lead");

    if (wa) {
      window.open("https://wa.me/" + wa + "?text=" + encodeURIComponent(body), "_blank");
    } else {
      const subject = encodeURIComponent("Lead Clartéo — " + data.prenom);
      window.open("mailto:" + C.email + "?subject=" + subject + "&body=" + encodeURIComponent(body), "_self");
    }

    location.href = "merci.html";
  });
})();
