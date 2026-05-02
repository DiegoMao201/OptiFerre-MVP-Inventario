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
          radial-gradient(circle at top left, rgba(16,183,196,0.12), transparent 28%),
          radial-gradient(circle at top right, rgba(25,74,145,0.18), transparent 32%),
          linear-gradient(180deg, #08111F 0%, #0A1526 36%, #07101B 100%);
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

      @media (max-width: 900px) {{
        .of-grid, .of-proof, .of-plan-strip, .of-trust-grid {{ grid-template-columns: 1fr; }}
        .of-public-topbar {{ flex-direction: column; align-items: flex-start; }}
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
