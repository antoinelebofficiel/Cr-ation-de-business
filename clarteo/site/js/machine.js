(function () {
  const D = window.CLARTEO_ADS;
  if (!D) return;

  document.querySelectorAll("[data-expert]").forEach((el) => {
    el.textContent = D.experts[el.getAttribute("data-expert")] || "";
  });

  const grid = document.getElementById("angle-grid");
  const copies = document.getElementById("copies");
  let current = D.angles[0];

  function copyText(text) {
    navigator.clipboard.writeText(text).catch(() => {
      const t = document.createElement("textarea");
      t.value = text;
      document.body.appendChild(t);
      t.select();
      document.execCommand("copy");
      t.remove();
    });
  }

  function block(title, text, id) {
    const el = document.createElement("div");
    el.className = "block";
    el.innerHTML =
      '<div class="row"><h3></h3><button type="button" class="copier">Copier</button></div><pre></pre>';
    el.querySelector("h3").textContent = title;
    el.querySelector("pre").id = id;
    el.querySelector("pre").textContent = text;
    el.querySelector(".copier").addEventListener("click", () => {
      copyText(text);
      el.querySelector(".copier").textContent = "Copié";
      setTimeout(() => {
        el.querySelector(".copier").textContent = "Copier";
      }, 1200);
    });
    return el;
  }

  function render(a) {
    current = a;
    document.querySelectorAll("#angle-grid button").forEach((b) => {
      b.classList.toggle("on", b.getAttribute("data-id") === a.id);
    });
    document.getElementById("ov").textContent = a.overlay;
    document.getElementById("primary-preview").textContent = a.primary;
    const url = "vitres.html?a=" + a.id;
    document.getElementById("url").textContent =
      "Landing (même phrase) : " + url + "  ·  Instant Form en parallèle";
    document.getElementById("crea").textContent = "Créa : " + a.crea;
    const sc = document.getElementById("scores");
    sc.innerHTML = "";
    [
      ["Schwartz", a.schwartz],
      ["Halbert", a.halbert],
      ["Wiebe", a.wiebe],
    ].forEach(([n, s]) => {
      const d = document.createElement("div");
      d.innerHTML = "<span></span><strong></strong><p></p>";
      d.querySelector("span").textContent = n;
      d.querySelector("strong").textContent = s.score + "/10";
      d.querySelector("p").textContent = s.note;
      sc.appendChild(d);
    });
    copies.innerHTML = "";
    copies.appendChild(block("Overlay image (max ~20 %)", a.overlay, "c-ov"));
    copies.appendChild(block("Texte principal", a.primary, "c-pr"));
    copies.appendChild(block("Titres (5, tester dans l’ordre)", a.titles.join("\n"), "c-ti"));
    copies.appendChild(block("Description", a.description, "c-de"));
  }

  D.angles.forEach((a) => {
    const b = document.createElement("button");
    b.type = "button";
    b.setAttribute("data-id", a.id);
    b.innerHTML = "<small></small><span></span>";
    b.querySelector("small").textContent = a.id;
    b.querySelector("span").textContent = a.overlay;
    b.addEventListener("click", () => render(a));
    grid.appendChild(b);
  });
  render(current);

  document.querySelectorAll(".tabs button").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tabs button").forEach((x) => x.classList.remove("on"));
      btn.classList.add("on");
      const id = btn.getAttribute("data-tab");
      document.querySelectorAll(".panel").forEach((p) => {
        p.hidden = p.id !== "panel-" + id;
      });
    });
  });

  const F = D.formA;
  document.getElementById("form-intro").textContent = F.name + "\n\n" + F.intro;
  document.getElementById("form-cut").textContent = "Coupé : " + F.cut;
  const ul = document.getElementById("form-qs");
  F.questions.forEach((q, i) => {
    const li = document.createElement("li");
    li.innerHTML = "<b></b><div></div><pre></pre>";
    li.querySelector("b").textContent = i + 1 + ". " + q.q + (q.required ? " (obligatoire)" : "");
    li.querySelector("div").textContent = q.why;
    li.querySelector("pre").textContent = q.options.join("\n");
    ul.appendChild(li);
  });
  document.getElementById("form-ty").textContent =
    F.thankTitle + "\n\n" + F.thankBody + "\n\nBouton : " + F.thankCta;

  document.querySelectorAll("button.copier[data-copy]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const pre = document.getElementById(btn.getAttribute("data-copy"));
      copyText(pre.textContent);
      btn.textContent = "Copié";
      setTimeout(() => {
        btn.textContent = "Copier";
      }, 1200);
    });
  });
})();
