# SOLATX

Static public-record briefing for Austin ISD school finance, Austin history, and the 2025–26 budget cycle.

Owner: **f33boatx**. Not affiliated with Austin ISD or the State of Texas.

The site is an old-school left-rail contents list. The homepage is a front door. The story is the numbered pages.

## Read order

1. `index.html` — start here
2. `history.html` — Edgewood, SB 7, why the press said Robin Hood
3. `austin.html` — 1928 plan through 2026 closures
4. `inflation.html` — $6,160 / $6,215 / inflation gap
5. `money.html` — recapture tables
6. `crisis.html` — the 2026 budget “crisis” (wound vs bandage)
7. `campuses.html` — where cuts landed
8. `libraries.html` — June 18 amendment
9. `questions.html` — what the meetings show (rhetoric, silence, the dais)
10. `action.html` / `sources.html` / `about.html`

Meeting search, caption read, and yearbook are **out of this folder for now**. They are saved for editing at `~/solatx-hold/meetings-section/`.

Spanish mirrors start at `inicio.html`. The 2026 chapter is `crisis-es.html`.

## Accuracy rules

- Prefer AISD and TEA tables. If two official pages disagree, show both (`money.html`).
- Meeting keyword counts are not findings.
- Footer credit is f33boatx only.

## Local preview (see the site before any push)

This is a static folder. Nothing goes live until you deploy it. On this Kubuntu box the preview is:

```bash
cd ~/solatx.org
./preview.sh
```

That serves the folder at `http://127.0.0.1:8080/` and opens Firefox. Refresh the browser after you save a file.

There is no Dreamweaver-style “studio” installed. The combination that is already here:

- **Firefox** — look at the site (`http://127.0.0.1:8080/`)
- **Kate** — edit the HTML (`kate index.html` or open the folder in Kate)
- **preview.sh** — the local server, so CSS, the sidebar, and `data/aisd.json` all load

To change the left-hand list for every page, edit `tools/stamp_chrome.py` and run `python3 tools/stamp_chrome.py`.

## Deploy

GitHub Pages or any static host. `CNAME` is `solatx.org`. `_headers` applies on Netlify.
