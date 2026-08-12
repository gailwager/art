/* Shared behavior: nav, favorites (stars), paint-trail cursor, lightweight analytics */

/* ---------- Configuration ---------- */
// Optional: create a free account at goatcounter.com, then set your code here
// (e.g. "gailwager") to collect real visit + region + artwork analytics.
const GOATCOUNTER_CODE = "";

/* ---------- Image URLs ---------- */
// Encode an image path that may contain subdirectories (e.g. oil_paintings/…)
function encodePath(p) {
  return p.split("/").map(encodeURIComponent).join("/");
}

/* ---------- Favorites (stars) ---------- */
const FAV_KEY = "gw_favorites";

function getFavorites() {
  try { return JSON.parse(localStorage.getItem(FAV_KEY)) || []; }
  catch (e) { return []; }
}
function saveFavorites(list) {
  localStorage.setItem(FAV_KEY, JSON.stringify(list));
}
function isFavorite(code) { return getFavorites().includes(code); }
function toggleFavorite(code) {
  const favs = getFavorites();
  const i = favs.indexOf(code);
  if (i >= 0) { favs.splice(i, 1); }
  else { favs.push(code); trackEvent("star-" + code); }
  saveFavorites(favs);
  return i < 0;
}
function clearFavorites() { saveFavorites([]); }

/* ---------- Analytics ---------- */
/* Counts are always kept on this device (localStorage). If GOATCOUNTER_CODE is
   set, pageviews and star events are also sent there, where visits and
   countries can be viewed and exported for the weekly report. */
const STATS_KEY = "gw_stats";

function loadStats() {
  try { return JSON.parse(localStorage.getItem(STATS_KEY)) || { visits: 0, pages: {}, stars: {}, views: {}, first: Date.now() }; }
  catch (e) { return { visits: 0, pages: {}, stars: {}, views: {}, first: Date.now() }; }
}
function saveStats(s) { localStorage.setItem(STATS_KEY, JSON.stringify(s)); }

function trackPage() {
  const s = loadStats();
  const p = location.pathname.split("/").pop() || "index.html";
  s.visits += 1;
  s.pages[p] = (s.pages[p] || 0) + 1;
  saveStats(s);
  if (GOATCOUNTER_CODE && window.goatcounter && window.goatcounter.count) {
    window.goatcounter.count({ path: p });
  }
}

function trackEvent(name) {
  const s = loadStats();
  if (name.startsWith("star-")) {
    const code = name.slice(5);
    s.stars[code] = (s.stars[code] || 0) + 1;
  } else if (name.startsWith("view-")) {
    const code = name.slice(5);
    s.views[code] = (s.views[code] || 0) + 1;
  }
  saveStats(s);
  if (GOATCOUNTER_CODE && window.goatcounter && window.goatcounter.count) {
    window.goatcounter.count({ path: name, event: true });
  }
}

function injectGoatCounter() {
  if (!GOATCOUNTER_CODE) return;
  const s = document.createElement("script");
  s.async = true;
  s.dataset.goatcounter = "https://" + GOATCOUNTER_CODE + ".goatcounter.com/count";
  s.src = "https://gc.zgo.at/count.js";
  document.head.appendChild(s);
}

/* ---------- Navigation ---------- */
function buildNav(activeKey) {
  const nav = document.createElement("nav");
  nav.className = "nav";
  const wcCats = CATALOG.categories.filter(c => c.key !== "collage" && c.key !== "oil");
  const wcActive = wcCats.some(c => c.key === activeKey);
  nav.innerHTML =
    `<a class="brand" href="index.html">Gail Wager</a>
     <a class="item ${activeKey === "collage" ? "active" : ""}" href="gallery.html?cat=collage">Mixed Media</a>
     <a class="item ${activeKey === "oil" ? "active" : ""}" href="gallery.html?cat=oil">Oil Paintings</a>
     <div class="dropdown">
       <button class="item drop-btn ${wcActive ? "active" : ""}" type="button"
               aria-haspopup="true" aria-expanded="false">Watercolor Collections <span class="caret">&#9662;</span></button>
       <div class="drop-menu">
         ${wcCats.map(c => `<a class="${activeKey === c.key ? "active" : ""}" href="gallery.html?cat=${c.key}">${c.name}</a>`).join("")}
       </div>
     </div>
     <a class="item ${activeKey === "about" ? "active" : ""}" href="about.html">About the Artist</a>
     <span class="spacer"></span>
     <a class="cta ${activeKey === "purchase" ? "active" : ""}" href="purchase.html">Purchase Inquiries</a>`;
  document.body.prepend(nav);

  const dd = nav.querySelector(".dropdown");
  const btn = dd.querySelector(".drop-btn");
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const open = dd.classList.toggle("open");
    btn.setAttribute("aria-expanded", open);
  });
  document.addEventListener("click", () => {
    dd.classList.remove("open");
    btn.setAttribute("aria-expanded", "false");
  });
}

function buildFooter() {
  const f = document.createElement("footer");
  f.innerHTML =
    `<div class="f-links">
       <a href="index.html">Home</a>
       <a href="about.html">About</a>
       <a href="purchase.html">Purchase</a>
       <a href="contact.html">Contact</a>
     </div>
     <div>&copy; ${new Date().getFullYear()} Gail Wager &middot; Evergreen, Colorado. All artwork remains the property of the artist.</div>`;
  document.body.appendChild(f);
}

/* ---------- Paintbrush trail ---------- */
function initPaintTrail() {
  if (!window.matchMedia("(pointer: fine)").matches) return;
  document.body.classList.add("brush-cursor");

  const canvas = document.createElement("canvas");
  canvas.id = "paint-trail";
  document.body.appendChild(canvas);
  const ctx = canvas.getContext("2d");
  let W, H;
  const fit = () => { W = canvas.width = innerWidth; H = canvas.height = innerHeight; };
  fit();
  addEventListener("resize", fit);

  const palette = ["#c94f3d", "#e0a63c", "#4d7c8a", "#7c9a5c", "#9a5c8a", "#c9a227", "#4f6d9a"];
  let hueIdx = 0;
  const blobs = [];
  let last = null;

  addEventListener("mousemove", (e) => {
    const p = { x: e.clientX, y: e.clientY };
    if (last) {
      const dx = p.x - last.x, dy = p.y - last.y;
      const dist = Math.hypot(dx, dy);
      const steps = Math.min(6, Math.max(1, Math.floor(dist / 9)));
      for (let i = 0; i < steps; i++) {
        const t = i / steps;
        blobs.push({
          x: last.x + dx * t + (Math.random() - .5) * 3,
          y: last.y + dy * t + (Math.random() - .5) * 3,
          r: 2.5 + Math.random() * 3.5 + Math.min(6, dist * 0.04),
          color: palette[hueIdx],
          born: performance.now(),
          life: 900 + Math.random() * 500,
        });
      }
      if (Math.random() < 0.02) hueIdx = (hueIdx + 1) % palette.length;
    }
    last = p;
  });

  (function paint(now) {
    ctx.clearRect(0, 0, W, H);
    for (let i = blobs.length - 1; i >= 0; i--) {
      const b = blobs[i];
      const age = (now - b.born) / b.life;
      if (age >= 1) { blobs.splice(i, 1); continue; }
      ctx.globalAlpha = 0.5 * (1 - age);
      ctx.fillStyle = b.color;
      ctx.beginPath();
      ctx.ellipse(b.x, b.y, b.r * (1 - age * .4), b.r * 0.72 * (1 - age * .4), 0.6, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(paint);
  })(performance.now());
}

/* ---------- Boot ---------- */
document.addEventListener("DOMContentLoaded", () => {
  injectGoatCounter();
  trackPage();
  initPaintTrail();
  buildFooter();
});
