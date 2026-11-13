#!/usr/bin/env python3
"""Bouwt de statische site in docs/. Gebruik: python3 build.py"""
import json, html, shutil, datetime
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
DOMAIN = "top10kindercadeaus.nl"
BASE = f"https://{DOMAIN}"
SITE = "Top 10 Kindercadeaus"
YEAR = 2026
UPDATED = datetime.date.today().strftime("%d-%m-%Y")
# Zet hier later het bol-partner-ID in; lege waarde = gewone links zonder commissie.
BOL_PARTNER_ID = ""
# Op False zetten na akkoord van de eigenaar (go-live); tot dan vragen we zoekmachines de site niet op te nemen.
NOINDEX = True
OWNER = {"naam": "[BEDRIJFSNAAM INVULLEN]", "adres": "Nieuwe Wetering", "kvk": "[KVK-NUMMER, IN AANVRAAG]",
         "btw": "[BTW-ID, IN AANVRAAG]", "email": f"info@{DOMAIN}"}

data = json.loads((ROOT / "data/lists.json").read_text(encoding="utf-8"))
e = html.escape

def shop_link(name):
    url = "https://www.bol.com/nl/nl/s/?searchtext=" + quote_plus(name)
    if BOL_PARTNER_ID:
        url = f"https://partner.bol.com/click/click?p=2&t=url&s={BOL_PARTNER_ID}&f=TXL&url={quote_plus(url)}"
    return url

REL = "sponsored nofollow noopener" if BOL_PARTNER_ID else "nofollow noopener"
NAV = [("/", "Home")] + [(f"/{l['slug']}/", l["age"]) for l in data["lists"]] + [("/speelgoed-van-het-jaar-2026/", "Speelgoed van het Jaar")]
DISCLOSURE = ('<p class="disclosure"><strong>Reclame:</strong> de knoppen naar winkels kunnen affiliate-links zijn. '
              'Koop je iets via zo\'n link, dan ontvangen wij mogelijk een kleine commissie. Jij betaalt niets extra. '
              '<a href="/over-ons/">Zo maken wij onze lijsten</a>.</p>')

def page(path, title, desc, body, schema=None):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == path else ""}>{e(t)}</a>' for h, t in NAV)
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    doc = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if NOINDEX else ""}
<link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}{path}">
<link rel="stylesheet" href="/style.css">
{ld}
</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="/"><span class="ten">10</span> Top 10 Kindercadeaus</a>
<nav aria-label="Hoofdmenu">{nav}</nav>
</div></header>
<main class="wrap">
{body}
</main>
<footer class="site"><div class="wrap">
<p>{e(SITE)} is een onafhankelijke cadeaugids voor ouders, opa's, oma's en iedereen die een kind iets leuks wil geven.</p>
<p><a href="/over-ons/">Over ons en werkwijze</a> · <a href="/privacy/">Privacy en cookies</a> · <a href="/contact/">Contact</a></p>
<p class="small">Merknamen zijn eigendom van de betreffende fabrikanten. Prijzen, voorraad en leeftijdsadvies controleer je altijd bij de winkel en op de verpakking.</p>
</div></footer>
</body>
</html>
"""
    target = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")

def item_html(i, it):
    badge = f'<p class="award">★ {e(it["award"])}</p>' if it.get("award") else ""
    return f"""<li class="item"><span class="rank">{i}</span><div>
<h2>{e(it["name"])}</h2>
<p class="meta">{e(it["brand"])} · {e(it["type"])}</p>{badge}
<p>{e(it["why"])}</p>
<a class="btn" href="{e(shop_link(it["name"]))}" rel="{REL}" target="_blank">Bekijk prijs en voorraad bij bol</a>
</div></li>"""

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT / "style.css", OUT / "style.css")
    (OUT / "CNAME").write_text(DOMAIN + "\n")
    (OUT / ".nojekyll").write_text("")
    urls = ["/"]

    cards = "".join(f'<a class="card" href="/{l["slug"]}/"><span class="age">{e(l["age"])}</span><span>Bekijk de top 10 →</span></a>' for l in data["lists"])
    page("/", f"{SITE} {YEAR}: de leukste cadeaus per leeftijd",
         "Top 10 cadeaus voor kinderen van 0 t/m 12 jaar, per leeftijd. Met de winnaars van Speelgoed van het Jaar 2026. Voor Sinterklaas, kerst en verjaardagen.",
         f"""<section class="hero"><h1>De leukste kindercadeaus, per leeftijd</h1>
<p>Sinterklaas, kerst of een verjaardag: in één minuut weet je wat je kunt geven. Tien cadeaus per leeftijdsgroep, met uitleg waarom ze op de lijst staan.</p></section>
<div class="cards">{cards}</div>
<section><h2>Hoe komen deze lijsten tot stand?</h2>
<p>Elke lijst combineert winnaars van de verkiezing <a href="/speelgoed-van-het-jaar-2026/">Speelgoed van het Jaar 2026</a> met klassiekers die al jaren goed vallen. We testen het speelgoed niet zelf en zeggen dat er ook eerlijk bij. Lees meer over <a href="/over-ons/">onze werkwijze</a>.</p></section>
{DISCLOSURE}""",
         {"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": BASE + "/"})

    for l in data["lists"]:
        path = f"/{l['slug']}/"; urls.append(path)
        items = "".join(item_html(i, it) for i, it in enumerate(l["items"], 1))
        others = " · ".join(f'<a href="/{o["slug"]}/">{e(o["age"])}</a>' for o in data["lists"] if o is not l)
        schema = {"@context": "https://schema.org", "@type": "ItemList", "name": l["title"],
                  "itemListElement": [{"@type": "ListItem", "position": i, "name": it["name"]} for i, it in enumerate(l["items"], 1)]}
        page(path, f"{l['title']} | {YEAR}", f"De 10 leukste cadeaus voor kinderen van {l['age']} in {YEAR}, met winnaars van Speelgoed van het Jaar en bewezen klassiekers.",
             f"""<h1>{e(l["title"])}</h1>
<p class="lead">{e(l["intro"])}</p>
{DISCLOSURE}
<ol class="list">{items}</ol>
<p class="note">Leeftijden zijn een richtlijn. Het leeftijdsadvies en de waarschuwingen van de fabrikant op de verpakking zijn leidend, zeker bij kinderen onder de 3 jaar (kleine onderdelen). Bijgewerkt op {UPDATED}.</p>
<p>Andere leeftijden: {others}</p>""", schema)

    path = "/speelgoed-van-het-jaar-2026/"; urls.append(path)
    cats = ""
    for cat, items in data["awards"].items():
        lis = "".join(f'<li><a href="{e(shop_link(it[0]))}" rel="{REL}" target="_blank">{e(it[0])}</a> <span class="meta">({e(it[1])})</span>{" <span class=pub>publiekswinnaar</span>" if len(it) > 2 else ""}</li>' for it in items)
        cats += f"<h2>{e(cat)}</h2><ul class='awards'>{lis}</ul>"
    page(path, "Speelgoed van het Jaar 2026: alle 33 winnaars op een rij",
         "Alle 33 vakjurywinnaars en de 11 publiekswinnaars van de verkiezing Speelgoed van het Jaar 2026, per categorie.",
         f"""<h1>Speelgoed van het Jaar 2026: alle winnaars</h1>
<p class="lead">De verkiezing Speelgoed van het Jaar bestaat sinds 1974. Een vakjury van twintig speelgoed- en spelexperts koos in 2026 in elf categorieën telkens drie winnaars. Daarna koos het publiek per categorie één favoriet.</p>
{DISCLOSURE}{cats}
<p class="note">Bron: de organisatie van de verkiezing Speelgoed van het Jaar. Deze site is niet verbonden aan de verkiezing.</p>""")

    path = "/over-ons/"; urls.append(path)
    page(path, f"Over ons en werkwijze | {SITE}", "Wie er achter Top 10 Kindercadeaus zit, hoe de lijsten worden gemaakt en hoe de site geld verdient.",
         f"""<h1>Over ons en onze werkwijze</h1>
<h2>Voor wie is deze site?</h2><p>Voor volwassenen die een cadeau zoeken voor een kind: ouders, grootouders, ooms, tantes en vrienden. De site is niet gericht op kinderen.</p>
<h2>Hoe maken wij de lijsten?</h2>
<ul><li>We nemen winnaars van de onafhankelijke verkiezing Speelgoed van het Jaar als basis.</li>
<li>We vullen aan met speelgoed en spellen die al jaren veel verkocht en gegeven worden.</li>
<li>We letten op spreiding: bouwen, spellen, creatief, buiten en leren.</li>
<li>We testen producten niet zelf. Waar we iets over een product zeggen, komt dat uit informatie van de fabrikant of de verkiezing.</li>
<li>De teksten zijn geschreven met hulp van AI en gecontroleerd door een mens.</li></ul>
<h2>Hoe verdient deze site geld?</h2><p>Met affiliate-links. Als je via een link op deze site iets koopt bij een winkel, ontvangen wij mogelijk een kleine commissie van die winkel. Dat kost jou niets extra. Winkels betalen niet voor een plek in de lijst.</p>
<h2>Wie zit erachter?</h2><p>{e(OWNER["naam"])}<br>{e(OWNER["adres"])}<br>KvK: {e(OWNER["kvk"])}<br>Btw-id: {e(OWNER["btw"])}<br>E-mail: <a href="mailto:{OWNER["email"]}">{OWNER["email"]}</a></p>""")

    path = "/privacy/"; urls.append(path)
    page(path, f"Privacy en cookies | {SITE}", "Welke gegevens Top 10 Kindercadeaus verwerkt en welke cookies de site gebruikt.",
         f"""<h1>Privacy en cookies</h1>
<p>Deze site is zo gemaakt dat er zo min mogelijk gegevens worden verwerkt.</p>
<h2>Cookies</h2><p>Deze site plaatst zelf geen cookies en gebruikt geen trackers of advertentienetwerken. Daarom zie je geen cookiemelding.</p>
<h2>Links naar winkels</h2><p>Klik je op een knop naar een winkel, dan verlaat je deze site. De winkel kan dan zelf cookies plaatsen, onder meer om te registreren dat je via ons kwam. Daarvoor geldt het privacy- en cookiebeleid van die winkel.</p>
<h2>Serverlogboeken</h2><p>De hostingpartij (GitHub Pages) kan technische gegevens zoals je IP-adres tijdelijk vastleggen om de site veilig te laten werken.</p>
<h2>E-mail</h2><p>Als je ons mailt, gebruiken we je bericht en e-mailadres alleen om te antwoorden. We bewaren e-mails maximaal twaalf maanden.</p>
<h2>Je rechten</h2><p>Je kunt inzage, correctie of verwijdering van je gegevens vragen via <a href="mailto:{OWNER["email"]}">{OWNER["email"]}</a>. Je kunt een klacht indienen bij de Autoriteit Persoonsgegevens.</p>
<p class="note">Verantwoordelijke: {e(OWNER["naam"])}, {e(OWNER["adres"])}. Laatst bijgewerkt op {UPDATED}.</p>""")

    path = "/contact/"; urls.append(path)
    page(path, f"Contact | {SITE}", "Neem contact op met Top 10 Kindercadeaus.",
         f"""<h1>Contact</h1><p>Een fout gezien, een tip of een vraag? Mail naar <a href="mailto:{OWNER["email"]}">{OWNER["email"]}</a>.</p>
<p>Vragen over een bestelling, levering of retour stel je aan de winkel waar je hebt gekocht. Wij verkopen zelf niets.</p>""")

    today = datetime.date.today().isoformat()
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(f"Gebouwd: {len(urls)} pagina's in {OUT}")

if __name__ == "__main__":
    build()
