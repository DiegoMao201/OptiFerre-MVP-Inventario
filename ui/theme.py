"""Theming white-label: inyección dinámica de CSS por tenant."""
from __future__ import annotations

import streamlit as st


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    try:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore
    except ValueError:
        return (255, 107, 26)


def inject_brand_css(primary_color: str = "#10B7C4", theme_mode: str = "dark") -> None:
    r, g, b = _hex_to_rgb(primary_color)
    primary_soft = f"rgba({r},{g},{b},0.15)"

    if theme_mode == "light":
      bg = "#F8FDFF"
      bg2 = "#FFFFFF"
      text = "#16314D"
      muted = "#5F7993"
      card_border = "rgba(19,62,97,0.12)"
    else:
      bg = "#F8FDFF"
      bg2 = "#FFFFFF"
      text = "#16314D"
      muted = "#5F7993"
      card_border = "rgba(19,62,97,0.12)"

    css = f"""
    <style>
      :root {{
        --primary: {primary_color};
        --primary-soft: {primary_soft};
        --bg: {bg};
        --bg2: {bg2};
        --text: {text};
        --muted: {muted};
        --card-border: {card_border};
      }}
      .stApp {{
        background:
          radial-gradient(circle at top left, rgba(100,222,255,0.28), transparent 20%),
          radial-gradient(circle at 20% 7%, rgba(16,183,196,0.16), transparent 22%),
          radial-gradient(circle at top right, rgba(92,152,255,0.18), transparent 26%),
          linear-gradient(180deg, #F7FDFF 0%, #EEF9FF 16%, #E3F5FF 36%, #DCF6F6 60%, #EEF8FF 100%);
        color: var(--text);
      }}
      section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(247,253,255,0.98), rgba(228,245,252,0.98));
        border-right: 1px solid rgba(19,62,97,0.08);
      }}
      .block-container {{ max-width: 1320px; padding-top: 2rem; padding-bottom: 3rem; }}
      h1, h2, h3, h4 {{ color: var(--text); letter-spacing: -0.01em; }}

      /* Botones */
      .stButton>button, .stDownloadButton>button, .stLinkButton>a {{
        background: var(--primary) !important;
        color: white !important;
        border: 0 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.1rem !important;
        transition: transform .08s ease, box-shadow .15s ease;
      }}
      .stButton>button:hover, .stDownloadButton>button:hover, .stLinkButton>a:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 18px var(--primary-soft);
        filter: brightness(1.05);
      }}

      /* KPI cards */
      .of-kpi {{
        background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(238,248,255,0.92));
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 16px 30px rgba(87, 137, 173, 0.09);
      }}
      .of-kpi .label {{ color: var(--muted); font-size: 0.82rem; text-transform: uppercase; letter-spacing: .08em; }}
      .of-kpi .value {{ color: var(--text); font-size: 1.85rem; font-weight: 700; margin-top: 6px; }}
      .of-kpi .delta {{ color: var(--primary); font-size: 0.85rem; margin-top: 4px; }}

      /* Banner */
      .of-banner {{
        background: linear-gradient(135deg, rgba(219,249,251,0.96), rgba(239,248,255,0.94));
        border: 1px solid rgba({r},{g},{b},0.28);
        border-radius: 14px;
        padding: 16px 20px;
        margin: 8px 0 18px 0;
        box-shadow: 0 14px 28px rgba(87, 137, 173, 0.08);
      }}
      .of-banner h4 {{ margin: 0 0 4px 0; color: var(--primary); }}
      .of-banner p {{ margin: 0; color: var(--text); opacity: 0.92; }}
      .of-section-shell {{ margin: 0 0 14px 0; }}
      .of-exec-shell {{
        background:
          radial-gradient(circle at top right, rgba(16,183,196,0.18), transparent 36%),
          linear-gradient(135deg, rgba(255,255,255,0.96), rgba(226,246,255,0.9));
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 18px 34px rgba(87, 137, 173, 0.1);
      }}
      .of-exec-grid {{
        display: grid;
        grid-template-columns: 1.4fr .8fr;
        gap: 14px;
        margin-top: 12px;
      }}
      .of-metric-strip {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin-top: 18px;
      }}
      .of-metric-pill {{
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 14px 16px;
        background: rgba(255,255,255,0.78);
      }}
      .of-metric-pill .caption {{ color: var(--muted); font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }}
      .of-metric-pill .value {{ color: var(--text); font-size: 1.45rem; font-weight: 700; margin-top: 6px; }}
      .of-priority-card {{
        background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(236,247,255,0.92));
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 16px 18px;
      }}
      .of-priority-list {{ margin: 12px 0 0 0; padding-left: 18px; }}
      .of-priority-list li {{ margin-bottom: 8px; color: var(--text); }}
      .of-chip-row {{
        display:grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap:12px;
        width: 100%;
        max-width: 760px;
        margin-top: 18px;
        align-items: stretch;
      }}
      .of-chip {{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        gap:8px;
        border:1px solid rgba(16,33,59,0.14);
        border-radius:999px;
        padding:12px 16px;
        background: rgba(255,255,255,0.48);
        color: #123154;
        font-size: .82rem;
        font-weight: 700;
        line-height: 1.25;
        min-height: 60px;
        box-shadow: 0 10px 28px rgba(10, 25, 47, 0.08);
        white-space: normal;
        text-align: center;
        text-wrap: balance;
        transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease, background .25s ease;
      }}
      .of-chip:hover {{
        transform: translateY(-2px);
        border-color: rgba(16,183,196,0.42);
        background: rgba(255,255,255,0.68);
        box-shadow: 0 16px 30px rgba(8, 17, 31, 0.12);
      }}
      .of-upload-promo {{
        background: linear-gradient(135deg, rgba(16,183,196,0.13), rgba(25,74,145,0.12));
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 18px;
      }}
      .of-upload-promo-grid {{ display:grid; grid-template-columns: 1.1fr .9fr; gap: 14px; }}
      .of-upload-stat {{
        background: rgba(255,255,255,0.82);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 14px 16px;
      }}

      /* Landing */
      .of-hero {{
        background:
          radial-gradient(circle at top right, rgba(16,183,196,0.18), transparent 35%),
          radial-gradient(circle at bottom left, rgba(25,74,145,0.14), transparent 35%),
          linear-gradient(180deg, rgba(255,255,255,0.03), transparent),
          var(--bg2);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 16px;
      }}
      .of-eyebrow {{
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: .12em;
        font-size: .76rem;
        font-weight: 700;
      }}
      .of-hero h1 {{
        font-size: clamp(2rem, 3vw, 3.5rem);
        line-height: 1.02;
        margin: 10px 0 14px 0;
      }}
      .of-hero p {{ color: var(--muted); font-size: 1rem; line-height: 1.6; }}
      .of-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
        margin-top: 18px;
      }}
      .of-card {{
        background: var(--bg2);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 16px 18px;
      }}
      .of-card strong {{ display:block; margin-bottom: 6px; font-size: 1rem; }}
      .of-card p {{ margin: 0; color: var(--muted); font-size: .95rem; }}
      .of-proof {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin-top: 20px;
      }}
      .of-proof .item {{
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 14px 16px;
      }}
      .of-proof .number {{ font-size: 1.5rem; font-weight: 700; color: var(--text); }}
      .of-proof .caption {{ color: var(--muted); font-size: .85rem; margin-top: 4px; }}
      .of-steps {{ margin-top: 18px; }}
      .of-steps div {{
        padding: 10px 0;
        border-bottom: 1px solid var(--card-border);
        color: var(--text);
      }}
      .of-steps div:last-child {{ border-bottom: 0; }}
      .of-plan-strip {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin-top: 16px;
      }}
      .of-plan {{
        background: var(--bg2);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 16px 18px;
      }}
      .of-plan.highlight {{ border-color: var(--primary); box-shadow: 0 0 0 1px var(--primary-soft) inset; }}
      .of-plan .price {{ font-size: 1.6rem; font-weight: 700; margin: 8px 0; }}
      .of-form-shell {{
        background: linear-gradient(180deg, rgba(255,255,255,0.02), transparent), var(--bg2);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 12px;
      }}
      .of-public-shell {{ margin-bottom: 18px; }}
      .of-public-topbar {{
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 18px;
        padding: 0 2px 8px 2px;
      }}
      .of-public-badge {{
        white-space: nowrap;
        border: 1px solid var(--card-border);
        border-radius: 999px;
        padding: 10px 14px;
        background: rgba(255,255,255,0.03);
        color: var(--text);
        font-size: .9rem;
        font-weight: 600;
      }}
      .of-mini-note {{ color: #55718B; font-size: .88rem; line-height: 1.6; }}
      .of-trust-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
        margin-top: 16px;
      }}
      .of-trust-card {{
        background: var(--bg2);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 16px 18px;
      }}
      .of-faq-shell {{
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 18px;
        margin-top: 18px;
      }}
      .of-landing-canvas {{ position: relative; overflow: hidden; }}
      .of-glow {{
        position: absolute;
        border-radius: 999px;
        filter: blur(120px);
        opacity: .34;
        pointer-events: none;
        animation: of-float 10s ease-in-out infinite;
      }}
      .of-glow.orb-a {{ width: 420px; height: 420px; top: -80px; left: -120px; background: rgba(255,255,255,0.5); }}
      .of-glow.orb-b {{ width: 340px; height: 340px; top: 130px; right: -70px; background: rgba(16,183,196,0.35); animation-delay: 2.8s; }}
      .of-glow.orb-c {{ width: 280px; height: 280px; bottom: 140px; left: 26%; background: rgba(25,74,145,0.24); animation-delay: 5.2s; }}
      @keyframes of-float {{
        0%, 100% {{ transform: translateY(0) scale(1); }}
        50% {{ transform: translateY(-24px) scale(1.08); }}
      }}
      @keyframes of-shimmer {{
        0% {{ background-position: -200% center; }}
        100% {{ background-position: 200% center; }}
      }}
      .card-hover {{ transition: transform .25s ease, box-shadow .25s ease; }}
      .card-hover:hover {{
        transform: translateY(-4px);
        box-shadow: 0 18px 44px rgba(7, 16, 27, 0.22);
      }}
      .testimonial-card {{ backdrop-filter: blur(12px); }}
      .of-stage-logo-wrap {{ min-height: 260px; display:flex; align-items:center; justify-content:center; }}
      .of-logo-panel {{
        width: min(100%, 360px);
        min-height: 260px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap: 14px;
        border-radius: 28px;
        border: 1px solid rgba(16,33,59,0.14);
        background:
          radial-gradient(circle at top, rgba(255,255,255,0.92), rgba(219,234,248,0.78) 46%, rgba(191,214,236,0.28) 100%),
          rgba(255,255,255,0.72);
        box-shadow: 0 28px 60px rgba(8, 17, 31, 0.16);
        padding: 24px 22px;
      }}
      .of-brand-logo,
      .of-logo-panel img {{
        display:block;
        margin: 0 auto;
        width: min(100%, 240px);
        height: auto;
        filter: drop-shadow(0 16px 32px rgba(10, 25, 47, 0.16));
      }}
      .of-logo-caption {{
        max-width: 250px;
        text-align: center;
        color: #264569;
        font-size: .88rem;
        line-height: 1.5;
        font-weight: 600;
      }}
      .of-stage-title-wrap {{
        padding-top: 12px;
        max-width: 620px;
        margin-left: auto;
      }}
      .of-stage-title-wrap .of-eyebrow {{
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(16,183,196,0.14);
        box-shadow: 0 10px 24px rgba(8, 17, 31, 0.1);
      }}
      .of-stage-title {{
        font-size: clamp(2.05rem, 4.1vw, 4.35rem);
        line-height: .96;
        margin: 10px 0 0 0;
        letter-spacing: -0.04em;
        color: #16314D;
        text-shadow: none;
      }}
      .of-shimmer-text {{
        background: linear-gradient(90deg, #EFF5FC 0%, #10B7C4 28%, #C0FF54 52%, #EFF5FC 76%, #EFF5FC 100%);
        background-size: 220% auto;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: of-shimmer 5s linear infinite;
      }}
      .of-stage-lead {{
        margin: 14px 0 0 0;
        max-width: 560px;
        color: #4E6A84;
        font-size: .98rem;
        line-height: 1.64;
        font-weight: 500;
        text-shadow: none;
      }}
      .of-hero-v2 {{
        position: relative;
        background:
          radial-gradient(circle at top right, rgba(255,255,255,0.72), transparent 32%),
          radial-gradient(circle at left top, rgba(16,183,196,0.16), transparent 34%),
          linear-gradient(180deg, rgba(255,255,255,0.96), rgba(226,243,255,0.92));
        border: 1px solid rgba(19,62,97,0.12);
        border-radius: 24px;
        padding: 24px 24px 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 22px 40px rgba(87, 137, 173, 0.12);
      }}
      .of-hero-v2 h2 {{
        font-size: clamp(2rem, 3.45vw, 3.7rem);
        line-height: .98;
        margin: 12px 0 14px 0;
        max-width: 760px;
        letter-spacing: -0.04em;
        color: #16314D;
        text-shadow: none;
      }}
      .of-hero-v2 p {{ color: #4E6A84; line-height: 1.72; max-width: 860px; margin: 0; }}
      .of-proof-v2 {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin-top: 22px;
      }}
      .of-proof-v2 .item {{
        background: rgba(255,255,255,0.84);
        border: 1px solid rgba(19,62,97,0.1);
        border-radius: 16px;
        padding: 16px;
      }}
      .of-proof-v2 .number {{ font-size: 1.7rem; font-weight: 800; letter-spacing: -0.03em; }}
      .of-proof-v2 .caption {{ color: #55718B; font-size: .9rem; margin-top: 6px; line-height: 1.5; }}
      .of-actionable-intro {{
        color: #55718B;
        font-size: .9rem;
        line-height: 1.55;
        margin: 2px 0 12px 0;
      }}
      .of-stat-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin: 18px 0 22px 0;
      }}
      .of-stat-card {{
        background: linear-gradient(180deg, rgba(255,255,255,0.78), rgba(225,236,248,0.58));
        border: 1px solid rgba(16,33,59,0.18);
        border-radius: 18px;
        padding: 18px 16px;
        box-shadow: 0 14px 30px rgba(8, 17, 31, 0.09);
      }}
      .of-stat-card .value {{
        display: inline-block;
        font-size: 1.65rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        background: linear-gradient(90deg, #102C49 0%, #10B7C4 35%, #0D3F7A 68%, #102C49 100%);
        background-size: 220% auto;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: of-shimmer 5s linear infinite;
      }}
      .of-stat-card .caption {{ color: rgba(18,49,84,0.92); font-size: .82rem; line-height: 1.45; margin-top: 6px; font-weight: 600; }}
      .of-stat-caption-card {{
        margin-top: 10px;
        min-height: 94px;
        padding: 14px 14px;
        border-radius: 16px;
        background: linear-gradient(180deg, rgba(248,251,255,0.9), rgba(229,239,249,0.74));
        border: 1px solid rgba(16,33,59,0.16);
        color: #163557;
        font-size: .84rem;
        line-height: 1.45;
        font-weight: 700;
        box-shadow: 0 12px 24px rgba(8,17,31,0.08);
      }}
      .of-stat-popover-kicker {{
        color: #0A7A89;
        font-size: .74rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .12em;
      }}
      .of-stat-popover-title {{
        margin-top: 6px;
        color: #102C49;
        font-size: 1.65rem;
        font-weight: 900;
        line-height: 1.04;
        letter-spacing: -0.03em;
      }}
      .of-feature-grid-v2 {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
      }}
      .of-feature-card-v2 {{
        background: linear-gradient(180deg, rgba(248,251,255,0.88), rgba(229,239,249,0.72));
        border: 1px solid rgba(16,33,59,0.18);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 16px 30px rgba(8, 17, 31, 0.1);
        min-height: 220px;
        transition: transform .28s ease, box-shadow .28s ease, border-color .28s ease, background .28s ease;
      }}
      .of-feature-card-v2:hover {{
        transform: translateY(-5px);
        border-color: rgba(16,183,196,0.45);
        background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(235,246,252,0.95));
        box-shadow: 0 22px 36px rgba(8, 17, 31, 0.14);
      }}
      .of-feature-card-v2 h4 {{ margin: 12px 0 8px 0; font-size: 1.05rem; color: #102C49; }}
      .of-feature-card-v2 p {{ margin: 0; color: rgba(16,44,73,0.94); font-size: .94rem; line-height: 1.58; font-weight: 500; }}
      .of-feature-icon {{
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(16,183,196,0.14);
        color: var(--primary);
        font-weight: 800;
      }}
      .of-auth-card {{
        background:
          radial-gradient(circle at top right, rgba(16,183,196,0.14), transparent 34%),
          linear-gradient(180deg, rgba(255,255,255,0.98), rgba(232,246,255,0.96));
        border: 1px solid rgba(167,204,233,0.34);
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 14px;
        box-shadow: 0 22px 40px rgba(87, 137, 173, 0.12);
      }}
      .of-auth-card .of-eyebrow {{ color: #6EF0FF; }}
      .of-auth-card h3 {{
        margin: 10px 0 10px 0;
        font-size: clamp(1.7rem, 2.2vw, 2.45rem);
        line-height: 1.06;
        letter-spacing: -0.03em;
        color: #16314D;
      }}
      .of-auth-card .of-mini-note {{ color: #55718B; }}
      .of-proof-grid-v2 {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin-top: 16px;
        margin-bottom: 12px;
      }}
      .of-proof-card-v2 {{
        background: linear-gradient(180deg, rgba(248,251,255,0.86), rgba(227,238,249,0.72));
        border: 1px solid rgba(16,33,59,0.18);
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 16px 34px rgba(8, 17, 31, 0.1);
      }}
      .of-proof-card-v2 p {{
        margin: 12px 0 14px 0;
        color: #102C49;
        font-size: 1rem;
        line-height: 1.7;
        font-weight: 500;
      }}
      .of-proof-person {{ color: rgba(16,44,73,0.82); font-size: .88rem; font-weight: 600; }}
      .of-price-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin-top: 8px;
      }}
      .of-price-card {{
        position: relative;
        background: linear-gradient(180deg, rgba(250,253,255,0.96), rgba(228,238,249,0.9));
        border: 1px solid rgba(16,33,59,0.22);
        border-radius: 22px;
        padding: 22px 20px;
        box-shadow: 0 18px 36px rgba(8, 17, 31, 0.11);
        transition: transform .28s ease, box-shadow .28s ease, border-color .28s ease, background .28s ease;
        cursor: pointer;
      }}
      .of-price-card:hover,
      .of-price-card:focus,
      .of-price-card:focus-visible {{
        transform: translateY(-6px) scale(1.01);
        border-color: rgba(16,183,196,0.58);
        background: linear-gradient(180deg, rgba(255,255,255,1), rgba(236,247,253,0.98));
        box-shadow: 0 26px 42px rgba(8, 17, 31, 0.16);
        outline: none;
      }}
      .of-price-popular {{
        background: linear-gradient(180deg, rgba(222,250,252,0.98), rgba(211,239,249,0.92));
        border-color: rgba(16,183,196,0.55);
        box-shadow: 0 0 0 1px rgba(16,183,196,0.12) inset, 0 20px 38px rgba(16,183,196,0.08);
      }}
      .of-price-popular:hover,
      .of-price-popular:focus,
      .of-price-popular:focus-visible {{
        border-color: rgba(16,183,196,0.78);
        box-shadow: 0 0 0 1px rgba(16,183,196,0.18) inset, 0 28px 46px rgba(16,183,196,0.14);
      }}
      .of-popular-badge {{
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        border-radius: 999px;
        padding: 4px 12px;
        background: var(--primary);
        color: #08111F;
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
      }}
      .of-price-card .of-pill {{ background: rgba(16,183,196,0.18); color: #0E445B; font-weight: 800; }}
      .of-price-main {{ margin: 14px 0 14px 0; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.04em; color: #0E2A48; }}
      .of-price-main span {{ color: rgba(18,49,84,0.9); font-size: .95rem; font-weight: 600; margin-left: 2px; }}
      .of-price-list {{ margin: 0; padding-left: 18px; color: #163557; }}
      .of-price-list li {{ margin-bottom: 8px; line-height: 1.45; color: #163557; font-weight: 600; }}
      .of-price-card:hover .of-pill,
      .of-price-card:focus .of-pill,
      .of-price-card:focus-visible .of-pill {{ background: rgba(16,183,196,0.22); color: #0A3851; }}
      .of-price-card:hover .of-price-main,
      .of-price-card:focus .of-price-main,
      .of-price-card:focus-visible .of-price-main,
      .of-price-card:hover .of-price-list li,
      .of-price-card:focus .of-price-list li,
      .of-price-card:focus-visible .of-price-list li {{ color: #102C49; }}
      .of-final-cta {{
        margin-top: 22px;
        padding: 28px 26px;
        border-radius: 28px;
        border: 1px solid rgba(19,62,97,0.14);
        background: linear-gradient(180deg, rgba(248,252,255,0.96), rgba(219,245,250,0.92));
        text-align: center;
        box-shadow: 0 22px 40px rgba(87, 137, 173, 0.1);
      }}
      .of-final-cta h3 {{
        font-size: clamp(1.8rem, 2.7vw, 3rem);
        line-height: .98;
        letter-spacing: -0.04em;
        margin: 12px 0;
      }}
      .of-final-cta .of-eyebrow {{ color: #10B7C4; }}
      .of-final-cta p {{ color: #55718B; }}
      .of-contact-panel {{
        margin-top: 16px;
        padding: 24px 26px;
        border-radius: 24px;
        border: 1px solid rgba(167,204,233,0.2);
        background:
          radial-gradient(circle at top right, rgba(16,183,196,0.14), transparent 34%),
          linear-gradient(180deg, rgba(255,255,255,0.98), rgba(233,247,255,0.95));
        box-shadow: 0 20px 38px rgba(87,137,173,0.1);
      }}
      .of-contact-name {{
        margin-top: 10px;
        color: #16314D;
        font-size: clamp(1.35rem, 2vw, 2rem);
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.03em;
      }}
      .of-contact-meta {{
        margin-top: 6px;
        color: #55718B;
        font-size: .95rem;
        font-weight: 600;
      }}
      .of-contact-link {{
        display: inline-flex;
        margin-top: 12px;
        align-items: center;
        justify-content: center;
        padding: 12px 16px;
        border-radius: 999px;
        background: rgba(232,249,251,0.94);
        color: #10304E;
        font-weight: 800;
        text-decoration: none;
        box-shadow: 0 14px 28px rgba(8,17,31,0.14);
      }}
      .of-contact-link:hover {{
        background: #FFFFFF;
        color: #0B2742;
      }}
      .of-support-shell {{
        margin-top: 16px;
        padding: 24px 26px;
        border-radius: 24px;
        border: 1px solid rgba(167,204,233,0.22);
        background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(233,247,255,0.95));
        box-shadow: 0 20px 40px rgba(87,137,173,0.1);
      }}
      .of-operator-banner {{
        margin: 10px 0 18px 0;
        padding: 14px 16px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(211,250,245,0.95), rgba(233,247,255,0.95));
        border: 1px solid rgba(16,183,196,0.24);
        color: #0F5273;
        box-shadow: 0 12px 24px rgba(87,137,173,0.08);
      }}

      div[data-testid="stPopover"] {{ width: 100%; }}
      div[data-testid="stPopover"] > button,
      div[data-testid="stPopover"] button[kind="secondary"],
      button[kind="secondaryFormSubmit"],
      button[kind="secondary"] {{
        width: 100% !important;
        justify-content: space-between !important;
        align-items: center !important;
        background: linear-gradient(180deg, rgba(248,251,255,0.98), rgba(229,239,250,0.95)) !important;
        color: #123154 !important;
        border: 1px solid rgba(16,33,59,0.16) !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 24px rgba(8, 17, 31, 0.08) !important;
        font-weight: 700 !important;
        min-height: 64px !important;
      }}
      div[data-testid="stPopover"] > button p,
      div[data-testid="stPopover"] button[kind="secondary"] p,
      button[kind="secondary"] p {{
        color: #123154 !important;
        opacity: 1 !important;
        font-weight: 700 !important;
      }}
      div[data-testid="stPopover"] > button svg,
      div[data-testid="stPopover"] button[kind="secondary"] svg,
      button[kind="secondary"] svg {{
        color: #123154 !important;
        opacity: 1 !important;
      }}
      div[data-testid="stPopover"] > button:hover,
      div[data-testid="stPopover"] > button:focus,
      div[data-testid="stPopover"] button[kind="secondary"]:hover,
      div[data-testid="stPopover"] button[kind="secondary"]:focus,
      button[kind="secondary"]:hover {{
        color: #0E2A48 !important;
        border-color: rgba(16,183,196,0.4) !important;
        background: linear-gradient(180deg, rgba(255,255,255,1), rgba(236,245,252,0.98)) !important;
        box-shadow: 0 14px 28px rgba(8, 17, 31, 0.12) !important;
      }}
      div[data-testid="stPopoverContent"] {{
        border-radius: 18px !important;
        border: 1px solid rgba(16,33,59,0.12) !important;
        background: linear-gradient(180deg, rgba(246,250,255,0.98), rgba(218,232,247,0.96)) !important;
      }}
      div[data-testid="stPopoverContent"] * {{ color: #123154 !important; }}

      @media (max-width: 900px) {{
        .of-grid, .of-proof, .of-plan-strip, .of-trust-grid {{ grid-template-columns: 1fr; }}
        .of-public-topbar {{ flex-direction: column; align-items: flex-start; }}
        .of-exec-grid, .of-metric-strip, .of-upload-promo-grid {{ grid-template-columns: 1fr; }}
        .of-stage-title-wrap {{ margin-left: 0; max-width: 100%; }}
        .of-chip-row {{ grid-template-columns: 1fr; width: 100%; }}
        .of-stat-grid, .of-proof-v2, .of-feature-grid-v2, .of-proof-grid-v2, .of-price-grid {{ grid-template-columns: 1fr; }}
        .of-stage-logo-wrap {{ min-height: auto; margin-bottom: 8px; }}
        .of-logo-panel {{ width: 100%; min-height: 220px; }}
      }}

      /* Pill / badge */
      .of-pill {{
        display: inline-block; padding: 3px 10px; border-radius: 999px;
        background: var(--primary-soft); color: var(--primary); font-size: 0.78rem;
        font-weight: 600; letter-spacing: .03em;
      }}

      /* Tabs */
      .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: rgba(255,255,255,0.74);
        border: 1px solid rgba(167,204,233,0.16);
        border-radius: 18px;
        padding: 8px;
        margin-bottom: 14px;
      }}
      .stTabs [data-baseweb="tab-list"] button {{
        background: rgba(255,255,255,0.62) !important;
        border-radius: 12px !important;
        color: #486785 !important;
        font-weight: 800 !important;
        min-height: 44px !important;
      }}
      .stTabs [data-baseweb="tab-list"] button:hover {{
        background: rgba(255,255,255,0.92) !important;
        color: #16314D !important;
      }}
      .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        background: linear-gradient(180deg, rgba(227,249,252,0.98), rgba(202,237,248,0.95)) !important;
        color: #10304E !important;
        border-bottom-color: transparent !important;
      }}

      /* Inputs */
      .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 14px !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.99), rgba(240,246,252,0.96)) !important;
        border: 1px solid rgba(84,120,153,0.28) !important;
        color: #123154 !important;
        box-shadow: 0 12px 24px rgba(8, 17, 31, 0.1) !important;
      }}
      .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: rgba(16,183,196,0.68) !important;
        box-shadow: 0 0 0 1px rgba(16,183,196,0.28), 0 14px 26px rgba(8, 17, 31, 0.14) !important;
      }}
      .stTextInput label p, .stNumberInput label p, .stCheckbox label p {{
        color: #486785 !important;
        font-weight: 700 !important;
        letter-spacing: .01em;
      }}
      .stCaption {{ color: #5F7993 !important; }}
      .stTextInput input::placeholder, .stNumberInput input::placeholder {{
        color: rgba(18,49,84,0.62) !important;
      }}
      .stCheckbox label span, .stCheckbox p {{
        color: #486785 !important;
      }}
      .stForm {{
        background: transparent !important;
      }}

      /* DataFrame */
      .stDataFrame {{ border-radius: 10px; overflow: hidden; }}

      footer {{ visibility: hidden; }}
      #MainMenu {{ visibility: hidden; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_brand_header(company_name: str, logo_url: str | None = None,
                        tagline: str = "Optimización Inteligente de Inventarios") -> None:
    cols = st.columns([1, 6])
    with cols[0]:
        if logo_url:
            st.image(logo_url, width=72)
        else:
            try:
                st.image("logo_nexus.png", width=86)
            except Exception:
                st.markdown(
                    "<div style='font-size:42px; line-height:1;'>🛠️</div>",
                    unsafe_allow_html=True,
                )
    with cols[1]:
        st.markdown(
            f"<h2 style='margin-bottom:0'>{company_name}</h2>"
            f"<div class='of-pill'>OptiFerre</div> "
            f"<span style='color:var(--muted); margin-left:8px;'>{tagline}</span>",
            unsafe_allow_html=True,
        )
    st.divider()
