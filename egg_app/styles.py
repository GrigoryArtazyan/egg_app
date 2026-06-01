"""Injected CSS that recreates the farm-fresh poster look.

Palette: yolk orange #F26B1D, golden #FFB81C, cream #FBF1DC, ink brown #3A2415.
Fonts: Bangers / Luckiest Guy (display), Nunito (body), Permanent Marker (CTA).
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Luckiest+Guy&family=Nunito:wght@400;600;800&family=Permanent+Marker&display=swap');

:root {
    --yolk: #F26B1D;
    --golden: #FFB81C;
    --cream: #FBF1DC;
    --ink: #3A2415;
    --spicy: #D63A1E;
}

html, body, [class*="css"], .stApp {
    font-family: 'Nunito', sans-serif;
    color: var(--ink);
}

.stApp { background-color: var(--cream); }

/* Hero badge */
.egg-badge {
    width: 130px; height: 130px; margin: 0 auto 0.5rem;
    border-radius: 50%;
    background: radial-gradient(circle at 50% 38%, #ff9a4d 0%, var(--yolk) 70%);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 6px 0 rgba(58,36,21,0.25);
    font-size: 3.5rem;
}

/* Starburst-style headline */
.egg-title {
    font-family: 'Luckiest Guy', cursive;
    color: var(--golden);
    text-align: center;
    font-size: 2.9rem;
    line-height: 1.05;
    letter-spacing: 1px;
    text-shadow:
        -2px -2px 0 var(--ink), 2px -2px 0 var(--ink),
        -2px 2px 0 var(--ink), 2px 2px 0 var(--ink),
        0 6px 0 rgba(58,36,21,0.35);
    margin: 0.2rem 0 0.1rem;
}

.egg-subtitle {
    font-family: 'Bangers', cursive;
    text-align: center;
    color: var(--yolk);
    font-size: 1.5rem;
    letter-spacing: 2px;
    margin-bottom: 1rem;
}

.egg-section {
    font-family: 'Bangers', cursive;
    color: var(--ink);
    font-size: 1.6rem;
    letter-spacing: 1px;
    margin: 0.6rem 0 0.2rem;
}

/* Sticker-style cards */
.egg-card {
    background: #fff;
    border: 2px solid var(--ink);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    box-shadow: 4px 4px 0 rgba(58,36,21,0.18);
    margin: 0.6rem 0;
}

.egg-price {
    font-family: 'Bangers', cursive;
    color: var(--spicy);
    font-size: 1.3rem;
}

/* Taped-label primary button (the PRE-ORDER NOW vibe) */
.stButton > button, .stFormSubmitButton > button {
    font-family: 'Permanent Marker', cursive !important;
    background: #fff !important;
    color: var(--ink) !important;
    border: 2px solid var(--ink) !important;
    border-radius: 4px !important;
    font-size: 1.15rem !important;
    padding: 0.5rem 1.4rem !important;
    box-shadow: 3px 3px 0 var(--yolk) !important;
    transform: rotate(-1.5deg);
    transition: transform 0.08s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: rotate(0deg) scale(1.02);
    background: var(--golden) !important;
}

.egg-total {
    font-family: 'Luckiest Guy', cursive;
    color: var(--yolk);
    font-size: 1.8rem;
    text-align: center;
}

/* Product option tiles rendered as full clickable buttons */
.st-key-pick_tray button, .st-key-pick_dozen button {
    transform: none !important;
    font-family: 'Bangers', cursive !important;
    letter-spacing: 1px;
    background: #fff !important;
    color: var(--ink) !important;
    border: 3px solid var(--ink) !important;
    border-radius: 16px !important;
    box-shadow: 4px 4px 0 rgba(58,36,21,0.18) !important;
    min-height: 160px !important;
    padding: 0.8rem 0.5rem !important;
    line-height: 1.35 !important;
    transition: opacity 0.12s ease, box-shadow 0.12s ease, transform 0.12s ease;
}
.st-key-pick_tray button:hover, .st-key-pick_dozen button:hover {
    background: #fff7ec !important;
    transform: translateY(-2px) !important;
}
.st-key-pick_tray button p, .st-key-pick_dozen button p { margin: 0.1rem 0 !important; }
.st-key-pick_tray button p:first-child,
.st-key-pick_dozen button p:first-child { font-size: 2.2rem !important; }

/* Tighten default padding so content fills small screens */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 640px;
}

/* Make form controls finger-friendly on touch devices */
.stButton > button, .stFormSubmitButton > button { width: 100%; }
input, .stNumberInput input, .stTextInput input { font-size: 16px !important; }

/* Phone-sized screens */
@media (max-width: 640px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .egg-badge { width: 96px; height: 96px; font-size: 2.6rem; }
    .egg-title { font-size: 2rem; }
    .egg-subtitle { font-size: 1.15rem; }
    .egg-section { font-size: 1.3rem; }
    .egg-card { padding: 0.85rem 1rem; }
    .egg-total { font-size: 1.5rem; }
}
</style>
"""


def inject() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def badge() -> None:
    st.markdown('<div class="egg-badge">🥚</div>', unsafe_allow_html=True)


def title(text: str) -> None:
    st.markdown(f'<div class="egg-title">{text}</div>', unsafe_allow_html=True)


def subtitle(text: str) -> None:
    st.markdown(f'<div class="egg-subtitle">{text}</div>', unsafe_allow_html=True)


def section(text: str) -> None:
    st.markdown(f'<div class="egg-section">{text}</div>', unsafe_allow_html=True)


_SELECTED = """
.st-key-pick_{sel} button {{
    border-color: var(--yolk) !important;
    background: #fff7ec !important;
    box-shadow: 5px 5px 0 var(--yolk) !important;
}}
.st-key-pick_{other} button {{
    opacity: 0.4 !important;
    filter: grayscale(0.6) !important;
    box-shadow: none !important;
}}
.st-key-pick_{other} button:hover {{
    opacity: 0.65 !important;
    background: #fff !important;
}}
"""


def option_state(product: str | None) -> None:
    """Highlight the chosen option tile and shade the other one."""
    if product not in ("tray", "dozen"):
        return
    other = "dozen" if product == "tray" else "tray"
    css = _SELECTED.format(sel=product, other=other)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
