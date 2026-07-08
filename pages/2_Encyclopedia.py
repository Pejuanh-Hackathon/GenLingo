import streamlit as st

st.set_page_config(
    page_title="Slang Encyclopedia",
    layout="centered",
    page_icon="./assets/logo-only-no-bg-brightened.png",
)

from styles import inject_global_styles, inject_logo, render_footer
import pandas as pd

# --- Inject shared styles ---
inject_global_styles()
inject_logo()

# --- Load slang data from CSV (single source of truth) ---
@st.cache_data(show_spinner=False)
def load_slang_data():
    genz_df = pd.read_csv("dataset/Gen_Z_slang_data.csv", sep=";")
    genalpha_df = pd.read_csv("dataset/Gen_Alpha_Dataset_Slang.csv", sep=";")

    genz_df["Gen"] = "Gen Z"
    genalpha_df["Gen"] = "Gen Alpha"

    df = pd.concat([genz_df, genalpha_df], ignore_index=True)
    # Remove duplicates — keep first occurrence per (Slang, Gen) pair
    df = df.drop_duplicates(subset=["Slang", "Gen"], keep="first")
    df["Slang_lower"] = df["Slang"].astype(str).str.lower()
    return df


df = load_slang_data()

# --- Page header ---
st.markdown("# Slang Encyclopedia")
st.markdown("*Powered by :blue[GenLingo]*")

# --- Filters ---
col_search, col_filter = st.columns([3, 1])

with col_search:
    text_search = st.text_input(
        "Search slangs",
        value="",
        placeholder="Type a slang term...",
        label_visibility="collapsed",
    )

with col_filter:
    gen_filter = st.selectbox(
        "Generation",
        ["All", "Gen Z", "Gen Alpha"],
        label_visibility="collapsed",
    )

# --- Apply filters ---
mask = pd.Series(True, index=df.index)

if text_search:
    mask = mask & (
        df["Slang_lower"].str.contains(text_search.lower(), na=False)
        | df["Meaning"].str.contains(text_search, case=False, na=False)
    )

if gen_filter != "All":
    mask = mask & (df["Gen"] == gen_filter)

df_filtered = df[mask]

# --- Results count ---
total = len(df)
showing = len(df_filtered)
st.markdown(
    f'<div class="gl-stat">Showing <strong>{showing}</strong> of <strong>{total}</strong> slangs</div>',
    unsafe_allow_html=True,
)

# --- Display results ---
if df_filtered.empty:
    st.markdown(f"### No slangs match :blue[{text_search}]")
    st.markdown("Try the **GenLingo Bot** for the latest slang updates.")
    if st.button("Chat with GenLingo Bot"):
        st.switch_page("./pages/1_GenLingo.py")
else:
    N_cards_per_row = 3
    for n_row, row in df_filtered.reset_index(drop=True).iterrows():
        i = n_row % N_cards_per_row
        if i == 0:
            cols = st.columns(N_cards_per_row, gap="medium")

        gen = row["Gen"].strip()
        badge_class = "badge-genz" if gen == "Gen Z" else "badge-genalpha"
        badge_label = "Gen Z" if gen == "Gen Z" else "Gen Alpha"

        with cols[i]:
            st.markdown(
                f"""<div class="slang-card">
                    <span class="slang-badge {badge_class}">{badge_label}</span>
                    <div class="slang-term">{row['Slang']}</div>
                    <div class="slang-meaning">{row['Meaning']}</div>
                </div>""",
                unsafe_allow_html=True,
            )

# --- Footer ---
render_footer()
