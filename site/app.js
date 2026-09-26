"use strict";

// The search box appears once the collection is large enough to need it.
const SEARCH_THRESHOLD = 6;

const grid = document.getElementById("grid");
const statusEl = document.getElementById("status");
const search = document.getElementById("search");
const dialog = document.getElementById("player");
const video = document.getElementById("player-video");

let videos = [];
// True when the open player added a history entry, so closing should go back.
let pushedHistory = false;

function formatDuration(seconds) {
  const s = Math.floor(seconds);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const ss = String(s % 60).padStart(2, "0");
  return h > 0 ? `${h}:${String(m).padStart(2, "0")}:${ss}` : `${m}:${ss}`;
}

function formatDate(iso) {
  const d = new Date(iso + "T00:00:00");
  if (isNaN(d)) return iso;
  return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

function el(tag, props = {}, children = []) {
  const node = document.createElement(tag);
  Object.assign(node, props);
  for (const child of children) node.append(child);
  return node;
}

function renderGrid() {
  const q = search.value.trim().toLowerCase();
  const shown = q
    ? videos.filter(v => (v.title + " " + v.description).toLowerCase().includes(q))
    : videos;

  grid.replaceChildren(...shown.map(v => {
    const card = el("button", { className: "card", type: "button" }, [
      el("div", { className: "thumb" }, [
        el("img", { src: v.thumbnail, alt: "", loading: "lazy" }),
        el("span", { className: "play" }),
        el("span", { className: "duration", textContent: formatDuration(v.duration) }),
      ]),
      el("div", { className: "card-body" }, [
        el("h3", { textContent: v.title }),
        ...(v.description ? [el("p", { className: "description", textContent: v.description })] : []),
        el("p", { className: "meta-line", textContent: formatDate(v.date) }),
      ]),
    ]);
    card.addEventListener("click", () => openVideo(v, true));
    return el("li", {}, [card]);
  }));

  statusEl.textContent = videos.length === 0
    ? "No videos yet."
    : shown.length === 0 ? "No videos match your search." : "";
}

function openVideo(v, push) {
  if (push) {
    history.pushState(null, "", "#" + encodeURIComponent(v.slug));
    pushedHistory = true;
  }
  document.getElementById("player-title").textContent = v.title;
  document.getElementById("player-info").textContent =
    `${formatDate(v.date)} · ${formatDuration(v.duration)}`;
  document.getElementById("player-description").textContent = v.description;
  document.title = `${v.title} · mip videos`;
  video.poster = v.thumbnail;
  video.src = v.video;
  if (!dialog.open) dialog.showModal();
  video.play().catch(() => {});
}

function currentSlug() {
  return decodeURIComponent(location.hash.slice(1));
}

// Keep the player in sync with the URL (initial load and back/forward).
function syncFromHash() {
  const slug = currentSlug();
  const v = slug && videos.find(x => x.slug === slug);
  if (v) {
    openVideo(v, false);
  } else if (dialog.open) {
    pushedHistory = false;
    dialog.close();
  }
}

dialog.addEventListener("close", () => {
  video.pause();
  video.removeAttribute("src");
  video.load();
  document.title = "mip videos";
  if (currentSlug()) {
    if (pushedHistory) history.back();
    else history.replaceState(null, "", location.pathname + location.search);
  }
  pushedHistory = false;
});

// Clicks on the dialog element itself (not its contents) are backdrop clicks.
dialog.addEventListener("click", e => { if (e.target === dialog) dialog.close(); });
dialog.querySelector(".close").addEventListener("click", () => dialog.close());

window.addEventListener("popstate", syncFromHash);
search.addEventListener("input", renderGrid);

fetch("videos.json")
  .then(r => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return r.json();
  })
  .then(data => {
    videos = data;
    search.hidden = videos.length < SEARCH_THRESHOLD;
    renderGrid();
    syncFromHash();
  })
  .catch(err => {
    statusEl.textContent = `Could not load videos (${err.message}).`;
  });
