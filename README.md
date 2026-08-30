# SOLATX

Static public-record briefing for Austin ISD school finance, Austin history, and the 2025–26 budget cycle.

Owner: **f33boatx**. Not affiliated with Austin ISD or the State of Texas.

## Read order

1. `index.html` — problem vs one-year patch  
2. `history.html` — Edgewood, SB 7, why the press said Robin Hood  
3. `austin.html` — 1928 plan through 2026 closures  
3. `inflation.html` — $6,160 / $6,215 / inflation gap  
4. `campuses.html` — where cuts landed  
5. `money.html` — recapture tables  
6. `libraries.html` — June 18 amendment  
7. `questions.html` — tests, not verdicts  
8. `meetings.html` — local transcript search (no upload)  
9. `action.html` / `sources.html` / `about.html`

## Accuracy rules

- Prefer AISD and TEA tables. If two official pages disagree, show both (`money.html`).
- Meeting keyword counts are not findings.
- Footer credit is f33boatx only.

## Local preview

```bash
cd ~/solatx.org
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080/`. To search board subtitles, use the file picker on `meetings.html`.

## Deploy

GitHub Pages or any static host. `CNAME` is `solatx.org`. `_headers` applies on Netlify.
