const root = document.documentElement;
root.classList.add("js");

const store = {
  get: (k) => { try { return localStorage.getItem(k); } catch { return null; } },
  set: (k, v) => { try { localStorage.setItem(k, v); } catch {} },
};

// Theme: explicit choice wins, otherwise follow the OS
const prefersDark = matchMedia("(prefers-color-scheme: dark)");
const themeBtns = document.querySelectorAll("[data-theme-set]");
const effectiveTheme = () => root.dataset.theme || (prefersDark.matches ? "dark" : "light");
const syncThemeBtns = () => {
  const t = effectiveTheme();
  themeBtns.forEach((b) => b.setAttribute("aria-pressed", b.dataset.themeSet === t));
};
themeBtns.forEach((b) =>
  b.addEventListener("click", () => {
    root.dataset.theme = b.dataset.themeSet;
    store.set("theme", b.dataset.themeSet);
    syncThemeBtns();
  })
);
prefersDark.addEventListener("change", syncThemeBtns);
syncThemeBtns();

// Mobile menu
const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");
if (menuBtn && mobileMenu) {
  const setMenu = (open) => {
    mobileMenu.classList.toggle("open", open);
    menuBtn.setAttribute("aria-expanded", open);
  };
  menuBtn.addEventListener("click", () => setMenu(!mobileMenu.classList.contains("open")));
  mobileMenu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  addEventListener("keydown", (e) => e.key === "Escape" && setMenu(false));
}

// Nav border on scroll + active link
const nav = document.getElementById("nav");
addEventListener("scroll", () => nav.classList.toggle("scrolled", scrollY > 8), { passive: true });
const links = document.querySelectorAll(".nav-links a[href^='#']");
if (links.length) {
  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        links.forEach((l) => l.classList.toggle("active", l.getAttribute("href") === "#" + e.target.id));
      });
    },
    { rootMargin: "-45% 0px -50% 0px" }
  );
  document.querySelectorAll("main section[id]").forEach((s) => sectionObserver.observe(s));
}

// Reveal on scroll
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add("in");
      revealObserver.unobserve(e.target);
    });
  },
  { threshold: 0.12 }
);
document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

// Count-up stats
const countObserver = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    const el = e.target;
    const target = +el.dataset.count;
    const start = performance.now();
    const tick = (now) => {
      const t = Math.min((now - start) / 900, 1);
      el.firstChild.textContent = Math.round(target * (1 - Math.pow(1 - t, 3)));
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    countObserver.unobserve(el);
  });
});
document.querySelectorAll("[data-count]").forEach((el) => countObserver.observe(el));

// Contact form: Formspree when configured, otherwise a pre-filled email
const form = document.getElementById("contactForm");
if (form) {
  const status = form.querySelector(".form-status");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = new FormData(form);
    if (form.action.includes("YOUR_FORM_ID")) {
      const body = [...data.entries()].map(([k, v]) => `${k}: ${v}`).join("\n");
      location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent("Hello from " + data.get("name"))}&body=${encodeURIComponent(body)}`;
      status.className = "form-status ok";
      status.textContent = "Opening your email app…";
      return;
    }
    status.className = "form-status";
    status.textContent = "Sending…";
    try {
      const res = await fetch(form.action, { method: "POST", body: data, headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error();
      form.reset();
      status.className = "form-status ok";
      status.textContent = "Thanks! I'll get back to you within 24 hours.";
    } catch {
      status.className = "form-status err";
      status.textContent = `Something went wrong. Please email me directly at ${form.dataset.email}.`;
    }
  });
}
