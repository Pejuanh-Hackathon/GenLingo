import streamlit as st

st.set_page_config(
    page_title="GenLingo — Master the Language of Tomorrow",
    layout="centered",
    page_icon="./assets/logo-only-no-bg-brightened.png",
)

from styles import inject_global_styles, inject_logo, render_feature_card, render_footer, render_hero
import pandas as pd

# --- Inject shared styles ---
inject_global_styles()
inject_logo()

# --- Count slang terms for hero stats ---
@st.cache_data(show_spinner=False)
def _count_slangs():
    genz = pd.read_csv("dataset/Gen_Z_slang_data.csv", sep=";")
    genalpha = pd.read_csv("dataset/Gen_Alpha_Dataset_Slang.csv", sep=";")
    return len(genz) + len(genalpha)

# --- Hero Section ---
render_hero(slang_count=_count_slangs())

col_cta1, col_cta2, _ = st.columns([1, 1, 2])
with col_cta1:
    if st.button("Try GenLingo", key="gl-bot-cta1", type="primary", use_container_width=True):
        st.switch_page("./pages/1_GenLingo.py")
with col_cta2:
    if st.button("Encyclopedia", key="ency-cta1", use_container_width=True):
        st.switch_page("./pages/2_Encyclopedia.py")

st.divider()

# --- About Section ---
st.markdown("## What is GenLingo?")
st.markdown(
    "GenLingo is a smart chatbot that helps you learn and engage with the "
    "slang and language styles of **Gen Z** and **Gen Alpha**. Whether you're a parent, "
    "teacher, or just curious — GenLingo keeps you fluent in the language that matters."
)

st.markdown(
    '<div class="gl-callout">'
    '<strong>Heads up:</strong> GenLingo is currently in development. '
    'Some responses may be imperfect — your feedback helps us improve.'
    '</div>',
    unsafe_allow_html=True,
)

# --- Key Features Section ---
st.markdown("## Why GenLingo?")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

render_feature_card(col1, "C", "Interactive Chatbot", "Switch between Gen Z and Gen Alpha modes to learn their unique slang in real conversations.")
render_feature_card(col2, "R", "Real-Time Updates", "Stay current with the latest trends and slang as they evolve across platforms.")
render_feature_card(col3, "E", "Educational Integration", "Enhance classroom interactions by understanding how your students actually communicate.")
render_feature_card(col4, "B", "Cultural Bridge", "Facilitate better communication and understanding between different generations.")

# --- Demographics Section ---
st.markdown("## Understanding the Generations")
col_z, col_a = st.columns(2)
with col_z:
    st.markdown(
        '<div class="gl-gen-card">'
        '<span class="gl-gen-label gl-gen-label-z">Gen Z</span>'
        '<h4>Born 1997 – 2012</h4>'
        '<p>About 20% of the global population. Known for their presence '
        'on TikTok and Instagram, and their focus on social activism and mental health awareness.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
with col_a:
    st.markdown(
        '<div class="gl-gen-card">'
        '<span class="gl-gen-label gl-gen-label-a">Gen Alpha</span>'
        '<h4>Born 2013 – 2025</h4>'
        '<p>Expected to reach 2 billion globally by 2025. Characterized by '
        'early exposure to technology and high levels of digital proficiency.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

# --- Who Benefits Section ---
st.markdown("## Who Can Benefit?")
benefits = [
    ("P", "Parents", "Stay connected with your kids by understanding the language they use every day."),
    ("E", "Educators", "Keep up with student slang to improve classroom engagement and rapport."),
    ("M", "Marketers", "Speak the language of your audience to create campaigns that actually resonate."),
    ("T", "Therapists", "Improve communication in sessions with younger clients through shared vocabulary."),
]
cols = st.columns(2)
for i, (letter, title, desc) in enumerate(benefits):
    with cols[i % 2]:
        render_feature_card(cols[i % 2], letter, title, desc)

# --- Bottom CTA ---
st.divider()
st.markdown("## Ready to Get Started?")
col_cta3, col_cta4, _ = st.columns([1, 1, 2])
with col_cta3:
    if st.button("Try GenLingo", key="gl-bot-cta2", use_container_width=True):
        st.switch_page("./pages/1_GenLingo.py")
with col_cta4:
    if st.button("Encyclopedia", key="ency-cta2", use_container_width=True):
        st.switch_page("./pages/2_Encyclopedia.py")

# --- Footer ---
render_footer()
