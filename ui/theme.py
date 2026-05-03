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
    primary_soft = f"rgba({r},{g},{b},0.18)"

    if theme_mode == "light":
      bg = "#07111F"
      bg2 = "rgba(9, 19, 37, 0.78)"
      text = "#ECF7FF"
      muted = "#9BB6D2"
      card_border = "rgba(78, 224, 255, 0.24)"
    else:
      bg = "#07111F"
      bg2 = "rgba(9, 19, 37, 0.78)"
      text = "#ECF7FF"
      muted = "#9BB6D2"
      card_border = "rgba(78, 224, 255, 0.24)"

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
          radial-gradient(circle at 14% 12%, rgba(0, 224, 255, 0.18), transparent 16%),
          radial-gradient(circle at 84% 8%, rgba(124, 58, 237, 0.18), transparent 18%),
          radial-gradient(circle at 50% 86%, rgba(0, 255, 163, 0.12), transparent 22%),
          linear-gradient(135deg, #07111F 0%, #0D1630 24%, #111C3E 52%, #091120 100%);
        color: var(--text);
      }}
      section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(8,18,34,0.96), rgba(7,14,28,0.98));
        border-right: 1px solid rgba(78, 224, 255, 0.12);
      }}
      .block-container {{ max-width: 1360px; padding-top: 2.35rem; padding-bottom: 3.4rem; }}
      h1, h2, h3, h4 {{ color: var(--text); letter-spacing: -0.01em; }}
      p, li, label, div {{ scrollbar-color: rgba(0,224,255,0.6) transparent; }}

      /* Botones */
      .stButton>button, .stDownloadButton>button, .stLinkButton>a {{
        background: linear-gradient(135deg, rgba(0,224,255,0.96), rgba(0,255,163,0.92)) !important;
        color: #04101F !important;
        border: 1px solid rgba(157,255,240,0.4) !important;
        border-radius: 16px !important;
        font-weight: 800 !important;
        padding: 0.72rem 1.18rem !important;
        transition: transform .08s ease, box-shadow .15s ease;
        box-shadow: 0 0 0 1px rgba(0,224,255,0.14) inset, 0 16px 30px rgba(0,224,255,0.18) !important;
      }}
      .stButton>button:hover, .stDownloadButton>button:hover, .stLinkButton>a:hover {{
        transform: translateY(-1px);
        box-shadow: 0 18px 36px rgba(0,224,255,0.24) !important;
        filter: brightness(1.03);
      }}

      /* KPI cards */
      .of-kpi {{
        background: linear-gradient(180deg, rgba(11,24,44,0.92), rgba(7,15,29,0.9));
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 0 0 1px rgba(0,224,255,0.08) inset, 0 18px 34px rgba(2, 8, 19, 0.34);
      }}
      .of-kpi .label {{ color: var(--muted); font-size: 0.82rem; text-transform: uppercase; letter-spacing: .08em; }}
      .of-kpi .value {{ color: var(--text); font-size: 1.85rem; font-weight: 700; margin-top: 6px; }}
      .of-kpi .delta {{ color: var(--primary); font-size: 0.85rem; margin-top: 4px; }}

      /* Banner */
      .of-banner {{
        background: linear-gradient(135deg, rgba(14,30,53,0.94), rgba(12,22,46,0.92));
        border: 1px solid rgba(0,224,255,0.22);
        border-radius: 18px;
        padding: 16px 20px;
        margin: 8px 0 18px 0;
        box-shadow: 0 18px 34px rgba(2, 8, 19, 0.28);
      }}
      .of-banner h4 {{ margin: 0 0 4px 0; color: var(--primary); }}
      .of-banner p {{ margin: 0; color: var(--text); opacity: 0.92; }}
      .of-section-shell {{ margin: 0 0 14px 0; }}
      .of-page-block {{ margin: 0 0 24px 0; }}
      .of-soft-panel {{
        background: linear-gradient(180deg, rgba(11,24,44,0.92), rgba(8,18,34,0.88));
        border: 1px solid rgba(0,224,255,0.18);
        border-radius: 22px;
        padding: 22px 24px;
        box-shadow: 0 18px 34px rgba(2, 8, 19, 0.3);
      }}
      .of-helper-line {{
        color: #9BB6D2;
        font-size: .9rem;
        line-height: 1.6;
        margin: 8px 0 0 0;
      }}
      .of-action-note {{
        margin: 12px 0 0 0;
        padding: 12px 14px;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(0,224,255,0.12), rgba(124,58,237,0.14));
        border: 1px solid rgba(0,224,255,0.22);
        color: #D8F4FF;
        font-size: .88rem;
        line-height: 1.55;
      }}
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
        background: linear-gradient(135deg, rgba(12,31,57,0.96), rgba(14,24,52,0.92));
        border: 1px solid var(--card-border);
        border-radius: 24px;
        padding: 18px 20px;
        margin-bottom: 26px;
        box-shadow: 0 18px 38px rgba(2, 8, 19, 0.3);
      }}
      .of-upload-promo-grid {{ display:grid; grid-template-columns: 1.1fr .9fr; gap: 14px; }}
      .of-upload-stat {{
        background: linear-gradient(180deg, rgba(16,35,64,0.94), rgba(11,25,47,0.9));
        border: 1px solid var(--card-border);
        border-radius: 18px;
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
        border: 1px solid rgba(0,224,255,0.22);
        border-radius: 999px;
        padding: 10px 14px;
        background: rgba(8,23,42,0.72);
        color: var(--text);
        font-size: .9rem;
        font-weight: 600;
      }}
      .of-mini-note {{ color: #9BB6D2; font-size: .88rem; line-height: 1.6; }}
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
        color: #D6F1FF;
        font-size: .88rem;
        line-height: 1.5;
        font-weight: 600;
      }}
      .of-stage-title-wrap {{
        padding-top: 18px;
        max-width: 620px;
        margin-left: auto;
      }}
      .of-stage-title-wrap .of-eyebrow {{
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(0,224,255,0.12);
        border: 1px solid rgba(0,224,255,0.18);
        box-shadow: 0 12px 28px rgba(0, 224, 255, 0.1);
      }}
      .of-stage-title {{
        font-size: clamp(2.05rem, 4.1vw, 4.35rem);
        line-height: .96;
        margin: 10px 0 0 0;
        letter-spacing: -0.04em;
        color: #F3FBFF;
        text-shadow: 0 0 22px rgba(0,224,255,0.08);
      }}
      .of-shimmer-text {{
        background: linear-gradient(90deg, #F7FDFF 0%, #00E0FF 24%, #00FFA3 52%, #8B5CF6 74%, #F7FDFF 100%);
        background-size: 220% auto;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: of-shimmer 5s linear infinite;
      }}
      .of-stage-lead {{
        margin: 14px 0 0 0;
        max-width: 560px;
        color: #A8C4DE;
        font-size: .98rem;
        line-height: 1.64;
        font-weight: 500;
        text-shadow: none;
      }}
      .of-hero-v2 {{
        position: relative;
        background:
          radial-gradient(circle at top right, rgba(0,224,255,0.18), transparent 30%),
          radial-gradient(circle at left bottom, rgba(124,58,237,0.16), transparent 34%),
          linear-gradient(180deg, rgba(10,22,41,0.98), rgba(6,14,26,0.96));
        border: 1px solid rgba(0,224,255,0.22);
        border-radius: 30px;
        padding: 32px 28px 26px 28px;
        margin-bottom: 34px;
        box-shadow: 0 0 0 1px rgba(0,224,255,0.08) inset, 0 24px 48px rgba(2, 8, 19, 0.36);
      }}
      .of-hero-v2 h2 {{
        font-size: clamp(2rem, 3.45vw, 3.7rem);
        line-height: .98;
        margin: 12px 0 14px 0;
        max-width: 760px;
        letter-spacing: -0.04em;
        color: #F5FBFF;
        text-shadow: 0 0 18px rgba(0,224,255,0.08);
      }}
      .of-hero-v2 p {{ color: #A8C4DE; line-height: 1.78; max-width: 860px; margin: 0; }}
      .of-proof-v2 {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin-top: 22px;
      }}
      .of-proof-v2 .item {{
        background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
        border: 1px solid rgba(0,224,255,0.16);
        border-radius: 16px;
        padding: 16px;
      }}
      .of-proof-v2 .number {{ font-size: 1.7rem; font-weight: 800; letter-spacing: -0.03em; }}
      .of-proof-v2 .caption {{ color: #A8C4DE; font-size: .9rem; margin-top: 6px; line-height: 1.5; }}
      .of-actionable-intro {{
        color: #A8C4DE;
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
        background: linear-gradient(180deg, rgba(11,24,44,0.9), rgba(7,15,29,0.88));
        border: 1px solid rgba(0,224,255,0.16);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 20px 36px rgba(2, 8, 19, 0.28);
        min-height: 220px;
        transition: transform .28s ease, box-shadow .28s ease, border-color .28s ease, background .28s ease;
      }}
      .of-feature-card-v2:hover {{
        transform: translateY(-5px);
        border-color: rgba(16,183,196,0.45);
        background: linear-gradient(180deg, rgba(14,32,59,0.98), rgba(8,18,36,0.96));
        box-shadow: 0 26px 42px rgba(2, 8, 19, 0.34);
      }}
      .of-feature-card-v2 h4 {{ margin: 12px 0 8px 0; font-size: 1.05rem; color: #F3FBFF; }}
      .of-feature-card-v2 p {{ margin: 0; color: #9BB6D2; font-size: .94rem; line-height: 1.58; font-weight: 500; }}
      .of-feature-icon {{
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(0,224,255,0.18), rgba(124,58,237,0.18));
        color: var(--primary);
        font-weight: 800;
        box-shadow: 0 0 18px rgba(0,224,255,0.14);
      }}
      .of-auth-card {{
        background:
          radial-gradient(circle at top right, rgba(16,183,196,0.14), transparent 34%),
          linear-gradient(180deg, rgba(10,22,41,0.96), rgba(7,15,29,0.94));
        border: 1px solid rgba(0,224,255,0.18);
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 14px;
        box-shadow: 0 24px 46px rgba(2, 8, 19, 0.34);
      }}
      .of-auth-card .of-eyebrow {{ color: #6EF0FF; }}
      .of-auth-card h3 {{
        margin: 10px 0 10px 0;
        font-size: clamp(1.7rem, 2.2vw, 2.45rem);
        line-height: 1.06;
        letter-spacing: -0.03em;
        color: #F3FBFF;
      }}
      .of-auth-card .of-mini-note {{ color: #A8C4DE; }}
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
        color: #F3FBFF;
        font-size: clamp(1.35rem, 2vw, 2rem);
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.03em;
      }}
      .of-contact-meta {{
        margin-top: 6px;
        color: #A8C4DE;
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
      .of-support-hero {{
        display: grid;
        grid-template-columns: minmax(0, 1.15fr) minmax(320px, .85fr);
        gap: 18px;
        margin-bottom: 24px;
      }}
      .of-support-guide {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin-top: 18px;
      }}
      .of-support-guide-card {{
        border: 1px solid rgba(19,62,97,0.12);
        border-radius: 18px;
        padding: 16px;
        background: rgba(255,255,255,0.78);
      }}
      .of-support-guide-card strong {{ display:block; color:#16314D; margin-bottom:8px; }}
      .of-support-guide-card p {{ margin:0; color:#55718B; font-size:.9rem; line-height:1.55; }}
      .of-operator-banner {{
        margin: 10px 0 18px 0;
        padding: 14px 16px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(211,250,245,0.95), rgba(233,247,255,0.95));
        border: 1px solid rgba(16,183,196,0.24);
        color: #0F5273;
        box-shadow: 0 12px 24px rgba(87,137,173,0.08);
      }}
      .of-ticket-meta-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
        margin-bottom: 14px;
      }}
      .of-ticket-meta {{
        border: 1px solid rgba(19,62,97,0.1);
        border-radius: 16px;
        background: rgba(255,255,255,0.78);
        padding: 12px 14px;
      }}
      .of-ticket-meta span {{ display:block; color:#8FADCA; font-size:.76rem; letter-spacing:.08em; text-transform:uppercase; margin-bottom:5px; font-weight:800; }}
      .of-ticket-meta strong {{ color:#F3FBFF; font-size:.94rem; }}
      .of-thread-stack {{ display:grid; gap:12px; margin:14px 0 18px 0; }}
      .of-thread-item {{
        border: 1px solid rgba(19,62,97,0.1);
        border-radius: 18px;
        padding: 15px 16px;
        background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(239,248,255,0.88));
      }}
      .of-thread-item.internal {{
        background: linear-gradient(180deg, rgba(233,248,243,0.96), rgba(223,244,239,0.92));
        border-color: rgba(16,183,196,0.22);
      }}
      .of-thread-head {{ display:flex; justify-content:space-between; gap:12px; align-items:baseline; margin-bottom:8px; }}
      .of-thread-head strong {{ color:#F3FBFF; font-size:.95rem; }}
      .of-thread-head span {{ color:#8FADCA; font-size:.82rem; }}
      .of-thread-body {{ color:#C9E6F8; line-height:1.65; white-space:pre-wrap; }}

      details[data-testid="stExpander"] {{
        border: 1px solid rgba(0,224,255,0.16) !important;
        border-radius: 20px !important;
        background: linear-gradient(180deg, rgba(11,24,44,0.92), rgba(7,15,29,0.9)) !important;
        box-shadow: 0 16px 32px rgba(2,8,19,0.3);
        overflow: hidden;
      }}
      details[data-testid="stExpander"] + details[data-testid="stExpander"] {{ margin-top: 14px; }}
      details[data-testid="stExpander"] summary {{ padding: 14px 18px !important; }}
      details[data-testid="stExpander"] summary p {{ color:#F3FBFF !important; font-weight:700 !important; }}
      details[data-testid="stExpander"] [data-testid="stExpanderDetails"] {{ padding: 0 18px 18px 18px !important; }}

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
        .of-support-hero, .of-support-guide, .of-ticket-meta-grid {{ grid-template-columns: 1fr; }}
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
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(0,224,255,0.14);
        border-radius: 18px;
        padding: 8px;
        margin-bottom: 14px;
      }}
      .stTabs [data-baseweb="tab-list"] button {{
        background: rgba(255,255,255,0.04) !important;
        border-radius: 12px !important;
        color: #9BB6D2 !important;
        font-weight: 800 !important;
        min-height: 44px !important;
      }}
      .stTabs [data-baseweb="tab-list"] button:hover {{
        background: rgba(0,224,255,0.1) !important;
        color: #F3FBFF !important;
      }}
      .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        background: linear-gradient(135deg, rgba(0,224,255,0.16), rgba(124,58,237,0.18)) !important;
        color: #F5FBFF !important;
        border-bottom-color: transparent !important;
      }}

      /* Inputs */
      .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 14px !important;
        background: linear-gradient(180deg, rgba(11,24,44,0.92), rgba(8,18,34,0.88)) !important;
        border: 1px solid rgba(0,224,255,0.18) !important;
        color: #123154 !important;
        box-shadow: 0 14px 28px rgba(2, 8, 19, 0.24) !important;
      }}
      .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{
        border-color: rgba(0,224,255,0.72) !important;
        box-shadow: 0 0 0 1px rgba(0,224,255,0.32), 0 0 24px rgba(0,224,255,0.14) !important;
      }}
      .stTextInput label p, .stNumberInput label p, .stTextArea label p, .stSelectbox label p, .stCheckbox label p {{
        color: #A8C4DE !important;
        font-weight: 700 !important;
        letter-spacing: .01em;
      }}
      .stCaption {{ color: #8FADCA !important; }}
      .stTextInput input::placeholder, .stNumberInput input::placeholder, .stTextArea textarea::placeholder {{
        color: rgba(191,224,246,0.48) !important;
      }}
      .stCheckbox label span, .stCheckbox p {{
        color: #A8C4DE !important;
      }}
      .stTextArea textarea {{ min-height: 128px !important; line-height: 1.6 !important; }}
      .stSelectbox div[data-baseweb="select"] * {{ color: #F3FBFF !important; }}
      div[data-baseweb="popover"] ul, div[role="listbox"] {{
        background: linear-gradient(180deg, rgba(11,24,44,0.98), rgba(8,18,34,0.96)) !important;
        border: 1px solid rgba(0,224,255,0.16) !important;
        border-radius: 16px !important;
      }}
      div[data-baseweb="popover"] li, div[role="option"] {{ color: #F3FBFF !important; }}
      .stForm {{
        background: transparent !important;
      }}
      div[data-testid="stForm"] {{
        border: 1px solid rgba(0,224,255,0.14);
        border-radius: 22px;
        padding: 20px 20px 14px 20px;
        background: linear-gradient(180deg, rgba(10,22,41,0.9), rgba(7,15,29,0.86));
        box-shadow: 0 18px 34px rgba(2,8,19,0.28);
      }}

      .stFileUploader [data-testid="stFileUploaderDropzone"] {{
        border: 1px dashed rgba(0,224,255,0.28) !important;
        border-radius: 20px !important;
        background: linear-gradient(180deg, rgba(10,22,41,0.92), rgba(7,15,29,0.88)) !important;
        padding: 18px !important;
        box-shadow: 0 16px 30px rgba(2,8,19,0.26) !important;
      }}
      .stFileUploader [data-testid="stFileUploaderDropzone"] * {{
        color: #DDF7FF !important;
      }}
      .stFileUploader section button {{
        border-radius: 14px !important;
        border: 1px solid rgba(0,224,255,0.2) !important;
      }}

      .stMarkdown code, .stCode, code {{
        background: linear-gradient(135deg, rgba(0,224,255,0.18), rgba(124,58,237,0.22)) !important;
        color: #EFFFFF !important;
        border: 1px solid rgba(0,224,255,0.18) !important;
        border-radius: 10px !important;
        padding: 0.22rem 0.46rem !important;
        font-weight: 700 !important;
      }}

      .stDataFrame, [data-testid="stDataFrame"] {{ border-radius: 16px; overflow: hidden; }}
      [data-testid="stDataFrame"] div[role="table"] {{
        background: linear-gradient(180deg, rgba(10,22,41,0.96), rgba(7,15,29,0.94)) !important;
        border: 1px solid rgba(0,224,255,0.14) !important;
      }}
      [data-testid="stDataFrame"] * {{ color: #EAF8FF !important; }}

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
