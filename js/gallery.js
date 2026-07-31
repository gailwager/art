/* Gallery page: renders a category's artwork grid, stars, codes, and lightbox */

function thumbName(file) {
  return file.replace(/\.[^.]+$/, ".jpg");
}

const params = new URLSearchParams(location.search);
const catKey = params.get("cat") || CATALOG.categories[0].key;
const cat = CATALOG.categories.find(c => c.key === catKey) || CATALOG.categories[0];
const works = CATALOG.artworks.filter(a => a.cat === cat.key);
let lbIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
  buildNav(cat.key);
  document.title = cat.name + " — Gail Wager";

  const head = document.getElementById("page-head");
  head.innerHTML =
    `<h1>${cat.name}</h1>
     <p class="tag">${cat.tag}</p>
     <div class="star-note">
       <span>&#9734; Click the star on any piece to add it to your favorites &mdash; they will be listed
       automatically if you <a href="contact.html">contact the artist</a>.</span>
       <button id="clear-stars" type="button">Clear all stars</button>
     </div>`;

  const grid = document.getElementById("grid");
  grid.innerHTML = works.map((w, i) => `
    <figure class="card" data-i="${i}">
      <button class="star-btn ${isFavorite(w.code) ? "starred" : ""}" data-code="${w.code}"
              title="Save to favorites" aria-label="Save ${w.title} to favorites">
        ${isFavorite(w.code) ? "&#9733;" : "&#9734;"}
      </button>
      <span class="code-chip">${w.code}</span>
      <div class="imgbox"><img loading="lazy" src="images/thumbs/${encodeURIComponent(thumbName(w.file))}" alt="${w.title}"></div>
      <figcaption class="meta"><div class="t">${w.title}</div></figcaption>
    </figure>`).join("");

  grid.addEventListener("click", (e) => {
    const starBtn = e.target.closest(".star-btn");
    if (starBtn) {
      const on = toggleFavorite(starBtn.dataset.code);
      starBtn.classList.toggle("starred", on);
      starBtn.innerHTML = on ? "&#9733;" : "&#9734;";
      return;
    }
    const card = e.target.closest(".card");
    if (card && e.target.closest(".imgbox")) openLightbox(+card.dataset.i);
  });

  document.getElementById("clear-stars").addEventListener("click", () => {
    clearFavorites();
    document.querySelectorAll(".star-btn").forEach(b => { b.classList.remove("starred"); b.innerHTML = "&#9734;"; });
  });

  // Lightbox
  const lb = document.getElementById("lightbox");
  lb.querySelector(".close").addEventListener("click", closeLightbox);
  lb.querySelector(".prev").addEventListener("click", () => nav(-1));
  lb.querySelector(".next").addEventListener("click", () => nav(1));
  lb.addEventListener("click", (e) => { if (e.target === lb) closeLightbox(); });
  lb.querySelector(".lb-star").addEventListener("click", () => {
    const w = works[lbIndex];
    const on = toggleFavorite(w.code);
    syncLbStar(on);
    const gridBtn = document.querySelector(`.star-btn[data-code="${w.code}"]`);
    if (gridBtn) { gridBtn.classList.toggle("starred", on); gridBtn.innerHTML = on ? "&#9733;" : "&#9734;"; }
  });
  document.addEventListener("keydown", (e) => {
    if (!lb.classList.contains("open")) return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowLeft") nav(-1);
    if (e.key === "ArrowRight") nav(1);
  });
});

function openLightbox(i) {
  lbIndex = i;
  const w = works[i];
  const lb = document.getElementById("lightbox");
  lb.querySelector("img").src = "images/" + encodeURIComponent(w.file);
  lb.querySelector("img").alt = w.title;
  lb.querySelector(".cap .t").textContent = w.title;
  lb.querySelector(".cap .c").textContent = w.code + " · " + cat.name.toUpperCase();
  lb.querySelector(".cap .n").textContent = w.note || "";
  syncLbStar(isFavorite(w.code));
  lb.classList.add("open");
  document.body.style.overflow = "hidden";
  trackEvent("view-" + w.code);
}

function syncLbStar(on) {
  const b = document.querySelector("#lightbox .lb-star");
  b.classList.toggle("starred", on);
  b.innerHTML = on ? "&#9733; Saved to favorites" : "&#9734; Save to favorites";
}

function closeLightbox() {
  document.getElementById("lightbox").classList.remove("open");
  document.body.style.overflow = "";
}

function nav(d) {
  openLightbox((lbIndex + d + works.length) % works.length);
}
