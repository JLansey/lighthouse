#!/usr/bin/env python3
"""
Static site generator for the United States Lightship Museum (LV-112).

This is a simple, dependency-free build helper that assembles the shared header,
footer and per-page content into plain static HTML files in the project root.
The generated *.html files are what gets deployed; this script just keeps the
shared chrome DRY. Run:  python3 build_site.py
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (top-level nav key) used to mark the current section
NAV = [
    ("lv112", "lv-112.html", "LV-112", [
        ("lv-112.html", "About LV-112"),
        ("mission.html", "Mission / Purpose"),
        ("current-lightships.html", "Current U.S. Lightship Museums"),
        ("crew-quotes.html", "Crew Quotes"),
        ("gallery.html", "Photo Gallery"),
        ("news.html", "News"),
        ("visiting-hours.html", "Visiting Hours"),
    ]),
    ("help", "how-to-help.html", "How to Help", [
        ("how-to-help.html", "How to Help"),
        ("volunteer.html", "Volunteer"),
        ("supporters.html", "Our Supporters"),
        ("vehicle-donation.html", "Vehicle Donation Program"),
    ]),
    ("contact", "contact.html", "Contact Us", None),
    ("newsletter", "newsletter.html", "Newsletter", None),
    ("membership", "membership.html", "Membership", None),
]


def nav_html(active):
    home_current = ' aria-current="page"' if active == "home" else ""
    items = [
        f'          <li class="nav-item"><a href="index.html"{home_current}>Home</a></li>'
    ]
    for key, href, label, sub in NAV:
        cur = ' aria-current="page"' if key == active else ""
        if sub:
            subitems = "\n".join(
                f'              <li><a href="{h}">{t}</a></li>' for h, t in sub
            )
            items.append(
                f'''          <li class="nav-item has-submenu">
            <a href="{href}"{cur}>{label}</a>
            <ul class="submenu">
{subitems}
            </ul>
          </li>'''
            )
        else:
            items.append(
                f'          <li class="nav-item"><a href="{href}"{cur}>{label}</a></li>'
            )
    return "\n".join(items)


def header(active):
    return f'''  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="container header-bar">
      <button class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Toggle menu">
        <span class="bars"><span></span></span>
        <span>Menu</span>
      </button>
      <nav class="main-nav" id="primary-nav" aria-label="Primary">
        <ul>
{nav_html(active)}
        </ul>
      </nav>
    </div>
    <div class="nav-backdrop"></div>
  </header>
'''


FOOTER = '''  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-about">
          <h4>United States Lightship Museum</h4>
          <p>Preserving <em>Nantucket Lightship / LV-112</em> &mdash; the largest and most famous U.S. lightship ever built and a National Historic Landmark &mdash; in her home port of Boston.</p>
          <div class="social">
            <a href="https://www.facebook.com/pages/NantucketLightshipLV-112/253217448024322" target="_blank" rel="noopener" aria-label="Facebook">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a href="https://www.youtube.com/user/NantucketLV112" target="_blank" rel="noopener" aria-label="YouTube">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
            </a>
          </div>
        </div>
        <div>
          <h4>Explore</h4>
          <ul class="footer-links">
            <li><a href="lv-112.html">About LV-112</a></li>
            <li><a href="mission.html">Mission / Purpose</a></li>
            <li><a href="gallery.html">Photo Gallery</a></li>
            <li><a href="visiting-hours.html">Visiting Hours</a></li>
            <li><a href="newsletter.html">Newsletter</a></li>
          </ul>
        </div>
        <div>
          <h4>Visit &amp; Contact</h4>
          <ul class="footer-links">
            <li>Boston Harbor Shipyard &amp; Marina<br>256 Marginal St., East Boston, MA</li>
            <li>Mailing: P.O. Box 454, Amesbury, MA 01913</li>
            <li><a href="tel:+16177970135">617.797.0135</a></li>
            <li><a href="mailto:rmmjr2@comcast.net">rmmjr2@comcast.net</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span data-year>2026</span> United States Lightship Museum, Inc.</span>
        <span>A 501(c)(3) non-profit organization</span>
      </div>
    </div>
  </footer>

  <script src="assets/js/main.js?v=3"></script>
</body>
</html>
'''


def page(filename, title, description, active, body, head_extra=""):
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Nantucket Lightship / LV-112</title>
  <meta name="description" content="{description}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/css/styles.css">{head_extra}
</head>
<body>
{header(active)}
  <main id="main">
{body}
  </main>

{FOOTER}'''
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)


def page_head(eyebrow, h1, crumb):
    return f'''    <section class="page-head">
      <div class="container">
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
      </div>
    </section>
    <div class="container">
      <p class="crumbs"><a href="index.html">Home</a> &rsaquo; {crumb}</p>
    </div>
'''


def two_col(content, sidebar):
    return f'''    <section class="section">
      <div class="container">
        <div class="layout">
          <div class="prose">
{content}
          </div>
          <aside class="sidebar">
{sidebar}
          </aside>
        </div>
      </div>
    </section>
'''


def single_col(content):
    return f'''    <section class="section">
      <div class="container">
        <div class="prose" style="max-width:820px;">
{content}
        </div>
      </div>
    </section>
'''


def side_photo(img, caption, alt=None):
    alt = alt if alt is not None else caption
    if caption:
        body = f'''              <figure>
                <img src="{img}" alt="{alt}">
                <figcaption class="side-caption">{caption}</figcaption>
              </figure>'''
    else:
        body = f'              <img src="{img}" alt="{alt}">'
    return f'''            <div class="side-card">
{body}
            </div>'''


DONATE_CARD = '''            <div class="side-card donate-card">
              <h3>Support the restoration</h3>
              <p>The USLM is a 501(c)(3) non-profit. Donations are tax-deductible to the full extent allowed by law.</p>
              <a class="btn btn-primary" href="how-to-help.html#donate">Donate Now</a>
            </div>'''


PAYPAL_FORM = '''<form action="https://www.paypal.com/cgi-bin/webscr" method="post" class="paypal-form">
              <input type="hidden" name="cmd" value="_s-xclick">
              <input type="hidden" name="hosted_button_id" value="7K5PGCBE8ZCR8">
              <button type="submit" class="btn btn-primary">Donate via PayPal</button>
            </form>'''


# ---------------------------------------------------------------------------
# PAGE CONTENT
# ---------------------------------------------------------------------------

def build():
    # ---- About LV-112 ----
    about = '''            <h2>About LV-112</h2>
            <p class="lead">Rescuing a U.S. National Historic Landmark.</p>
            <figure class="figure">
              <img src="assets/images/nantucket_lightship2016.jpg" alt="Nantucket Lightship LV-112 berthed in Boston Harbor">
              <figcaption><em>Nantucket Lightship / LV-112</em></figcaption>
            </figure>
            <h3>Lifelines on the sea</h3>
            <p>Lightships were stationed at the most dangerous areas along the U.S. oceanic and Great Lakes coastlines. These floating sentinels were part of a lifeline that played an important role in the development of our country. They are a part of our maritime heritage and serve as a memorial to the brave U.S. Coast Guard (USCG) lightship sailors who served on them, risking and sacrificing their lives.</p>
            <p>Lightship duty for crewmembers was extremely hazardous, especially on the Nantucket Shoals station &mdash; considered the most dangerous lightship assignment in the USCG and the world.</p>
            <p>During the winter months, nor&rsquo;easters could last for days. Howling winds and mountainous seas tossed lightships so violently, even the most seasoned sailors became seasick. The constant odor of diesel fumes was equally nauseating, in addition to the ship's piercing and incessant fog signals, which caused ear pain and even deafness.</p>
            <p>A lightship station at night was a profoundly lonely and dangerous place to be, especially during foul weather. Located beyond sight of land in the pitch-black isolation of night, the ship&rsquo;s only sign of civilization was the ephemeral passing of ships, which could possibly be called upon for emergency assistance.</p>
            <p>Poor visibility is another hazard on the Nantucket Shoals, where blinding fog is a common occurrence. There was always the threat of being rammed by huge freighters, tankers or ocean liners trying to navigate through the pea-soup murkiness.</p>
            <p>Like a traffic cop at a busy intersection, <em>Nantucket Lightship / LV-112</em> was stationed in one of the busiest shipping lanes in the world, sometimes referred to as &ldquo;the Times Square of the Atlantic.&rdquo; (<em>Desperate Hours</em>) There were numerous accounts of near misses and actual collisions involving &ldquo;the Nantucket.&rdquo;</p>
            <p>During World War II (1942-1945), <em>LV-112</em> was withdrawn from lightship duty, painted battleship gray, designated as the USS Nantucket and served as an examination Patrol Vessel off Portland, Maine; saved crewmembers of the USS Eagle-56, which was torpedoed and sunk off Portland by a German U-Boat, U-853. After sinking another U.S. merchant ship off Port Judith, Rhode Island, the U-853 was tracked down and sunk by the U.S. Navy in Rhode Island waters, where it lies submerged to this day.</p>
            <p>Nantucket Shoals was no stranger to ship collisions and fatal sinkings. On July 25, 1956, the ill-fated <em><a href="http://www.pbs.org/lostliners/andrea.html" target="_blank" rel="noopener">Andrea Doria</a></em> passed within one mile of the station. However, on that day <em>LV-112</em> was not on station. She had been temporarily relieved by <em><a href="http://www.lighthousefriends.com/light.asp?ID=617" target="_blank" rel="noopener">Relief / LV-114 / WAL 536</a></em> (LV-114 later became <em>New Bedford</em>, but was scrapped in 2007 after a long period of neglect and sinking at her dock. More than $200,000 of taxpayer money was spent raising her, only to have her sold to a salvage company for just $10,000.).</p>
            <p>Lightship duty was not always horrific. The sea can sometimes be exceedingly calm, and there were times of peace and solitude with occasional visits by whales and dolphins.</p>
            <p>In all, 179 lightships were built between 1820 through 1952. At one time, 51 (46 on the eastern seaboard and 5 on the Pacific Coast) lightships were stationed at various locations around the United States. Today, only 17 lightships still exist.</p>
            <p>Eight of these lightships have qualified for National Historic Landmark status by possessing unique characteristics of historic significance; they are currently public museums. National Historic Landmark designation, which currently only includes under 2,500 structures, is considered a more prestigious designation than a listing on the register of National Historic Places, which currently includes approximately 85,000 structures.</p>

            <h3><em>LV-112</em> Facts</h3>
            <p>The U.S. <em><a href="http://www.uscg.mil/history/weblightships/LV112.asp" target="_blank" rel="noopener">Nantucket Lightship / LV-112</a></em> was built by Pusey &amp; Jones Shipbuilders in 1936 at Wilmington, Delaware, as a steam-propelled vessel with a compound reciprocating engine that included two oil fired Babcock-Wilcox water tube boilers, producing a maximum speed of 12 knots. Her $300,956 cost, greater than that of any predecessor, was paid for by the White Star Line as compensation for the 1934 collision and sinking of <em>LV-112</em>&rsquo;s predecessor, <em>LV-117</em>, which while on duty at Nantucket station, was rammed by the <em>RMS Olympic</em>, the sister ship to the <em>Titanic</em>. Seven of the lightship&rsquo;s 11 crew members were killed. In 1960, <em>LV-112</em> underwent major modifications, modernization and refitting: smoke stack removed; re-powered with Cooper-Bessemer 900 HP diesel main engine; up until this time, <em>LV-112</em> was the last steam-propelled U.S. lightship. Her navigational lighting aids also were updated.</p>
            <ul>
              <li>Largest lightship ever built in the United States</li>
              <li>Built to the specifications of a war time U.S. Navy vessel with a double hull, double hull shell plating and a high degree of compartmentalization (43). <em>LV-112</em> was designed and built to be virtually unsinkable.</li>
              <li>Served longer than any other U.S. lightship on Nantucket Station &mdash; 39&nbsp;years</li>
              <li>Last of the U.S. lightship stations to be discontinued (1985)</li>
              <li>Farthest offshore station (100 miles from the mainland)</li>
              <li>Only U.S. lightship stationed in international waters</li>
              <li>Last lightship seen by vessels departing the United States and the first beacon seen entering U.S. waters</li>
              <li>Declared a National Historic Landmark in 1989 by the National Park Service &mdash; U.S. Department of the Interior</li>
              <li>Selected as a National Treasure in 2012 (one of 32 in the United States) by the <a href="http://www.savingplaces.org/treasures/nantucket-lightship" target="_blank" rel="noopener">National Trust for Historic Preservation</a></li>
            </ul>
            <p><em>LV-112</em> specifications:<br>
              Length: 148&rsquo; 10&rdquo;&nbsp;&nbsp;|&nbsp;&nbsp;Beam: 32&rsquo;&nbsp;&nbsp;|&nbsp;&nbsp;Draft: 16&rsquo;&nbsp;&nbsp;|&nbsp;&nbsp;Tonnage: 1,050 displ.</p>
            <p>Most U.S. lightships of the same vintage or later averaged 500-600 displacement tons.</p>

            <h3>Moving and rescuing the ship</h3>
            <p>The <em><a href="http://www.lighthousefriends.com/light.asp?ID=805" target="_blank" rel="noopener">Nantucket Lightship</a></em> was transported to Boston Harbor in May 2010 from Oyster Bay, NY where she sat idle for the last eight years. <em>LV-112</em> is currently berthed in East Boston at the <a href="http://www.bhsmarina.com/" target="_blank" rel="noopener">Boston Harbor Shipyard &amp; Marina</a>. For all her years on the seas and in port, the ship is seaworthy and essentially in sound condition. Many people have cared about her past and her future.</p>
            <p>Since <em>LV-112</em>&rsquo;s decommissioning in 1975 in Boston, the historic ship has been used as a museum and has changed ownership and ports several times. Past owners were well intentioned, but <em>LV-112</em> repeatedly fell victim to politics, lack of adequate marketing and media coverage, and most importantly, funding.</p>
            <p>On October 20, 2009, the United States Lightship Museum (USLM), a 501(c)3 nonprofit organization, became <em>LV-112's</em> new owners / steward. The USLM is implementing a strategy that includes <em>LV-112's</em> continuation as a lightship museum and floating school with a primary focus on showcasing its remarkable history. Fortunately, the transfer of <em>LV-112's</em> ownership includes a Covenant intended to prevent the lightship from ever being used for anything other than a nonprofit museum and educational institution.</p>

            <h3><em>LV-112</em>'s restoration</h3>
            <p>There is cause to celebrate. So far the U.S. Lightship Museum (USLM) has restored 95% of <em>LV-112's</em> exterior (hull and superstructure). Most of the shipboard lighting has also been restored and is operational again. Presently, our restoration efforts are focused on <em>LV-112's</em> interior (i.e., electrical infrastructure, plumbing, heating system, ventilation, engines, etc.).</p>
            <p>The main eight cylinder 900 HP Cooper-Bessemer diesel engine has not been operated for several years, but it appears to be in good condition and can be restarted. There are six other smaller (three GM-371's and three GM-271 engines) diesel engines (three electrical generators and three air compressors that start the main engine and operate the navigational fog signal). Two of the engines are currently in running condition. The others need varying degrees of repairs. Two of the electrical generators need extensive repair and restoration.</p>

            <h3>Throwing the ship a lifeline</h3>
            <p>The USLM has transported <em>LV-112</em> back to Boston Harbor from Oyster Bay, Long Island, NY. While commissioned as a lightship, Nantucket / <em>LV-112's</em> home port was Boston (U.S. Coast Guard First District headquarters). <em>LV-112</em> was also decommissioned in Boston. Once again, Boston is <em>LV-112's</em> home port.</p>
            <div class="callout">
              <p>Every little bit helps! Even if you can only afford $1.00, any amount you are able to contribute would be greatly appreciated. The United States Lightship Museum (USLM) is a 501(c)3 non-profit organization. Charitable donations are tax-deductible to the full extent allowed by law. If you prefer to mail in your contribution instead of donating electronically on our website (<a href="how-to-help.html">How to Help</a>), please make your check payable to: <strong>USLM / <em>Nantucket / LV-112</em></strong> and mail it to: United States Lightship Museum, Inc., P.O. Box 454, Amesbury, MA 01913. Thank you!</p>
            </div>

            <h3>Acknowledgements</h3>
            <p>We would like to thank the following for helping us with our research, regarding <em>LV-112</em>:</p>
            <p>USCG Lightship Sailors Association, especially their President, Larry Ryan (lightship veteran, 1960-61), who was extremely helpful in assisting us with our historic research and providing lightship crew contacts.</p>
            <p><a href="http://www.uscg.mil/history/default.asp" target="_blank" rel="noopener">USCG Historians Office</a>, USCG Lightship Sailors Association International, crew members of <em>LV-112</em>, USCG Art Program, Overfalls Maritime Museum Foundation.</p>
            <p>Other Information sources: &ldquo;A History of U.S. Lightships&rdquo; by Willard Flint, &ldquo;Desperate Hours&rdquo; by Richard Goldstein, the National Lighthouse Museum, National Park Service, <em>The Boston Globe, Nantucket Inquirer and Mirror</em>, and Jerry Roberts, Executive Director, <a href="http://www.ctrivermuseum.org/default.aspx" target="_blank" rel="noopener">Connecticut River Museum</a>.</p>
            <p>Robert Mannino, Jr., of South Hampton, New Hampshire, is spearheading the effort to save <em>LV-112</em>. He is a marketing communications and public relations consultant, specializing in development programs for nonprofit organizations including maritime museums, historical societies and shipbuilding preservation projects. His experience also includes chairing municipal historical commissions.</p>'''
    about_side = '''            <div class="side-card">
              <figure>
                <img src="assets/images/pg2_lightship_right_rev.jpg" alt="Painting of Lightship Nantucket LV-117 being rammed by RMS Olympic">
                <figcaption class="side-caption"><em>Lightship Nantucket / LV-117</em> rammed by <em>RMS&nbsp;Olympic</em>. Painted by Charles Mazoujian.</figcaption>
              </figure>
              <div class="side-body">
                <h3>Lightship Nantucket sunk by RMS&nbsp;Olympic</h3>
                <p>On May 15, 1934, <em>Nantucket / LV-117</em> was struck by the passenger liner <em>Olympic</em>, sister ship to the <em>Titanic</em>. <em>Olympic</em>, nearly 75 times larger than the lightship and traveling at about 20 knots, struck it broadside in heavy fog and drove it to the bottom. Boats from <em>Olympic</em> were immediately put over, but the lightship sank within minutes, killing seven of the eleven crewmembers. (USCG)</p>
              </div>
            </div>''' + "\n" + DONATE_CARD
    page("lv-112.html", "About LV-112",
         "The history of Nantucket Lightship / LV-112, a National Historic Landmark, and the United States Lightship Museum's effort to rescue and restore her.",
         "lv112",
         page_head("LV-112", "About LV-112", "About LV-112") + two_col(about, about_side))

    # ---- Mission ----
    mission = '''            <h2>Mission Statement</h2>
            <h3>Mission</h3>
            <p>The mission of the United States Lightship Museum (USLM) is to preserve and maintain <em>Nantucket Lightship / LV-112</em> in perpetuity, reestablishing this National Historic Landmark in its homeport of Boston. It serves as a floating museum and learning center for the general public, chronicling the maritime history of the U.S. Lightship Service from its inception in 1820 to its end in 1985. Visitors will experience what lightship service was like for crewmembers living aboard these &ldquo;floating lighthouses,&rdquo; whose duty was to stay on their station regardless of conditions, faithfully and courageously guiding transoceanic commerce to and from the United States through dangerous seas.</p>
            <h3>Vision and Goals</h3>
            <p><img src="assets/images/boy_at_wheel.jpg" alt="Boy at the wheel of LV-112" class="img-right">The long-term goals of the United States Lightship Museum are two-fold. First and foremost, our objective is to preserve and protect the structural integrity of <em>Nantucket Lightship / LV-112</em> &mdash; the largest and most famous U.S. lightship ever built &mdash; consistent with its use as a commissioned U.S. Coast Guard lightship vessel, based in Boston and stationed on the treacherous Nantucket Shoals from 1936 to 1975. The ship is shared with the public as a floating educational institution, including exhibits to illuminate the importance of the U.S. Lightship Service and its historic relevance to transoceanic commerce and transportation.</p>
            <figure class="figure" style="max-width:260px;">
              <img src="assets/images/winter_volunteers.jpg" alt="Winter volunteers on LV-112">
              <figcaption>Winter volunteers on LV-112.</figcaption>
            </figure>
            <p>In addition, <em>Nantucket Lightship / LV-112</em> serves as a catalyst for people to gain a broad understanding of maritime history and marine sciences. Much of what determines our future is learned from our past. The museum offers interactive programs in collaboration with various educational institutions, maritime and marine-science organizations. Through an engaging learning environment and hands-on programs, this 150-foot living museum engenders an appreciation of maritime history as well as contemporary marine and nautical sciences including engineering, navigational, environmental and weather sciences.</p>
            <p>The museum reaches out to diverse populations of all backgrounds and ages. Instructors from learning institutions and youth groups coordinate with the museum, utilizing it as part of a customized curriculum for their students. In addition, the museum serves as a resource and field trip destination for groups such as special-needs individuals, inner-city children and senior citizens.</p>
            <p>Among its long-term goals, the USLM aims to provide impetus for the establishment of a maritime center for Boston Harbor. The United States Lightship Museum is a 501(c)3 non-profit organization.</p>'''
    mission_side = side_photo(
        "assets/images/pg2_nantucket_shoals.jpg",
        "<em>LV-112</em>, on Nantucket Shoals station, prior to 1960.",
        "LV-112 on Nantucket Shoals station prior to 1960") + "\n" + DONATE_CARD
    page("mission.html", "Mission / Purpose",
         "The mission of the United States Lightship Museum: to preserve and maintain Nantucket Lightship / LV-112 in perpetuity as a floating museum and learning center in Boston.",
         "lv112",
         page_head("LV-112", "Mission / Purpose", "Mission / Purpose") + two_col(mission, mission_side))

    # ---- Current lightships ----
    lightships = '''            <h2>Current U.S. Lightship Museums</h2>
            <p>There are currently nine lightship museums, eight of which are actively open to the public. Some operate as independent museums, but most are part of maritime museum organizations that include other historic vessels and landmarks. They are as follows:</p>
            <ol>
              <li><a href="http://www.hnsa.org/ships/swiftsure.htm" target="_blank" rel="noopener">LV-83 &ldquo;Swiftsure,&rdquo; Northwest Seaport, Seattle, WA</a></li>
              <li><a href="http://www.feuerschiffseite.de/SCHIFFE/USA/WAL512/wal512gb.htm" target="_blank" rel="noopener">LV-87 &ldquo;Ambrose,&rdquo; South Street Seaport Museum, New York, NY</a></li>
              <li><a href="http://www.lighthousefriends.com/light.asp?ID=447" target="_blank" rel="noopener">LV-101 &ldquo;Portsmouth,&rdquo; Naval Shipyard Museum, Portsmouth, VA</a></li>
              <li><a href="http://www.lighthousefriends.com/light.asp?ID=166" target="_blank" rel="noopener">LV-103 &ldquo;Huron,&rdquo; Port Huron Museum, Port Huron, MI</a></li>
              <li>LV-112 &ldquo;Nantucket,&rdquo; <a href="http://www.bhsmarina.com/" target="_blank" rel="noopener">Boston, Massachusetts</a></li>
              <li><a href="http://www.lighthousefriends.com/light.asp?ID=420" target="_blank" rel="noopener">LV-116 &ldquo;Chesapeake,&rdquo; Baltimore Maritime Museum, Baltimore, MD</a></li>
              <li><a href="http://www.lighthousefriends.com/light.asp?ID=554" target="_blank" rel="noopener">WLV-604 &ldquo;Columbia,&rdquo; Columbia River Maritime Museum, Astoria, OR</a></li>
              <li><a href="http://www.uslhs.org/about_lightship.php" target="_blank" rel="noopener">WLV-605 &ldquo;Relief,&rdquo; Lightship Relief, Oakland, CA</a></li>
              <li><a href="http://www.overfalls.org/" target="_blank" rel="noopener">LV-118 &ldquo;Overfalls,&rdquo; Overfalls Lightship Museum, Lewes, DE</a></li>
            </ol>
            <p>Two other Nantucket lightships are in existence and privately owned: LV-613 and LV-612.</p>'''
    lightships_side = side_photo(
        "assets/images/pg2_lv112a.jpg",
        "<em>LV-112</em>: Original structure, prior to receiving major damage caused by Hurricane Edna while on station on 9/14/54 (when the bridge was rebuilt, fewer port holes were installed). During Hurricane Edna in 70 ft seas and 110 mph winds, bow plates were damaged, the bridge and pilot house stove in, small boats demolished and the rudder severely damaged; minor injuries to several crew members. (USCG photo &mdash; courtesy of Bernie Webber)",
        "LV-112 original structure prior to Hurricane Edna damage") + "\n" + DONATE_CARD
    page("current-lightships.html", "Current U.S. Lightship Museums",
         "A directory of the surviving U.S. lightship museums open to the public, including LV-112 in Boston.",
         "lv112",
         page_head("LV-112", "Current U.S. Lightship Museums", "Current U.S. Lightship Museums") + two_col(lightships, lightships_side))

    # ---- Crew quotes ----
    crew = '''            <h2>Crew Quotes</h2>
            <h3>Accounts of duty from <em>LV-112</em> crew members</h3>
            <p>Below are accounts of duty on the <em>Nantucket Lightship LV-112</em> from former crew members. Normal duty on the <em>112</em> and most other isolated stations would be three weeks on and then two weeks off. The crew was split into thirds, with crews overlapping. The only time the three weeks on duty were extended was due to weather. (The returning crew had to literally jump from the &lsquo;tender&rsquo; to the lightship via a jacobs ladder as they came along side. The ship's stores would need to be replenished more often than 6-8 weeks, normally at least every two weeks.)</p>
            <p>Twenty-one former <em>LV-112</em> crew members live in different parts of the country. <a href="http://www.uscglightshipsailors.org/crossed_the_bar/webber/" target="_blank" rel="noopener">Bernie Webber</a>, who served on <em>LV-112</em> from 1958&ndash;60 was awarded the Gold Life Saving Medal for his involvement in the oil tanker Pendleton disaster that occurred off Cape Cod's Monomoy Island (&ldquo;A true USCG hero,&rdquo; said Larry Ryan, President, USCG LSA, USCG Lightship veteran, 1960&ndash;61). Unfortunately, Mr. Webber recently and unexpectedly passed away in January of this year. He was very helpful and involved with the <em>LV-112</em> rescue and preservation effort.</p>
            <p>Several of the former crew members who served on <em>LV-112</em> as engineers, electricians and deckhands have offered to volunteer their time as part of a riding crew when the ship is relocated to its home port.</p>

            <h3>Bernie Webber</h3>
            <blockquote>
              <p>&ldquo;I was stationed aboard LV112/WAL534 Nantucket/Relief 1958-59-60 as Chief Executive Petty Officer. Let me say this it was the best coast guard duty I had. I'm taking the photo of the crew (see <a href="gallery.html">LV-112 Photo Gallery</a>) so I'm not in it. The Lightship at the time being steam powered had the largest crew of any Lightship and ratings like Machinest Mates that the other Lightships didn't have.&rdquo;</p>
              <p>&ldquo;The Nantucket Station was 100 miles offshore from Woods Hole MA-45 miles SE of Nantucket Island at the time and was the easternmost Navigational Aid all shipping would make Nantucket Station before branching off to New York etc. However the Station was in various locations during its history. As a Relief Lightship it relieved stations from Portland Maine to Brenton Reef Rhode Island and was at the entrance to the harbors or right in the shipping channels.&rdquo;</p>
              <p>&ldquo;Having spent some 45 yrs on the water it's difficult to think in terms of most pleasurable or terrifying. However, on LV112/Wal535 Nantucket/Relief my most pleasurable was the day when the Captain Robert J.W. Collins received a message while we were on Nantucket Station (100 miles off-shore from Woods Hole, MA) that we were being relieved and brought in to become a Relief Lightship. The only terror I felt was when on Nantucket Station in rough foggy weather a Radar Target would be observed headed directly towards the Lightship as it got close you could hear its engines and soon out of the fog so close you could spit on it would come one of the great liners sailing the seas at the time like the S.S. United States or S.S. France etc.&rdquo;</p>
              <p>&mdash; Bernard Webber, former LV-112 crew member, 1958-1960</p>
            </blockquote>

            <h3>Bob Gubitosi</h3>
            <blockquote>
              <p>&ldquo;I went aboard <em>Light Vessel #112</em> on a foggy day in 1957. I was 17 years old and saw this big red ship with 'Nantucket' painted on it anchored in the calm sea belching out the most ear-piercing foghorn I have ever heard. I think it was then that I realized that my life was about to change. I was the ship's new cook and had to feed 15 men aboard this ship, and I just came from commissarymen school at Groton, Connecticut, where they taught me to feed about a thousand. This was a terrifying experience at that time. I was on the <em>112</em> until 1961. I could not get a transfer and had four different skippers during my tour. There were many storms and hurricanes. One scary night was in, I believe 1958, when we broke our anchor chain and did not know it. We wound up off the coast of New Jersey the next day with our radio beacon still going. I remember going on the bridge that night and watching the ship through the porthole going up walls of water that looked like five- to ten-story buildings high, then taking a nose dive straight down. The most pleasurable time was when the mail came, the few calm summer days without the fog horn, the fishing, watching the aurora borealis and the sea life.&rdquo;</p>
              <p>&mdash; Bob Gubitosi, 2nd VP, USCG LSA, <em>LV-112</em> Commissaryman (ship's cook) 1957&ndash;61</p>
            </blockquote>

            <h3>Rich Racicott</h3>
            <blockquote>
              <p>&ldquo;During one nor'easter, I remember the skipper and I were on the bridge watching the anemometer. It was marked 0 to 100, but gusts were pushing the needle into the space above 100 and against the pin on the dial. We joked about it for a while and then it dropped to zero and moments later we heard a crash. Seems that the anemometer blew off the yardarm, must have bounced once somewhere on the deck then disappeared over the side. We never found it.&rdquo;</p>
              <p>&mdash; Rich Racicott, crew member <em>LV-112</em>, 1964-66</p>
            </blockquote>

            <h3>Peter Brunk</h3>
            <blockquote>
              <p>&ldquo;The worst thing that happened was going through a bad storm the first week of March 1971. My father died on March 7, and they couldn't get me off the ship for over a week. We left Boston on the 6th and storm warnings were up. When we got to station, the Relief Lightship didn't leave for almost a week, so we had two lightships on Nantucket station. The wind blew at over 100 mph for a week. Another interesting event happened in April or May 1970. An American submarine hit the ship with what we think was a dummy torpedo. We were on the corner of the New London sub-operating area, and they were around us a lot.&rdquo;</p>
              <p>&mdash; Peter Brunk, Commanding Officer, <em>LV-112</em>, 1970&ndash;71</p>
            </blockquote>'''
    crew_side = side_photo(
        "assets/images/pg2_nantucket_shoals_storm.jpg",
        "<em>LV-112</em>, on Nantucket Shoals station during a storm at sea with a wave breaking over the stern section. Photo taken from another vessel, prior to 1960. (Photo courtesy of Don Yeskoo)",
        "LV-112 in a storm with a wave breaking over the stern") + "\n" + DONATE_CARD
    page("crew-quotes.html", "Crew Quotes",
         "First-hand accounts of duty aboard Nantucket Lightship LV-112 from the U.S. Coast Guard sailors who served on her.",
         "lv112",
         page_head("LV-112", "Crew Quotes", "Crew Quotes") + two_col(crew, crew_side))

    # ---- Visiting hours ----
    visiting = '''            <h2>Visiting <em>Nantucket Lightship / LV-112</em></h2>
            <p><em>Nantucket / LV-112</em> is currently undergoing restoration. During this time period, the ship is open to the general public for tours, educational programs and special events on a limited basis. We look forward to your visit.</p>
            <h3>Location and Directions</h3>
            <p><em>Nantucket / LV-112</em> is berthed at the Boston Harbor Shipyard &amp; Marina, 256 Marginal St., East Boston, MA, <a href="https://goo.gl/maps/Dgxsv24qcc32" target="_blank" rel="noopener">directions</a>. MBTA subway: take the Blue Line to Maverick Station, walk to the shipyard/marina (approx. 15 minutes), <a href="https://goo.gl/maps/zndRAx9DYxL2" target="_blank" rel="noopener">view walking route</a>.</p>
            <h3>Our hours</h3>
            <p><em>Nantucket Lightship / LV-112</em> is open for the season on Saturdays, 10am&ndash;4pm, from the last Saturday in April through the last Saturday in October. Individual and group tours can also be arranged by appointment throughout the year on other days.</p>
            <h3>Admission</h3>
            <p>We request a $5 donation per person. Children under age 5 are free. <em>Nantucket / LV-112</em> is not handicap accessible.</p>
            <h3>More information</h3>
            <p>Please call <a href="tel:+16177970135">617.797.0135</a> or send an email to <a href="mailto:rmmjr2@comcast.net">rmmjr2@comcast.net</a>.</p>'''
    visiting_side = side_photo(
        "assets/images/lightship_boston.jpg",
        "<em>LV-112</em>, at the Boston Harbor Shipyard &amp; Marina.",
        "LV-112 at the Boston Harbor Shipyard and Marina") + "\n" + DONATE_CARD
    page("visiting-hours.html", "Visiting Hours",
         "Visit Nantucket Lightship / LV-112 at the Boston Harbor Shipyard & Marina in East Boston. Hours, directions, and admission information.",
         "lv112",
         page_head("LV-112", "Visiting Hours", "Visiting Hours") + two_col(visiting, visiting_side))

    # ---- How to help ----
    help_body = '''            <h2 id="donate">How to Help</h2>
            <p><img src="assets/images/visitors_children.jpg" alt="Visitors boarding LV-112 for a tour" class="img-right">Help us save <em>Nantucket Lightship / LV-112</em>, a National Historic Landmark, and preserve her in perpetuity. <em>LV-112</em> is the world's most famous and largest U.S. lightship ever built.</p>
            <p>In this challenging economic climate, regarding charitable donations, every little bit helps&mdash;even if you can only donate $1.00, any amount you are able to contribute would be greatly appreciated. The United States Lightship Museum is a 501(c)3 non-profit organization. Charitable donations are tax-deductible to the full extent allowed by law. Your support and commitment to preserving one of America's most unique historic landmarks would also be valued. With your support, <em>LV-112</em> can continue to educate and serve future generations as an institution of lifelong learning. Preserving this United States Historic Landmark is an important part of our nation's heritage.</p>
            <p>You can forward your contribution electronically on our website using <strong>PayPal</strong>, or if you prefer, please make your check payable to <strong><em>USLM Nantucket / LV-112</em></strong> and mail it to: United States Lightship Museum, Inc., P.O. Box 454, Amesbury, MA 01913. Thank you!</p>
            <div class="callout">
              ''' + PAYPAL_FORM + '''
              <p class="donate-note" style="margin-top:.8rem;">All electronic donations are processed securely by PayPal.</p>
            </div>
            <p>Even though <em>Nantucket Lightship / LV-112</em> is a National Historic Landmark and National Treasure, the historic vessel's existence is still at risk. Approximately 50% of <em>LV-112's</em> restoration has been completed. However, there is still much more that needs to be accomplished in order to finish stabilizing the ship from further corrosive deterioration of the seawater environment. Our next primary goal is to restore <em>LV-112's</em> plumbing and heating systems (currently not operational). Once this has been accomplished we can schedule our planned educational programs for students and youth groups on a year-round basis. Your contributions will help us achieve our fundraising goals and save this precious National Treasure for everyone to learn from and enjoy.</p>
            <p>Corporate sponsorships of <em>LV-112</em>&rsquo;s restoration and preservation are also welcome. For more information, please <a href="mailto:rmmjr2@comcast.net">contact us</a>.</p>
            <p>Everyone who donates $25 or more will become an automatic member of the U.S. Lightship Museum, receive membership privileges to other Council of American Maritime Museums (CAMM) members and the USLM periodic eNews newsletter via email.</p>
            <div class="btn-row">
              <a class="btn btn-outline" href="membership.html">Become a Member</a>
              <a class="btn btn-outline" href="volunteer.html">Volunteer</a>
            </div>'''
    help_side = side_photo(
        "assets/images/pg2_at_helm.jpg",
        "A volunteer at the helm of <em>LV-112</em>, while underway (c. 1990 &mdash; Photo courtesy of Don Yeskoo).",
        "A volunteer at the helm of LV-112 while underway") + "\n" + '''            <div class="side-card donate-card">
              <h3>Make a gift today</h3>
              <p>Every dollar helps preserve a National Historic Landmark for future generations.</p>
              ''' + PAYPAL_FORM + '''
            </div>'''
    page("how-to-help.html", "How to Help",
         "Donate to help save and preserve Nantucket Lightship / LV-112, a National Historic Landmark. Give securely online via PayPal or by mail.",
         "help",
         page_head("How to Help", "How to Help", "How to Help") + two_col(help_body, help_side))

    # ---- Volunteer ----
    volunteer = '''            <h2>Volunteer Information</h2>
            <figure class="figure">
              <img src="assets/images/volunteer_group.jpg" alt="Volunteers helping with LV-112's pre-tow projects in Oyster Bay">
              <figcaption>Volunteers that helped with <em>LV-112's</em> pre-tow projects in Oyster Bay, Long Island, NY during a bitterly cold January 2010 weekend. Many of the volunteers were from the Lightship Sailors Association, flew in from all parts of the U.S. and were former <em>LV-112</em> U.S. Coast Guard crew members. Also present is the regular crew of local volunteers from the Oyster Bay area.</figcaption>
            </figure>
            <h3>Become a volunteer</h3>
            <p><img src="assets/images/volunteers_securing_lv-112.jpg" alt="Volunteers securing LV-112's dock lines" class="img-right">The United States Lightship Museum is looking for volunteers who are passionate and committed to preserving historic properties and artifacts. As a volunteer, you will be involved in helping to restore and preserve one of our nation&rsquo;s most unique maritime treasures &mdash; <em>Nantucket Lightship / LV-112</em>, a designated National Historic Landmark. Moreover, you will meet a group of people who share your interests and commitment to historic preservation. In addition, the <em>LV-112</em> Preservation Project will provide an exceptional teaching and learning environment &mdash; a floating learning center. We are looking for individuals willing to volunteer their time in the following areas:</p>
            <ul>
              <li>Administration</li>
              <li>Mechanical repair (marine diesel engines, air compressors, electrical generators, etc.)</li>
              <li>Welding / metal fabrication</li>
              <li>Plumbing / heating</li>
              <li>Preparation and paint (all phases of metal prep, sandblasting, etc.)</li>
              <li>Tour guides</li>
              <li>Research</li>
              <li>Writing and editing (website / newsletter)</li>
              <li>Desktop publishing (Mac)</li>
              <li>Photography / videography</li>
              <li>Grant writing</li>
              <li>Marine electrical systems</li>
              <li>General miscellaneous duties</li>
            </ul>
            <figure class="figure">
              <img src="assets/images/volunteer_pre-tow_lunch.jpg" alt="Volunteers break for lunch in LV-112's galley">
              <figcaption>The January weekend volunteers breaking for lunch, enjoying hearty, hot, homemade soup and fish chowder with all the fixings in <em>LV-112's</em> heated galley.</figcaption>
            </figure>
            <p>The United States Lightship Museum is composed entirely of volunteers who include former U.S. Coast Guard lightship veterans, maritime historians and enthusiasts. Moreover, we are looking for anyone who has an interest and passion for maritime history.</p>
            <div class="callout">
              <p><strong>Please download the <a href="assets/pdf/lv112_volunteer_form2013.pdf" target="_blank" rel="noopener">printable volunteer form</a> and mail it to: United States Lightship Museum, P.O. Box 454, Amesbury, MA 01913.</strong></p>
            </div>'''
    volunteer_side = side_photo(
        "assets/images/pg2_volunteer.jpg",
        "A volunteer during January 2010, getting ready to board <em>LV-112</em> and join the others to prepare the ship for its tow to its new home port of Boston.",
        "A volunteer preparing to board LV-112 in January 2010") + "\n" + DONATE_CARD
    page("volunteer.html", "Volunteer",
         "Volunteer with the United States Lightship Museum to help restore and preserve Nantucket Lightship / LV-112.",
         "help",
         page_head("How to Help", "Volunteer", "Volunteer") + two_col(volunteer, volunteer_side))

    # ---- Supporters ----
    supporters = '''            <h2>Our Supporters</h2>
            <p>The United States Lightship Museum is extremely grateful for the generosity of the following donors who have contributed to the Museum and the restoration and preservation of <em>Nantucket Lightship / LV-112</em>, a National Historic Landmark and important part of our nation's maritime history. We are also very thankful to all the individual USLM members and donors who have contributed to our cause.</p>
            <ul>
              <li>Cameron International Corporation / Houston, Texas</li>
              <li>The Lenfest Foundation</li>
              <li>National Trust for Historic Preservation</li>
              <li>Boston Harbor Shipyard &amp; Marina</li>
              <li>Capt. Robertson Dinsmore Charitable Fund</li>
              <li>New England Lighthouse Lovers / Chapter &mdash; American Lighthouse Foundation</li>
              <li>Crandell Dry Dock Engineers, Inc.</li>
              <li>J. Hewitt Marine Electrical Services</li>
              <li>Bluefin Robotics Corporation</li>
              <li>West Marine</li>
              <li>Foss Maritime</li>
              <li>U.S. Coast Guard Lightship Sailors Association, International</li>
              <li>Donahue, Tucker &amp; Ciandella, PLLC</li>
              <li>T &amp; M Services</li>
              <li>Town of Oyster Bay, New York</li>
              <li>Bluejacket Shipcrafters, Inc., Searsport, Maine</li>
              <li>Amex Industrial Services, Inc.</li>
              <li>Fitzgerald Shipyard</li>
              <li>Eastern Bank</li>
              <li>Sherwin-Williams</li>
            </ul>'''
    supporters_side = side_photo(
        "assets/images/nell_112.jpg",
        "Members of the New England Lighthouse Lovers (NELL) on board LV-112 on a cold mid-winter day, present a check for $3,000 to the United States Lightship Museum's Nantucket / LV-112 restoration project. NELL's donation will be directed to the restoration of LV-112's radio beacon control room.",
        "Members of NELL presenting a check aboard LV-112") + "\n" + DONATE_CARD
    page("supporters.html", "Our Supporters",
         "The United States Lightship Museum gratefully acknowledges the donors and organizations supporting the restoration of Nantucket Lightship / LV-112.",
         "help",
         page_head("How to Help", "Our Supporters", "Our Supporters") + two_col(supporters, supporters_side))

    # ---- Vehicle donation ----
    vehicle = '''            <h2>Support <em>Nantucket / LV-112</em> by Donating a Vehicle</h2>
            <p><img src="assets/images/car_junky.jpg" alt="Junk car to donate" class="img-right">Considering selling or trading in your old or collectible car, truck, or even a boat or camper? Give it new life by donating it to our museum. Our national car donation program is a hassle-free way of putting your used vehicle to work, supporting our efforts to preserve <em>Nantucket Lightship / LV-112</em> as a floating learning center. Plus, you may be eligible to receive a tax deduction.</p>
            <h3>How it works</h3>
            <p><img src="assets/images/car_flying_cloud.jpg" alt="Donate your car" class="img-left">We have teamed with Charitable Auto Resources, Inc. (CARS) to accept vehicle donations across the U.S. Once you contact our customer service representative about making the donation, everything will be taken care of, including a receipt for your tax records. Sale proceeds will be donated to the USLM in your name. If the car sells for less than $500, the receipt provided when the car is towed away will serve as your tax receipt. If the car sells for $500 or more, you will receive a 1098-C form for tax purposes. Donating your car to the U.S. Lightship Museum (USLM) is as easy as calling our representative toll-free at <a href="tel:+18555007433">855-500-7433</a>, or visit the website by <a href="http://www.careasy.org/details?2864" target="_blank" rel="noopener">clicking here</a>.</p>'''
    vehicle_side = side_photo(
        "assets/images/lv112_restored2016.jpg",
        "<em>Nantucket Lightship / LV-112</em>, restored.",
        "Nantucket Lightship LV-112 restored") + "\n" + DONATE_CARD
    page("vehicle-donation.html", "Vehicle Donation Program",
         "Donate a car, truck, boat or camper to support Nantucket Lightship / LV-112. A hassle-free, tax-deductible way to help the United States Lightship Museum.",
         "help",
         page_head("How to Help", "Vehicle Donation Program", "Vehicle Donation Program") + two_col(vehicle, vehicle_side))

    # ---- Contact ----
    contact = '''            <h2>Contact Us</h2>
            <p>For more information about <em>Nantucket / LV-112</em>, or if you have any questions in regard to visiting <em>LV-112</em>, please contact us via <a href="mailto:rmmjr2@comcast.net">email</a>. Your comments and suggestions are also welcomed. Thank you.</p>
            <div class="callout">
              <p><strong>United States Lightship Museum, Inc.</strong><br>
              Phone: <a href="tel:+16177970135">617.797.0135</a><br>
              Email: <a href="mailto:rmmjr2@comcast.net">rmmjr2@comcast.net</a></p>
              <p><strong>Berthed at:</strong> Boston Harbor Shipyard &amp; Marina, 256 Marginal St., East Boston, MA<br>
              <strong>Mailing address:</strong> P.O. Box 454, Amesbury, MA 01913</p>
            </div>'''
    contact_side = side_photo(
        "assets/images/pg2_radio_room.jpg",
        "Radio Room, LS-112, 1936; Photo No. 214, 1936; photographer unknown. (Courtesy of USCG)",
        "Radio Room of LS-112 in 1936") + "\n" + DONATE_CARD
    page("contact.html", "Contact Us",
         "Contact the United States Lightship Museum for information about visiting or supporting Nantucket Lightship / LV-112.",
         "contact",
         page_head("Contact", "Contact Us", "Contact Us") + two_col(contact, contact_side))

    # ---- Newsletter ----
    newsletters = [
        ("https://conta.cc/4sJGskH", "Spring 2026 eNews"),
        ("https://conta.cc/4iRVzEn", "USLM Annual Appeal 2025"),
        ("https://conta.cc/3IluATX", "Fall 2025 eNews"),
        ("https://conta.cc/4jMjjsk", "Summer 2025 eNews"),
        ("https://conta.cc/42wA3xq", "Spring 2025 eNews"),
        ("https://conta.cc/4iG2DDO", "December 2024 eNews Special Edition"),
        ("https://conta.cc/4hGUcaQ", "Fall 2024 eNews"),
        ("https://conta.cc/4faTAJ4", "'Celebrating Lifesavers at Sea' July 24-26"),
        ("https://conta.cc/4bKuBJD", "Invitation to July 24-26 Events"),
        ("https://conta.cc/3KV8pBR", "Celebrate Boston Harbor Fireworks"),
        ("https://conta.cc/3XcKdCk", "2024 USLM Summer Activities"),
        ("https://conta.cc/3VwMuH6", "'Celebrating Lifesavers at Sea' 2024"),
        ("https://conta.cc/4auuG46", "Spring 2024 eNews"),
        ("https://conta.cc/3TtqbSa", "USLM Annual Appeal 2023"),
        ("https://conta.cc/45f8nMR", "Fall 2023 eNews"),
        ("https://conta.cc/3IUzNPB", "USLM Summer Activities 2023"),
        ("https://conta.cc/42dEe0d", "Spring 2023 eNews"),
        ("https://conta.cc/3I9CMEd", "USLM Annual Appeal 2022"),
        ("https://conta.cc/3T7VXQT", "Fall 2022 eNews"),
        ("https://conta.cc/3xb6MJ0", "'Kids in Boating Day' | Fireworks 2022"),
        ("https://conta.cc/3lilCHS", "eNews Special Edition 2022"),
        ("https://conta.cc/3y3ZTer", "Spring 2022 eNews"),
        ("https://conta.cc/3FvdhJv", "USLM Annual Appeal 2021"),
        ("https://conta.cc/30MM2Lq", "Winter 2021 eNews"),
        ("https://conta.cc/2WL2n17", "Summer 2021 eNews"),
        ("https://conta.cc/3tW9rm3", "eNews Special Edition 2021"),
        ("https://conta.cc/3vxRnQw", "Spring 2021 Newsletter"),
        ("https://conta.cc/2KNbqsp", "USLM Annual Appeal 2020"),
        ("https://conta.cc/3mHZLcf", "Fall 2020 Newsletter"),
        ("https://conta.cc/2DKal0Y", "Summer 2020 Newsletter"),
        ("https://conta.cc/2SvXxPN", "Spring 2020 Newsletter"),
        ("https://conta.cc/39hMy3e", "USLM Annual Appeal 2019"),
        ("https://conta.cc/2Dr99M3", "November 2019 Newsletter"),
        ("https://conta.cc/2XMvsVi", "Boston Harbor Fireworks: June 30, 2019 Newsletter"),
        ("https://conta.cc/2JGRplU", "March 2019 Newsletter"),
        ("https://conta.cc/2EU3Cjg", "USLM Annual Appeal 2018"),
        ("https://conta.cc/2Eqj8no", "December 2018 Newsletter"),
        ("https://conta.cc/2vgcs59", "August 2018 Newsletter"),
        ("https://conta.cc/2KKBA9W", "Summer 2018 Newsletter"),
        ("https://conta.cc/2JGsElj", "Boston Harbor Fireworks: June 30, 2018 Newsletter"),
        ("https://conta.cc/2HKgw2Z", "Spring 2018 Newsletter"),
        ("http://conta.cc/2qqxbDe", "2017 End of Year eNews"),
        ("http://conta.cc/2Ga4TRr", "Preservation matters! December eNews"),
        ("http://conta.cc/2qtcpDh", "Fall 2017 Newsletter"),
        ("http://conta.cc/2i0iK4F", "Boston Harbor Labor Day Fireworks 2017 Newsletter"),
        ("http://conta.cc/2eKtRxj", "Summer 2017 Newsletter"),
        ("http://conta.cc/2obYiQ0", "Spring 2017 Newsletter"),
        ("http://conta.cc/2ia7Okp", "Winter 2016 Newsletter"),
        ("http://conta.cc/2eV0qrs", "Fall 2016 Newsletter"),
        ("http://conta.cc/2bDDl8w", "Boston Harbor Labor Day Fireworks 2016 Newsletter"),
        ("http://conta.cc/29SM2cf", "Beacon Relighting 2016 Newsletter"),
        ("http://conta.cc/28VZNpS", "Harborfest Fireworks 2016 Newsletter"),
        ("http://conta.cc/1qQLFre", "Spring 2016 Newsletter"),
        ("http://conta.cc/1Uf28hz", "Winter 2015 Newsletter"),
        ("http://conta.cc/1Qg6mWF", "October 2015 Newsletter"),
        ("http://conta.cc/1Jsw8nV", "July 2015 Special Edition"),
        ("http://conta.cc/1RSdPJ5", "July 2015 Newsletter"),
        ("http://conta.cc/1EvXyX0", "February 2015 Newsletter"),
    ]
    nl_items = "\n".join(
        f'              <li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for u, t in newsletters
    )
    newsletter_body = f'''            <h2>Newsletter</h2>
            <p>Read the latest news from the United States Lightship Museum. Our periodic eNews keeps members and friends up to date on restoration progress, events and ways to help. Links open in a new tab.</p>
            <ul class="link-list">
{nl_items}
            </ul>'''
    newsletter_side = side_photo(
        "assets/images/ss_unitedstates_c1955.jpg",
        "<em>LV-112</em> (c. 1955) on Nantucket Lightship Station. The <em>SS United States</em> passes by, heading to New York City Harbor from Europe.",
        "LV-112 with the SS United States passing by, c.1955") + "\n" + '''            <div class="side-card">
              <div class="side-body">
                <h3><em>Nantucket Lightship / LV-112</em> eNews</h3>
                <p>Our periodic eNews keeps members and friends up to date on restoration progress, events, and ways to help.</p>
                <p>Sign up for our eNews by emailing <a href="mailto:rmmjr2@comcast.net">rmmjr2@comcast.net</a>.</p>
              </div>
            </div>''' + "\n" + DONATE_CARD
    page("newsletter.html", "Newsletter",
         "Read the United States Lightship Museum's eNews and newsletter archive with restoration updates, events, and news about Nantucket Lightship / LV-112.",
         "newsletter",
         page_head("Newsletter", "Newsletter", "Newsletter") + two_col(newsletter_body, newsletter_side))

    # ---- Membership ----
    tiers = [
        ("Individual", "$25", "Includes basic membership privileges."),
        ("Family", "$35", "Includes basic membership privileges plus two adults and their children."),
        ("Friend", "$50", "Includes family membership privileges plus two guest admissions."),
        ("Patron", "$75", "Includes family membership privileges plus 4 guest admissions."),
        ("Partner", "$150", "Includes family membership privileges plus 6 guest admissions."),
        ("Corporate", "$250", "Includes basic membership privileges plus 8 guest admissions, and a one-time use of <em>Nantucket / LV-112</em> for a private function for up to 25 guests."),
        ("Benefactor", "$500", "Includes family membership privileges plus 10 guest admissions, a private tour and a one-time use of <em>Nantucket / LV-112</em> for a private function for up to 35 guests."),
        ("Lifetime Membership", "$1,000", "Includes family membership privileges plus 12 guest admissions, a private tour, and a two-time use of <em>Nantucket / LV-112</em> for a private function up to 50 guests."),
    ]
    tier_html = "\n".join(
        f'''              <div class="tier">
                <span class="tname">{n}</span>
                <span class="price">{p}</span>
                <p>{d}</p>
              </div>''' for n, p, d in tiers
    )
    membership = f'''            <h2>Museum Membership</h2>
            <p class="lead">A USLM membership will help us fund <em>Nantucket / LV-112's</em> historic restoration and preservation.</p>
            <p>When you become a member of the United States Lightship Museum (USLM), you will be helping to rescue and preserve <em>Nantucket Lightship / LV-112</em>, a National Historic Landmark and precious national treasure that is an important part of our nation&rsquo;s maritime heritage and culture. Plus you will have the satisfaction of knowing you are a contributing partner in the legacy of the world&rsquo;s most famous and largest U.S. lightship ever built!</p>
            <p>The United States Lightship Museum (USLM) is a 501(c)3 non-profit organization entirely composed of volunteers who include former U.S. Coast Guard lightship veterans, maritime historians and enthusiasts. Anyone who has an interest and passion for maritime history is welcome to participate. Join today!</p>
            <h3>Rescuing a National Historic Landmark and National Treasure</h3>
            <p><img src="assets/images/volunteers_wheel.jpg" alt="Volunteers at the wheel of LV-112" class="img-right">In 2008, after nearly seven years of neglect, while berthed at Oyster Bay, Long Island NY, <em>LV-112</em> was in danger of being scrapped. A group of preservation-minded individuals formed a nonprofit organization &mdash; the United States Lightship Museum (USLM) &mdash; to rescue and restore <em>Nantucket / LV-112</em>. The USLM purchased <em>LV-112</em> for one dollar in October 2009 and transported the historic ship back to its home port of Boston in May 2010.</p>
            <p><em>Nantucket / LV-112</em> was considered state-of-the-art when built, exclusively designed to be unsinkable and to withstand the treacherous conditions of Nantucket Shoals Lightship Station, where it served for 39 years. As a 501(c)3 nonprofit group, the United States Lightship Museum (USLM) was exclusively established to rescue <em>LV-112</em> from being destroyed. The USLM&rsquo;s mission is to restore and reopen it as a museum and floating learning center. In 2010, the USLM brought the historic ship back to its original home port of Boston from Oyster Bay, Long Island, NY, after it was neglected and virtually abandoned for several years. So far, the USLM has restored approximately 50% of the ship and in 2010 reopened it as a museum and floating learning center. <em>LV-112</em> is berthed at the Boston Harbor Shipyard &amp; Marina on the East Boston waterfront.</p>
            <p><img src="assets/images/volunteer_ladder.jpg" alt="Volunteer working on LV-112's ladder" class="img-left"><em>LV-112</em> is bound by a covenant and can only be utilized as a museum and floating learning center open to the general public. The ship is currently undergoing a multi-phase restoration and is open to the general public on Saturdays, 10&ndash;4 (April &ndash; Oct.). Tours for individuals/groups and private events can be arranged by appointment on all other days. For more information call <a href="tel:+16177970135">617.797.0135</a> or email <a href="mailto:rmmjr2@comcast.net">rmmjr2@comcast.net</a>.</p>
            <div class="callout">
              <p><strong>Experience what shipboard life was like on LV-112! To join, please download the <a href="assets/pdf/USLM_Membership_Form_2025a.pdf" target="_blank" rel="noopener">printable Membership form</a>.</strong> When downloaded to your computer, the form can be filled out electronically, printed and mailed in with your payment to: USLM / Nantucket LV-112. You can also pay electronically via PayPal (please include mailing address) by clicking the &ldquo;Donate&rdquo; button on the homepage or <a href="how-to-help.html#donate">How to Help</a> page. Thank you!</p>
            </div>
            <h3>Basic Museum Membership</h3>
            <p>Includes a Museum Membership Card, free unlimited admission, subscription to the Museum Quarterly newsletter, and invitations and discounts to museum programs and members-only events. The USLM is a member of the Council of American Maritime Museums (<a href="http://www.councilofamericanmaritimemuseums.org/" target="_blank" rel="noopener">CAMM</a>) and the Historic Naval Ships Association (<a href="http://www.hnsa.org/index.htm" target="_blank" rel="noopener">HNSA</a>). USLM members will be granted reciprocal privileges (free admission) at participating <a href="https://councilofamericanmaritimemuseums.org/member-directory/" target="_blank" rel="noopener">CAMM</a> institutions.</p>
            <hr class="rule">
            <h3>Membership Levels</h3>
            <div class="tiers">
{tier_html}
            </div>
            <h3>Private shipboard functions for USLM members</h3>
            <p>Members who have private function privileges must schedule them in advance with the museum and are subject to availability on a first-come, first-served basis. Members who do not have private function privileges can donate to the USLM separately for use of the ship for a private function. Private functions are limited to 4 hours on board <em>LV-112</em>. To request more information, please contact <a href="tel:+16177970135">617.797.0135</a> or <a href="mailto:rmmjr2@comcast.net">rmmjr2@comcast.net</a>.</p>'''
    membership_side = side_photo(
        "assets/images/pg2_statue_liberty.jpg",
        "<em>LV-112</em>, at the Statue of Liberty re-dedication, 1986.",
        "LV-112 at the Statue of Liberty re-dedication in 1986") + "\n" + '''            <div class="side-card">
              <div class="side-body">
                <h3>Members of</h3>
                <p class="side-caption"><a href="http://www.councilofamericanmaritimemuseums.org/" target="_blank" rel="noopener">Council of American Maritime Museums (CAMM)</a><br>
                <a href="http://www.hnsa.org/index.htm" target="_blank" rel="noopener">Historic Naval Ships Association (HNSA)</a></p>
              </div>
            </div>''' + "\n" + DONATE_CARD
    page("membership.html", "Membership",
         "Become a member of the United States Lightship Museum and help fund the restoration of Nantucket Lightship / LV-112. Membership levels from $25.",
         "membership",
         page_head("Membership", "Museum Membership", "Membership") + two_col(membership, membership_side))

    # ---- News ----
    news_body = '''            <h2>News</h2>
            <ul class="link-list">
              <li><a href="#nationaltreasure">Nantucket Lightship / LV-112 selected as National Treasure</a></li>
              <li><a href="#channel5">Nantucket / LV-112 featured on television</a></li>
              <li><a href="#powerships">LV-112 featured in issue of &ldquo;PowerShips&rdquo; magazine</a></li>
              <li><a href="#boston">Nantucket / LV-112 moves back home to Boston</a></li>
              <li><a href="#seahistory">LV-112 featured in &ldquo;Sea History&rdquo; magazine</a></li>
              <li><a href="#model">LV-112 model kit available</a></li>
              <li><a href="#finesthours">New book release &mdash; &ldquo;The Finest Hours&rdquo;</a></li>
              <li><a href="#enemy">Recommended reading &mdash; &ldquo;Due to Enemy Action&rdquo;</a></li>
              <li><a href="#webber">Former LV-112 life saving hero celebrated</a></li>
              <li><a href="#coverage">In the news &amp; further reading</a></li>
            </ul>
            <hr class="rule">

            <h3 id="nationaltreasure">Nantucket Lightship / LV-112 selected as National Treasure</h3>
            <p><strong>National Treasures</strong> &mdash; <em>People Saving Places</em> (National Trust for Historic Preservation). In 2012, <em><a href="assets/pdf/LV-112_NTHP_national_treasure_1.pdf" target="_blank" rel="noopener">Nantucket Lightship / LV-112</a></em> was designated a <a href="https://savingplaces.org/places/nantucket-lightship-lv-112" target="_blank" rel="noopener">National Treasure</a> (one of 32 historic sites in the United States) by the <a href="https://savingplaces.org/places/nantucket-lightship-lv-112" target="_blank" rel="noopener">National Trust for Historic Preservation</a>.</p>
            <p>National Treasures are historic places that tell the American story &mdash; and they need your help. From beloved schoolhouses to inspiring monuments, from ancient sites to modern masterpieces, thousands of these icons are endangered as never before. Join our National Treasures campaign and help us save these irreplaceable gems. Learn more about <a href="https://savingplaces.org/places/nantucket-lightship-lv-112" target="_blank" rel="noopener">National Treasures</a>.</p>

            <h3 id="channel5">Nantucket / LV-112 featured on television</h3>
            <p>Once again, <em>Nantucket / LV-112</em> was a featured segment on ABC-TV Boston affiliate WCVB Channel 5 Boston&rsquo;s <em>Chronicle HD</em> (2012). Chronicle airs at 7:30 pm Monday through Friday and mostly features stories about New England events and places. <em>LV-112</em> was included in a segment about the City of Chelsea, Massachusetts. A section of Chelsea is on the Boston Harbor waterfront and is home to the historic Fitzgerald Shipyard. <em>LV-112</em> is shown in dry-dock at the shipyard, undergoing its first major phase of restoration. In addition, <em>LV-112's</em> home port was the United States Light House Service (USLHS), Second District Depot from 1936&ndash;1939. The USLHS merged with the U.S. Coast Guard (USCG) in 1939. Boston was the USCG's First District Headquarters. <em>Nantucket / LV-112</em> always operated out of Chelsea / Boston from 1936 until she was decommissioned in 1975.</p>
            <p>In 2010/2011, <em>Nantucket / LV-112</em> was a featured segment on ABC-TV Boston affiliate WCVB's <em>Chronicle HD</em>. <em>LV-112</em> was included in a segment about the Boston &ldquo;Harborwalk,&rdquo; where the city meets the sea, and is open to all: 39 miles of waterfront access that can be explored by foot and other transportation alternatives.</p>

            <h3 id="powerships">LV-112 featured in issue of &ldquo;PowerShips&rdquo; magazine</h3>
            <p>The Steamship Historical Society of America publishes <em>PowerShips, The Magazine of Engine-Powered Vessels</em>. Launched in 1940 as <em>The Steamboat Bill of Facts</em>, this quarterly magazine has been published continuously for 71 years, without interruption. This 88-page magazine includes regional columns from across the United States and overseas, special columns on cruise ships, yachts and tugboats, reviews of newly published maritime books and much more. (Read the <a href="assets/pdf/powerships_nantucket_lightship.pdf" target="_blank" rel="noopener"><em>LV-112</em> feature</a>.)</p>

            <h3 id="boston">Nantucket / LV-112 moves back home to Boston</h3>
            <figure class="figure">
              <img src="assets/images/news/nantucket_tow.jpg" alt="Nantucket / LV-112 being towed to Boston">
              <figcaption>Photo: Courtesy of Ron Janard</figcaption>
            </figure>
            <p>After being stranded and virtually neglected at the public pier in Oyster Bay, Long Island, NY for eight years, <em>Nantucket / LV-112</em> was finally towed on May 10th by the tugboat <em>Lynx</em> to Boston Harbor. <em>LV-112</em> arrived on May 11, 2010, and was welcomed by former crewmembers, National Park Service personnel and the general public. The historic <em>LV-112</em> had not been back to Boston since the U.S. Coast Guard decommissioned her in 1975.</p>
            <p>The U.S. Lightship Museum (USLM &mdash; new owners of <em>LV-112</em>) is extremely grateful to everyone who helped with <em>LV-112's</em> transport / rescue and continues to assist with the ship's preservation. In addition, the USLM is especially thankful to the Town of Oyster Bay, NY and its residents for their patience and support. Contemporaneous coverage of the May 2010 tow, including photos of <em>LV-112</em> arriving in Boston, appeared on the maritime blog <a href="https://tugster.wordpress.com/2010/05/12/" target="_blank" rel="noopener">tugster</a>.</p>

            <h3 id="seahistory">LV-112 featured in &ldquo;Sea History&rdquo; magazine</h3>
            <p>Co-authored by Robert Mannino, Jr. and Donald Whitehead, <em>Nantucket Lightship / LV-112</em> is featured in the Spring 2009 issue of <em>Sea History</em> magazine (No. 126, National Maritime Historical Society). <em>Sea History</em> is published by the National Maritime Historical Society and is recognized as the pre-eminent journal of advocacy and education in its field. In addition, <em>Sea History</em> covers the world of maritime museums, sail training, art, literature, lore and learning of the sea with a national focus and an international scope.</p>

            <h3 id="model">LV-112 model kit available</h3>
            <p><img src="assets/images/news/nantucket_model.jpg" alt="Nantucket Lightship / LV-112 model kit" class="img-right">A <a href="https://www.bluejacketinc.com/shop/model-ships/kits-model-ships/power-vessels/nantucket/" target="_blank" rel="noopener"><em>Nantucket Lightship / LV-112</em> model kit</a> is available from Blue Jacket Shipcrafters in Searsport, Maine. Blue Jacket Shipcrafters is the oldest (since 1905) ship and boat modeling company in the United States, and every kit and ship model is built in Maine by their own craftsmen. The Blue Jacket kit shows <em>LV-112</em> as launched with a tall stack for her steam boiler, which was modified in 1960 when she was converted to diesel power. This is a dramatic and colorful model with many custom etched brass and Britannia fittings.</p>
            <p>Blue Jacket Shipcrafters offers many other replica model kits of famous sail and power vessels in addition to half-hull models, miscellaneous fittings, tools and books. For more information, log on to the Blue Jacket website at <a href="http://www.bluejacketinc.com" target="_blank" rel="noopener">www.bluejacketinc.com</a> or call 1-800-448-5567 to order a product catalog.</p>

            <h3 id="finesthours">New book release &mdash; &ldquo;The Finest Hours&rdquo;</h3>
            <p><em>The Finest Hours: The True Story of the U.S. Coast Guard&rsquo;s Most Daring Sea Rescue</em>, by Michael J. Tougias and Casey Sherman, tells the story of the rescue involving former <em>LV-112</em> crew member Bernie Webber.</p>
            <p>In the winter of 1952, New England was battered by the most brutal nor'easter in years. As the weather wreaked havoc on land, the freezing Atlantic became a wind-whipped zone of peril.</p>
            <p>In the early hours of Monday, February 18, while the storm raged, two oil tankers, the <em>Pendleton</em> and the <em>Fort Mercer</em>, found themselves in the same horrifying predicament. Built with &ldquo;dirty steel&rdquo; and not prepared to withstand such ferocious seas, both tankers split in two, leaving the dozens of men on board utterly at the Atlantic's mercy.</p>
            <p><em>The Finest Hours</em> is the gripping, true story of the valiant attempt to rescue the souls huddling inside the broken halves of the two ships. Coast Guard cutters raced to the aid of those on the <em>Fort Mercer</em>, and when it became apparent that the halves of the <em>Pendleton</em> were in danger of capsizing, the Guard sent out two thirty-six-foot lifeboats as well. These wooden boats, manned by only four seamen, were dwarfed by the enormous seventy-foot seas. As the tiny rescue vessels set out from the coast of Cape Cod, the men aboard were all fully aware that they were embarking on what could easily become a suicide mission.</p>
            <p>The spellbinding tale is overflowing with breathtaking scenes that sear themselves into the mind's eye, as boats capsize, bows and sterns crash into one another, and men hurl themselves into the raging sea in their terrifying battle for survival.</p>
            <p>Not all of the eighty-four men caught at sea in the midst of that brutal storm survived, but considering the odds, it's a miracle &mdash; and a testament to their bravery &mdash; that any came home to tell their tales at all.</p>
            <p>Michael J. Tougias and Casey Sherman have seamlessly woven together their extensive research and firsthand interviews to create an unforgettable tale of heroism, triumph and tragedy, one that truly tells of the Coast Guard's finest hours. The book inspired the 2016 Disney film <a href="https://en.wikipedia.org/wiki/The_Finest_Hours_(2016_film)" target="_blank" rel="noopener"><em>The Finest Hours</em></a>, dramatizing the rescue of the crew of the <a href="https://en.wikipedia.org/wiki/SS_Pendleton" target="_blank" rel="noopener">SS <em>Pendleton</em></a>.</p>
            <p><strong>Product details:</strong> Scribner, May 2009. Hardcover, 224 pages. ISBN-10: 1-4165-6721-6; ISBN-13: 978-1-4165-6721-9.</p>

            <h3 id="enemy">Recommended reading &mdash; &ldquo;Due to Enemy Action&rdquo;</h3>
            <p><em>Due to Enemy Action: The True World War II Story of the USS Eagle 56</em>, by Stephen Puleo, tells the story of <em>Nantucket / LV-112's</em> involvement with a German U-Boat attack off Portland, Maine, during WWII.</p>
            <p>It is the story of a small U.S. sub-chaser, the <em>Eagle 56</em>, caught in the crosshairs of a German U-boat, the <em>U-853</em>, whose brazen commander doomed his own crew in a desperate, last-ditch attempt to record final kills before his country's imminent defeat a few weeks later in May. And it is the account of how one man, Paul M. Lawton, embarked on an unrelenting quest for the truth and changed naval history.</p>

            <h3 id="webber">In Memoriam, Bernard C. Webber (USCG, Ret.)</h3>
            <p><img src="assets/images/news/bernie_webber3.jpg" alt="Bernard C. Webber" class="img-right">Mr. Webber (Bernie) suddenly and unexpectedly passed away in January 2009. He was considered &ldquo;A Real American Hero&rdquo; and served as a crew member on <em>Nantucket Lightship / LV-112</em>, 1958&ndash;1960. Bernie was awarded the coveted USCG Gold Lifesaving Medal for his heroism in what is considered by maritime historians to be <a href="http://www.cg36500.org/rescue.html" target="_blank" rel="noopener">&ldquo;The Greatest Small Boat Rescue in Coast Guard History.&rdquo;</a> You can <a href="http://www.cg36500.org/rescue_audio.html" target="_blank" rel="noopener">listen to the historic audio interview</a> of his harrowing rescue experience at sea. Mr. Webber, who was a member of the USCG Lightship Sailors Association, was very helpful in helping us compile research information and historic photos of <em>LV-112</em>. He was a pleasure and an honor to work with. We will miss him dearly.</p>

            <h3 id="coverage">In the news &amp; further reading</h3>
            <p>Selected coverage and references about <em>Nantucket / LV-112</em> and her history (external links open in a new tab):</p>
            <ul class="link-list">
              <li><a href="https://chelsearecord.com/2021/05/05/nantucket-lightship-returns-home-after-seven-months-in-chelsea-dry-dock/" target="_blank" rel="noopener">Chelsea Record &mdash; &ldquo;Nantucket Lightship Returns Home After Seven Months in Chelsea Dry Dock&rdquo; (2021)</a></li>
              <li><a href="https://www.lighthousedigest.com/Digest/StoryPage.cfm?StoryKey=7227" target="_blank" rel="noopener">Lighthouse Digest &mdash; &ldquo;Nantucket Lightship / LV-112 awarded &lsquo;Save America&rsquo;s Treasures&rsquo; grant&rdquo;</a></li>
              <li><a href="https://www.iampe.org/single-post/nantucket-lightship-lv-112" target="_blank" rel="noopener">IAMPE &mdash; &ldquo;Restored Nantucket Lightship LV-112 Open for Tours&rdquo;</a></li>
              <li><a href="https://savingplaces.org/places/nantucket-lightship-lv-112" target="_blank" rel="noopener">National Trust for Historic Preservation &mdash; Nantucket Lightship / LV-112</a></li>
              <li><a href="https://en.wikipedia.org/wiki/United_States_lightship_Nantucket_(LV-112)" target="_blank" rel="noopener">Wikipedia &mdash; United States lightship Nantucket (LV-112)</a></li>
            </ul>'''
    news_side = side_photo(
        "assets/images/news/pg2_lv112_roughseas.jpg",
        "<em>LV-112</em> on Nantucket Shoals station, prior to 1960.",
        "LV-112 on Nantucket Shoals station prior to 1960") + "\n" + DONATE_CARD
    page("news.html", "News",
         "News and milestones for Nantucket Lightship / LV-112: National Treasure designation, television and magazine features, book releases, and remembrances.",
         "lv112",
         page_head("LV-112", "News", "News") + two_col(news_body, news_side))

    # ---- Gallery ----
    gallery_imgs = [
        ("LV-112_Map", "LV-112_Map.jpg", "Nantucket lightship station location (approximately 100 miles off mainland &mdash; 40 deg., 33 min., North / 69 deg., 28 min., West; 192 ft. depth of water) in relation to shipping lanes and the location of the SS Andrea Doria collision with the MS Stockholm. Nantucket lightship was the most remote location and was stationed farther offshore than all other U.S. lightships."),
        ("LV-112_CREW_1958_fs", "LV-112_CREW_1958_fs.jpg", "LS 112-534; 1958-60 LV-112 crew. (Photo courtesy of crew member Bernie Webber)"),
        ("LV-112_RADIO_ROOM_fs", "LV-112_RADIO_ROOM_fs.jpg", "Radio Room, LS 112, 1936; Photo No. 214, photographer unknown. (Courtesy of USCG)"),
        ("lv112_017_fs", "lv112_017_fs.jpg", "LV-112, on Nantucket Shoals station, prior to 1960."),
        ("EDNA_fs", "EDNA_fs.jpg", "LV-112 original structure, prior to receiving major damage caused by Hurricane Edna while on station on 9/14/54 (when the bridge was rebuilt, fewer port holes were installed &mdash; compare photo of LV-112 bridge as a Relief vessel). During Hurricane Edna in 70 ft seas and 110 mph winds, bow plates were damaged, bridge and pilot house stove in, small boats demolished and rudder severely damaged; minor injuries to several crew members. (USCG photo &mdash; courtesy of Bernie Webber)"),
        ("nantucket_shoals_fs", "nantucket_shoals_fs.jpg", "LV-112, on Nantucket Shoals station during a storm at sea with a wave breaking over the stern section. Photo taken from another vessel, prior to 1960. (Photo courtesy of Don Yeskoo)"),
        ("LV112_men_mast_fs", "LV112_men_mast_fs.jpg", "LV-112 &mdash; view from the top of the aft mast to the forward mast. Enginemen were replacing navigational lights. The anemometer is halfway out on the yardarm on the left. Photo taken by crewman Rich Racicot, 1964-66."),
        ("LV-112_BRIDGE_fs", "LV-112_BRIDGE_fs.jpg", "The bridge of the LV-112; the photograph probably dates from 1936, the year she was built. (Courtesy of USCG)"),
        ("onstationthumbnail_fs", "onstationthumbnail_fs.jpg", "LV-112 on Nantucket Shoals Station, 1975."),
        ("OLYMPICthmbnail_fs", "OLYMPICthmbnail_fs.jpg", "The Cunard-White Star liner SS Olympic, sister to the Titanic, passes very close aboard the LV-117 on the Nantucket station in early April 1934. The following month the Olympic collided with LV-117 and sent it to the bottom in seconds. Four crewmen went down with the ship while the Olympic rescued the remaining seven; three of these men later died from injuries and exposure. The British Government paid for the construction of LV-112 as reparation. (Courtesy of USCG)"),
        ("LV-112_STEAM_POWERED_fs", "LV-112_STEAM_POWERED_fs.jpg", "LV-112, 1936. (Photo by George F. Stewart, U.S.L.H.S.)"),
        ("2_relief_LS112_fs", "2_relief_LS112_fs.jpg", "Relief LS 112534 (LV-112 as Relief Lightship, 1958-60). (Photo courtesy of Bernie Webber)"),
        ("at_helm_fs", "at_helm_fs.jpg", "A volunteer at the helm of LV-112, while underway (c. 1990). (Photo courtesy of Don Yeskoo)"),
        ("WWII0351_fs", "WWII0351_fs.jpg", "Helping to protect the United States Atlantic coast during WWII, LV-112 was withdrawn from lightship duty, converted to an examination vessel (1942-45, designated as USS Nantucket), painted battleship gray and armed, serving Portland, Maine. Many lightships were temporarily converted to examination vessels during the war and assigned to inspect merchant vessels before they were allowed to enter U.S. ports. The examination vessels were also on constant watch for German U-Boats navigating along the U.S. coastlines. U-Boats that escaped the watchful eyes of the examination vessels sank hundreds of merchant ships along the U.S. East Coast. In October 1942, 105 U-Boats were reported off the Atlantic Seaboard. In addition, during the first six months of 1942, German U-Boats were responsible for sinking 171 merchant vessels, from Maine to Florida. LV-112 saved crewmembers of the USS Eagle-56, which was torpedoed and sunk off Portland by a German U-Boat, U-853. After sinking another U.S. merchant ship off Port Judith, Rhode Island, the U-853 was tracked down and sunk by the U.S. Navy in Rhode Island waters, where it lies submerged to this day. (Photo courtesy of Don Yeskoo, Maritime Maine)"),
        ("examination_vessel1942-45_fs", "examination_vessel1942-45_fs.jpg", "During WWII, while assigned to Portland, Maine, a crewman stands ready at a machine gun mounted on LV-112's foredeck. One 3&quot; gun was also mounted on the stern section. (Photo courtesy of Don Yeskoo, Maritime Maine)"),
        ("christening_1936_fs", "christening_1936_fs.jpg", "LV-112, being christened at a launching ceremony in Wilmington, Delaware, 1936. (Photo courtesy of Don Yeskoo)"),
        ("volunteer_mechanics_fs", "volunteer_mechanics_fs.jpg", "Vocational school students participating in repairs during an instructional class on LV-112's 8-cylinder, 900hp Cooper-Bessemer diesel main engine. Three of the cylinder heads are shown in the foreground. (Photo courtesy of Don Yeskoo)"),
        ("cooper_bessemer_fs", "cooper_bessemer_fs.jpg", "A volunteer stands next to the Cooper-Bessemer 900 HP diesel main engine in LV-112's engine room."),
        ("lightship_tow_1_fs", "lightship_tow_1_fs.jpg", "Nantucket / LV-112 being towed by the tugboat Lynx, heading east-bound from Oyster Bay, Long Island, NY to Boston on the Cape Cod Canal, May 2010. Photo: Courtesy of Ron Janard"),
        ("nantucket_undersail_fs", "nantucket_undersail_fs.jpg", "Nantucket / LV-112 being towed by the tugboat Lynx, heading east-bound from Oyster Bay, Long Island, NY to Boston on the Cape Cod Canal, May 2010. Photo: Courtesy of Ron Janard"),
        ("nantucket_bostonharbor_fs", "nantucket_bostonharbor_fs.jpg", "Nantucket / LV-112 berthed at the Boston Harbor Shipyard &amp; Marina in East Boston, 2010."),
        ("bowthumbnail_fs", "bowthumbnail_fs.jpg", "LV-112, bow / mushroom anchors, 7,000 lbs. each (2008)."),
        ("wheelhousethmbnail_fs", "wheelhousethmbnail_fs.jpg", "Bridge / wheelhouse (2008)."),
        ("charttablethumbnail_fs", "charttablethumbnail_fs.jpg", "Navigational chart table in wheelhouse (2008)."),
        ("bunksthumbnail_fs", "bunksthumbnail_fs.jpg", "Crew bunk area (2008)."),
        ("foredeckthumbnail_fs", "foredeckthumbnail_fs.jpg", "Navigational signal bell (2008)."),
        ("radioroomthmbnail_fs", "radioroomthmbnail_fs.JPG", "Entrance to Radio Room (2008)."),
        ("radioroom2thmbnail_fs", "radioroom2thmbnail_fs.jpg", "Radio Room / radio control panels (2008)."),
        ("officersquartersthmbnail_fs", "officersquartersthmbnail_fs.jpg", "Officers' quarters (2008)."),
        ("galley2thmbnail_fs", "galley2thmbnail_fs.jpg", "Galley (2008)."),
        ("docksidethumbnail_fs", "docksidethumbnail_fs.JPG", "LV-112 berthed at Oyster Bay Pier (2008)."),
    ]
    tiles = "\n".join(
        f'''            <a class="gallery-item" href="assets/images/gallery/fullsize/{fs}" data-lightbox=""
              data-caption="{cap}">
              <img src="assets/images/gallery/fullsize/{fs}" alt="{cap_plain}" loading="lazy">
            </a>'''
        for _id, fs, cap in gallery_imgs
        for cap_plain in [cap.replace('"', '&quot;')]
    )
    gallery_body = f'''    <section class="section">
      <div class="container">
        <div class="prose" style="max-width:760px;">
          <p>A collection of historic and contemporary photographs of <em>Nantucket Lightship / LV-112</em>, her crews, and her restoration. Select any photo to view it larger.</p>
        </div>
        <div class="gallery-grid">
{tiles}
        </div>
      </div>
    </section>
'''
    page("gallery.html", "Photo Gallery",
         "Historic and contemporary photographs of Nantucket Lightship / LV-112, her crews, and her restoration.",
         "lv112",
         page_head("LV-112", "Photo Gallery", "Photo Gallery") + gallery_body)


if __name__ == "__main__":
    build()
