#!/usr/bin/env python3
"""Stamp the left-rail chrome onto every SOLATX page.

Edit the story lists here, then run:

    python3 tools/stamp_chrome.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STORY_EN = [
    ("index.html", "01", "Start here"),
    ("history.html", "02", "Recapture is a court order"),
    ("austin.html", "03", "How Austin was drawn “rich”"),
    ("inflation.html", "04", "The allotment froze"),
    ("money.html", "05", "The recapture bill"),
    ("crisis.html", "06", "The 2026 budget “crisis”"),
    ("campuses.html", "07", "Campuses took the load"),
    ("libraries.html", "08", "The librarian bandage"),
    ("questions.html", "09", "What the meetings show"),
]
FILES_EN = [
    ("action.html", "What still needs doing"),
    ("sources.html", "Sources"),
    ("about.html", "About"),
]
STORY_ES = [
    ("inicio.html", "01", "Empiece aquí"),
    ("historia.html", "02", "La recaptura es orden de corte"),
    ("austin-es.html", "03", "Cómo Austin se volvió “rico”"),
    ("inflacion.html", "04", "Se congeló la asignación"),
    ("dinero.html", "05", "La factura de recaptura"),
    ("crisis-es.html", "06", "La “crisis” presupuestal 2026"),
    ("planteles.html", "07", "Los planteles cargaron"),
    ("bibliotecas.html", "08", "El parche de bibliotecarios"),
    ("preguntas.html", "09", "Lo que muestran las juntas"),
]
FILES_ES = [
    ("accion.html", "Qué falta hacer"),
    ("fuentes.html", "Fuentes"),
    ("acerca.html", "Acerca"),
]

# page -> (lang, alt href, you-are-here)
PAGES = {
    "index.html": ("en", "inicio.html", "01 · Start here"),
    "history.html": ("en", "historia.html", "02 · Recapture is a court order"),
    "austin.html": ("en", "austin-es.html", "03 · How Austin was drawn “rich”"),
    "inflation.html": ("en", "inflacion.html", "04 · The allotment froze"),
    "money.html": ("en", "dinero.html", "05 · The recapture bill"),
    "crisis.html": ("en", "crisis-es.html", "06 · The 2026 budget “crisis”"),
    "campuses.html": ("en", "planteles.html", "07 · Campuses took the load"),
    "libraries.html": ("en", "bibliotecas.html", "08 · The librarian bandage"),
    "questions.html": ("en", "preguntas.html", "09 · What the meetings show"),
    "action.html": ("en", "accion.html", "The files · What still needs doing"),
    "sources.html": ("en", "fuentes.html", "The files · Sources"),
    "about.html": ("en", "acerca.html", "The files · About"),
    "inicio.html": ("es", "index.html", "01 · Empiece aquí"),
    "historia.html": ("es", "history.html", "02 · La recaptura es orden de corte"),
    "austin-es.html": ("es", "austin.html", "03 · Cómo Austin se volvió “rico”"),
    "inflacion.html": ("es", "inflation.html", "04 · Se congeló la asignación"),
    "dinero.html": ("es", "money.html", "05 · La factura de recaptura"),
    "crisis-es.html": ("es", "crisis.html", "06 · La “crisis” presupuestal 2026"),
    "planteles.html": ("es", "campuses.html", "07 · Los planteles cargaron"),
    "bibliotecas.html": ("es", "libraries.html", "08 · El parche de bibliotecarios"),
    "preguntas.html": ("es", "questions.html", "09 · Lo que muestran las juntas"),
    "accion.html": ("es", "action.html", "Los archivos · Qué falta hacer"),
    "fuentes.html": ("es", "sources.html", "Los archivos · Fuentes"),
    "acerca.html": ("es", "about.html", "Los archivos · Acerca"),
}

PAGERS = {
    "history.html": (
        "index.html", "Start here",
        "austin.html", "How Austin was drawn",
    ),
    "austin.html": (
        "history.html", "Recapture is a court order",
        "inflation.html", "The allotment froze",
    ),
    "inflation.html": (
        "austin.html", "How Austin was drawn",
        "money.html", "The recapture bill",
    ),
    "money.html": (
        "inflation.html", "The allotment froze",
        "crisis.html", "The 2026 budget “crisis”",
    ),
    "crisis.html": (
        "money.html", "The recapture bill",
        "campuses.html", "Campuses took the load",
    ),
    "campuses.html": (
        "crisis.html", "The 2026 budget “crisis”",
        "libraries.html", "The librarian bandage",
    ),
    "libraries.html": (
        "campuses.html", "Campuses took the load",
        "questions.html", "Ask why",
    ),
    "questions.html": (
        "libraries.html", "The librarian bandage",
        "action.html", "What still needs doing",
    ),
    "historia.html": (
        "inicio.html", "Empiece aquí",
        "austin-es.html", "Cómo se dibujó Austin",
    ),
    "austin-es.html": (
        "historia.html", "La recaptura es orden de corte",
        "inflacion.html", "Se congeló la asignación",
    ),
    "inflacion.html": (
        "austin-es.html", "Cómo se dibujó Austin",
        "dinero.html", "La factura de recaptura",
    ),
    "dinero.html": (
        "inflacion.html", "Se congeló la asignación",
        "crisis-es.html", "La “crisis” presupuestal 2026",
    ),
    "crisis-es.html": (
        "dinero.html", "La factura de recaptura",
        "planteles.html", "Los planteles cargaron",
    ),
    "planteles.html": (
        "crisis-es.html", "La “crisis” presupuestal 2026",
        "bibliotecas.html", "El parche de bibliotecarios",
    ),
    "bibliotecas.html": (
        "planteles.html", "Los planteles cargaron",
        "preguntas.html", "Preguntar por qué",
    ),
    "preguntas.html": (
        "bibliotecas.html", "El parche de bibliotecarios",
        "accion.html", "Qué falta hacer",
    ),
}


def rail_links(items, current: str, numbered: bool) -> str:
    lines = []
    for row in items:
        href, *rest = row
        if numbered:
            num, label = rest
            inner = f'<span class="n">{num}</span><span>{label}</span>'
        else:
            label = rest[0]
            inner = f"<span>{label}</span>"
        cur = ' aria-current="page"' if href == current else ""
        lines.append(f'        <li><a href="{href}"{cur}>{inner}</a></li>')
    return "\n".join(lines)


def chrome(current: str, lang: str, alt: str, here: str) -> tuple[str, str]:
    if lang == "es":
        skip = "Saltar al contenido"
        home = "inicio.html"
        tagline = "Austin ISD, en el expediente"
        story_h = "La historia, en orden"
        story_note = "Recaptura, luego la “crisis” presupuestal. Léala de arriba abajo."
        files_h = "Los archivos"
        menu = "Menú"
        here_l = "Está aquí"
        lang_lab = "English"
        foot_note = "Registros públicos. No es AISD. No es el Estado de Texas."
        story, files = STORY_ES, FILES_ES
        brand_href = "inicio.html"
        ch_h, contact_h = "Capítulos", "Contacte a AISD, no a nosotros"
        blurb = "Educación comunitaria a partir de registros públicos. No está afiliado a Austin ISD ni al Estado de Texas. Verifique cada cifra en la <a href=\"fuentes.html\">página de fuentes</a>."
        comment = "Comentario público · 512-414-0130"
        still = ("accion.html", "Qué falta hacer")
        sources = ("fuentes.html", "Fuentes")
        footer_links = [
            ("historia.html", "Historia"),
            ("dinero.html", "Recaptura"),
            ("crisis-es.html", "La “crisis”"),
            ("planteles.html", "Planteles"),
            ("fuentes.html", "Fuentes"),
        ]
    else:
        skip = "Skip to content"
        home = "index.html"
        tagline = "Austin ISD, on the record"
        story_h = "The story, in order"
        story_note = "Recapture, then the budget “crisis.” Read top to bottom."
        files_h = "The files"
        menu = "Menu"
        here_l = "You are here"
        lang_lab = "Español"
        foot_note = "Public records. Not AISD. Not the State of Texas."
        story, files = STORY_EN, FILES_EN
        brand_href = "index.html"
        ch_h, contact_h = "Chapters", "Contact AISD, not us"
        blurb = "Community education from public records. Not affiliated with Austin ISD or the State of Texas. Verify every figure on the <a href=\"sources.html\">sources page</a>."
        comment = "Public comment · 512-414-0130"
        still = ("action.html", "What still needs doing")
        sources = ("sources.html", "Sources")
        footer_links = [
            ("history.html", "History"),
            ("money.html", "Recapture"),
            ("crisis.html", "The “crisis”"),
            ("campuses.html", "Campuses"),
            ("sources.html", "Sources"),
        ]

    header = f'''<a class="skip" href="#main">{skip}</a>
  <button class="backdrop" type="button" aria-label="Close menu"></button>
  <aside class="rail" id="site-nav">
    <a class="brand" href="{brand_href}">
      <img src="assets/img/mark.svg" alt="">
      <div>
        <strong>SOLATX</strong>
        <span>{tagline}</span>
      </div>
    </a>
    <p class="rail-tag">{story_h}</p>
    <p class="rail-note">{story_note}</p>
    <nav aria-label="{story_h}">
      <ol class="story">
{rail_links(story, current, True)}
      </ol>
    </nav>
    <p class="rail-tag">{files_h}</p>
    <nav aria-label="{files_h}">
      <ul class="files">
{rail_links(files, current, False)}
      </ul>
    </nav>
    <a class="lang" href="{alt}" lang="{'en' if lang == 'es' else 'es'}" hreflang="{'en' if lang == 'es' else 'es'}">{lang_lab}</a>
    <p class="rail-foot">{foot_note}</p>
  </aside>
  <header class="mast">
    <p class="here">{here_l}: <b>{here}</b></p>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">{menu}</button>
  </header>'''

    fl = "\n".join(f"            <li><a href=\"{h}\">{t}</a></li>" for h, t in footer_links)
    footer = f'''<footer class="site-footer">
    <div class="wrap">
      <div class="foot-grid">
        <div>
          <h2>SOLATX</h2>
          <p>{blurb}</p>
        </div>
        <div>
          <h2>{ch_h}</h2>
          <ul>
{fl}
          </ul>
        </div>
        <div>
          <h2>{contact_h}</h2>
          <ul>
            <li><a href="mailto:board@austinisd.org">board@austinisd.org</a></li>
            <li><a href="https://www.austinisd.org/board/meetings">{comment}</a></li>
            <li><a href="{still[0]}">{still[1]}</a></li>
          </ul>
        </div>
      </div>
      <p class="owner">© 2026 SOLATX. Owned by <strong>f33boatx</strong>. All rights reserved. Copyright and site ownership rest with f33boatx.</p>
    </div>
  </footer>'''
    return header, footer


def pager_html(page: str, lang: str) -> str | None:
    if page not in PAGERS:
        return None
    prev_h, prev_t, next_h, next_t = PAGERS[page]
    back = "Atrás" if lang == "es" else "Back"
    nxt = "Siguiente" if lang == "es" else "Next"
    return f'''        <div class="pager">
          <a href="{prev_h}"><small>{back}</small> ← {prev_t}</a>
          <a href="{next_h}"><small>{nxt}</small> {next_t} →</a>
        </div>'''


def stamp_file(name: str) -> None:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    lang, alt, here = PAGES[name]
    header, footer = chrome(name, lang, alt, here)

    new, n = re.subn(
        r'<a class="skip"[\s\S]*?</header>',
        header,
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"header pattern missed: {name} ({n})")
    new2, n2 = re.subn(
        r'<footer class="site-footer"[\s\S]*?</footer>',
        footer,
        new,
        count=1,
    )
    if n2 != 1:
        raise SystemExit(f"footer pattern missed: {name} ({n2})")

    pg = pager_html(name, lang)
    if pg:
        new3, n3 = re.subn(
            r'(?:      <div class="wrap pager">|        <div class="pager">)[\s\S]*?</div>',
            pg,
            new2,
            count=1,
        )
        if n3 == 0:
            new2 = new2.replace(
                "  </main>",
                f"    <section class=\"section\">\n      <div class=\"wrap\">\n{pg}\n      </div>\n    </section>\n  </main>",
                1,
            )
        else:
            new2 = new3

    path.write_text(new2, encoding="utf-8")
    print("stamped", name)


def main() -> None:
    for name in PAGES:
        if not (ROOT / name).exists():
            print("skip missing", name)
            continue
        stamp_file(name)


if __name__ == "__main__":
    main()
