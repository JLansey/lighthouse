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

  /* On mobile, let a parent submenu link expand instead of navigate via a tap region.
     We keep links functional; submenus are shown inline by CSS at small widths. */
  var submenuLinks = document.querySelectorAll(".has-submenu > a");
  submenuLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      // Check if we are in mobile view by checking if the menu is actively open
      if (document.body.classList.contains("nav-open") || window.innerWidth <= 980) {
        e.preventDefault();
        e.stopPropagation();

        var li = this.parentElement;
        var wasExpanded = li.classList.contains("expanded");

        // Collapse all others
        document.querySelectorAll(".has-submenu.expanded").forEach(function(el) {
          if (el !== li) el.classList.remove("expanded");
        });

        if (!wasExpanded) {
          li.classList.add("expanded");
        } else {
          li.classList.remove("expanded");
        }

        // Fetch page behind the scenes
        var url = this.getAttribute("href");
        if (url && url !== "#") {
          fetch(url)
            .then(function(res) { return res.text(); })
            .then(function(html) {
              var parser = new DOMParser();
              var doc = parser.parseFromString(html, "text/html");
              var newMain = doc.querySelector("main");
              var currentMain = document.querySelector("main");
              if (newMain && currentMain) {
                currentMain.innerHTML = newMain.innerHTML;
                document.title = doc.title;
                history.pushState(null, "", url);

                // Update active state in nav
                document.querySelectorAll(".main-nav a").forEach(function(a) {
                  a.removeAttribute("aria-current");
                  if (a.getAttribute("href") === url || a.getAttribute("href") === url.split('/').pop()) {
                    a.setAttribute("aria-current", "page");
                  }
                });
              }
            })
            .catch(function(err) {
              console.error("Failed to load page behind the scenes", err);
            });
        }
      }
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
