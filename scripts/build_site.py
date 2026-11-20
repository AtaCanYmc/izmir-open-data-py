#!/usr/bin/env python3
"""Build site documentation pages for GitHub Pages.

Converts markdown docs into interactive, responsive HTML pages with anti-slop principles.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
SITE_DIR = ROOT_DIR / "site"
SPECS_DIR = SITE_DIR / "specs"

CATEGORY_MAP = {
    "afetler": {"cat": "afet", "icon": "afet.svg", "label": "Afet & Acil Durum"},
    "itfaiye": {"cat": "afet", "icon": "afet.svg", "label": "Afet & Acil Durum"},
    "eshot": {"cat": "ulasim", "icon": "ulasim.svg", "label": "Ulaşım & Hareketlilik"},
    "izban": {"cat": "ulasim", "icon": "ulasim.svg", "label": "Ulaşım & Hareketlilik"},
    "metro": {"cat": "ulasim", "icon": "ulasim.svg", "label": "Ulaşım & Hareketlilik"},
    "tramvay": {
        "cat": "ulasim",
        "icon": "ulasim.svg",
        "label": "Ulaşım & Hareketlilik",
    },
    "vapur": {"cat": "ulasim", "icon": "ulasim.svg", "label": "Ulaşım & Hareketlilik"},
    "tren": {"cat": "ulasim", "icon": "ulasim.svg", "label": "Ulaşım & Hareketlilik"},
    "taksi": {"cat": "ulasim", "icon": "ulasim.svg", "label": "Ulaşım & Hareketlilik"},
    "trafik": {"cat": "ulasim", "icon": "ulasim.svg", "label": "Ulaşım & Hareketlilik"},
    "otopark": {
        "cat": "ulasim",
        "icon": "ulasim.svg",
        "label": "Ulaşım & Hareketlilik",
    },
    "izmirimkart": {
        "cat": "ulasim",
        "icon": "ulasim.svg",
        "label": "Ulaşım & Hareketlilik",
    },
    "izum": {"cat": "ulasim", "icon": "ulasim.svg", "label": "Ulaşım & Hareketlilik"},
    "ulasim": {"cat": "ulasim", "icon": "ulasim.svg", "label": "Ulaşım & Hareketlilik"},
    "eczaneler": {"cat": "saglik", "icon": "saglik.svg", "label": "Sağlık & Eczane"},
    "saglik": {"cat": "saglik", "icon": "saglik.svg", "label": "Sağlık & Eczane"},
    "turuncucember": {
        "cat": "saglik",
        "icon": "saglik.svg",
        "label": "Sağlık & Eczane",
    },
    "ckan": {"cat": "dijital", "icon": "dijital.svg", "label": "Dijital & CKAN"},
    "veri": {"cat": "dijital", "icon": "dijital.svg", "label": "Dijital & CKAN"},
    "iztek": {"cat": "dijital", "icon": "dijital.svg", "label": "Dijital & CKAN"},
    "wizmirnet": {"cat": "dijital", "icon": "dijital.svg", "label": "Dijital & CKAN"},
    "yardimci": {"cat": "dijital", "icon": "dijital.svg", "label": "Dijital & CKAN"},
    "bisim": {
        "cat": "rekreasyon",
        "icon": "rekreasyon.svg",
        "label": "Rekreasyon & Spor",
    },
    "spor": {
        "cat": "rekreasyon",
        "icon": "rekreasyon.svg",
        "label": "Rekreasyon & Spor",
    },
    "plaj": {
        "cat": "rekreasyon",
        "icon": "rekreasyon.svg",
        "label": "Rekreasyon & Spor",
    },
    "tarihi": {"cat": "tarih", "icon": "tarih.svg", "label": "Tarih & Miras"},
    "tarih": {"cat": "tarih", "icon": "tarih.svg", "label": "Tarih & Miras"},
    "egitim": {"cat": "egitim", "icon": "egitim.svg", "label": "Eğitim"},
    "etkinlikler": {"cat": "kultur", "icon": "kultur.svg", "label": "Kültür Sanat"},
    "kutuphane": {"cat": "kultur", "icon": "kultur.svg", "label": "Kültür Sanat"},
    "izsu": {"cat": "yasam", "icon": "yasam.svg", "label": "Kentsel Yaşam"},
    "iklim": {"cat": "yasam", "icon": "yasam.svg", "label": "Kentsel Yaşam"},
    "cografi": {"cat": "yasam", "icon": "yasam.svg", "label": "Kentsel Yaşam"},
    "pazarlar": {"cat": "yasam", "icon": "yasam.svg", "label": "Kentsel Yaşam"},
    "sosyal": {"cat": "yasam", "icon": "yasam.svg", "label": "Kentsel Yaşam"},
    "tuvalet": {"cat": "yasam", "icon": "yasam.svg", "label": "Kentsel Yaşam"},
    "kamu": {"cat": "yonetim", "icon": "yonetim.svg", "label": "Yönetim & Hizmet"},
    "hizmet": {"cat": "yonetim", "icon": "yonetim.svg", "label": "Yönetim & Hizmet"},
    "muhtarliklar": {
        "cat": "yonetim",
        "icon": "yonetim.svg",
        "label": "Yönetim & Hizmet",
    },
}


def resolve_category(key: str) -> dict[str, str]:
    norm = re.sub(r"[^a-z]", "", key.lower())
    for k, v in CATEGORY_MAP.items():
        if k in norm:
            return v
    return {"cat": "dijital", "icon": "dijital.svg", "label": "Genel Veri"}


def get_common_head(
    title: str,
    description: str,
    relative_root: str = "",
    active_page: str = "",
    canonical_path: str = "",
    breadcrumb_name: str = "",
) -> str:
    canonical_url = f"https://atacanymc.github.io/izmir-open-data-py/{canonical_path}"
    og_image = "https://atacanymc.github.io/izmir-open-data-py/assets/logo.svg"

    json_ld: dict[str, object] = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": canonical_url,
                "url": canonical_url,
                "name": f"{title} · izmir-open-data-py",
                "description": description,
                "inLanguage": "tr",
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": "https://atacanymc.github.io/izmir-open-data-py/#website",
                    "url": "https://atacanymc.github.io/izmir-open-data-py/",
                    "name": "İzmir Open Data Python",
                },
            }
        ],
    }

    if breadcrumb_name:
        graph = json_ld["@graph"]
        assert isinstance(graph, list)
        graph.append(
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Ana Sayfa",
                        "item": "https://atacanymc.github.io/izmir-open-data-py/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": breadcrumb_name,
                        "item": canonical_url,
                    },
                ],
            }
        )

    json_ld_str = json.dumps(json_ld, indent=2, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light dark">
  <script>
    try {{
      const stored = localStorage.getItem("color-scheme");
      if (stored) {{
        document.querySelector('meta[name="color-scheme"]').content = stored;
        document.documentElement.setAttribute("data-theme", stored);
        document.documentElement.style.colorScheme = stored;
      }}
    }} catch (e) {{}}
  </script>
  
  <title>{title} · izmir-open-data-py</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="İzmir Open Data Python">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{title} · izmir-open-data-py">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:locale" content="tr_TR">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:url" content="{canonical_url}">
  <meta name="twitter:title" content="{title} · izmir-open-data-py">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{og_image}">

  <!-- Structured Data (JSON-LD) -->
  <script type="application/ld+json">
{json_ld_str}
  </script>
  
  <link rel="icon" type="image/svg+xml" href="{relative_root}assets/logo.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="{relative_root}styles.css">
</head>
<body>

  <!-- Site Header -->
  <header class="site-header">
    <div class="container nav-wrapper">
      <a href="{relative_root}index.html" class="brand-link" aria-label="İzmir Open Data Python Ana Sayfa">
        <img src="{relative_root}assets/logo.svg" alt="Logo" class="brand-logo" width="32" height="32">
        <span>izmir-open-data-py</span>
        <span class="version-pill">v0.3.0</span>
      </a>

      <nav class="nav-menu" aria-label="Ana Gezinti">
        <a href="{relative_root}index.html#playground" class="nav-link">Canlı Demo</a>
        <a href="{relative_root}index.html#features" class="nav-link">Özellikler</a>
        <a href="{relative_root}index.html#categories" class="nav-link">Kategoriler</a>
        <a href="{relative_root}ENDPOINTS.html" class="nav-link {"active" if active_page == "endpoints" else ""}" {'aria-current="page"' if active_page == "endpoints" else ""}>Uç Noktalar</a>
        <a href="{relative_root}CLI.html" class="nav-link {"active" if active_page == "cli" else ""}" {'aria-current="page"' if active_page == "cli" else ""}>CLI</a>
        <a href="{relative_root}MCP.html" class="nav-link {"active" if active_page == "mcp" else ""}" {'aria-current="page"' if active_page == "mcp" else ""}>MCP</a>
        <a href="{relative_root}specs/index.html" class="nav-link {"active" if active_page == "specs" else ""}" {'aria-current="page"' if active_page == "specs" else ""}>Şartnameler</a>
      </nav>

      <div class="header-actions">
        <!-- Theme Toggle Button -->
        <button type="button" id="theme-toggle" class="theme-toggle-btn" aria-label="Temayı değiştir">
          <svg class="theme-icon-light" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <svg class="theme-icon-dark" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>

        <a href="https://github.com/AtaCanYmc/izmir-open-data-py" class="btn-github" target="_blank" rel="noopener noreferrer">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
          </svg>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </header>"""


def get_common_footer(relative_root: str = "") -> str:
    return f"""  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div style="display: flex; align-items: center; gap: 0.6rem; font-weight: 700; font-size: 1.125rem;">
            <img src="{relative_root}assets/logo.svg" alt="Logo" width="24" height="24">
            <span>izmir-open-data-py</span>
          </div>
          <p class="footer-brand-desc">
            İzmir Büyükşehir Belediyesi Açık Veri Portalı için bağımsız, açık kaynaklı Python istemcisi, terminal aracı ve Model Context Protocol sunucusu.
          </p>
        </div>

        <div>
          <div class="footer-heading">Dokümantasyon</div>
          <ul class="footer-links">
            <li><a href="{relative_root}ENDPOINTS.html" class="footer-link">Uç Nokta Listesi</a></li>
            <li><a href="{relative_root}CLI.html" class="footer-link">CLI Kılavuzu</a></li>
            <li><a href="{relative_root}MCP.html" class="footer-link">Model Context Protocol (MCP)</a></li>
            <li><a href="{relative_root}specs/index.html" class="footer-link">Resmi Şartnameler (Specs)</a></li>
          </ul>
        </div>

        <div>
          <div class="footer-heading">Topluluk & Dağıtım</div>
          <ul class="footer-links">
            <li><a href="https://github.com/AtaCanYmc/izmir-open-data-py" class="footer-link" target="_blank" rel="noopener noreferrer">GitHub Deposu</a></li>
            <li><a href="https://github.com/AtaCanYmc/homebrew-tap" class="footer-link" target="_blank" rel="noopener noreferrer">Homebrew Tap</a></li>
            <li><a href="https://pypi.org/project/izmir-open-data-py/" class="footer-link" target="_blank" rel="noopener noreferrer">PyPI Paketi</a></li>
            <li><a href="https://acikveri.bizizmir.com/" class="footer-link" target="_blank" rel="noopener noreferrer">İzmir Açık Veri Portalı</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div>Apache-2.0 Lisansı · Copyright © 2026 Ata Can Yaymacı.</div>
        <div>İzmir Büyükşehir Belediyesi ile resmi bağlantısı bulunmayan açık kaynak topluluk projesidir.</div>
      </div>
    </div>
  </footer>

  <script src="{relative_root}app.js"></script>
</body>
</html>"""


def build_endpoints_html() -> None:
    endpoints_md = DOCS_DIR / "ENDPOINTS.md"
    content = endpoints_md.read_text(encoding="utf-8")
    lines = content.splitlines()

    sections: list[dict[str, object]] = []
    current_sec: dict[str, object] | None = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            title_line = stripped[3:].strip()
            title = title_line
            namespace = ""
            m = re.match(r"^(.*?)\s*\(`(.*?)`\)", title_line)
            if m:
                title = m.group(1).strip()
                namespace = m.group(2).strip()

            cat_info = resolve_category(title)
            current_sec = {
                "title": title,
                "namespace": namespace,
                "category": cat_info["cat"],
                "icon": cat_info["icon"],
                "category_label": cat_info["label"],
                "methods": [],
            }
            sections.append(current_sec)
            continue

        if stripped.startswith("|") and current_sec is not None:
            if (
                "Metod Adı" in stripped
                or "Fonksiyon / Sınıf" in stripped
                or "---" in stripped
            ):
                continue

            parts = [p.strip() for p in stripped.split("|") if p.strip()]
            if len(parts) >= 2:
                name = parts[0].replace("`", "")
                desc = parts[1]
                if len(parts) >= 3 and "Yardımcı" in str(current_sec["title"]):
                    desc = (
                        f"{parts[2]} (Modül: <code>{parts[1].replace('`', '')}</code>)"
                    )
                methods = current_sec["methods"]
                assert isinstance(methods, list)
                methods.append({"name": name, "desc": desc})

    total_methods = sum(
        len(s["methods"]) for s in sections if isinstance(s["methods"], list)
    )

    cards_html = []
    for s in sections:
        methods = s["methods"]
        assert isinstance(methods, list)
        if not methods:
            continue

        rows_html = []
        for m in methods:
            row_search = html.escape(
                f"{m['name'].lower()} {m['desc'].lower()}", quote=True
            )
            rows_html.append(
                f"""                <tr class="endpoint-row" data-search="{row_search}">
                  <td><code class="method-chip">{html.escape(m["name"])}</code></td>
                  <td>{m["desc"]}</td>
                </tr>"""
            )

        ns_badge = (
            f'<span class="doc-card-badge">{html.escape(str(s["namespace"]))}</span>'
            if s["namespace"]
            else ""
        )
        escaped_title = html.escape(str(s["title"]), quote=True).lower()
        escaped_ns = html.escape(str(s["namespace"]), quote=True).lower()
        cards_html.append(
            f"""      <section class="doc-card endpoint-module-card" data-category="{s["category"]}" data-title="{escaped_title}" data-namespace="{escaped_ns}">
        <div class="doc-card-header">
          <div class="doc-card-title">
            <div class="category-icon-wrap" style="width: 32px; height: 32px;">
              <img src="assets/categories/{s["icon"]}" alt="{s["category_label"]}" class="category-icon" width="18" height="18">
            </div>
            <h2 class="doc-card-heading">{s["title"]}</h2>
            {ns_badge}
          </div>
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span class="doc-card-badge" style="background: rgba(2, 132, 199, 0.05); color: var(--text-muted);">{s["category_label"]}</span>
            <span class="text-muted" style="font-size: 0.8125rem;">{len(methods)} metot</span>
          </div>
        </div>
        <div class="doc-table-wrapper">
          <table class="doc-table">
            <thead>
              <tr>
                <th style="width: 38%;">Metot / Fonksiyon</th>
                <th>Açıklama</th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows_html)}
            </tbody>
          </table>
        </div>
      </section>"""
        )

    cards_str = "\n".join(cards_html)
    ulasim_count = len([s for s in sections if s["category"] == "ulasim"])

    body_content = f"""  <main class="doc-page">
    <div class="container">
      <nav class="breadcrumb-nav" aria-label="Ekmek kırıntısı">
        <a href="index.html" class="breadcrumb-link">Ana Sayfa</a>
        <span>/</span>
        <span class="text-secondary">Dokümantasyon</span>
        <span>/</span>
        <span aria-current="page">Uç Noktalar</span>
      </nav>

      <div class="doc-hero-with-illustration">
        <div class="doc-hero-text">
          <h1 class="doc-title">İzmir Open Data Python Uç Nokta Kataloğu</h1>
          <p class="doc-lead">
            İzmir Büyükşehir Belediyesi Açık Veri Portalı ve REST web servislerinin <code>izmir-open-data-py</code> istemcisi içindeki asenkron modül, metot, veri bilimi ve normalleştirici referansı.
          </p>

          <div class="doc-search-wrapper">
            <div class="doc-search-box">
              <svg class="doc-search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input 
                type="search" 
                id="endpoint-search-input" 
                class="doc-search-input" 
                placeholder="Uç nokta veya metot ara (örn: eshot, nobetci, baraj, ckan, to_dataframe)..." 
                aria-label="Uç noktalarda ara"
                autocomplete="off"
              >
            </div>
            <div class="doc-search-stats" id="endpoint-search-stats" aria-live="polite">
              Toplam {len(sections)} servis grubu ve {total_methods} metot listeleniyor.
            </div>
          </div>

          <!-- Category Quick Filter Buttons -->
          <div class="doc-quick-filters" role="group" aria-label="Kategoriye göre filtrele">
            <button type="button" class="quick-filter-btn" data-filter="all" aria-pressed="true">
              <span>Tümü</span>
            </button>
            <button type="button" class="quick-filter-btn" data-filter="ulasim">
              <img src="assets/categories/ulasim.svg" class="quick-filter-icon" alt="">
              <span>Ulaşım ({ulasim_count})</span>
            </button>
            <button type="button" class="quick-filter-btn" data-filter="saglik">
              <img src="assets/categories/saglik.svg" class="quick-filter-icon" alt="">
              <span>Sağlık & Eczane</span>
            </button>
            <button type="button" class="quick-filter-btn" data-filter="yasam">
              <img src="assets/categories/yasam.svg" class="quick-filter-icon" alt="">
              <span>Kentsel Yaşam & Su</span>
            </button>
            <button type="button" class="quick-filter-btn" data-filter="afet">
              <img src="assets/categories/afet.svg" class="quick-filter-icon" alt="">
              <span>Afet & İtfaiye</span>
            </button>
            <button type="button" class="quick-filter-btn" data-filter="dijital">
              <img src="assets/categories/dijital.svg" class="quick-filter-icon" alt="">
              <span>CKAN & Veri Bilimi</span>
            </button>
            <button type="button" class="quick-filter-btn" data-filter="rekreasyon">
              <img src="assets/categories/rekreasyon.svg" class="quick-filter-icon" alt="">
              <span>BİSİM & Spor</span>
            </button>
            <button type="button" class="quick-filter-btn" data-filter="kultur">
              <img src="assets/categories/kultur.svg" class="quick-filter-icon" alt="">
              <span>Kültür & Etkinlik</span>
            </button>
          </div>
        </div>

        <div class="doc-hero-image-wrap">
          <img src="assets/illustrations/smart_city.svg" alt="İzmir Akıllı Şehir Açık Veri Ağı" class="doc-hero-img" width="220" height="180">
        </div>
      </div>

      <div id="endpoint-modules-container">
{cards_str}
      </div>
    </div>
  </main>

  <script>
    document.addEventListener("DOMContentLoaded", () => {{
      const searchInput = document.getElementById("endpoint-search-input");
      const statsEl = document.getElementById("endpoint-search-stats");
      const cards = document.querySelectorAll(".endpoint-module-card");
      const filterBtns = document.querySelectorAll(".quick-filter-btn");
      const totalCount = {total_methods};

      let activeCategory = "all";

      function updateResults() {{
        const query = searchInput.value.trim().toLowerCase();
        let visibleCards = 0;
        let matchedMethods = 0;

        cards.forEach(card => {{
          const cardCat = card.getAttribute("data-category") || "";
          const cardTitle = card.getAttribute("data-title") || "";
          const cardNs = card.getAttribute("data-namespace") || "";
          const rows = card.querySelectorAll(".endpoint-row");

          const matchesCategory = activeCategory === "all" || cardCat === activeCategory;

          if (!matchesCategory) {{
            card.style.display = "none";
            return;
          }}

          if (!query) {{
            card.style.display = "";
            rows.forEach(r => r.style.display = "");
            visibleCards++;
            matchedMethods += rows.length;
            return;
          }}

          let cardMatches = 0;
          const cardHeaderMatch = cardTitle.includes(query) || cardNs.includes(query);

          rows.forEach(row => {{
            const rowText = row.getAttribute("data-search") || "";
            if (cardHeaderMatch || rowText.includes(query)) {{
              row.style.display = "";
              cardMatches++;
              matchedMethods++;
            }} else {{
              row.style.display = "none";
            }}
          }});

          if (cardMatches > 0) {{
            card.style.display = "";
            visibleCards++;
          }} else {{
            card.style.display = "none";
          }}
        }});

        if (query || activeCategory !== "all") {{
          statsEl.textContent = `Filtrelenen: ${{matchedMethods}} metot (${{visibleCards}} servis grubu).`;
        }} else {{
          statsEl.textContent = `Toplam ${{cards.length}} servis grubu ve ${{totalCount}} metot listeleniyor.`;
        }}
      }}

      if (searchInput) {{
        searchInput.addEventListener("input", updateResults);
      }}

      filterBtns.forEach(btn => {{
        btn.addEventListener("click", () => {{
          filterBtns.forEach(b => b.setAttribute("aria-pressed", "false"));
          btn.setAttribute("aria-pressed", "true");
          activeCategory = btn.getAttribute("data-filter") || "all";
          updateResults();
        }});
      }});
    }});
  </script>"""

    head = get_common_head(
        title="Uç Nokta Kataloğu (API Reference)",
        description="İzmir Büyükşehir Belediyesi Açık Veri Portalı tüm API uç noktaları, ESHOT, İZSU, BİSİM, CKAN ve Python SDK metotları referansı.",
        relative_root="",
        active_page="endpoints",
        canonical_path="ENDPOINTS.html",
        breadcrumb_name="Uç Noktalar",
    )
    footer = get_common_footer()

    out_file = SITE_DIR / "ENDPOINTS.html"
    out_file.write_text(f"{head}\n{body_content}\n{footer}", encoding="utf-8")
    print("Generated site/ENDPOINTS.html")


def build_cli_html() -> None:
    body_content = """  <main class="doc-page">
    <div class="container" style="max-width: 920px;">
      <nav class="breadcrumb-nav" aria-label="Ekmek kırıntısı">
        <a href="index.html" class="breadcrumb-link">Ana Sayfa</a>
        <span>/</span>
        <span class="text-secondary">Dokümantasyon</span>
        <span>/</span>
        <span aria-current="page">CLI Kılavuzu</span>
      </nav>

      <div class="doc-hero-with-illustration">
        <div class="doc-hero-text">
          <h1 class="doc-title">Terminal CLI Kılavuzu</h1>
          <p class="doc-lead">
            <code>izmir-open-data-py</code>, belediye açık veri portallarını terminal üzerinden sorgulamak, filtrelemek ve ASCII tabloları halinde görselleştirmek için <code>izmir-data</code> komut satırı aracını sunar.
          </p>
        </div>
        <div class="doc-hero-image-wrap">
          <img src="assets/illustrations/map_mobility.svg" alt="Terminal Hareketlilik Haritası" class="doc-hero-img" width="220" height="180">
        </div>
      </div>

      <div class="doc-section">
        <h2>Kurulum ve Paket Yöneticileri</h2>

        <h3 style="margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 1.125rem;">1. Homebrew ile Kurulum (macOS / Linux - Önerilen CLI)</h3>
        <p class="text-secondary">İzole ortamda resmi tap üzerinden CLI ve MCP araçlarını kurmak için:</p>

        <div class="doc-code-block">
          <div class="doc-code-header">
            <span>bash</span>
            <button type="button" class="copy-btn" data-copy="brew install AtaCanYmc/tap/izmir-data" aria-label="Komutu kopyala">Kopyala</button>
          </div>
          <div class="doc-code-content"># AtaCanYmc/tap üzerinden tek komutla kurulum
brew install AtaCanYmc/tap/izmir-data

# Alternatif olarak tap ekleyip kurma:
# brew tap AtaCanYmc/tap && brew install izmir-data</div>
        </div>

        <h3 style="margin-top: 2rem; margin-bottom: 0.5rem; font-size: 1.125rem;">2. uvx / pipx ile Anında Çalıştırma (Kurulumsuz)</h3>
        <p class="text-secondary">Sisteminizde Python ortamı kirletmeden tek komutla çalıştırma:</p>
        
        <div class="doc-code-block">
          <div class="doc-code-header">
            <span>bash</span>
            <button type="button" class="copy-btn" data-copy="uvx --from izmir-open-data-py izmir-data get nobetcieczaneler" aria-label="Komutu kopyala">Kopyala</button>
          </div>
          <div class="doc-code-content"># uvx ile çalıştırma (Hızlı ve izole)
uvx --from izmir-open-data-py izmir-data get nobetcieczaneler

# pipx ile çalıştırma
pipx run --spec izmir-open-data-py izmir-data get cbs/bisimistasyon</div>
        </div>

        <h3 style="margin-top: 2rem; margin-bottom: 0.5rem; font-size: 1.125rem;">3. pip / uv ile Global veya Sanal Ortam Kurulumu</h3>
        <div class="doc-code-block">
          <div class="doc-code-header">
            <span>bash</span>
            <button type="button" class="copy-btn" data-copy="pip install izmir-open-data-py" aria-label="Komutu kopyala">Kopyala</button>
          </div>
          <div class="doc-code-content"># pip ile kurulum
pip install izmir-open-data-py

# uv ile proje ortamına ekleme
uv add izmir-open-data-py</div>
        </div>
      </div>

      <div class="doc-section">
        <h2>Komut Referansı</h2>
        <div class="doc-card" style="margin-top: 1rem;">
          <div class="doc-table-wrapper">
            <table class="doc-table">
              <thead>
                <tr>
                  <th style="width: 22%;">Komut</th>
                  <th style="width: 32%;">Parametreler</th>
                  <th>Açıklama</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code class="method-chip">get</code></td>
                  <td><code>&lt;dataset_id&gt;</code></td>
                  <td>Belirtilen veri seti kimliğine ait kayıtları çeker ve terminal tablosunda listeler.</td>
                </tr>
                <tr>
                  <td><code class="method-chip">search</code></td>
                  <td><code>&lt;query&gt; [-l limit]</code></td>
                  <td>Portaldaki 260+ veri setini arar ve kaynak sayılarıyla birlikte listeler.</td>
                </tr>
                <tr>
                  <td><code class="method-chip">datastore</code></td>
                  <td><code>&lt;resource_id&gt; [-l limit] [-q query]</code></td>
                  <td>Herhangi bir CKAN Datastore UUID'sinden canlı kayıtları çeker ve tablolar.</td>
                </tr>
                <tr>
                  <td><code class="method-chip">--help</code></td>
                  <td>-</td>
                  <td>Komut satırı kullanım kılavuzunu ve seçenekleri görüntüler.</td>
                </tr>
                <tr>
                  <td><code class="method-chip">--version</code></td>
                  <td>-</td>
                  <td>Yüklü paket sürümünü görüntüler.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="doc-section">
        <h2>Detaylı Kullanım Senaryoları & Örnekler</h2>
        
        <div class="doc-card" style="padding: 1.5rem; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <img src="assets/categories/rekreasyon.svg" width="20" height="20" alt="">
            <h3 style="font-size: 1rem;">1. BİSİM Akıllı Bisiklet İstasyonları</h3>
          </div>
          <p class="text-secondary" style="font-size: 0.875rem; margin-bottom: 0.75rem;">
            İzmir genelindeki tüm BİSİM istasyonlarının koordinat ve kapasite bilgilerini çeker:
          </p>
          <div class="doc-code-block" style="margin: 0;">
            <div class="doc-code-header">
              <span>bash</span>
              <button type="button" class="copy-btn" data-copy="izmir-data get cbs/bisimistasyon" aria-label="Kopyala">Kopyala</button>
            </div>
            <div class="doc-code-content">izmir-data get cbs/bisimistasyon</div>
          </div>
        </div>

        <div class="doc-card" style="padding: 1.5rem; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <img src="assets/categories/ulasim.svg" width="20" height="20" alt="">
            <h3 style="font-size: 1rem;">2. Canlı Otopark Doluluk Verileri</h3>
          </div>
          <p class="text-secondary" style="font-size: 0.875rem; margin-bottom: 0.75rem;">
            İZELMAN otoparklarının anlık boş kapasiteleri ve toplam kontenjanları:
          </p>
          <div class="doc-code-block" style="margin: 0;">
            <div class="doc-code-header">
              <span>bash</span>
              <button type="button" class="copy-btn" data-copy="izmir-data get otopark/otoparklar" aria-label="Kopyala">Kopyala</button>
            </div>
            <div class="doc-code-content">izmir-data get otopark/otoparklar</div>
          </div>
        </div>

        <div class="doc-card" style="padding: 1.5rem; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <img src="assets/categories/dijital.svg" width="20" height="20" alt="">
            <h3 style="font-size: 1rem;">3. CKAN Veri Seti Arama (Package Search)</h3>
          </div>
          <p class="text-secondary" style="font-size: 0.875rem; margin-bottom: 0.75rem;">
            Portaldaki 260+ veri seti arasında anahtar kelime ile arama:
          </p>
          <div class="doc-code-block" style="margin: 0;">
            <div class="doc-code-header">
              <span>bash</span>
              <button type="button" class="copy-btn" data-copy="izmir-data search itfaiye -l 5" aria-label="Kopyala">Kopyala</button>
            </div>
            <div class="doc-code-content"># İtfaiye ile ilgili ilk 5 veri setini listele
izmir-data search itfaiye -l 5

# Tuvalet veri setlerini ara
izmir-data search tuvalet</div>
          </div>
        </div>

        <div class="doc-card" style="padding: 1.5rem; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <img src="assets/categories/dijital.svg" width="20" height="20" alt="">
            <h3 style="font-size: 1rem;">4. Canlı Datastore Sorgulama (Resource UUID)</h3>
          </div>
          <p class="text-secondary" style="font-size: 0.875rem; margin-bottom: 0.75rem;">
            Belirli bir CKAN tablosundan canlı kayıtları filtreleyip tablolar:
          </p>
          <div class="doc-code-block" style="margin: 0;">
            <div class="doc-code-header">
              <span>bash</span>
              <button type="button" class="copy-btn" data-copy="izmir-data datastore d87de3c1-9bc0-4a8c-842a-90cd2a30d03a -l 10" aria-label="Kopyala">Kopyala</button>
            </div>
            <div class="doc-code-content">izmir-data datastore d87de3c1-9bc0-4a8c-842a-90cd2a30d03a -l 10</div>
          </div>
        </div>
      </div>

      <div class="doc-section">
        <h2>Boru Hatları & Kabuk Entegrasyonu (Pipelines)</h2>
        <p class="text-secondary">
          <code>izmir-data</code> komutları Unix felsefesine uygun olarak tasarlanmıştır. Çıktıları <code>grep</code>, <code>fzf</code>, <code>awk</code> veya <code>crontab</code> süreçlerine bağlayabilirsiniz.
        </p>

        <div class="doc-code-block" style="margin-top: 1rem;">
          <div class="doc-code-header"><span>Boru Hattı Örneği</span></div>
          <div class="doc-code-content"># Nöbetçi eczaneler arasından sadece Konak ilçesini filtreleme
izmir-data get nobetcieczaneler | grep -i "Konak"

# Günlük otopark durumunu bir metin dosyasına arşivleme (Cronjob)
0 * * * * izmir-data get otopark/otoparklar >> /var/log/izmir_otopark.log</div>
        </div>
      </div>
    </div>
  </main>"""

    head = get_common_head(
        title="CLI Kullanım Kılavuzu",
        description="İzmir Açık Veri terminal aracı (izmir-data) kullanım kılavuzu. Canlı ESHOT, İZSU, BİSİM ve CKAN sorgulama komutları.",
        relative_root="",
        active_page="cli",
        canonical_path="CLI.html",
        breadcrumb_name="CLI Kılavuzu",
    )
    footer = get_common_footer()

    out_file = SITE_DIR / "CLI.html"
    out_file.write_text(f"{head}\n{body_content}\n{footer}", encoding="utf-8")
    print("Generated site/CLI.html")


def build_mcp_html() -> None:
    body_content = """  <main class="doc-page">
    <div class="container" style="max-width: 920px;">
      <nav class="breadcrumb-nav" aria-label="Ekmek kırıntısı">
        <a href="index.html" class="breadcrumb-link">Ana Sayfa</a>
        <span>/</span>
        <span class="text-secondary">Dokümantasyon</span>
        <span>/</span>
        <span aria-current="page">Model Context Protocol</span>
      </nav>

      <div class="doc-hero-with-illustration">
        <div class="doc-hero-text">
          <h1 class="doc-title">Model Context Protocol (MCP) Sunucusu</h1>
          <p class="doc-lead">
            <code>izmir-open-data-py</code>, FastMCP altyapısı üzerine inşa edilmiş tam uyumlu bir MCP sunucusu içerir. Claude Desktop, Cursor veya yerel AI ajanlarının İzmir Açık Veri API'lerini doğrudan çalıştırmasını sağlar.
          </p>
        </div>
        <div class="doc-hero-image-wrap">
          <img src="assets/illustrations/city_analytics.svg" alt="MCP Şehir Analitiği ve Yapay Zeka" class="doc-hero-img" width="220" height="180">
        </div>
      </div>

      <div class="doc-section">
        <h2>Sunucuyu Başlatma</h2>
        <p class="text-secondary">MCP sunucusu standart girdi ve çıktı (<code>stdio</code>) üzerinden çalışır:</p>

        <div class="doc-code-block">
          <div class="doc-code-header">
            <span>bash</span>
            <button type="button" class="copy-btn" data-copy="uvx --from izmir-open-data-py izmir-mcp" aria-label="Kopyala">Kopyala</button>
          </div>
          <div class="doc-code-content"># uvx ile anında çalıştırma (Önerilen)
uvx --from izmir-open-data-py izmir-mcp

# Homebrew (brew install AtaCanYmc/tap/izmir-data) veya global paket ile:
izmir-mcp</div>
        </div>
      </div>

      <div class="doc-section">
        <h2>İstemci Entegrasyonları & Yapılandırma</h2>

        <h3 style="margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 1.125rem;">1. Claude Desktop Entegrasyonu</h3>
        <p class="text-secondary">
          <code>~/Library/Application Support/Claude/claude_desktop_config.json</code> (macOS) veya <code>%APPDATA%\\Claude\\claude_desktop_config.json</code> (Windows) dosyasına aşağıdaki sunucu tanımını ekleyin:
        </p>

        <div class="doc-code-block">
          <div class="doc-code-header">
            <span>claude_desktop_config.json</span>
            <button type="button" class="copy-btn" data-copy='{\\n  "mcpServers": {\\n    "izmir-open-data": {\\n      "command": "uvx",\\n      "args": ["--from", "izmir-open-data-py", "izmir-mcp"]\\n    }\\n  }\\n}' aria-label="Kopyala">Kopyala</button>
          </div>
          <div class="doc-code-content">{
  "mcpServers": {
    "izmir-open-data": {
      "command": "uvx",
      "args": ["--from", "izmir-open-data-py", "izmir-mcp"]
    }
  }
}</div>
        </div>

        <h3 style="margin-top: 2rem; margin-bottom: 0.5rem; font-size: 1.125rem;">2. Cursor IDE Entegrasyonu</h3>
        <p class="text-secondary">
          Proje kök dizinindeki <code>.cursor/mcp.json</code> dosyasında MCP sunucusunu tanımlayın:
        </p>

        <div class="doc-code-block">
          <div class="doc-code-header">
            <span>.cursor/mcp.json</span>
            <button type="button" class="copy-btn" data-copy='{\\n  "mcpServers": {\\n    "izmir-api": {\\n      "command": "uvx",\\n      "args": ["--from", "izmir-open-data-py", "izmir-mcp"]\\n    }\\n  }\\n}' aria-label="Kopyala">Kopyala</button>
          </div>
          <div class="doc-code-content">{
  "mcpServers": {
    "izmir-api": {
      "command": "uvx",
      "args": ["--from", "izmir-open-data-py", "izmir-mcp"]
    }
  }
}</div>
        </div>
      </div>

      <div class="doc-section">
        <h2>Sağlanan Araçlar (Tools Reference)</h2>
        <div class="doc-card" style="margin-top: 1rem;">
          <div class="doc-card-header">
            <span class="doc-card-title">1. list_endpoints</span>
            <span class="doc-card-badge">Discovery Tool</span>
          </div>
          <div style="padding: 1.25rem;">
            <p class="text-secondary" style="font-size: 0.9375rem; margin-bottom: 0.75rem;">
              İstemcideki tüm servis ad alanlarını ve bunlara bağlı çağrılabilir metotları dinamik olarak listeler. Yapay zeka modeli önce bu aracı çağırarak hangi belediye servislerinin mevcut olduğunu keşfeder.
            </p>
            <div class="doc-code-block" style="margin: 0;">
              <div class="doc-code-header"><span>Örnek Dizi Yanıtı</span></div>
              <div class="doc-code-content">[
  "bisim.get_istasyon_list",
  "eczaneler.get_nobetci_list",
  "eshot.get_hatlar",
  "eshot.get_yakin_durak_list",
  "izsu.get_baraj_doluluk_oranlari",
  "otopark.get_list",
  "ckan.search_packages"
]</div>
            </div>
          </div>
        </div>

        <div class="doc-card">
          <div class="doc-card-header">
            <span class="doc-card-title">2. call_endpoint</span>
            <span class="doc-card-badge">Execution Tool</span>
          </div>
          <div style="padding: 1.25rem;">
            <p class="text-secondary" style="font-size: 0.9375rem; margin-bottom: 0.75rem;">
              Keşfedilen belirli bir belediye API metodunu parametreleriyle birlikte yürütür ve JSON yanıtını model bağlamına döndürür.
            </p>

            <div class="doc-table-wrapper" style="margin-bottom: 1rem;">
              <table class="doc-table">
                <thead>
                  <tr>
                    <th>Alan Adı</th>
                    <th>Tip</th>
                    <th>Zorunlu</th>
                    <th>Açıklama</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><code>namespace</code></td>
                    <td><code>string</code></td>
                    <td>Evet</td>
                    <td>Servis grubu adı (ör: <code>eshot</code>, <code>eczaneler</code>, <code>izsu</code>, <code>bisim</code>).</td>
                  </tr>
                  <tr>
                    <td><code>endpoint_name</code></td>
                    <td><code>string</code></td>
                    <td>Evet</td>
                    <td>Çağrılacak metodun adı (ör: <code>get_nobetci_list</code>, <code>get_yakin_durak_list</code>).</td>
                  </tr>
                  <tr>
                    <td><code>args</code></td>
                    <td><code>array</code></td>
                    <td>Hayır</td>
                    <td>Metoda aktarılacak sıralı parametre listesi (ör: koordinatlar, hat no, tarih).</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="doc-code-block" style="margin: 0;">
              <div class="doc-code-header"><span>Örnek Parametre Çağrısı</span></div>
              <div class="doc-code-content">{
  "namespace": "eshot",
  "endpoint_name": "get_yakin_durak_list",
  "args": [38.4192, 27.1287]
}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="doc-section">
        <h2>Örnek Yapay Zeka Ajanı Diyalogları</h2>
        
        <div class="doc-card" style="padding: 1.5rem; margin-bottom: 1.25rem;">
          <h3 style="font-size: 1rem; color: var(--brand-aegean); margin-bottom: 0.5rem;">Soru: "Şu an Konak'ta açık olan nöbetçi eczaneler nerede?"</h3>
          <p class="text-secondary" style="font-size: 0.875rem;">
            Ajan otomatik olarak <code>call_endpoint({ "namespace": "eczaneler", "endpoint_name": "get_nobetci_list" })</code> metodunu tetikler. Gelen listeden Konak bölgesindeki eczanelerin telefon, harita koordinatları ve adres bilgilerini özetleyerek kullanıcıya sunar.
          </p>
        </div>

        <div class="doc-card" style="padding: 1.5rem; margin-bottom: 1.25rem;">
          <h3 style="font-size: 1rem; color: var(--brand-aegean); margin-bottom: 0.5rem;">Soru: "İzmir barajlarının güncel doluluk durumu nedir?"</h3>
          <p class="text-secondary" style="font-size: 0.875rem;">
            Ajan <code>call_endpoint({ "namespace": "izsu", "endpoint_name": "get_baraj_durum_list" })</code> aracını çağırır. Tahtalı, Balçova, Gördes ve Ürkmez barajlarının su hacimlerini ve yıllık doluluk oranlarını karşılaştırmalı olarak analiz eder.
          </p>
        </div>
      </div>
    </div>
  </main>"""

    head = get_common_head(
        title="Model Context Protocol (MCP) Sunucusu",
        description="İzmir Açık Veri Portalı için Claude Desktop, Cursor ve yapay zeka ajanları uyumlu FastMCP sunucusu entegrasyon kılavuzu.",
        relative_root="",
        active_page="mcp",
        canonical_path="MCP.html",
        breadcrumb_name="MCP Sunucusu",
    )
    footer = get_common_footer()

    out_file = SITE_DIR / "MCP.html"
    out_file.write_text(f"{head}\n{body_content}\n{footer}", encoding="utf-8")
    print("Generated site/MCP.html")


def build_specs_html() -> None:
    SPECS_DIR.mkdir(parents=True, exist_ok=True)

    body_content = """  <main class="doc-page">
    <div class="container" style="max-width: 920px;">
      <nav class="breadcrumb-nav" aria-label="Ekmek kırıntısı">
        <a href="../index.html" class="breadcrumb-link">Ana Sayfa</a>
        <span>/</span>
        <span class="text-secondary">Dokümantasyon</span>
        <span>/</span>
        <span aria-current="page">Resmi Şartnameler (Specs)</span>
      </nav>

      <div class="doc-hero-with-illustration">
        <div class="doc-hero-text">
          <h1 class="doc-title">Resmi API Şartnameleri Arşivi</h1>
          <p class="doc-lead">
            İzmir Büyükşehir Belediyesi Bilgi İşlem Dairesi Başkanlığı ve bağlı iştirakleri (İZBAN, İZSU, İzmir Metro A.Ş.) resmi web servis şartnameleri, veri modelleri ve entegrasyon kuralları.
          </p>
        </div>
        <div class="doc-hero-image-wrap">
          <img src="../assets/illustrations/open_data_mesh.svg" alt="Açık Veri Standartları" class="doc-hero-img" width="220" height="180">
        </div>
      </div>

      <div class="doc-card" style="margin-bottom: 2rem;">
        <div class="doc-table-wrapper">
          <table class="doc-table">
            <thead>
              <tr>
                <th>Kurum / İştirak</th>
                <th>Sürüm</th>
                <th>Kapsam</th>
                <th>Doküman</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>İZBAN A.Ş.</strong></td>
                <td><span class="method-chip">V.1.0</span></td>
                <td>Banliyö istasyonları, sefer saatleri, Gittiğin Kadar Öde tutar hesaplama</td>
                <td><a href="https://github.com/AtaCanYmc/izmir-open-data-py/blob/main/docs/specs/IZBAN.md" class="footer-link" target="_blank" rel="noopener noreferrer">IZBAN.md ↗</a></td>
              </tr>
              <tr>
                <td><strong>İzmir Metro A.Ş.</strong></td>
                <td><span class="method-chip">V.1.0</span></td>
                <td>Metro istasyonları, sefer sıklığı, tramvay hatları (1-8), tramvay durakları</td>
                <td><a href="https://github.com/AtaCanYmc/izmir-open-data-py/blob/main/docs/specs/METRO_TRAMVAY.md" class="footer-link" target="_blank" rel="noopener noreferrer">METRO_TRAMVAY.md ↗</a></td>
              </tr>
              <tr>
                <td><strong>İZSU Genel Müdürlüğü</strong></td>
                <td><span class="method-chip">V.1.0</span></td>
                <td>Su arıza/kesinti, baraj durumları, su üretimi, su analizleri, vezne ve şubeler</td>
                <td><a href="https://github.com/AtaCanYmc/izmir-open-data-py/blob/main/docs/specs/IZSU.md" class="footer-link" target="_blank" rel="noopener noreferrer">IZSU.md ↗</a></td>
              </tr>
              <tr>
                <td><strong>İZBB CBS Şube Müdürlüğü</strong></td>
                <td><span class="method-chip">V.1.1</span></td>
                <td>88 Kentsel katman (POI) ve Noktaya Yakın Otobüs Durakları servisi</td>
                <td><a href="https://github.com/AtaCanYmc/izmir-open-data-py/blob/main/docs/specs/CBS.md" class="footer-link" target="_blank" rel="noopener noreferrer">CBS.md ↗</a></td>
              </tr>
              <tr>
                <td><strong>İZBB Yazılım Şube Müdürlüğü</strong></td>
                <td><span class="method-chip">V.1.0</span></td>
                <td>Turuncu Çember, Hal Fiyatları, Güncel Hava Kalitesi, Eczaneler, Kültür-Sanat</td>
                <td><a href="https://github.com/AtaCanYmc/izmir-open-data-py/blob/main/docs/specs/YAZILIM_SUBE.md" class="footer-link" target="_blank" rel="noopener noreferrer">YAZILIM_SUBE.md ↗</a></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="doc-section">
        <h2>Ortak Teknik Standartlar</h2>
        <div class="doc-card" style="padding: 1.5rem;">
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.85rem; font-size: 0.9375rem; color: var(--text-secondary);">
            <li><strong>1. İletişim Protokolü:</strong> RESTful HTTP GET.</li>
            <li><strong>2. Yetkilendirme:</strong> Açık Veri Portalı servisleri anonim erişime açıktır.</li>
            <li><strong>3. Veri Formatı:</strong> Tüm uç noktalar <code>application/json</code> veya CSV üretir.</li>
            <li><strong>4. Koordinat Referans Sistemi:</strong> Tüm coğrafi konum verileri (enlem/boylam) WGS84 (<code>EPSG:4326</code>) projeksiyonundadır.</li>
            <li><strong>5. Kentsel POI Şeması:</strong> CBS katmanları standart <code>DefaultOnemliYer</code> şemasına (<code>ADI, ILCE, MAHALLE, YOL, KAPINO, ENLEM, BOYLAM</code>) uyar.</li>
          </ul>
        </div>
      </div>
    </div>
  </main>"""

    head = get_common_head(
        title="Resmi Şartnameler (Specs)",
        description="İzmir Büyükşehir Belediyesi ve bağlı iştirakleri (İZBAN, İZSU, Metro) resmi web servis şartnameleri, veri modelleri ve entegrasyon kuralları.",
        relative_root="../",
        active_page="specs",
        canonical_path="specs/index.html",
        breadcrumb_name="Resmi Şartnameler",
    )
    footer = get_common_footer(relative_root="../")

    out_file = SPECS_DIR / "index.html"
    out_file.write_text(f"{head}\n{body_content}\n{footer}", encoding="utf-8")
    print("Generated site/specs/index.html")


def main() -> None:
    build_endpoints_html()
    build_cli_html()
    build_mcp_html()
    build_specs_html()
    print("Site build completed successfully.")


if __name__ == "__main__":
    main()
