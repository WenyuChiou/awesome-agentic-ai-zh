/* One progressive enhancement for normal loads and Material instant navigation. */
(() => {
  "use strict";
  if (window.__aazBannerMotionInitialized) return;
  window.__aazBannerMotionInitialized = true;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let userPaused = false;

  function renderBanners() {
    const playing = !reducedMotion.matches && !userPaused;
    document.querySelectorAll(".aaz-banner").forEach((banner) => {
      const image = banner.querySelector("img");
      const button = banner.querySelector(".aaz-banner__toggle");
      const original = banner.querySelector(".aaz-banner__original");
      if (!image || !button || !original) return;

      const src = playing ? banner.dataset.animatedSrc : banner.dataset.staticSrc;
      // Repeated document$ emissions must not restart the SVG animation.
      if (image.getAttribute("src") !== src) image.setAttribute("src", src);
      original.setAttribute("href", src);
      banner.querySelector(".aaz-diagram__image-link")?.setAttribute("href", src);
      button.textContent = reducedMotion.matches
        ? banner.dataset.reducedLabel
        : playing ? banner.dataset.stopLabel : banner.dataset.playLabel;
      button.disabled = reducedMotion.matches;
      button.hidden = false;
    });
  }

  // Delegation avoids retaining removed pages or adding a listener on every visit.
  document.addEventListener("click", (event) => {
    const button = event.target.closest?.(".aaz-banner__toggle");
    if (!button || !button.closest(".aaz-banner") || button.disabled) return;
    userPaused = !userPaused;
    renderBanners();
  });
  reducedMotion.addEventListener("change", renderBanners);
  if (typeof document$ !== "undefined") document$.subscribe(renderBanners);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderBanners, { once: true });
  } else {
    renderBanners();
  }
})();
