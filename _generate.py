#!/usr/bin/env python3
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent

BOOT = """<script>
(function () {
  try {
    var saved = localStorage.getItem("mho-theme");
    var theme = saved === "light" || saved === "dark"
      ? saved
      : (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    document.documentElement.setAttribute("data-theme", theme);
  } catch (e) {}
})();
</script>"""

TOGGLE = """
      <button type="button" class="theme-toggle" aria-label="Switch to dark theme" title="Switch to dark theme" aria-pressed="false">
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <circle cx="12" cy="12" r="4"></circle>
          <path d="M12 3v2M12 19v2M5.2 5.2l1.4 1.4M17.4 17.4l1.4 1.4M3 12h2M19 12h2M5.2 18.8l1.4-1.4M17.4 6.6l1.4-1.4"></path>
        </svg>
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M21 14.5A8.5 8.5 0 1 1 9.5 3 7 7 0 0 0 21 14.5z"></path>
        </svg>
      </button>"""

SPORTS = [
    ("/youth-sports-officials/", "Overview"),
    ("/youth-sports-officials/youth-basketball/", "Basketball"),
    ("/youth-sports-officials/youth-soccer/", "Soccer"),
    ("/youth-sports-officials/youth-wrestling/", "Wrestling"),
    ("/youth-sports-officials/youth-football/", "Football"),
    ("/youth-sports-officials/youth-baseball/", "Baseball"),
]

def nav_html(active):
    def item(href, label, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    parts = []
    for href, label in SPORTS:
        cur = ' aria-current="page"' if active == href else ""
        parts.append(f'<a href="{href}"{cur}>{label}</a>')
    drop_links = "\n            ".join(parts)
    drop_open = " is-open" if active.startswith("/youth-sports-officials") else ""
    return f"""    <nav class="nav" id="site-nav" aria-label="Primary">
      {item("/", "Home", "/")}
      {item("/about-us/", "About Us", "/about-us/")}
      {item("/donate/", "Donate", "/donate/")}
      {item("/board-of-directors/", "Board of Directors", "/board-of-directors/")}
      <div class="drop{drop_open}">
        <button type="button" class="drop-btn" aria-expanded="false" aria-haspopup="true">Youth Sports Officials</button>
        <div class="drop-menu">
            {drop_links}
        </div>
      </div>
      <a class="nav-cta" href="/contact-us/">Contact Us</a>
    </nav>"""

def page(path, title, description, active, content, extra_head=""):
    full_title = "Mile High Officials" if title == "Home" else f"{title} | Mile High Officials"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {BOOT}
  <title>{escape(full_title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#d4690f">
  <meta property="og:title" content="{escape(full_title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="/assets/img/logo-mark.png">
  <meta property="og:type" content="website">
  <link rel="icon" href="/assets/img/favicon.ico" sizes="32x32">
  <link rel="icon" type="image/png" href="/assets/img/favicon.png">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css?v=court1">
  {extra_head}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="/">
        <img src="/assets/img/logo-mark-256.png" width="48" height="48" alt="Mile High Officials logo">
        <span class="brand-text">
          <span class="brand-name">Mile High Officials</span>
          <span class="brand-tag">Denver, CO · Est. 2008</span>
        </span>
      </a>
{nav_html(active)}
      <div class="header-tools">
        {TOGGLE}
        <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span></span></button>
      </div>
    </div>
  </header>
  <main id="main">
{content}
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="/assets/img/logo-mark-256.png" width="64" height="64" alt="Mile High Officials logo">
          <h2>Mile High Officials</h2>
          <p>Mile High Officials provides professional assigning services and recruits officials for youth basketball, baseball, softball, football, soccer, and wrestling throughout Colorado.</p>
        </div>
        <div class="footer-col">
          <h3>Quick links</h3>
          <a href="/">Home</a>
          <a href="/about-us/">About Us</a>
          <a href="/board-of-directors/">Board of Directors</a>
          <a href="/donate/">Donate</a>
        </div>
        <div class="footer-col">
          <h3>Officials</h3>
          <a href="/contact-us/">Become an official</a>
          <a href="/contact-us/">Request more info</a>
          <a href="mailto:admin@milehighofficials.com">Email MHO</a>
          <a href="tel:7204320354">Call 720-432-0354</a>
        </div>
        <div class="footer-col">
          <h3>Contact</h3>
          <a href="tel:7204320354">720-432-0354</a>
          <a href="mailto:admin@milehighofficials.com">admin@milehighofficials.com</a>
          <p>150 Wells St #582<br>Erie, CO 80516</p>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© 2026 Mile High Officials. All rights reserved.</div>
        <div>Professional officiating. Strong communication. Reliable game support.</div>
      </div>
    </div>
  </footer>
  <script src="/assets/js/main.js"></script>
</body>
</html>
"""
    dest = ROOT / path.lstrip("/")
    if path.endswith("/"):
        dest = dest / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    print("wrote", dest.relative_to(ROOT))

def sport_nav(current):
    links = []
    for href, label in SPORTS:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return '<nav class="subnav" aria-label="Youth sports">\n          ' + "\n          ".join(links) + "\n        </nav>"

def cards_html(items, cols="cards"):
    out = [f'<div class="{cols}">']
    for item in items:
        num = f'<div class="card-num">{escape(item["num"])}</div>' if item.get("num") else ""
        out.append(f"""        <article class="card">
          {num}
          <h3>{item['title']}</h3>
          <p>{item['text']}</p>
        </article>""")
    out.append("      </div>")
    return "\n".join(out)

# ----- Pages -----

page("/", "Home",
     "Mile High Officials is recruiting Colorado basketball officials who want real development, flexible work, and a professional path in the game.",
     "/",
"""    <section class="hero">
      <div class="wrap hero-grid">
        <div>
          <p class="eyebrow">Colorado basketball officials wanted</p>
          <h1>Own the floor. Lead the game.</h1>
          <p class="lead">Mile High Officials is recruiting people who love basketball, want real development, and are ready to step into a role that demands confidence, professionalism, and presence. This is education with edge: learn the game, command the court, and build a schedule that works for you.</p>
          <div class="actions">
            <a class="btn btn-primary" href="tel:7204320354">Call 720-432-0354</a>
            <a class="btn btn-secondary" href="/contact-us/">Request more info</a>
          </div>
        </div>
        <aside class="hero-panel">
          <img src="/assets/img/logo-mark-256.png" width="220" height="220" alt="Mile High Officials logo">
          <p>Nationwide shortages mean there is real demand for strong youth basketball officials right now.</p>
        </aside>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        """ + cards_html([
            {"title": "Get trained", "text": "Learn positioning, communication, mechanics, and game management from experienced officials."},
            {"title": "Get paid", "text": "Turn your basketball knowledge into flexible earning opportunities with meaningful impact."},
            {"title": "Stay in the game", "text": "Keep your connection to youth sports while helping athletes compete in the right environment."},
            {"title": "Build respect", "text": "Develop discipline, communication, and leadership skills that carry beyond the court."},
        ]) + """
        <div class="actions">
          <a class="btn btn-primary" href="/contact-us/">Start recruiting me</a>
          <a class="btn btn-secondary" href="/contact-us/">Get more info</a>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Hard-core recruiting. Real development.</p>
          <h2>A reputation built on consistency and preparation.</h2>
        </div>
        <div class="stats">
          <div class="stat"><strong>8+ years</strong><p>Serving the Denver Metro area and building a reputation around consistency, communication, and professionalism.</p></div>
          <div class="stat"><strong>250+ officials</strong><p>Supported by a deep network of qualified officials working high school and collegiate levels.</p></div>
          <div class="stat"><strong>Game ready</strong><p>Training, standards, site supervision, and assignment support built to prepare officials for each game.</p></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Why officials join</p>
          <h2>More than a side hustle. A basketball lane.</h2>
          <p>If you want to work hard, grow fast, and stay close to basketball, officiating gives you a path with purpose. Mile High Officials offers flexibility, structure, and a way to lead the game from the best seat in the building.</p>
        </div>
        """ + cards_html([
            {"num": "01", "title": "Flexible schedule", "text": "Choose assignments that fit your availability and stay active without being locked into a rigid weekly routine."},
            {"num": "02", "title": "Leadership on court", "text": "Officiating builds poise under pressure, clear communication, and the confidence to make difficult decisions in real time."},
            {"num": "03", "title": "Give back", "text": "Help youth basketball run the right way by creating safer, more organized, and more competitive game environments."},
        ], "cards cards-3") + """
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Mission in action</p>
          <h2>MHO trains officials to be fundamentally prepared.</h2>
          <p>The mission centers on development, conditioning, education, and professionalism. Every official is expected to arrive ready, know the rules, move with purpose, communicate well, and manage the game from tip-off to final whistle.</p>
        </div>
        <div class="split">
          <div class="list-block">
            <h3>What MHO brings</h3>
            <ul class="plain-list">
              <li>Structured assignment support and up-to-date scheduling.</li>
              <li>Professional expectations backed by site supervision.</li>
              <li>A reputation built on consistency and communication.</li>
              <li>A staff culture that values preparation, accountability, and growth.</li>
            </ul>
          </div>
          <div class="list-block">
            <h3>What we need from you</h3>
            <ul class="plain-list">
              <li>Professional conduct before, during, and after every game.</li>
              <li>Willingness to learn mechanics, rules, and positioning.</li>
              <li>Strong communication and calm under pressure.</li>
              <li>Commitment to showing up early and staying ready.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Simple path in</p>
          <h2>From basketball fan to trusted official.</h2>
        </div>
        <div class="steps">
          <div class="step"><div class="step-num">Step 1</div><h3>Reach out</h3><p>Call or submit an inquiry so MHO can learn your background, availability, and level of basketball experience.</p></div>
          <div class="step"><div class="step-num">Step 2</div><h3>Get guided</h3><p>Receive direction on expectations, training, assignments, and what it takes to work games the MHO way.</p></div>
          <div class="step"><div class="step-num">Step 3</div><h3>Take the floor</h3><p>Start building confidence, earning opportunities, and game presence while serving youth basketball in your community.</p></div>
        </div>
      </div>
    </section>

    <section class="cta-band">
      <div class="wrap">
        <h2>Basketball needs more strong officials.</h2>
        <p>If you love the game and want a role with responsibility, development, and real opportunity, Mile High Officials is ready to talk.</p>
        <div class="actions">
          <a class="btn btn-primary" href="tel:7204320354">Call 720-432-0354 now</a>
          <a class="btn btn-secondary" href="/contact-us/">Request more info</a>
        </div>
      </div>
    </section>
""")

page("/about-us/", "About Us",
     "Mile High Officials is a family-owned assigning company serving the Denver Metro area, developing and supplying officials who are fundamentally prepared for every game.",
     "/about-us/",
"""    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">About Mile High Officials</p>
        <h1>Built for the game. Driven by standards.</h1>
        <p class="lead">Mile High Officials is a family-owned assigning company serving the Denver Metro area. The mission is clear: develop, condition, supply, and educate officials so they are fundamentally prepared for every game assignment.</p>
        <p class="lead">This is not just about filling games. It is about building a reliable, professional, and organized sports environment where leagues, tournaments, athletes, and families can trust the people on the floor.</p>
        <div class="actions">
          <a class="btn btn-primary" href="tel:7204320354">Call 720-432-0354</a>
          <a class="btn btn-secondary" href="/contact-us/">Contact MHO</a>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        <div class="stats">
          <div class="stat"><strong>8+ years</strong><p>Serving the Denver Metro area with a focus on consistency, preparation, and reputation.</p></div>
          <div class="stat"><strong>250+ officials</strong><p>A large staff of highly qualified officials working high school and collegiate levels.</p></div>
          <div class="stat"><strong>$3M coverage</strong><p>Insurance protection covering contracted officials, staff members, and assigned groups.</p></div>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Who we are</p>
          <h2>A strong assigning service with real accountability.</h2>
        </div>
        """ + cards_html([
            {"num": "01", "title": "Family owned", "text": "MHO is operated by its founder and built with a hands-on standard of service, communication, and long-term relationships."},
            {"num": "02", "title": "Professional standards", "text": "Officials are expected to arrive early, know the rules, communicate well, and manage each contest with professionalism."},
            {"num": "03", "title": "Organized support", "text": "From assignments to site supervision, the system is designed to reduce confusion and keep programs running smoothly."},
        ], "cards cards-3") + """
        <blockquote class="quote" style="margin-top:1.5rem">“The mission of Mile High Officials is to develop, condition, supply, and educate officials to be fundamentally prepared for each game assignment.”</blockquote>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What we offer</p>
          <h2>More than officials. A full system.</h2>
        </div>
        <div class="split">
          <div class="list-block">
            <h3>For leagues and tournaments</h3>
            <ul class="plain-list">
              <li>Reliable assigning services built around consistency.</li>
              <li>Constant communication between clients, assignors, and officials.</li>
              <li>Site supervisors available to address concerns and issues.</li>
              <li>Affordable and flexible service options based on organizational needs.</li>
              <li>Up-to-date scheduling through Arbiter Sports with 24/7 access.</li>
            </ul>
          </div>
          <div class="list-block">
            <h3>For officials</h3>
            <ul class="plain-list">
              <li>Clear expectations and monitored professional standards.</li>
              <li>A development-focused environment built around preparation.</li>
              <li>Access to organized assignments and support.</li>
              <li>A team culture that values communication and accountability.</li>
              <li>A pathway to represent the organization with pride and discipline.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">At a glance</p>
          <h2>Why organizations trust MHO.</h2>
        </div>
        <div class="stats">
          <div class="stat"><strong>24/7</strong><p>Schedule visibility and assignment access through Arbiter Sports.</p></div>
          <div class="stat"><strong>Early</strong><p>Officials are expected to arrive ahead of game time and be ready.</p></div>
          <div class="stat"><strong>Clear</strong><p>Strong communication between assignor, client, and officiating staff.</p></div>
        </div>
        <p style="margin-top:1.25rem;color:var(--ink-2)">Reliable. Built to support a smooth, organized, and well-managed sports program.</p>
      </div>
    </section>

    <section class="cta-band">
      <div class="wrap">
        <h2>Need officials who show up ready?</h2>
        <p>Mile High Officials is ready to discuss assigning services, answer questions, and support your organization with a dependable, professional officiating program.</p>
        <div class="actions">
          <a class="btn btn-primary" href="/contact-us/">Talk with MHO</a>
          <a class="btn btn-secondary" href="mailto:admin@milehighofficials.com">Email admin@milehighofficials.com</a>
        </div>
      </div>
    </section>
""")

page("/donate/", "Donate",
     "Support Mile High Officials as we train, mentor, and develop the next generation of youth sports officials across Colorado.",
     "/donate/",
"""    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">Donate to the mission</p>
        <h1>Empowering youth for a bright future.</h1>
        <p class="lead">Mile High Officials sees youth sports officiating as more than game coverage. It develops work ethic, discipline, confidence, leadership, and long-term opportunity for young people stepping into responsibility.</p>
        <p class="lead">Your support helps strengthen the pipeline of youth sports officials and supports the training, development, and mentorship that make that path possible.</p>
        <div class="actions">
          <a class="btn btn-primary" href="/contact-us/">Give today</a>
          <a class="btn btn-secondary" href="tel:7204320354">Call 720-432-0354</a>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        """ + cards_html([
            {"title": "Shortage", "text": "The current shortage of youth sports officials means more opportunity and greater need for development support."},
            {"title": "Training", "text": "New officials need classroom learning, field training, and self-study before they ever step onto the court or field."},
            {"title": "Mentorship", "text": "Young officials benefit from guidance by experienced referees, coordinators, coaches, and sports leaders."},
        ], "cards cards-3") + """
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Why donate</p>
          <h2>Support youth sports. Build future leaders.</h2>
          <p>Officiating is not just a job. It is character-building work that teaches accountability, decision-making, professionalism, and confidence in high-pressure environments.</p>
        </div>
        """ + cards_html([
            {"num": "01", "title": "Work development", "text": "Young people gain real-world experience through commitment, preparation, communication, and performance under pressure."},
            {"num": "02", "title": "Long-term opportunity", "text": "Officiating opens doors to employment, networking, mentorship, and future leadership roles in and beyond sports."},
            {"num": "03", "title": "Character and confidence", "text": "Refereeing helps young men and women develop authority, resilience, judgment, and the confidence to lead."},
        ], "cards cards-3") + """
        <blockquote class="quote" style="margin-top:1.5rem">“All of this is time well spent, and time building skills and character, all essential for success in the increasingly complex world of the 21st century.”</blockquote>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What donations help support</p>
          <h2>Back the people who keep youth sports moving.</h2>
        </div>
        <div class="split">
          <div class="list-block">
            <h3>Impact areas</h3>
            <ul class="plain-list">
              <li>Training and development for new youth sports officials.</li>
              <li>Mentorship from experienced referees and coordinators.</li>
              <li>Pathways for boys and girls to step into positions of authority early.</li>
              <li>Opportunities that keep young people connected to the sports they love.</li>
              <li>Growth of a stronger pipeline of officials for the future.</li>
            </ul>
          </div>
          <div class="list-block">
            <h3>Why it matters</h3>
            <ul class="plain-list">
              <li>Shortages in officiating affect the quality and consistency of youth sports programs.</li>
              <li>Refereeing offers flexible work while still leaving room for school, family, and other jobs.</li>
              <li>Young officials build valuable contacts and professional references early.</li>
              <li>The responsibility of officiating creates leadership skills that carry into adult life.</li>
              <li>For many, officiating becomes a lifelong passion and calling.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">At a glance</p>
          <h2>The value of early responsibility.</h2>
        </div>
        <div class="stats">
          <div class="stat"><strong>Real</strong><p>Work experience at an early age.</p></div>
          <div class="stat"><strong>Strong</strong><p>Leadership and management skills.</p></div>
          <div class="stat"><strong>Wide</strong><p>Networking and reference-building opportunities.</p></div>
        </div>
        <p style="margin-top:1.25rem;color:var(--ink-2)">Lasting: a foundation for future employment and confidence.</p>
      </div>
    </section>

    <section class="cta-band">
      <div class="wrap">
        <h2>Don’t delay. Give today.</h2>
        <p>Help support the next generation of youth sports officials and invest in the training, guidance, and opportunity that turn sports into a path for growth.</p>
        <div class="actions">
          <a class="btn btn-primary" href="/contact-us/">Support the mission</a>
          <a class="btn btn-secondary" href="mailto:admin@milehighofficials.com">Email MHO</a>
        </div>
      </div>
    </section>
""")

page("/board-of-directors/", "Board of Directors",
     "Meet the Mile High Officials board: Verne Harris, Josh Cochran, and Jon Sanders, leaders in officiating, education, and youth sports.",
     "/board-of-directors/",
"""    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">Board of Directors</p>
        <h1>Leadership with game-level experience.</h1>
        <p class="lead">The Mile High Officials Board of Directors reflects a strong blend of officiating experience, school leadership, and sports organization insight. That mix matters in this industry, where credibility, standards, and relationships shape every assignment.</p>
        <p class="lead">In youth and amateur sports, strong leadership behind the scenes helps create consistency on the court. A knowledgeable board supports standards, development, and partnerships that leagues, schools, and families can trust.</p>
        <div class="actions">
          <a class="btn btn-primary" href="/contact-us/">Connect with MHO</a>
          <a class="btn btn-secondary" href="tel:7204320354">Call 720-432-0354</a>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        """ + cards_html([
            {"title": "Industry perspective", "text": "Leadership connected to officiating, education, and organized sports administration."},
            {"title": "Credibility", "text": "Board representation that signals professionalism and confidence to schools, leagues, and event partners."},
            {"title": "Standards", "text": "Support for the kind of accountability and consistency that strong officiating programs need."},
        ], "cards cards-3") + """
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Board members</p>
          <h2>A board built around leadership and trust.</h2>
          <p>The Board of Directors highlights three leaders whose backgrounds speak directly to the sports officiating space.</p>
        </div>
        <div class="people">
          <article class="person">
            <h3>Verne Harris</h3>
            <div class="role">NCAA Men’s Basketball Official</div>
            <p>Brings high-level officiating credibility and direct insight into the standards, mechanics, judgment, and professionalism required in competitive basketball environments.</p>
          </article>
          <article class="person">
            <h3>Josh Cochran</h3>
            <div class="role">Executive Director, Stargate Charter School</div>
            <p>Offers an educational leadership perspective that aligns with youth development, organizational structure, and the importance of dependable support for student-athletes and school-based programs.</p>
          </article>
          <article class="person">
            <h3>Jon Sanders</h3>
            <div class="role">Founder/CEO, 50-Allstars</div>
            <p>Contributes sports business and program-building experience, helping connect operations, community relationships, and strategic growth within the youth sports space.</p>
          </article>
        </div>
        <p style="margin-top:1.5rem;color:var(--ink-2);max-width:44rem">Mile High Officials’ Board of Directors represents the kind of leadership that matters in the officiating industry: experienced, connected, and grounded in real sports environments.</p>
      </div>
    </section>

    <section class="cta-band">
      <div class="wrap">
        <h2>Serious leadership for a serious sports program.</h2>
        <p>Mile High Officials is guided by leaders who understand the demands of officiating, the needs of youth sports organizations, and the importance of building trust across every level of competition.</p>
        <div class="actions">
          <a class="btn btn-primary" href="/about-us/">Learn more about MHO</a>
          <a class="btn btn-secondary" href="mailto:admin@milehighofficials.com">Email MHO</a>
        </div>
      </div>
    </section>
""")

page("/youth-sports-officials/", "Youth Sports Officials",
     "Mile High Officials is recruiting youth sports referees, umpires, and officials across Colorado. Flexible paid work, training, and a path forward.",
     "/youth-sports-officials/",
"""    <section class="page-hero">
      <div class="wrap">
        """ + sport_nav("/youth-sports-officials/") + """
        <p class="eyebrow">Youth sports referee recruiting</p>
        <h1>There’s a nationwide shortage of youth sports referees.</h1>
        <p class="lead">Mile High Officials is recruiting youth sports referees, umpires, and officials across Colorado. If you love sports, want flexible paid work, and are ready to lead with confidence, this is a real opportunity.</p>
        <p class="lead">Sports officials play a vital role in shaping the quality of youth athletic programs. It is a challenging job, but when handled the right way, it is rewarding, respected, and deeply connected to the sports you love.</p>
        <div class="actions">
          <a class="btn btn-primary" href="/contact-us/">Become a youth sports official</a>
          <a class="btn btn-secondary" href="mailto:admin@milehighofficials.com">Email admin@milehighofficials.com</a>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        """ + cards_html([
            {"title": "All sports need officials", "text": "Basketball, baseball, football, soccer, softball, and more all depend on trained youth sports referees and umpires."},
            {"title": "Flexible work", "text": "Officiating can fit around school, work, family life, and other responsibilities while keeping you close to sports."},
            {"title": "Real growth", "text": "Officials build confidence, communication, decision-making, and leadership under pressure."},
        ], "cards cards-3") + """
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Why this matters</p>
          <h2>Officials shape the game experience.</h2>
        </div>
        """ + cards_html([
            {"num": "01", "title": "Instant decision-making", "text": "Sports officials must make fast judgments, stay calm, and manage game situations with professionalism and authority."},
            {"num": "02", "title": "Conflict resolution", "text": "Referees and umpires help keep games organized by communicating clearly and resolving tension in real time."},
            {"num": "03", "title": "Fitness and focus", "text": "Depending on the sport, officials need awareness, mobility, and the ability to keep up with the action from start to finish."},
        ], "cards cards-3") + """
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Who can become an official</p>
          <h2>You don’t need a perfect background. You need the right mindset.</h2>
        </div>
        <div class="list-block">
          <ul class="plain-list">
            <li>Former athletes, ex-competitors, parents, teachers, students, and fans can all become youth sports referees.</li>
            <li>You can start by learning the rules of the sport, attending clinics, and getting experience at the local level.</li>
            <li>From there, officials can advance into high school and college sports, and in some cases pursue elite-level opportunities.</li>
            <li>What matters most is professionalism, consistency, communication, and a real passion for officiating.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Why join Mile High Officials</p>
          <h2>Training, opportunity, and a path forward.</h2>
        </div>
        """ + cards_html([
            {"num": "01", "title": "Learn the role", "text": "Get guidance on rules, mechanics, professionalism, and the real expectations of working youth sports events."},
            {"num": "02", "title": "Stay in sports", "text": "Keep your connection to the games you love while helping young athletes compete in a structured environment."},
            {"num": "03", "title": "Build a future", "text": "Officiating can begin as part-time work and grow into a serious long-term lane for skilled, dependable officials."},
        ], "cards cards-3") + """
      </div>
    </section>

    <section class="cta-band">
      <div class="wrap">
        <h2>Don’t wait. Sports need more strong officials.</h2>
        <p>If you are ready to become a youth sports referee, youth sports umpire, or youth sports official in Colorado, contact Mile High Officials today and start the process.</p>
        <div class="actions">
          <a class="btn btn-primary" href="/contact-us/">Request more info</a>
          <a class="btn btn-secondary" href="mailto:admin@milehighofficials.com">Email admin@milehighofficials.com</a>
        </div>
      </div>
    </section>
""")

# Sport detail pages
SPORT_PAGES = {
    "youth-basketball": dict(
        title="Youth Basketball Officials",
        kicker="Youth basketball officials",
        h1="Become a youth basketball referee in Colorado.",
        desc="Mile High Officials is recruiting youth basketball officials and new basketball referees in Colorado. Get trained, get paid, and stay in the game.",
        leads=[
            "Mile High Officials is recruiting youth basketball officials, new basketball referees, and experienced sports officials who want to stay in the game, get trained, and get paid. If you love basketball, there is a place for you here.",
            "We help youth basketball referees build confidence, learn mechanics, improve communication, and step onto the court ready to manage the game the right way.",
        ],
        cta=("Apply to officiate basketball", "mailto:admin@milehighofficials.com?subject=Youth%20Basketball%20Official%20Interest"),
        highlights=[
            {"title": "Train fast", "text": "Learn youth basketball rules, positioning, game flow, and mechanics from experienced officials."},
            {"title": "Work flexible", "text": "Choose opportunities that fit your schedule while staying close to the sport you love."},
            {"title": "Lead games", "text": "Build poise, decision-making, and court presence in live game environments."},
        ],
        why_kicker="Why basketball officials join",
        why_title="The best seat in the gym. The most important job on the floor.",
        why=[
            {"num": "01", "title": "Get paid to stay in basketball", "text": "Youth basketball officiating keeps you connected to the game while opening up flexible earning opportunities."},
            {"num": "02", "title": "Develop leadership", "text": "Basketball referees learn communication, confidence, conflict management, and decision-making under pressure."},
            {"num": "03", "title": "Serve the game", "text": "Strong youth basketball officials help create fair, organized, and competitive experiences for players and families."},
        ],
        looking_title="Officials who show up ready.",
        looking=[
            "People interested in becoming youth basketball referees in Colorado.",
            "Former players, coaches, parents, students, and sports fans who know the game.",
            "Officials willing to learn rules, mechanics, positioning, and professionalism.",
            "Applicants who can communicate clearly and stay composed under pressure.",
            "Reliable people who want to grow with a respected assigning organization.",
        ],
        band_title="Youth basketball needs more strong officials.",
        band_text="If you are ready to become a youth basketball official, basketball referee, or game official in Colorado, contact Mile High Officials today and take the first step.",
        band_primary=("Call 720-432-0354 now", "tel:7204320354"),
    ),
    "youth-soccer": dict(
        title="Youth Soccer Referees",
        kicker="Youth soccer referees",
        h1="Become a youth soccer referee in Colorado.",
        desc="Mile High Officials is recruiting youth soccer referees and soccer officials in Colorado who want flexible work and a strong connection to the sport.",
        leads=[
            "Mile High Officials is recruiting youth soccer referees, soccer officials, and new referees who want to stay active in the sport and build a flexible source of income. If you know soccer and want to lead matches with confidence, we want to hear from you.",
            "We help youth soccer officials learn positioning, match control, communication, and professional standards so they can walk onto the field prepared.",
        ],
        cta=("Apply to referee soccer", "mailto:admin@milehighofficials.com?subject=Youth%20Soccer%20Referee%20Interest"),
        highlights=[
            {"title": "Stay in soccer", "text": "Keep your connection to youth soccer while supporting fair, organized competition."},
            {"title": "Learn match control", "text": "Build confidence with rules knowledge, communication, and on-field presence."},
            {"title": "Flexible income", "text": "Soccer officiating offers a schedule that can work around school, work, and family life."},
        ],
        why_kicker="Why soccer officials join",
        why_title="Run the match. Support the game.",
        why=[
            {"num": "01", "title": "Get trained", "text": "Learn youth soccer referee expectations, rules, match flow, and professional conduct."},
            {"num": "02", "title": "Get experience", "text": "Develop leadership skills, communication, and decision-making that carry beyond sports."},
            {"num": "03", "title": "Get involved", "text": "Make a real impact in youth soccer by helping games stay safe, fair, and competitive."},
        ],
        looking_title="Who should apply",
        looking=[
            "People interested in becoming youth soccer referees in Colorado.",
            "Former soccer players, coaches, fans, students, and parents.",
            "Applicants who want flexible work and a strong connection to the sport.",
            "Officials ready to learn, communicate, and show professionalism on the field.",
        ],
        band_title="Soccer needs more reliable referees.",
        band_text="If you are ready to become a youth soccer referee or soccer official in Colorado, contact Mile High Officials today.",
        band_primary=("Call to join soccer officiating", "tel:7204320354"),
    ),
    "youth-wrestling": dict(
        title="Youth Wrestling Officials",
        kicker="Youth wrestling officials",
        h1="Become a youth wrestling official in Colorado.",
        desc="Mile High Officials is recruiting youth wrestling officials and wrestling referees in Colorado who can manage matches with discipline and composure.",
        leads=[
            "Mile High Officials is recruiting youth wrestling officials, wrestling referees, and sports officials who understand the pace, discipline, and control required in wrestling. If you want to stay involved in the sport, this is a meaningful way to do it.",
            "We help wrestling officials develop mat awareness, rules knowledge, confidence, and the composure needed to manage every match professionally.",
        ],
        cta=("Apply to officiate wrestling", "mailto:admin@milehighofficials.com?subject=Youth%20Wrestling%20Official%20Interest"),
        highlights=[
            {"title": "Know the rules", "text": "Train on wrestling rules, positioning, control, and proper match administration."},
            {"title": "Build confidence", "text": "Develop the authority and presence needed for youth wrestling events."},
            {"title": "Stay connected", "text": "Keep your place in wrestling while helping young athletes compete in the right environment."},
        ],
        why_kicker="Why wrestling officials matter",
        why_title="Discipline, control, and match integrity.",
        why=[
            {"num": "01", "title": "Structured training", "text": "Learn how to manage youth wrestling matches with consistency and rule-based confidence."},
            {"num": "02", "title": "Real leadership", "text": "Wrestling officials must stay sharp, decisive, and calm under pressure in every situation."},
            {"num": "03", "title": "Community impact", "text": "Help young wrestlers compete in safe, organized, and professionally managed events."},
        ],
        looking_title="Who should apply",
        looking=[
            "People interested in becoming youth wrestling referees in Colorado.",
            "Former wrestlers, coaches, parents, and fans who know the sport.",
            "Applicants who value discipline, professionalism, and preparation.",
            "Officials willing to learn mat control, mechanics, and consistent communication.",
        ],
        band_title="Wrestling needs more prepared officials.",
        band_text="If you want to become a youth wrestling official or wrestling referee in Colorado, contact Mile High Officials today and take the next step.",
        band_primary=("Call to join wrestling officiating", "tel:7204320354"),
    ),
    "youth-football": dict(
        title="Youth Football Officials",
        kicker="Youth football officials",
        h1="Become a youth football official in Colorado.",
        desc="Mile High Officials is recruiting youth football officials and football referees in Colorado. Learn mechanics, crew communication, and game management.",
        leads=[
            "Mile High Officials is recruiting youth football officials, football referees, and game officials who want to stay involved in football and work in a role that requires confidence, awareness, and strong communication. If you know the game, there is a place for you here.",
            "We help new and experienced football officials learn mechanics, crew communication, rule enforcement, and game management so they arrive prepared every week.",
        ],
        cta=("Apply to officiate football", "mailto:admin@milehighofficials.com?subject=Youth%20Football%20Official%20Interest"),
        highlights=[
            {"title": "Crew-based training", "text": "Learn football mechanics, positioning, signals, and communication with the full crew in mind."},
            {"title": "Flexible opportunity", "text": "Football officiating offers meaningful work for people who want to stay connected to the sport."},
            {"title": "Game-day leadership", "text": "Take ownership of pace, control, and professionalism on the field."},
        ],
        why_kicker="Why football officials join",
        why_title="Know the game. Lead the field.",
        why=[
            {"num": "01", "title": "Stay in football", "text": "Youth football officiating keeps former players, coaches, and fans active in the sport they know best."},
        ],
        looking_title=None,
        looking=None,
        band_title="Ready to officiate youth football in Colorado?",
        band_text="If you know the game and want to work as a youth football official, contact Mile High Officials to talk about training, expectations, and next steps.",
        band_primary=("Call 720-432-0354", "tel:7204320354"),
        truncated=True,
    ),
    "youth-baseball": dict(
        title="Youth Baseball Umpires",
        kicker="Youth baseball umpires",
        h1="Become a youth baseball umpire in Colorado.",
        desc="Mile High Officials is recruiting youth baseball umpires and baseball officials in Colorado. Train on mechanics, positioning, and professional communication.",
        leads=[
            "Mile High Officials is recruiting youth baseball umpires, baseball officials, and dependable sports-minded people who want to stay involved in baseball while earning income and developing leadership skills.",
            "We train youth baseball umpires in rules, positioning, mechanics, game flow, and professional communication so they can step on the field prepared.",
        ],
        cta=("Apply to umpire baseball", "mailto:admin@milehighofficials.com?subject=Youth%20Baseball%20Umpire%20Interest"),
        highlights=[
            {"title": "Baseball mechanics", "text": "Train on plate work, base coverage, positioning, signals, and game control."},
            {"title": "Flexible paid work", "text": "Baseball umpiring offers schedule flexibility and a strong way to stay in the sport."},
            {"title": "Professional growth", "text": "Develop confidence, communication, and leadership every time you take the field."},
        ],
        why_kicker="Why baseball umpires join",
        why_title="Call it clean. Run it right.",
        why=[
            {"num": "01", "title": "Stay in baseball", "text": "Youth baseball umpiring keeps you around the game while helping the next generation compete."},
            {"num": "02", "title": "Build authority", "text": "Umpires sharpen judgment, calm communication, and the ability to manage pressure professionally."},
            {"num": "03", "title": "Support fair play", "text": "Reliable baseball officials are essential to organized, fair, and well-run youth games."},
        ],
        looking_title="Who should apply",
        looking=[
            "People interested in becoming youth baseball umpires in Colorado.",
            "Former players, coaches, students, parents, and baseball fans.",
            "Applicants willing to learn rules, rotations, mechanics, and game management.",
            "Dependable people who want to represent baseball with professionalism.",
        ],
        band_title="Baseball needs more reliable umpires.",
        band_text="If you are ready to become a youth baseball umpire or baseball official in Colorado, contact Mile High Officials today.",
        band_primary=("Request more info", "/contact-us/"),
    ),
}

for slug, s in SPORT_PAGES.items():
    href = f"/youth-sports-officials/{slug}/"
    looking = ""
    if s.get("looking"):
        looking = f"""
    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What we’re looking for</p>
          <h2>{escape(s['looking_title'])}</h2>
        </div>
        <div class="list-block">
          <ul class="plain-list">
            {''.join(f'<li>{escape(i)}</li>' for i in s['looking'])}
          </ul>
        </div>
      </div>
    </section>
"""
    primary_href = s["band_primary"][1]
    page(href, s["title"], s["desc"], href,
f"""    <section class="page-hero">
      <div class="wrap">
        {sport_nav(href)}
        <p class="eyebrow">{escape(s['kicker'])}</p>
        <h1>{escape(s['h1'])}</h1>
        {''.join(f'<p class="lead">{escape(t)}</p>' for t in s['leads'])}
        <div class="actions">
          <a class="btn btn-primary" href="{s['cta'][1]}">{escape(s['cta'][0])}</a>
          <a class="btn btn-secondary" href="mailto:admin@milehighofficials.com">Email admin@milehighofficials.com</a>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        {cards_html(s['highlights'], 'cards cards-3')}
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">{escape(s['why_kicker'])}</p>
          <h2>{escape(s['why_title'])}</h2>
        </div>
        {cards_html(s['why'], 'cards cards-3' if len(s['why']) > 1 else 'cards')}
      </div>
    </section>
{looking}
    <section class="cta-band">
      <div class="wrap">
        <h2>{escape(s['band_title'])}</h2>
        <p>{escape(s['band_text'])}</p>
        <div class="actions">
          <a class="btn btn-primary" href="{primary_href}">{escape(s['band_primary'][0])}</a>
          <a class="btn btn-secondary" href="/contact-us/">Request more info</a>
        </div>
      </div>
    </section>
""")

page("/contact-us/", "Contact Us",
     "Contact Mile High Officials at 720-432-0354 or admin@milehighofficials.com, or send a message to become an official or request assigning services.",
     "/contact-us/",
"""    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">Contact Us</p>
        <h1>Ready to talk about officials?</h1>
        <p class="lead">Whether you want to become a youth sports official or need dependable assigning support for your organization, Mile High Officials is ready to connect.</p>
        <p class="lead">Email us directly at <a href="mailto:admin@milehighofficials.com">admin@milehighofficials.com</a>.</p>
        <div class="actions">
          <a class="btn btn-primary" href="tel:7204320354">Call 720-432-0354</a>
          <a class="btn btn-secondary" href="mailto:admin@milehighofficials.com?subject=Contact%20Mile%20High%20Officials">Email MHO</a>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap contact-grid">
        <form class="form" id="contact-form" action="/api/contact" method="post" novalidate>
          <h2 style="font-size:1.35rem">Send a message</h2>
          <p class="form-status" hidden></p>
          <div class="hp" aria-hidden="true">
            <label for="company">Company</label>
            <input type="text" id="company" name="company" tabindex="-1" autocomplete="off">
          </div>
          <div class="field">
            <label for="name">Name</label>
            <input id="name" name="name" type="text" autocomplete="name" required maxlength="120">
          </div>
          <div class="field">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" autocomplete="email" required maxlength="160">
          </div>
          <div class="field">
            <label for="phone">Phone</label>
            <input id="phone" name="phone" type="tel" autocomplete="tel" maxlength="40">
          </div>
          <div class="field">
            <label for="message">Message</label>
            <textarea id="message" name="message" required maxlength="4000" placeholder="Tell us about officiating interest, assigning needs, or a question."></textarea>
          </div>
          <button class="btn btn-primary" type="submit">Send message</button>
        </form>

        <aside class="contact-aside">
          <article class="card">
            <div class="card-num">Main phone</div>
            <h3><a href="tel:7204320354">720-432-0354</a></h3>
            <p>Call today to become a youth sports official with MHO.</p>
          </article>
          <article class="card" style="margin-top:1rem">
            <div class="card-num">Office address</div>
            <h3>150 Wells St #582</h3>
            <p>Erie, CO 80516</p>
            <p>Use this address for official business correspondence and organization contact details.</p>
          </article>
          <article class="card" style="margin-top:1rem">
            <div class="card-num">Email</div>
            <h3><a href="mailto:admin@milehighofficials.com">admin@milehighofficials.com</a></h3>
            <p>Best for questions about services, officiating opportunities, and general inquiries.</p>
          </article>
        </aside>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">How we help</p>
          <h2>One contact point. Multiple needs covered.</h2>
          <p>Reach out if you want to become an official, request assigning support, or ask a question about services and availability.</p>
        </div>
        """ + cards_html([
            {"num": "01", "title": "Become an official", "text": "Reach out if you want to step into youth sports officiating and learn more about expectations, opportunities, and next steps."},
            {"num": "02", "title": "Request services", "text": "Contact MHO if your league, tournament, or school needs dependable officials and organized assigning support."},
            {"num": "03", "title": "Ask questions", "text": "Use phone or email to ask about scheduling, availability, training, officiating standards, or service needs."},
        ], "cards cards-3") + """
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Best reasons to reach out</p>
          <h2>Fast, clear, and professional communication.</h2>
        </div>
        <div class="list-block">
          <ul class="plain-list">
            <li>You are interested in becoming a youth sports official.</li>
            <li>Your organization needs officials for basketball, baseball, football, or soccer.</li>
            <li>You want more information about MHO assigning services.</li>
            <li>You need a dependable contact for officiating support and coordination.</li>
            <li>You want to connect with a sports assigning company that values consistency and professionalism.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="cta-band">
      <div class="wrap">
        <h2>Call today or email admin@milehighofficials.com</h2>
        <p>We are ready to talk about becoming an official or assigning support for your program.</p>
        <div class="actions">
          <a class="btn btn-primary" href="tel:7204320354">Call 720-432-0354</a>
          <a class="btn btn-secondary" href="mailto:admin@milehighofficials.com?subject=Contact%20Mile%20High%20Officials">Email MHO</a>
        </div>
      </div>
    </section>
""")

# 404
page("/404.html", "Page not found",
     "The page you are looking for is not on the Mile High Officials website.",
     "/",
"""    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">404</p>
        <h1>We couldn’t find that page.</h1>
        <p class="lead">The link may be outdated. Head back to the home page or contact us and we’ll help you find the right place.</p>
        <div class="actions">
          <a class="btn btn-primary" href="/">Back to home</a>
          <a class="btn btn-secondary" href="/contact-us/">Contact us</a>
        </div>
      </div>
    </section>
""")

print("done")
