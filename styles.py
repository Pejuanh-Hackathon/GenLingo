"""
Shared styles and UI helpers for GenLingo.
Import this instead of Home to avoid re-rendering the home page.
"""

import streamlit as st
from PIL import Image
import os

# --- Shared Assets ---
_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def get_logo():
    """Load the GenLingo logo image."""
    return Image.open(os.path.join(_ASSETS_DIR, "logo-only-no-bg.png"))

def inject_logo():
    """Render the sidebar logo with proper sizing."""
    st.markdown("""<style>
        img[data-testid="stLogo"] { height: 2rem !important; }
    </style>""", unsafe_allow_html=True)
    st.logo(
        os.path.join(_ASSETS_DIR, "logo-with-inline-text-brightened.png"),
        icon_image=os.path.join(_ASSETS_DIR, "logo-only-no-bg-brightened.png"),
    )

# --- Global CSS ---
GLOBAL_CSS = """<style>
    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .main, .stApp {
        font-family: 'Inter', sans-serif !important;
    }

    /* Smooth page transitions */
    .main .block-container {
        animation: fadeIn 0.45s cubic-bezier(0.22, 1, 0.36, 1);
        max-width: 900px;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Section spacing */
    .gl-section-gap {
        margin-top: 48px;
    }

    /* Button styles */
    .stButton > button {
        font-size: 15px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(50, 98, 240, 0.25);
        background: rgba(50, 98, 240, 0.06);
        transition: all 0.22s cubic-bezier(0.22, 1, 0.36, 1);
        letter-spacing: 0.01em;
    }

    .stButton > button:hover {
        border-color: rgba(50, 98, 240, 0.6) !important;
        background: rgba(50, 98, 240, 0.12) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(50, 98, 240, 0.18);
    }

    .stButton > button:active {
        color: #fff !important;
        background: linear-gradient(135deg, #3262f0, #5b8af5) !important;
        border-color: transparent !important;
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(50, 98, 240, 0.3);
    }

    /* Feature cards */
    .gl-card {
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.85) 0%, rgba(30, 58, 110, 0.65) 100%);
        padding: 28px 24px;
        border-radius: 16px;
        border: 1px solid rgba(50, 98, 240, 0.1);
        margin-bottom: 16px;
        transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1);
        backdrop-filter: blur(8px);
        position: relative;
        overflow: hidden;
    }

    .gl-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(50, 98, 240, 0.4), transparent);
        opacity: 0;
        transition: opacity 0.28s ease;
    }

    .gl-card:hover {
        border-color: rgba(50, 98, 240, 0.35);
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(50, 98, 240, 0.1);
    }

    .gl-card:hover::before {
        opacity: 1;
    }

    .gl-card-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 14px;
        background: linear-gradient(135deg, rgba(50, 98, 240, 0.15), rgba(91, 138, 245, 0.1));
        color: #7ba4f7;
        border: 1px solid rgba(50, 98, 240, 0.15);
    }

    .gl-card-title {
        font-size: 17px;
        font-weight: 700;
        color: #e8eaf0;
        margin-bottom: 8px;
        letter-spacing: -0.01em;
    }

    .gl-card-desc {
        font-size: 14px;
        color: #9ca3b4;
        line-height: 1.6;
    }

    /* CTA buttons */
    .gl-cta {
        display: inline-block;
        background: linear-gradient(135deg, #3262f0, #5b8af5);
        color: white !important;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 15px;
        text-decoration: none;
        transition: all 0.22s cubic-bezier(0.22, 1, 0.36, 1);
        border: none;
        cursor: pointer;
    }

    .gl-cta:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(50, 98, 240, 0.3);
    }

    /* Footer */
    .gl-footer {
        font-size: 13px;
        color: #525a6b;
        text-align: center;
        margin-top: 64px;
        padding: 24px 0 12px 0;
        border-top: 1px solid rgba(255, 255, 255, 0.04);
        letter-spacing: 0.01em;
    }

    .gl-footer span {
        color: #6c7590;
    }

    /* Slang cards for Encyclopedia */
    .slang-card {
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.85) 0%, rgba(28, 45, 80, 0.65) 100%);
        padding: 20px;
        border-radius: 14px;
        border: 1px solid rgba(50, 98, 240, 0.08);
        margin-bottom: 12px;
        transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
        backdrop-filter: blur(8px);
    }

    .slang-card:hover {
        border-color: rgba(50, 98, 240, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(50, 98, 240, 0.08);
    }

    .slang-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-genz {
        background: rgba(139, 92, 246, 0.15);
        color: #a78bfa;
    }

    .badge-genalpha {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
    }

    .slang-term {
        font-size: 17px;
        font-weight: 700;
        color: #e8eaf0;
        margin: 10px 0 6px 0;
    }

    .slang-meaning {
        font-size: 13px;
        color: #9ca3b4;
        line-height: 1.5;
    }

    /* ===== Hero Section ===== */
    .gl-hero {
        position: relative;
        padding: 56px 0 40px 0;
    }

    /* Ambient glow orbs */
    .gl-hero::before,
    .gl-hero::after {
        content: '';
        position: absolute;
        border-radius: 50%;
        filter: blur(120px);
        opacity: 0.12;
        pointer-events: none;
        z-index: 0;
    }

    .gl-hero::before {
        width: 400px;
        height: 400px;
        background: #3262f0;
        top: -100px;
        left: -120px;
        animation: heroOrbDrift 8s ease-in-out infinite alternate;
    }

    .gl-hero::after {
        width: 300px;
        height: 300px;
        background: #8b5cf6;
        bottom: -80px;
        right: -80px;
        animation: heroOrbDrift 10s ease-in-out infinite alternate-reverse;
    }

    @keyframes heroOrbDrift {
        0%   { transform: translate(0, 0) scale(1); }
        100% { transform: translate(30px, 20px) scale(1.1); }
    }

    .gl-hero-inner {
        position: relative;
        z-index: 1;
    }

    /* Top badge */
    .gl-hero-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.4px;
        background: rgba(50, 98, 240, 0.1);
        color: #7ba4f7;
        border: 1px solid rgba(50, 98, 240, 0.15);
        margin-bottom: 20px;
    }

    /* Animated gradient title */
    .gl-hero-title {
        font-size: 42px;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.025em;
        margin-bottom: 18px;
        background: linear-gradient(135deg, #e8eaf0 0%, #7ba4f7 40%, #a78bfa 60%, #e8eaf0 100%);
        background-size: 250% 250%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: heroGradient 6s ease-in-out infinite;
    }

    @keyframes heroGradient {
        0%, 100% { background-position: 0% 50%; }
        50%      { background-position: 100% 50%; }
    }

    .gl-hero-title span {
        -webkit-text-fill-color: #5b8af5;
    }

    .gl-hero-sub {
        font-size: 17px;
        color: #8b93a7;
        margin-bottom: 32px;
        line-height: 1.65;
        max-width: 560px;
    }

    /* Hero CTA row */
    .gl-hero-ctas {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }

    .gl-hero-cta-primary {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 13px 28px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
        border: none;
        background: linear-gradient(135deg, #3262f0, #5b8af5);
        color: #fff !important;
        transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
        box-shadow: 0 4px 16px rgba(50, 98, 240, 0.25);
    }

    .gl-hero-cta-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(50, 98, 240, 0.35);
    }

    .gl-hero-cta-primary .gl-cta-arrow {
        transition: transform 0.2s ease;
    }

    .gl-hero-cta-primary:hover .gl-cta-arrow {
        transform: translateX(3px);
    }

    .gl-hero-cta-secondary {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 13px 28px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
        background: rgba(50, 98, 240, 0.08);
        border: 1px solid rgba(50, 98, 240, 0.2);
        color: #9bb0e8 !important;
        transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
    }

    .gl-hero-cta-secondary:hover {
        background: rgba(50, 98, 240, 0.14);
        border-color: rgba(50, 98, 240, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(50, 98, 240, 0.12);
    }

    /* Stats strip under hero */
    .gl-hero-stats {
        display: flex;
        gap: 40px;
        margin-top: 36px;
        padding-top: 24px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }

    .gl-hero-stat-item {
        display: flex;
        flex-direction: column;
    }

    .gl-hero-stat-num {
        font-size: 22px;
        font-weight: 700;
        color: #e8eaf0;
        letter-spacing: -0.02em;
    }

    .gl-hero-stat-label {
        font-size: 12px;
        color: #6c7590;
        margin-top: 2px;
        letter-spacing: 0.02em;
    }

    /* Chat page */
    .gl-persona-header {
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.85) 0%, rgba(30, 58, 110, 0.65) 100%);
        padding: 18px 22px;
        border-radius: 14px;
        margin-bottom: 20px;
        border: 1px solid rgba(50, 98, 240, 0.1);
        backdrop-filter: blur(8px);
    }

    .gl-persona-name {
        font-size: 18px;
        font-weight: 700;
        color: #e8eaf0;
        letter-spacing: -0.01em;
    }

    .gl-persona-desc {
        font-size: 13px;
        color: #8b93a7;
        margin-top: 2px;
    }

    /* Stat counter */
    .gl-stat {
        font-size: 13px;
        color: #525a6b;
        padding: 6px 0;
    }

    .gl-stat strong {
        color: #8b93a7;
    }

    /* Generation info cards */
    .gl-gen-card {
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.7) 0%, rgba(30, 50, 90, 0.5) 100%);
        padding: 24px;
        border-radius: 14px;
        border: 1px solid rgba(50, 98, 240, 0.08);
        height: 100%;
    }

    .gl-gen-card h4 {
        font-size: 16px;
        font-weight: 700;
        color: #e8eaf0;
        margin-bottom: 8px;
    }

    .gl-gen-card p {
        font-size: 14px;
        color: #9ca3b4;
        line-height: 1.55;
        margin: 0;
    }

    .gl-gen-label {
        display: inline-block;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        padding: 3px 10px;
        border-radius: 6px;
        margin-bottom: 12px;
    }

    .gl-gen-label-z {
        background: rgba(139, 92, 246, 0.12);
        color: #a78bfa;
    }

    .gl-gen-label-a {
        background: rgba(34, 197, 94, 0.12);
        color: #4ade80;
    }

    /* Info callout (replaces st.info) */
    .gl-callout {
        background: rgba(50, 98, 240, 0.06);
        border: 1px solid rgba(50, 98, 240, 0.12);
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 14px;
        color: #9ca3b4;
        line-height: 1.55;
        margin: 16px 0;
    }

    .gl-callout strong {
        color: #b0b8cc;
    }

    /* Sidebar polish */
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 14px;
    }

    /* Hide default Streamlit elements when hero is used */
    .gl-hero-wrapper + div hr {
        margin-top: 0;
    }
</style>"""


def inject_global_styles():
    """Inject all shared CSS styles into the page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_feature_card(container, icon_letter, title, description):
    """Render a styled feature card in the given Streamlit container.
    
    icon_letter: a single letter or short text to display in the icon badge.
                 Pass empty string to skip the icon.
    """
    icon_html = ""
    if icon_letter:
        icon_html = f'<div class="gl-card-icon">{icon_letter}</div>'
    
    container.markdown(
        f'<div class="gl-card">{icon_html}<div class="gl-card-title">{title}</div><div class="gl-card-desc">{description}</div></div>',
        unsafe_allow_html=True,
    )


def render_hero(slang_count=None):
    """Render the full hero section with animated title, glow orbs, CTAs, and stats."""
    stats_html = ""
    if slang_count:
        stats_html = (
            '<div class="gl-hero-stats">'
            '<div class="gl-hero-stat-item">'
            f'<span class="gl-hero-stat-num">{slang_count}+</span>'
            '<span class="gl-hero-stat-label">Slang terms</span>'
            '</div>'
            '<div class="gl-hero-stat-item">'
            '<span class="gl-hero-stat-num">2</span>'
            '<span class="gl-hero-stat-label">Generations</span>'
            '</div>'
            '<div class="gl-hero-stat-item">'
            '<span class="gl-hero-stat-num">AI</span>'
            '<span class="gl-hero-stat-label">Powered chat</span>'
            '</div>'
            '</div>'
        )

    st.markdown(
        '<div class="gl-hero">'
        '<div class="gl-hero-inner">'
        '<div class="gl-hero-badge">Generational language, decoded</div>'
        '<div class="gl-hero-title">Master the Language<br/>of Tomorrow with <span>GenLingo</span></div>'
        '<p class="gl-hero-sub">Understand how Gen Z and Gen Alpha actually talk — learn the slang, bridge the gap, and stay connected across generations.</p>'
        f'{stats_html}'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_footer():
    """Render the shared footer."""
    st.markdown(
        '<div class="gl-footer">'
        'Built by <span>Samuel T. Gunawan</span> · <span>Axel D. Suryanto</span> · <span>Jeremy T. Putra</span> · <span>M. Noor Abdi</span>'
        '</div>',
        unsafe_allow_html=True,
    )
