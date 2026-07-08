"""
Pop Quiz — GenLingo
===================
Learning Science Principles Applied:
  1. SPACED REPETITION  — Wrong answers re-enter the queue ~4 cards later
  2. ACTIVE RECALL       — Three quiz modes force memory retrieval
  3. DESIRABLE DIFFICULTY — Progressive hints add scaffolding without giving away
  4. ELABORATIVE FEEDBACK — Post-answer context with usage tips deepens encoding
  5. METACOGNITION        — Per-term mastery tracking shows what you know / don't
  6. TESTING EFFECT       — Repeated testing outperforms passive re-reading
  7. INTERLEAVING         — Gen Z + Gen Alpha terms mixed by default
"""

import streamlit as st

st.set_page_config(
    page_title="Pop Quiz — GenLingo",
    layout="centered",
    page_icon="./assets/logo-only-no-bg-brightened.png",
)

from styles import inject_global_styles, inject_logo, render_footer
import pandas as pd
import random

# --- Inject shared styles ---
inject_global_styles()
inject_logo()

# --- Quiz-specific CSS ---
st.markdown("""<style>
    /* Flashcard */
    .quiz-flashcard {
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.9) 0%, rgba(30, 58, 110, 0.7) 100%);
        border: 1px solid rgba(50, 98, 240, 0.12);
        border-radius: 18px;
        padding: 48px 32px;
        text-align: center;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(8px);
        transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        animation: cardSlideIn 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    }

    @keyframes cardSlideIn {
        from { opacity: 0; transform: translateY(16px) scale(0.98); }
        to   { opacity: 1; transform: translateY(0) scale(1); }
    }

    .quiz-flashcard::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3262f0, #a78bfa, #3262f0);
        background-size: 200% 100%;
        animation: shimmer 3s ease-in-out infinite;
    }

    @keyframes shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    .quiz-flashcard:hover {
        border-color: rgba(50, 98, 240, 0.35);
        transform: translateY(-3px);
        box-shadow: 0 16px 40px rgba(50, 98, 240, 0.12);
    }

    .quiz-flashcard-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #6c7590;
        margin-bottom: 16px;
    }

    .quiz-flashcard-term {
        font-size: 32px;
        font-weight: 800;
        color: #e8eaf0;
        letter-spacing: -0.02em;
        margin-bottom: 8px;
    }

    .quiz-flashcard-meaning {
        font-size: 18px;
        color: #9bb0e8;
        line-height: 1.5;
        max-width: 440px;
    }

    .quiz-flashcard-hint {
        font-size: 12px;
        color: #525a6b;
        margin-top: 20px;
    }

    /* Score display */
    .quiz-score {
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.7) 0%, rgba(30, 50, 90, 0.5) 100%);
        border: 1px solid rgba(50, 98, 240, 0.1);
        border-radius: 14px;
        padding: 18px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }

    .quiz-score-item { text-align: center; }

    .quiz-score-num {
        font-size: 24px;
        font-weight: 700;
        color: #e8eaf0;
    }

    .quiz-score-num.correct { color: #4ade80; }
    .quiz-score-num.wrong { color: #f87171; }
    .quiz-score-num.streak { color: #facc15; }

    .quiz-score-label {
        font-size: 11px;
        color: #6c7590;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }

    /* Result feedback */
    .quiz-correct {
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 12px;
        padding: 16px 20px;
        color: #4ade80;
        font-size: 15px;
        font-weight: 600;
        margin: 12px 0;
        animation: cardSlideIn 0.3s ease;
    }

    .quiz-wrong {
        background: rgba(248, 113, 113, 0.08);
        border: 1px solid rgba(248, 113, 113, 0.3);
        border-radius: 12px;
        padding: 16px 20px;
        color: #f87171;
        font-size: 15px;
        font-weight: 600;
        margin: 12px 0;
        animation: cardSlideIn 0.3s ease;
    }

    /* Progress bar */
    .quiz-progress {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        height: 6px;
        margin-bottom: 24px;
        overflow: hidden;
    }

    .quiz-progress-fill {
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #3262f0, #a78bfa);
        transition: width 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    }

    /* Hint box */
    .quiz-hint-box {
        background: rgba(250, 204, 21, 0.06);
        border: 1px solid rgba(250, 204, 21, 0.2);
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 14px;
        color: #facc15;
        margin: 8px 0 12px 0;
        animation: cardSlideIn 0.3s ease;
    }

    /* Learning tip box (post-answer) */
    .quiz-learn-tip {
        background: rgba(50, 98, 240, 0.06);
        border: 1px solid rgba(50, 98, 240, 0.15);
        border-radius: 12px;
        padding: 14px 18px;
        margin: 12px 0;
        animation: cardSlideIn 0.3s ease;
    }

    .quiz-learn-tip-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #7ba4f7;
        margin-bottom: 6px;
    }

    .quiz-learn-tip-text {
        font-size: 14px;
        color: #9ca3b4;
        line-height: 1.55;
    }

    /* Retry badge */
    .quiz-retry-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: rgba(250, 204, 21, 0.12);
        color: #facc15;
        margin-bottom: 8px;
    }

    /* Mastery cards for summary */
    .mastery-card {
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.7) 0%, rgba(30, 50, 90, 0.5) 100%);
        border-radius: 14px;
        padding: 16px 20px;
        border: 1px solid rgba(50, 98, 240, 0.08);
        margin-bottom: 8px;
    }

    .mastery-card-header {
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .mastery-card-header.mastered { color: #4ade80; }
    .mastery-card-header.learning { color: #facc15; }
    .mastery-card-header.missed   { color: #f87171; }

    .mastery-term {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        margin: 3px 4px 3px 0;
    }

    .mastery-term.mastered {
        background: rgba(34, 197, 94, 0.1);
        color: #4ade80;
    }

    .mastery-term.learning {
        background: rgba(250, 204, 21, 0.1);
        color: #facc15;
    }

    .mastery-term.missed {
        background: rgba(248, 113, 113, 0.1);
        color: #f87171;
    }
</style>""", unsafe_allow_html=True)


# --- Load slang data ---
@st.cache_data(show_spinner=False)
def load_all_slang():
    genz_df = pd.read_csv("dataset/Gen_Z_slang_data.csv", sep=";")
    genalpha_df = pd.read_csv("dataset/Gen_Alpha_Dataset_Slang.csv", sep=";")
    genz_df["Gen"] = "Gen Z"
    genalpha_df["Gen"] = "Gen Alpha"
    df = pd.concat([genz_df, genalpha_df], ignore_index=True)
    df = df.drop_duplicates(subset=["Slang"], keep="first")
    return df


df = load_all_slang()
all_slangs = list(zip(df["Slang"], df["Meaning"], df["Gen"]))


# --- Learning science helpers ---

def generate_usage_tip(slang, meaning, gen):
    """Generate a contextual usage example (Elaborative Feedback)."""
    templates_genz = [
        f'Try it: "That new song is {slang.lower()} fr" — telling a friend something is {meaning.lower()}.',
        f'In context: "She really {slang.lower()}ed that outfit today" — when someone {meaning.lower()}.',
        f'Use it like: "Ngl, that was so {slang.lower()}" — expressing that something is {meaning.lower()}.',
    ]
    templates_alpha = [
        f'Try it: "Bro that\'s so {slang.lower()}" — telling your friends something is {meaning.lower()}.',
        f'In context: "That was {slang.lower()} fr fr" — when something is {meaning.lower()}.',
        f'Use it like: "Yo, major {slang.lower()} moment" — reacting to {meaning.lower()}.',
    ]
    templates = templates_genz if gen == "Gen Z" else templates_alpha
    return random.choice(templates)


def generate_hint(slang, meaning, gen):
    """Generate a progressive hint (Desirable Difficulty / Scaffolding)."""
    hints = []
    # Level 1: Category hint
    hints.append(f"🏷️ This is a **{gen}** slang term.")
    # Level 2: First letter + length
    hints.append(f"🔤 The meaning starts with **\"{meaning[0].upper()}\"** and is {len(meaning.split())} words long.")
    # Level 3: Partial reveal
    words = meaning.split()
    if len(words) >= 3:
        revealed = words[0] + " " + " ".join(["___" for _ in words[1:]])
        hints.append(f"💡 Partial meaning: **{revealed}**")
    else:
        hints.append(f"💡 Think about what it means to be **{meaning.split()[0].lower()}**...")
    return hints


def requeue_wrong_answer(slang, meaning, gen):
    """Spaced Repetition: Re-insert wrong answer ~4 positions later."""
    pool = st.session_state["quiz_pool"]
    idx = st.session_state["quiz_index"]
    insert_pos = min(idx + random.randint(3, 5), len(pool))
    pool.insert(insert_pos, (slang, meaning, gen))
    # Extend total to accommodate the retry
    st.session_state["quiz_total"] = min(
        st.session_state["quiz_total"] + 1,
        len(pool),
    )


# --- Session state init ---
def init_quiz_state(pool, length):
    """Initialize all quiz session state."""
    random.shuffle(pool)
    st.session_state["quiz_pool"] = pool
    st.session_state["quiz_index"] = 0
    st.session_state["quiz_correct"] = 0
    st.session_state["quiz_wrong"] = 0
    st.session_state["quiz_streak"] = 0
    st.session_state["quiz_best_streak"] = 0
    st.session_state["quiz_answered"] = False
    st.session_state["quiz_answer_correct"] = None
    st.session_state["quiz_selected"] = None
    st.session_state["quiz_flipped"] = False
    st.session_state["quiz_total"] = min(length, len(pool))
    # Learning tracking (Metacognition)
    st.session_state["quiz_term_results"] = {}  # slang → {"correct": n, "wrong": n, "hints": n}
    st.session_state["quiz_hint_level"] = 0  # current hint depth for active card
    st.session_state["quiz_hint_used"] = False
    st.session_state["quiz_is_retry"] = False  # flag if current card is a spaced-rep retry


if "quiz_pool" not in st.session_state:
    init_quiz_state(all_slangs.copy(), 15)


# --- Track per-term results ---
def record_result(slang, correct, hint_used=False):
    """Track per-term learning data for mastery analysis."""
    results = st.session_state.setdefault("quiz_term_results", {})
    if slang not in results:
        results[slang] = {"correct": 0, "wrong": 0, "hints": 0, "attempts": 0}
    results[slang]["attempts"] += 1
    if correct:
        results[slang]["correct"] += 1
    else:
        results[slang]["wrong"] += 1
    if hint_used:
        results[slang]["hints"] += 1


# --- Page header ---
st.markdown("# :blue[Pop Quiz]")
st.markdown("*Powered by :blue[GenLingo]*")

# --- Sidebar ---
with st.sidebar:
    st.markdown("### Quiz Settings")

    gen_filter = st.selectbox(
        "Generation",
        ["All", "Gen Z", "Gen Alpha"],
        key="quiz_gen_filter",
    )

    quiz_mode = st.radio(
        "Quiz Mode",
        ["🃏 Flashcards", "📝 Multiple Choice", "✍️ Type the Answer"],
        key="quiz_mode_radio",
    )

    quiz_length = st.select_slider(
        "Questions",
        options=[5, 10, 15, 20, 30],
        value=15,
        key="quiz_length_slider",
    )

    st.divider()

    if st.button("🔄 New Quiz", use_container_width=True):
        if gen_filter != "All":
            filtered = [s for s in all_slangs if s[2] == gen_filter]
        else:
            filtered = all_slangs.copy()
        init_quiz_state(filtered, quiz_length)
        st.toast("New quiz started! 🔥")
        st.rerun()


# --- Main quiz fragment (no scroll-to-top on interaction) ---
def quiz_area():
    pool = st.session_state["quiz_pool"]
    idx = st.session_state["quiz_index"]
    total = st.session_state["quiz_total"]
    correct = st.session_state["quiz_correct"]
    wrong = st.session_state["quiz_wrong"]
    streak = st.session_state["quiz_streak"]
    best_streak = st.session_state["quiz_best_streak"]
    mode = st.session_state.get("quiz_mode_radio", "🃏 Flashcards")
    gen_filter = st.session_state.get("quiz_gen_filter", "All")
    quiz_length = st.session_state.get("quiz_length_slider", 15)

    # --- Score bar ---
    st.markdown(
        f'<div class="quiz-score">'
        f'<div class="quiz-score-item"><div class="quiz-score-num">{idx}/{total}</div>'
        f'<div class="quiz-score-label">Progress</div></div>'
        f'<div class="quiz-score-item"><div class="quiz-score-num correct">{correct}</div>'
        f'<div class="quiz-score-label">Correct</div></div>'
        f'<div class="quiz-score-item"><div class="quiz-score-num wrong">{wrong}</div>'
        f'<div class="quiz-score-label">Wrong</div></div>'
        f'<div class="quiz-score-item"><div class="quiz-score-num streak">🔥 {streak}</div>'
        f'<div class="quiz-score-label">Streak</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # --- Progress bar ---
    progress_pct = (idx / total * 100) if total > 0 else 0
    st.markdown(
        f'<div class="quiz-progress"><div class="quiz-progress-fill" style="width:{progress_pct}%"></div></div>',
        unsafe_allow_html=True,
    )

    # ===================== QUIZ COMPLETE =====================
    if idx >= total or idx >= len(pool):
        st.markdown("---")
        st.markdown("### 🎉 Quiz Complete!")

        accuracy = (correct / total * 100) if total > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Score", f"{correct}/{total}")
        col2.metric("Accuracy", f"{accuracy:.0f}%")
        col3.metric("Best Streak", f"🔥 {best_streak}")

        if accuracy >= 90:
            st.success("You're absolutely slaying it! 💅🔥")
        elif accuracy >= 70:
            st.info("Solid work — you're getting the hang of it! ✨")
        elif accuracy >= 50:
            st.warning("Not bad, but keep practicing! 💪")
        else:
            st.error("Time to hit the Encyclopedia and study up! 📚")

        # === MASTERY DASHBOARD (Metacognition) ===
        results = st.session_state.get("quiz_term_results", {})
        if results:
            mastered = []  # Got right on first try, no hints
            learning = []  # Got right but needed hints or retries
            missed = []    # Never got right

            for term, data in results.items():
                if data["correct"] > 0 and data["wrong"] == 0 and data["hints"] == 0:
                    mastered.append(term)
                elif data["correct"] > 0:
                    learning.append(term)
                else:
                    missed.append(term)

            st.markdown("---")
            st.markdown("### 🧠 Learning Summary")
            st.caption(
                "Based on the **testing effect** and **metacognition** research, "
                "reviewing what you know vs. don't know improves long-term retention."
            )

            if mastered:
                terms_html = "".join(f'<span class="mastery-term mastered">{t}</span>' for t in mastered)
                st.markdown(
                    f'<div class="mastery-card">'
                    f'<div class="mastery-card-header mastered">✅ Mastered — {len(mastered)} terms</div>'
                    f'{terms_html}</div>',
                    unsafe_allow_html=True,
                )

            if learning:
                terms_html = "".join(f'<span class="mastery-term learning">{t}</span>' for t in learning)
                st.markdown(
                    f'<div class="mastery-card">'
                    f'<div class="mastery-card-header learning">🔄 Learning — {len(learning)} terms</div>'
                    f'{terms_html}'
                    f'<div style="font-size:12px;color:#6c7590;margin-top:8px">'
                    f'You got these right but needed hints or retries. Keep practicing!</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            if missed:
                terms_html = "".join(f'<span class="mastery-term missed">{t}</span>' for t in missed)
                st.markdown(
                    f'<div class="mastery-card">'
                    f'<div class="mastery-card-header missed">❌ Needs Review — {len(missed)} terms</div>'
                    f'{terms_html}'
                    f'<div style="font-size:12px;color:#6c7590;margin-top:8px">'
                    f'Check these in the Encyclopedia and try again!</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # Learning tip
            st.markdown(
                '<div class="quiz-learn-tip">'
                '<div class="quiz-learn-tip-label">💡 Learning Tip</div>'
                '<div class="quiz-learn-tip-text">'
                'Research shows you retain <b>80% more</b> through active recall (quizzing yourself) '
                'vs. passive review (re-reading). Come back tomorrow and re-test the '
                '"Learning" and "Needs Review" terms — <b>spaced repetition</b> is the #1 '
                'evidence-backed technique for long-term memory.'
                '</div></div>',
                unsafe_allow_html=True,
            )

        if st.button("🔄 Play Again", use_container_width=True):
            filtered = all_slangs.copy()
            if gen_filter != "All":
                filtered = [s for s in filtered if s[2] == gen_filter]
            init_quiz_state(filtered, quiz_length)
            st.rerun()

        return

    # ===================== ACTIVE QUIZ =====================
    current_slang, current_meaning, current_gen = pool[idx]
    badge_class = "badge-genz" if current_gen == "Gen Z" else "badge-genalpha"

    # Check if this is a spaced-rep retry
    term_data = st.session_state.get("quiz_term_results", {}).get(current_slang, {})
    is_retry = term_data.get("wrong", 0) > 0

    # --- Shared post-answer feedback ---
    def show_post_answer_feedback(was_correct, slang, meaning, gen):
        """Show elaborative feedback after answering (Elaborative Interrogation)."""
        if was_correct:
            st.success("Nice one! 🔥")
        else:
            st.error(f"The correct answer: **{meaning}**")

        # Usage tip for deeper encoding
        tip = generate_usage_tip(slang, meaning, gen)
        st.markdown(
            f'<div class="quiz-learn-tip">'
            f'<div class="quiz-learn-tip-label">💬 How to use it</div>'
            f'<div class="quiz-learn-tip-text">{tip}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # --- Hint button helper ---
    def show_hint_button(slang, meaning, gen):
        """Progressive hint system (Desirable Difficulty)."""
        hints = generate_hint(slang, meaning, gen)
        hint_level = st.session_state.get("quiz_hint_level", 0)

        if hint_level < len(hints):
            if st.button("💡 Need a hint?", use_container_width=True):
                st.session_state["quiz_hint_level"] = hint_level + 1
                st.session_state["quiz_hint_used"] = True
                st.rerun()

        # Show all revealed hints
        for i in range(min(hint_level, len(hints))):
            st.markdown(
                f'<div class="quiz-hint-box">{hints[i]}</div>',
                unsafe_allow_html=True,
            )

    # --- Next card helper ---
    def advance_to_next(was_correct):
        """Handle scoring, spaced repetition, and advance."""
        hint_used = st.session_state.get("quiz_hint_used", False)
        record_result(current_slang, was_correct, hint_used)

        if was_correct:
            st.session_state["quiz_correct"] += 1
            st.session_state["quiz_streak"] += 1
            st.session_state["quiz_best_streak"] = max(
                st.session_state["quiz_best_streak"],
                st.session_state["quiz_streak"],
            )
        else:
            st.session_state["quiz_wrong"] += 1
            st.session_state["quiz_streak"] = 0
            # SPACED REPETITION: re-queue wrong answer
            requeue_wrong_answer(current_slang, current_meaning, current_gen)

        st.session_state["quiz_index"] += 1
        st.session_state["quiz_hint_level"] = 0
        st.session_state["quiz_hint_used"] = False

    # =================== FLASHCARD MODE ===================
    if mode == "🃏 Flashcards":
        flipped = st.session_state.get("quiz_flipped", False)

        retry_html = '<div class="quiz-retry-badge">🔄 Review Card</div>' if is_retry else ""

        if not flipped:
            st.markdown(
                f'<div class="quiz-flashcard">'
                f'{retry_html}'
                f'<div class="quiz-flashcard-label">What does this mean?</div>'
                f'<div class="quiz-flashcard-term">{current_slang}</div>'
                f'<span class="slang-badge {badge_class}">{current_gen}</span>'
                f'<div class="quiz-flashcard-hint">Click "Reveal" to see the answer</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown("")
            show_hint_button(current_slang, current_meaning, current_gen)
            if st.button("👀 Reveal Answer", use_container_width=True):
                st.session_state["quiz_flipped"] = True
                st.rerun()
        else:
            st.markdown(
                f'<div class="quiz-flashcard">'
                f'{retry_html}'
                f'<div class="quiz-flashcard-label">Answer</div>'
                f'<div class="quiz-flashcard-term">{current_slang}</div>'
                f'<div class="quiz-flashcard-meaning">{current_meaning}</div>'
                f'<span class="slang-badge {badge_class}" style="margin-top:12px">{current_gen}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Usage tip (Elaborative Feedback)
            tip = generate_usage_tip(current_slang, current_meaning, current_gen)
            st.markdown(
                f'<div class="quiz-learn-tip">'
                f'<div class="quiz-learn-tip-label">💬 How to use it</div>'
                f'<div class="quiz-learn-tip-text">{tip}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown("")
            col_knew, col_didnt = st.columns(2)
            with col_knew:
                if st.button("✅ I knew it!", use_container_width=True):
                    advance_to_next(True)
                    st.session_state["quiz_flipped"] = False
                    st.rerun()
            with col_didnt:
                if st.button("❌ Didn't know", use_container_width=True):
                    advance_to_next(False)
                    st.session_state["quiz_flipped"] = False
                    st.rerun()

    # =================== MULTIPLE CHOICE MODE ===================
    elif mode == "📝 Multiple Choice":
        if "quiz_mcq_options" not in st.session_state or st.session_state.get("quiz_mcq_idx") != idx:
            wrong_options = [s for s in all_slangs if s[0] != current_slang]
            distractors = random.sample(wrong_options, min(3, len(wrong_options)))
            options = [(current_meaning, True)] + [(d[1], False) for d in distractors]
            random.shuffle(options)
            st.session_state["quiz_mcq_options"] = options
            st.session_state["quiz_mcq_idx"] = idx
            st.session_state["quiz_answered"] = False
            st.session_state["quiz_answer_correct"] = None
            st.session_state["quiz_selected"] = None

        retry_html = '<div class="quiz-retry-badge">🔄 Review Card</div>' if is_retry else ""
        st.markdown(
            f'<div class="quiz-flashcard">'
            f'{retry_html}'
            f'<div class="quiz-flashcard-label">What does this mean?</div>'
            f'<div class="quiz-flashcard-term">{current_slang}</div>'
            f'<span class="slang-badge {badge_class}">{current_gen}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("")
        options = st.session_state["quiz_mcq_options"]
        answered = st.session_state["quiz_answered"]

        if not answered:
            show_hint_button(current_slang, current_meaning, current_gen)

        for i, (option_text, is_correct) in enumerate(options):
            if not answered:
                if st.button(option_text, key=f"mcq_{idx}_{i}", use_container_width=True):
                    st.session_state["quiz_answered"] = True
                    st.session_state["quiz_selected"] = i
                    was_correct = is_correct
                    st.session_state["quiz_answer_correct"] = was_correct
                    advance_to_next(was_correct)
                    # Don't increment index yet — show feedback first
                    st.session_state["quiz_index"] -= 1
                    st.rerun()
            else:
                selected = st.session_state["quiz_selected"]
                if i == selected and is_correct:
                    st.markdown(f'<div class="quiz-correct">✅ {option_text}</div>', unsafe_allow_html=True)
                elif i == selected and not is_correct:
                    st.markdown(f'<div class="quiz-wrong">❌ {option_text}</div>', unsafe_allow_html=True)
                elif is_correct:
                    st.markdown(f'<div class="quiz-correct">✅ {option_text}</div>', unsafe_allow_html=True)
                else:
                    st.button(option_text, key=f"mcq_{idx}_{i}", use_container_width=True, disabled=True)

        if answered:
            show_post_answer_feedback(
                st.session_state["quiz_answer_correct"],
                current_slang, current_meaning, current_gen,
            )
            if st.button("Next →", use_container_width=True):
                st.session_state["quiz_index"] += 1
                st.session_state["quiz_answered"] = False
                st.session_state["quiz_answer_correct"] = None
                st.session_state["quiz_selected"] = None
                st.rerun()

    # =================== TYPE THE ANSWER MODE ===================
    elif mode == "✍️ Type the Answer":
        retry_html = '<div class="quiz-retry-badge">🔄 Review Card</div>' if is_retry else ""
        st.markdown(
            f'<div class="quiz-flashcard">'
            f'{retry_html}'
            f'<div class="quiz-flashcard-label">What does this slang term mean?</div>'
            f'<div class="quiz-flashcard-term">{current_slang}</div>'
            f'<span class="slang-badge {badge_class}">{current_gen}</span>'
            f'<div class="quiz-flashcard-hint">Type a short description of the meaning</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("")
        answered = st.session_state.get("quiz_answered", False)

        if not answered:
            show_hint_button(current_slang, current_meaning, current_gen)
            user_answer = st.text_input(
                "Your answer:",
                key=f"type_answer_{idx}",
                placeholder="Type what you think it means...",
                label_visibility="collapsed",
            )

            if st.button("Submit Answer", use_container_width=True, disabled=not user_answer):
                meaning_words = set(current_meaning.lower().replace(",", "").replace(".", "").split())
                answer_words = set(user_answer.lower().replace(",", "").replace(".", "").split())
                fillers = {"a", "an", "the", "is", "or", "to", "of", "and", "for", "in", "it", "be", "as", "at", "on"}
                meaning_key = meaning_words - fillers
                answer_key = answer_words - fillers

                overlap = meaning_key & answer_key
                match_ratio = len(overlap) / max(len(meaning_key), 1)
                was_correct = match_ratio >= 0.35

                st.session_state["quiz_answered"] = True
                st.session_state["quiz_answer_correct"] = was_correct
                st.session_state["quiz_user_answer"] = user_answer
                advance_to_next(was_correct)
                st.session_state["quiz_index"] -= 1  # Show feedback first
                st.rerun()
        else:
            user_answer = st.session_state.get("quiz_user_answer", "")
            st.markdown(f"**Your answer:** {user_answer}")

            show_post_answer_feedback(
                st.session_state["quiz_answer_correct"],
                current_slang, current_meaning, current_gen,
            )

            if st.button("Next →", use_container_width=True):
                st.session_state["quiz_index"] += 1
                st.session_state["quiz_answered"] = False
                st.session_state["quiz_answer_correct"] = None
                st.rerun()


# Run the fragment
quiz_area()

# --- Footer ---
render_footer()
