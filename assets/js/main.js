/* Nantucket Lightship / LV-112 — site interactions */
(function () {
  "use strict";

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var body = document.body;

  function closeNav() {
    body.classList.remove("nav-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var backdrop = document.querySelector(".nav-backdrop");
  if (backdrop) backdrop.addEventListener("click", closeNav);

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeNav();
  });

  /* On mobile, tapping a parent submenu link expands its submenu inline instead of
     navigating. The mobile menu (and the inline submenu CSS) only exist at <= 760px,
     so we gate the behavior on that exact breakpoint to avoid hijacking the desktop
     hover dropdowns shown in the 761-980px range. */
  var mobileNav = window.matchMedia("(max-width: 760px)");

  // Pull the <main> from a same-origin page and swap it into the current document so
  // that closing the menu leaves the user on the freshly tapped page. Best-effort only.
  function swapMainFromPage(url) {
    // fetch() against file:// always rejects, so skip the prefetch in that case.
    if (window.location.protocol === "file:") return;

    fetch(url, { credentials: "same-origin" })
      .then(function (res) {
        if (!res.ok) throw new Error("Bad response: " + res.status);
        return res.text();
      })
      .then(function (html) {
        var parsed = new DOMParser().parseFromString(html, "text/html");
        var nextMain = parsed.querySelector("main");
        var currentMain = document.querySelector("main");
        if (nextMain && currentMain) {
          currentMain.replaceWith(nextMain);
        }
        if (parsed.title) document.title = parsed.title;
        // Reflect the new location without a reload; closing the menu keeps them here.
        history.pushState({ url: url }, parsed.title || "", url);
      })
      .catch(function () {
        /* Network/parse failure: leave the current page untouched. */
      });
  }

  var submenuLinks = document.querySelectorAll(".has-submenu > a");
  submenuLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      if (!mobileNav.matches) return; // desktop: let the link navigate normally

      e.preventDefault();
      e.stopPropagation();

      var li = this.parentElement;
      var wasExpanded = li.classList.contains("expanded");

      // Accordion: collapse any other open submenus.
      document.querySelectorAll(".has-submenu.expanded").forEach(function (el) {
        if (el !== li) el.classList.remove("expanded");
      });

      if (wasExpanded) {
        li.classList.remove("expanded");
      } else {
        li.classList.add("expanded");
        // Bonus: prefetch this top-level page and swap it in behind the open menu.
        swapMainFromPage(this.getAttribute("href"));
      }
    });
  });

  /* Mark a nav link as active on click so it changes color immediately, instead of
     only reacting to hover. This listener runs after the submenu handler above, so if
     that called preventDefault (mobile submenu toggle), we skip the active styling. */
  var navLinks = document.querySelectorAll(".main-nav a");
  navLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      if (e.defaultPrevented) return; // submenu toggle, not a real navigation
      navLinks.forEach(function (other) { other.classList.remove("is-active"); });
      this.classList.add("is-active");
    });
  });

  /* ---------- Gallery lightbox ---------- */
  var items = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox]"));
  if (items.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.innerHTML =
      '<button class="lb-close" aria-label="Close">&times;</button>' +
      '<button class="lb-prev" aria-label="Previous">&#8249;</button>' +
      '<button class="lb-next" aria-label="Next">&#8250;</button>' +
      '<img alt="">' +
      '<div class="lb-caption"></div>';
    document.body.appendChild(lb);

    var lbImg = lb.querySelector("img");
    var lbCap = lb.querySelector(".lb-caption");
    var current = 0;

    function imageSrc(el) {
      return el.getAttribute("href") || (el.querySelector("img") && el.querySelector("img").getAttribute("src")) || "";
    }

    function show(i) {
      current = (i + items.length) % items.length;
      var el = items[current];
      var cap = el.getAttribute("data-caption") || "";
      lbImg.src = imageSrc(el);
      lbImg.alt = cap.replace(/<[^>]*>/g, "");
      lbCap.innerHTML = cap;
    }

    function open(i) {
      show(i);
      lb.classList.add("open");
      body.style.overflow = "hidden";
    }
    function close() {
      lb.classList.remove("open");
      body.style.overflow = "";
    }

    items.forEach(function (el, i) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        open(i);
      });
      el.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          open(i);
        }
      });
    });

    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-next").addEventListener("click", function () { show(current + 1); });
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(current - 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowRight") show(current + 1);
      if (e.key === "ArrowLeft") show(current - 1);
    });
  }

  /* ---------- Footer year ---------- */
  var yr = document.querySelector("[data-year]");
  if (yr) yr.textContent = new Date().getFullYear();
})();
