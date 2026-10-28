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
  paintHero3d();
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

// 3D models: the hero room follows the theme. At night the room dims to moonlight,
// the screens keep glowing and the desk lamp switches on.
const dayColors = new WeakMap();
let glowRunning = false;
const NIGHT_KEEP = /^(Scr|Sky|Orb|Bulb|Lamp|Spill|CityLights|Bubble)/; // light sources keep their own colours
// night-only light shapes: [material, alpha, emissive]; Spill* is the screens' light and flickers with them
const LAMP_LIGHT = [["LampGlow", 0.26], ["LampPool", 0.45], ["LampPoolCore", 0.65]];
const SCREEN_LIGHT = [["SpillDesk", 0.55], ["SpillDeskCore", 0.6], ["SpillFloor", 0.38], ["SpillFloorCore", 0.42],
  ["SpillHalo0", 0.28], ["SpillHalo1", 0.36], ["SpillHalo2", 0.45]];
const setGlow = (m, alpha, emissive) => {
  const [r, g, b] = dayColors.get(m);
  m.pbrMetallicRoughness.setBaseColorFactor([r, g, b, alpha]);
  m.setEmissiveFactor(emissive);
};
const NIGHT_PERSON = /^(Skin|Hair|Shirt|Jeans|Lip|Mouth|EyeWhite|Shoe|Sole|ChairFabric)$/; // lit by the screens

// Desk lamp: level 0 (off) to 1 (on) drives the bulb and its light cone/pool
function setLamp(mv, level) {
  const mat = (name) => mv.model.getMaterialByName(name);
  mat("Bulb")?.pbrMetallicRoughness.setBaseColorFactor(level > 0.5 ? "#fff1b8" : "#e8e2d0");
  mat("Bulb")?.setEmissiveFactor([level, 0.85 * level, 0.45 * level]);
  for (const [name, alpha] of LAMP_LIGHT) {
    const m = mat(name);
    if (m) setGlow(m, alpha * level, [level, 0.85 * level, 0.5 * level]);
  }
}
// [ms since switch, level]: catches, drops out, sputters, then settles on
const LAMP_FLICKER = [[0, 0], [60, 1], [120, 0], [250, 0], [300, 0.7], [360, 0.1], [500, 0.1], [550, 1], [620, 0.55], [690, 1]];
// Lamp switch click, synthesised with Web Audio (no sound file): press + release, two short filtered noise ticks.
// Switching off is a touch lower and softer than switching on.
let audioCtx;
const CLICK_ON = [[0, 2600, 0.32], [0.05, 1600, 0.18]];
const CLICK_OFF = [[0, 1900, 0.26], [0.045, 1200, 0.15]];
function playLampClick(ticks) {
  try {
    audioCtx ??= new (window.AudioContext || window.webkitAudioContext)();
    const t = audioCtx.currentTime;
    for (const [at, freq, gain] of ticks) {
      const len = Math.floor(audioCtx.sampleRate * 0.03);
      const buf = audioCtx.createBuffer(1, len, audioCtx.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < len; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / len) ** 6;
      const src = audioCtx.createBufferSource();
      src.buffer = buf;
      const band = audioCtx.createBiquadFilter();
      band.type = "bandpass";
      band.frequency.value = freq;
      band.Q.value = 4;
      const vol = audioCtx.createGain();
      vol.gain.value = gain;
      src.connect(band).connect(vol).connect(audioCtx.destination);
      src.start(t + at);
    }
  } catch {}
}

let lastNight = null;
let lampTimers = [];
function flickerLamp(mv) {
  lampTimers.forEach(clearTimeout);
  lampTimers = LAMP_FLICKER.map(([ms, level]) =>
    setTimeout(() => setLamp(mv, effectiveTheme() === "dark" ? level : 0), ms)
  );
}
// Curtains: the model holds CURTAIN_STEPS curtain positions (open to closed, materials Curtain0..N).
// Only one is visible; stepping through them slides the curtains.
const CURTAIN_STEPS = 8;
let curtainStep = null;
let curtainTimers = [];
function setCurtains(mv, step) {
  curtainStep = step;
  for (let k = 0; k < CURTAIN_STEPS; k++) {
    const m = mv.model.getMaterialByName(`Curtain${k}`);
    if (!m) continue;
    if (m.getAlphaMode() !== "MASK") {
      m.setAlphaMode("MASK");
      m.setAlphaCutoff(0.5);
    }
    const [r, g, b] = m.pbrMetallicRoughness.baseColorFactor;
    m.pbrMetallicRoughness.setBaseColorFactor([r, g, b, k === step ? 1 : 0]);
  }
}
function moveCurtains(mv, target) {
  curtainTimers.forEach(clearTimeout);
  const from = curtainStep ?? target;
  const dir = Math.sign(target - from);
  curtainTimers = [];
  for (let s = from + dir, i = 1; dir && s !== target + dir; s += dir, i++) {
    curtainTimers.push(setTimeout(() => setCurtains(mv, s), i * 90));
  }
}

function paintHero3d() {
  const mv = document.querySelector(".hero-art model-viewer");
  if (!mv || !mv.model) return;
  const night = effectiveTheme() === "dark";
  const mat = (name) => mv.model.getMaterialByName(name);
  for (const m of mv.model.materials) {
    const pbr = m.pbrMetallicRoughness;
    if (!dayColors.has(m)) dayColors.set(m, [...pbr.baseColorFactor]);
    if (NIGHT_KEEP.test(m.name)) continue;
    const [r, g, b] = dayColors.get(m);
    const tint = !night ? [1, 1, 1] : NIGHT_PERSON.test(m.name) ? [0.42, 0.42, 0.52] : [0.11, 0.13, 0.22];
    pbr.setBaseColorFactor([r * tint[0], g * tint[1], b * tint[2], pbr.baseColorFactor[3]]); // keep alpha (curtains)
  }
  mat("Sky")?.pbrMetallicRoughness.setBaseColorFactor(night ? "#1b2b4a" : "#bfe3f5");
  mat("Sky")?.setEmissiveFactor(night ? [0.03, 0.05, 0.12] : [0.27, 0.36, 0.42]);
  mat("Orb")?.pbrMetallicRoughness.setBaseColorFactor(night ? "#e6f2ec" : "#f2b134");
  mat("Orb")?.setEmissiveFactor(night ? [0.75, 0.8, 0.78] : [0.53, 0.26, 0.02]);
  // the lamp flickers on when switching from light to dark; otherwise it's simply on or off
  const switchedOn = night && lastNight === false;
  const switchedOff = !night && lastNight === true;
  lastNight = night;
  if (switchedOn) playLampClick(CLICK_ON);
  if (switchedOff) playLampClick(CLICK_OFF);
  if (switchedOn && !reduceMotion.matches) {
    flickerLamp(mv);
  } else {
    lampTimers.forEach(clearTimeout);
    setLamp(mv, night ? 1 : 0);
  }
  // curtains draw shut at night and open by day
  const curtainTarget = night ? CURTAIN_STEPS - 1 : 0;
  if ((switchedOn || switchedOff) && !reduceMotion.matches) {
    moveCurtains(mv, curtainTarget);
  } else {
    curtainTimers.forEach(clearTimeout);
    setCurtains(mv, curtainTarget);
  }
  // screen light in the room: invisible by day (screenGlow animates it at night)
  for (const [name] of SCREEN_LIGHT) {
    const m = mat(name);
    if (m && !night) setGlow(m, 0, [0, 0, 0]);
  }
  mv.exposure = night ? 0.7 : 1.05;
  if (night && !glowRunning) {
    glowRunning = true;
    requestAnimationFrame(screenGlow);
  }
  if (!night) mat("Skin")?.setEmissiveFactor([0, 0, 0]);
}

// Night only: the monitors' cool glow on face and hands, plus their light on the desk, floor and wall.
// Face glow is brightest while facing the screens, easing off (but staying readable) while turned
// round to wave; follows the 8 s Blender loop.
const smoothstep = (e0, e1, x) => {
  const t = Math.min(Math.max((x - e0) / (e1 - e0), 0), 1);
  return t * t * (3 - 2 * t);
};
let heroVisible = true;
const heroMv = document.querySelector(".hero-art model-viewer");
if (heroMv) new IntersectionObserver(([e]) => (heroVisible = e.isIntersecting)).observe(heroMv);
function screenGlow(now) {
  const mv = heroMv;
  if (mv && !heroVisible && effectiveTheme() === "dark") return requestAnimationFrame(screenGlow); // skip material updates offscreen
  const skin = mv?.model?.getMaterialByName("Skin");
  if (!skin || effectiveTheme() !== "dark") {
    glowRunning = false;
    return;
  }
  const f = ((mv.currentTime * 24) % 192) + 1; // Blender frame
  const turned = smoothstep(80, 100, f) * (1 - smoothstep(156, 174, f));
  const flicker = 0.93 + 0.04 * Math.sin(now / 130) + 0.03 * Math.sin(now / 47);
  const k = (1 - 0.35 * turned) * flicker;
  skin.setEmissiveFactor([0.15 * k, 0.17 * k, 0.2 * k]);
  for (const [name, alpha] of SCREEN_LIGHT) {
    const m = mv.model.getMaterialByName(name);
    if (m) setGlow(m, alpha * flicker, [0.55 * flicker, 0.75 * flicker, 0.95 * flicker]);
  }
  requestAnimationFrame(screenGlow);
}
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");
document.querySelectorAll("model-viewer").forEach((mv) =>
  mv.addEventListener("load", () => {
    paintHero3d();
    if (!reduceMotion.matches) mv.play();
  })
);

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

// Marquees: auto-scroll, plus wheel / drag to scroll by hand while hovered
document.querySelectorAll(".marquee").forEach((m) => {
  const track = m.querySelector(".marquee-track");
  const speed = track.classList.contains("reverse") ? 55 : -70; // px per second
  let x = 0, hover = false, drag = null, last = 0, running = false;
  track.style.animation = "none";
  m.style.cursor = "grab";
  const wrap = () => {
    const half = track.scrollWidth / 2;
    x = ((x % half) + half) % half - half;
    track.style.transform = `translate3d(${x}px,0,0)`;
  };
  const tick = (now) => {
    const dt = Math.min(now - last, 100) / 1000;
    last = now;
    if (!hover && !drag && !reduceMotion.matches) x += speed * dt;
    wrap();
    if (running) requestAnimationFrame(tick);
  };
  new IntersectionObserver(([e]) => {
    const was = running;
    running = e.isIntersecting;
    if (running && !was) { last = performance.now(); requestAnimationFrame(tick); }
  }).observe(m);
  m.addEventListener("pointerenter", () => (hover = true));
  m.addEventListener("pointerleave", () => (hover = false));
  m.addEventListener("wheel", (e) => {
    e.preventDefault();
    x -= Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
    wrap();
  }, { passive: false });
  m.addEventListener("pointerdown", (e) => {
    drag = e.clientX;
    m.setPointerCapture(e.pointerId);
    m.style.cursor = "grabbing";
  });
  m.addEventListener("pointermove", (e) => {
    if (drag === null) return;
    x += e.clientX - drag;
    drag = e.clientX;
    wrap();
  });
  const endDrag = () => { drag = null; m.style.cursor = "grab"; };
  m.addEventListener("pointerup", endDrag);
  m.addEventListener("pointercancel", endDrag);
});

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
