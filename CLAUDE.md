# top10kindercadeaus.nl — instructions for AI assistants

A Dutch gift guide: top-10 lists of presents for children, per age group. The site earns affiliate
commission from retailers and sells nothing itself. This repository is **public**: commit only what
belongs on a public website. No plans, personal details, credentials or internal notes.

The project plan, decisions and open tasks live outside this repository, in the owner's project
guide. Read that first if you have access to it.

## Layout

| Path | What |
| --- | --- |
| `data/lists.json` | All content: four age lists of ten products, and the 33 Speelgoed van het Jaar 2026 winners |
| `build.py` | Generator. Reads the data, writes the whole site to `docs/` |
| `style.css` | Single stylesheet, copied into `docs/` by the build |
| `docs/` | Generated output, served by GitHub Pages from branch `main`. Never edit by hand |
| `docs/CNAME` | Custom domain, written by the build |

## Build and check

```
python3 build.py
python3 -m http.server 8765 -d docs   # then open http://localhost:8765/
```

Before every push: build, look at the home page and at least one list page at desktop width and at
phone width (about 390 px), and click through the navigation. Commit `docs/` together with the
source change that produced it.

## Settings in build.py

- `OWNER` — identity shown on the about and privacy pages. Placeholders in square brackets must be
  replaced with real details before go-live.
- `NOINDEX` — `True` adds a robots noindex tag to every page. Set to `False` only after the owner
  has approved go-live.
- `BOL_PARTNER_ID` — empty means plain bol search links without commission. **The affiliate URL
  format in `shop_link()` is unverified.** Confirm it against the bol partner dashboard before
  filling in the ID. With an ID set, links get `rel="sponsored"`.

## Content rules

1. Never invent product facts. If you cannot verify what a product does, state only what is
   verifiable: brand, category, award. No test claims, review scores, prices or stock claims.
2. The manufacturer's age advice leads. Verify it per product before placing a product in an age
   list.
3. Write for adults buying a present (parents, grandparents), in Dutch, informal "je". Never
   address children.
4. Every list page keeps the advertising notice at the top. Do not weaken or move it.
5. No product photos unless supplied through a retailer's affiliate programme. No generated images
   of branded toys or characters. No retailer or brand logos.
6. The site sets no cookies and loads no third-party scripts, which is why it has no cookie banner
   and why the privacy page says so. Do not add analytics, fonts, embeds or ad scripts from other
   domains without first updating the privacy page and adding consent.
7. Rankings follow the criteria on the about page. If the criteria change, change that page too.
8. Each list has exactly ten items.
9. When content changes, set `updated` in `data/lists.json` to that day. Pages show it as
   "Bijgewerkt op" and the sitemap uses it, so it must reflect a real content change, not a rebuild.

## Adding a page type

List pages are generated from the `lists` array in `data/lists.json`; a new list there becomes a
new page and is added to the sitemap. The navigation is built from the same array, so many new
lists need a navigation change in `build.py` (group them, do not show them all in the header).

## Going live

Pushing to `main` changes the live site once GitHub Pages is switched on. Keep unreviewed work on a
branch or behind `NOINDEX = True`. Going live, and any change to legal or identity text, needs the
owner's approval first.
