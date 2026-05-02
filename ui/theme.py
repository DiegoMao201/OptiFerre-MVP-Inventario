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
        bg = "#FFFFFF"
        bg2 = "#F5F6FA"
        text = "#1A1F2B"
        muted = "#5b6479"
        card_border = "rgba(0,0,0,0.08)"
    else:
        bg = "#08111F"
        bg2 = "#101C32"
        text = "#F7FAFC"
        muted = "#AAB7CC"
        card_border = "rgba(255,255,255,0.08)"

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
          radial-gradient(circle at top left, rgba(255,255,255,0.42), transparent 18%),
          radial-gradient(circle at 20% 7%, rgba(16,183,196,0.16), transparent 21%),
          radial-gradient(circle at top right, rgba(25,74,145,0.14), transparent 24%),
          linear-gradient(180deg, #DCEBFA 0%, #B9D0E7 10%, #6F97BE 20%, #23446D 34%, #10213B 50%, #08111F 100%);
        color: var(--text);
      }}
      section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(16,28,50,0.98), rgba(8,17,31,0.98));
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
        background: var(--bg2);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 18px 20px;
        height: 100%;
      }}
      .of-kpi .label {{ color: var(--muted); font-size: 0.82rem; text-transform: uppercase; letter-spacing: .08em; }}
      .of-kpi .value {{ color: var(--text); font-size: 1.85rem; font-weight: 700; margin-top: 6px; }}
      .of-kpi .delta {{ color: var(--primary); font-size: 0.85rem; margin-top: 4px; }}

      /* Banner */
      .of-banner {{
        background: linear-gradient(135deg, var(--primary-soft), transparent);
        border: 1px solid var(--primary);
        border-radius: 14px;
        padding: 16px 20px;
        margin: 8px 0 18px 0;
      }}
      .of-banner h4 {{ margin: 0 0 4px 0; color: var(--primary); }}
      .of-banner p {{ margin: 0; color: var(--text); opacity: 0.92; }}
      .of-section-shell {{ margin: 0 0 14px 0; }}
      .of-exec-shell {{
        background:
          radial-gradient(circle at top right, rgba(16,183,196,0.18), transparent 36%),
          linear-gradient(135deg, rgba(255,255,255,0.03), transparent),
          var(--bg2);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 18px;
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
        background: rgba(255,255,255,0.025);
      }}
      .of-metric-pill .caption {{ color: var(--muted); font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }}
      .of-metric-pill .value {{ color: var(--text); font-size: 1.45rem; font-weight: 700; margin-top: 6px; }}
      .of-priority-card {{
        background: rgba(255,255,255,0.025);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 16px 18px;
      }}
      .of-priority-list {{ margin: 12px 0 0 0; padding-left: 18px; }}
      .of-priority-list li {{ margin-bottom: 8px; color: var(--text); }}
      .of-chip-row {{ display:flex; flex-wrap:wrap; gap:10px; margin-top: 14px; }}
      .of-chip {{
        display:inline-flex;
        align-items:center;
        gap:8px;
        border:1px solid rgba(16,33,59,0.14);
        border-radius:999px;
        padding:8px 12px;
        background: rgba(255,255,255,0.48);
        color: #123154;
        font-size: .85rem;
        font-weight: 700;
        box-shadow: 0 10px 28px rgba(10, 25, 47, 0.08);
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
        background: rgba(8,17,31,0.35);
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
      .of-mini-note {{ color: var(--muted); font-size: .86rem; line-height: 1.55; }}
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
      .of-stage-title {{
        font-size: clamp(2.4rem, 4.8vw, 5rem);
        line-height: .96;
        margin: 10px 0 0 0;
        letter-spacing: -0.04em;
        background: linear-gradient(180deg, #143153 0%, #214874 34%, #6E96C0 68%, #F2F7FD 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 0 12px 30px rgba(8, 17, 31, 0.08);
      }}
      .of-stage-lead {{
        margin: 16px 0 0 0;
        max-width: 560px;
        color: rgba(227,237,248,0.92);
        font-size: 1.04rem;
        line-height: 1.72;
        font-weight: 500;
        text-shadow: 0 8px 20px rgba(8, 17, 31, 0.12);
      }}
      .of-hero-v2 {{
        position: relative;
        background:
          radial-gradient(circle at top right, rgba(255,255,255,0.16), transparent 32%),
          radial-gradient(circle at left top, rgba(16,183,196,0.16), transparent 34%),
          linear-gradient(180deg, rgba(28,53,87,0.96), rgba(11,23,42,0.98));
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        padding: 28px 26px 26px 26px;
        margin-bottom: 22px;
        box-shadow: 0 24px 46px rgba(8, 17, 31, 0.22);
      }}
      .of-hero-v2 h2 {{
        font-size: clamp(2.35rem, 4vw, 4.4rem);
        line-height: .98;
        margin: 14px 0 16px 0;
        max-width: 760px;
        letter-spacing: -0.04em;
      }}
      .of-hero-v2 p {{ color: var(--muted); line-height: 1.7; max-width: 860px; margin: 0; }}
      .of-proof-v2 {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin-top: 22px;
      }}
      .of-proof-v2 .item {{
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 16px;
      }}
      .of-proof-v2 .number {{ font-size: 1.7rem; font-weight: 800; letter-spacing: -0.03em; }}
      .of-proof-v2 .caption {{ color: var(--muted); font-size: .88rem; margin-top: 6px; line-height: 1.45; }}
      .of-stat-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin: 18px 0 22px 0;
      }}
      .of-stat-card {{
        background: linear-gradient(180deg, rgba(255,255,255,0.28), rgba(255,255,255,0.1));
        border: 1px solid rgba(16,33,59,0.12);
        border-radius: 18px;
        padding: 18px 16px;
        box-shadow: 0 12px 28px rgba(8, 17, 31, 0.08);
      }}
      .of-stat-card .value {{ color: #123154; font-size: 1.65rem; font-weight: 800; letter-spacing: -0.03em; }}
      .of-stat-card .caption {{ color: rgba(18,49,84,0.78); font-size: .82rem; line-height: 1.4; margin-top: 6px; }}
      .of-feature-grid-v2 {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
      }}
      .of-feature-card-v2 {{
        background: linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0.06));
        border: 1px solid rgba(16,33,59,0.12);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 14px 28px rgba(8, 17, 31, 0.08);
      }}
      .of-feature-card-v2 h4 {{ margin: 12px 0 8px 0; font-size: 1.05rem; color: #123154; }}
      .of-feature-card-v2 p {{ margin: 0; color: rgba(18,49,84,0.78); font-size: .92rem; line-height: 1.55; }}
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
        background: linear-gradient(180deg, rgba(255,255,255,0.14), rgba(15,28,50,0.96));
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 14px;
        box-shadow: 0 22px 44px rgba(8, 17, 31, 0.2);
      }}
      .of-auth-card h3 {{
        margin: 10px 0 10px 0;
        font-size: clamp(1.7rem, 2.2vw, 2.45rem);
        line-height: 1.06;
        letter-spacing: -0.03em;
      }}
      .of-proof-grid-v2 {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin-top: 16px;
        margin-bottom: 12px;
      }}
      .of-proof-card-v2 {{
        background: linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0.06));
        border: 1px solid rgba(16,33,59,0.12);
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 16px 34px rgba(8, 17, 31, 0.08);
      }}
      .of-proof-card-v2 p {{
        margin: 12px 0 14px 0;
        color: #123154;
        font-size: 1rem;
        line-height: 1.7;
      }}
      .of-proof-person {{ color: rgba(18,49,84,0.76); font-size: .88rem; }}
      .of-price-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin-top: 8px;
      }}
      .of-price-card {{
        position: relative;
        background: linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0.08));
        border: 1px solid rgba(16,33,59,0.12);
        border-radius: 22px;
        padding: 22px 20px;
        box-shadow: 0 16px 34px rgba(8, 17, 31, 0.08);
      }}
      .of-price-popular {{
        background: linear-gradient(180deg, rgba(16,183,196,0.09), rgba(255,255,255,0.03));
        border-color: rgba(16,183,196,0.55);
        box-shadow: 0 0 0 1px rgba(16,183,196,0.12) inset;
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
      .of-price-main {{ margin: 14px 0 14px 0; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.04em; }}
      .of-price-main span {{ color: rgba(18,49,84,0.7); font-size: .95rem; font-weight: 500; margin-left: 2px; }}
      .of-price-list {{ margin: 0; padding-left: 18px; color: rgba(18,49,84,0.82); }}
      .of-price-list li {{ margin-bottom: 8px; line-height: 1.45; }}
      .of-final-cta {{
        margin-top: 22px;
        padding: 32px 28px;
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.18);
        background: linear-gradient(180deg, rgba(230,241,251,0.58), rgba(19,41,70,0.9));
        text-align: center;
        box-shadow: 0 24px 48px rgba(8, 17, 31, 0.18);
      }}
      .of-final-cta h3 {{
        font-size: clamp(2rem, 3vw, 3.35rem);
        line-height: .98;
        letter-spacing: -0.04em;
        margin: 12px 0;
      }}

      @media (max-width: 900px) {{
        .of-grid, .of-proof, .of-plan-strip, .of-trust-grid {{ grid-template-columns: 1fr; }}
      .of-final-cta .of-eyebrow {{ color: #10B7C4; }}
      .of-final-cta p {{ color: rgba(234,242,251,0.86); }}

      div[data-testid="stPopover"] > button,
      div[data-testid="stPopover"] button[kind="secondary"],
      button[kind="secondaryFormSubmit"],
      button[kind="secondary"] {{
        background: linear-gradient(180deg, rgba(248,251,255,0.96), rgba(220,233,247,0.92)) !important;
        color: #123154 !important;
        border: 1px solid rgba(16,33,59,0.14) !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 24px rgba(8, 17, 31, 0.08) !important;
        font-weight: 700 !important;
      }}
      div[data-testid="stPopover"] > button:hover,
      div[data-testid="stPopover"] button[kind="secondary"]:hover,
      button[kind="secondary"]:hover {{
        color: #0E2A48 !important;
        border-color: rgba(16,183,196,0.4) !important;
        box-shadow: 0 14px 28px rgba(8, 17, 31, 0.12) !important;
      }}
      div[data-testid="stPopoverContent"] {{
        border-radius: 18px !important;
        border: 1px solid rgba(16,33,59,0.12) !important;
        background: linear-gradient(180deg, rgba(246,250,255,0.98), rgba(218,232,247,0.96)) !important;
      }}
      div[data-testid="stPopoverContent"] * {{ color: #123154 !important; }}
        .of-public-topbar {{ flex-direction: column; align-items: flex-start; }}
        .of-exec-grid, .of-metric-strip, .of-upload-promo-grid {{ grid-template-columns: 1fr; }}
        .of-stage-title-wrap {{ margin-left: 0; max-width: 100%; }}
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
      .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: var(--primary) !important;
        border-bottom-color: var(--primary) !important;
      }}

      /* Inputs */
      .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 10px !important;
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
            f"<div class='of-pill'>OptiFerre SaaS</div> "
            f"<span style='color:var(--muted); margin-left:8px;'>{tagline}</span>",
            unsafe_allow_html=True,
        )
    st.divider()
