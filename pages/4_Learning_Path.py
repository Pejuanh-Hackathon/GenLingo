"""
Learning Path — GenLingo
========================
A Duolingo-style structured learning journey with themed units,
progressive unlocking, XP system, and mini-quizzes per unit.
"""

import streamlit as st

st.set_page_config(
    page_title="Learning Path — GenLingo",
    layout="centered",
    page_icon="./assets/logo-only-no-bg-brightened.png",
)

from styles import inject_global_styles, inject_logo, render_footer
import pandas as pd
import random
import json

# --- Inject shared styles ---
inject_global_styles()
inject_logo()

# --- Learning Path CSS ---
st.markdown("""<style>
    /* XP bar at top */
    .lp-xp-bar {
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.7) 0%, rgba(30, 50, 90, 0.5) 100%);
        border: 1px solid rgba(50, 98, 240, 0.1);
        border-radius: 14px;
        padding: 16px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 28px;
    }

    .lp-xp-item { text-align: center; }

    .lp-xp-num {
        font-size: 22px;
        font-weight: 700;
        color: #e8eaf0;
    }

    .lp-xp-num.xp { color: #facc15; }
    .lp-xp-num.level { color: #a78bfa; }
    .lp-xp-num.units { color: #4ade80; }

    .lp-xp-label {
        font-size: 11px;
        color: #6c7590;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }

    /* Overall progress bar */
    .lp-progress-outer {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        height: 8px;
        margin-bottom: 32px;
        overflow: hidden;
    }

    .lp-progress-inner {
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #3262f0, #a78bfa, #4ade80);
        background-size: 200% 100%;
        animation: progressShimmer 4s ease-in-out infinite;
        transition: width 0.5s cubic-bezier(0.22, 1, 0.36, 1);
    }

    @keyframes progressShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Unit card */
    .lp-unit {
        position: relative;
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.85) 0%, rgba(30, 58, 110, 0.65) 100%);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        border: 1px solid rgba(50, 98, 240, 0.1);
        backdrop-filter: blur(8px);
        transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1);
        animation: cardSlideIn 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    }

    @keyframes cardSlideIn {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .lp-unit:hover {
        border-color: rgba(50, 98, 240, 0.35);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(50, 98, 240, 0.1);
    }

    .lp-unit.locked {
        opacity: 0.45;
        pointer-events: none;
    }

    .lp-unit.completed {
        border-color: rgba(34, 197, 94, 0.3);
    }

    .lp-unit.completed::after {
        content: '✅';
        position: absolute;
        top: 16px;
        right: 20px;
        font-size: 20px;
    }

    .lp-unit.active {
        border-color: rgba(50, 98, 240, 0.4);
        box-shadow: 0 0 20px rgba(50, 98, 240, 0.08);
    }

    .lp-unit-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 10px;
    }

    .lp-unit-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
    }

    .lp-unit-icon.available {
        background: linear-gradient(135deg, rgba(50, 98, 240, 0.15), rgba(91, 138, 245, 0.1));
        border: 1px solid rgba(50, 98, 240, 0.15);
    }

    .lp-unit-icon.completed {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.08));
        border: 1px solid rgba(34, 197, 94, 0.2);
    }

    .lp-unit-icon.locked {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .lp-unit-title {
        font-size: 17px;
        font-weight: 700;
        color: #e8eaf0;
        letter-spacing: -0.01em;
    }

    .lp-unit-subtitle {
        font-size: 13px;
        color: #8b93a7;
        margin-top: 2px;
    }

    .lp-unit-desc {
        font-size: 14px;
        color: #9ca3b4;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .lp-unit-terms {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 14px;
    }

    .lp-unit-term {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        background: rgba(50, 98, 240, 0.08);
        color: #7ba4f7;
        border: 1px solid rgba(50, 98, 240, 0.1);
    }

    .lp-unit-term.mastered {
        background: rgba(34, 197, 94, 0.08);
        color: #4ade80;
        border-color: rgba(34, 197, 94, 0.15);
    }

    /* Unit progress bar */
    .lp-unit-progress {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 6px;
        height: 5px;
        overflow: hidden;
        margin-bottom: 6px;
    }

    .lp-unit-progress-fill {
        height: 100%;
        border-radius: 6px;
        background: linear-gradient(90deg, #3262f0, #a78bfa);
        transition: width 0.4s ease;
    }

    .lp-unit-progress-fill.complete {
        background: linear-gradient(90deg, #22c55e, #4ade80);
    }

    .lp-unit-progress-text {
        font-size: 11px;
        color: #525a6b;
    }

    /* Connector line between units */
    .lp-connector {
        width: 3px;
        height: 20px;
        margin: 0 auto;
        border-radius: 3px;
    }

    .lp-connector.done {
        background: linear-gradient(180deg, rgba(34, 197, 94, 0.3), rgba(50, 98, 240, 0.2));
    }

    .lp-connector.next {
        background: linear-gradient(180deg, rgba(50, 98, 240, 0.2), rgba(255, 255, 255, 0.05));
    }

    .lp-connector.locked {
        background: rgba(255, 255, 255, 0.04);
    }

    /* Lock badge */
    .lp-lock-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.04);
        color: #525a6b;
    }

    /* Lesson quiz flashcard (reuse from quiz page) */
    .lp-quiz-card {
        background: linear-gradient(145deg, rgba(26, 39, 68, 0.9) 0%, rgba(30, 58, 110, 0.7) 100%);
        border: 1px solid rgba(50, 98, 240, 0.12);
        border-radius: 18px;
        padding: 40px 28px;
        text-align: center;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        animation: cardSlideIn 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    }

    .lp-quiz-card::before {
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

    .lp-quiz-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6c7590;
        margin-bottom: 14px;
    }

    .lp-quiz-term {
        font-size: 30px;
        font-weight: 800;
        color: #e8eaf0;
        margin-bottom: 6px;
    }

    .lp-quiz-meaning {
        font-size: 17px;
        color: #9bb0e8;
        line-height: 1.5;
        max-width: 420px;
    }

    /* XP gain animation */
    .lp-xp-gain {
        background: rgba(250, 204, 21, 0.08);
        border: 1px solid rgba(250, 204, 21, 0.2);
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 14px;
        font-weight: 600;
        color: #facc15;
        text-align: center;
        margin: 8px 0;
        animation: cardSlideIn 0.3s ease;
    }

    /* Result boxes */
    .lp-correct {
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 12px;
        padding: 14px 18px;
        color: #4ade80;
        font-size: 15px;
        font-weight: 600;
        margin: 8px 0;
        animation: cardSlideIn 0.3s ease;
    }

    .lp-wrong {
        background: rgba(248, 113, 113, 0.08);
        border: 1px solid rgba(248, 113, 113, 0.3);
        border-radius: 12px;
        padding: 14px 18px;
        color: #f87171;
        font-size: 15px;
        font-weight: 600;
        margin: 8px 0;
        animation: cardSlideIn 0.3s ease;
    }
</style>""", unsafe_allow_html=True)


# =====================================================================
#  UNIT DEFINITIONS — Themed learning units
# =====================================================================
UNITS = [
    {
        "id": "basics",
        "icon": "🔤",
        "title": "The Basics",
        "desc": "Essential slang everyone should know — the building blocks.",
        "terms": ["Bet", "Fam", "Lit", "Fire", "Dope", "W", "Vibe", "Chill"],
        "xp": 50,
    },
    {
        "id": "reactions",
        "icon": "😱",
        "title": "Reactions & Emotions",
        "desc": "How to react when something shocks, amuses, or annoys you.",
        "terms": ["Dead", "Shook", "Salty", "Cringe", "Yikes", "Big mood", "Ick", "Mood"],
        "xp": 60,
    },
    {
        "id": "compliments",
        "icon": "💅",
        "title": "Compliments & Hype",
        "desc": "Learn how to gas someone up — the art of slang praise.",
        "terms": ["Slay", "Bussin", "Ate", "Snatched", "GOAT", "Fire", "Drip", "Glow up"],
        "xp": 60,
    },
    {
        "id": "social_media",
        "icon": "📱",
        "title": "Social Media & Internet",
        "desc": "Navigate the online world — DMs, clout, and going viral.",
        "terms": ["Ghost", "Stan", "Cap", "No cap", "Trolling", "Ratioed", "Clout", "Slide into DMs"],
        "xp": 70,
    },
    {
        "id": "relationships",
        "icon": "💕",
        "title": "Relationships & Drama",
        "desc": "The language of love, heartbreak, and everything in between.",
        "terms": ["Bae", "Simp", "Situationship", "Ship", "Red flag", "Beige flag", "Curve", "Ick"],
        "xp": 70,
    },
    {
        "id": "trends",
        "icon": "✨",
        "title": "Trends & Culture",
        "desc": "The slang that defines moments, eras, and main characters.",
        "terms": ["Era", "Canon event", "Main character", "Roman Empire", "It's giving", "Demure", "Understood the assignment", "Periodt"],
        "xp": 80,
    },
    {
        "id": "brainrot",
        "icon": "🧠",
        "title": "Gen Alpha Brainrot",
        "desc": "Skibidi, sigma, and the memes that rule the playground.",
        "terms": ["Skibidi", "Sigma", "Aura", "Rizz", "Mewing", "Ohio", "NPC", "Fanum tax"],
        "xp": 80,
    },
    {
        "id": "advanced",
        "icon": "🎓",
        "title": "Advanced Slang",
        "desc": "Master-level terms that prove you truly understand the culture.",
        "terms": ["Finesse", "Glazing", "Let him cook", "Looksmaxxing", "Mogged", "Delulu", "Crash out", "Cooked"],
        "xp": 100,
    },
]


# --- Load slang data for quiz lookups ---
@st.cache_data(show_spinner=False)
def load_slang_lookup():
    genz_df = pd.read_csv("dataset/Gen_Z_slang_data.csv", sep=";")
    genalpha_df = pd.read_csv("dataset/Gen_Alpha_Dataset_Slang.csv", sep=";")
    genz_dict = dict(zip(genz_df["Slang"], genz_df["Meaning"]))
    genalpha_dict = dict(zip(genalpha_df["Slang"], genalpha_df["Meaning"]))
    combined = {**genz_dict, **genalpha_dict}
    # All meanings for distractors
    all_meanings = list(set(combined.values()))
    return combined, all_meanings


SLANG_LOOKUP, ALL_MEANINGS = load_slang_lookup()


# --- Session state init ---
if "lp_progress" not in st.session_state:
    # Track per-unit: {"basics": {"completed": False, "score": 0, "mastered_terms": []}, ...}
    st.session_state["lp_progress"] = {}
if "lp_xp" not in st.session_state:
    st.session_state["lp_xp"] = 0
if "lp_active_unit" not in st.session_state:
    st.session_state["lp_active_unit"] = None
if "lp_quiz_state" not in st.session_state:
    st.session_state["lp_quiz_state"] = None


def get_unit_status(unit_idx):
    """Determine if a unit is locked, available, or completed."""
    unit = UNITS[unit_idx]
    progress = st.session_state["lp_progress"].get(unit["id"], {})

    if progress.get("completed"):
        return "completed"

    # First unit is always available
    if unit_idx == 0:
        return "available"

    # Available if previous unit is completed
    prev_unit = UNITS[unit_idx - 1]
    prev_progress = st.session_state["lp_progress"].get(prev_unit["id"], {})
    if prev_progress.get("completed"):
        return "available"

    return "locked"


def get_level():
    """Calculate level from total XP (100 XP per level)."""
    return st.session_state["lp_xp"] // 100 + 1


def get_completed_count():
    """Count completed units."""
    return sum(
        1 for u in UNITS
        if st.session_state["lp_progress"].get(u["id"], {}).get("completed")
    )


# --- Page header ---
st.markdown("# :blue[Learning Path]")
st.markdown("*Powered by :blue[GenLingo]*")

# --- XP bar ---
total_xp = st.session_state["lp_xp"]
level = get_level()
completed = get_completed_count()
xp_in_level = total_xp % 100
level_progress = xp_in_level / 100 * 100

st.markdown(
    f'<div class="lp-xp-bar">'
    f'<div class="lp-xp-item"><div class="lp-xp-num level">Lvl {level}</div>'
    f'<div class="lp-xp-label">Level</div></div>'
    f'<div class="lp-xp-item"><div class="lp-xp-num xp">⭐ {total_xp}</div>'
    f'<div class="lp-xp-label">Total XP</div></div>'
    f'<div class="lp-xp-item"><div class="lp-xp-num units">{completed}/{len(UNITS)}</div>'
    f'<div class="lp-xp-label">Units Done</div></div>'
    f'</div>',
    unsafe_allow_html=True,
)

# Overall progress
overall_pct = (completed / len(UNITS) * 100) if UNITS else 0
st.markdown(
    f'<div class="lp-progress-outer">'
    f'<div class="lp-progress-inner" style="width:{overall_pct}%"></div>'
    f'</div>',
    unsafe_allow_html=True,
)


# =====================================================================
#  UNIT LESSON VIEW (when a unit is selected)
# =====================================================================
if st.session_state["lp_active_unit"] is not None:
    unit = UNITS[st.session_state["lp_active_unit"]]
    unit_id = unit["id"]

    # Init quiz state for this unit if needed
    if st.session_state["lp_quiz_state"] is None or st.session_state["lp_quiz_state"].get("unit_id") != unit_id:
        terms_with_meanings = []
        for term in unit["terms"]:
            meaning = SLANG_LOOKUP.get(term, "Unknown meaning")
            terms_with_meanings.append((term, meaning))
        random.shuffle(terms_with_meanings)

        st.session_state["lp_quiz_state"] = {
            "unit_id": unit_id,
            "terms": terms_with_meanings,
            "index": 0,
            "correct": 0,
            "wrong": 0,
            "answered": False,
            "answer_correct": None,
            "selected": None,
            "mcq_options": None,
            "mastered": [],
        }

    qs = st.session_state["lp_quiz_state"]
    terms = qs["terms"]
    q_idx = qs["index"]
    total_q = len(terms)

    # Back button
    if st.button("← Back to Path"):
        st.session_state["lp_active_unit"] = None
        st.session_state["lp_quiz_state"] = None
        st.rerun()

    st.markdown(f"### {unit['icon']} {unit['title']}")
    st.caption(unit["desc"])

    # Progress for this lesson
    lesson_pct = (q_idx / total_q * 100) if total_q > 0 else 0
    st.markdown(
        f'<div class="lp-unit-progress" style="height:6px;margin:8px 0 16px 0">'
        f'<div class="lp-unit-progress-fill" style="width:{lesson_pct}%"></div></div>',
        unsafe_allow_html=True,
    )

    # === LESSON COMPLETE ===
    if q_idx >= total_q:
        accuracy = (qs["correct"] / total_q * 100) if total_q > 0 else 0
        passed = accuracy >= 70  # Need 70% to pass

        st.markdown("---")

        if passed:
            st.markdown("### 🎉 Unit Complete!")
            xp_earned = unit["xp"]

            # Mark as completed
            if not st.session_state["lp_progress"].get(unit_id, {}).get("completed"):
                st.session_state["lp_progress"][unit_id] = {
                    "completed": True,
                    "score": accuracy,
                    "mastered_terms": qs["mastered"],
                }
                st.session_state["lp_xp"] += xp_earned

            st.markdown(
                f'<div class="lp-xp-gain">+{xp_earned} XP earned! ⭐</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown("### Almost there! 💪")
            st.warning(f"You scored **{accuracy:.0f}%** — you need **70%** to pass this unit. Try again!")

        col1, col2 = st.columns(2)
        col1.metric("Score", f"{qs['correct']}/{total_q}")
        col2.metric("Accuracy", f"{accuracy:.0f}%")

        # Show mastered vs missed
        mastered = qs["mastered"]
        missed = [t for t, _ in terms if t not in mastered]

        if mastered:
            st.markdown("**✅ Mastered:** " + ", ".join(mastered))
        if missed:
            st.markdown("**❌ Review these:** " + ", ".join(missed))

        st.markdown("")

        col_retry, col_back = st.columns(2)
        with col_retry:
            if st.button("🔄 Retry Unit", use_container_width=True):
                st.session_state["lp_quiz_state"] = None
                st.rerun()
        with col_back:
            if st.button("← Back to Path", use_container_width=True, key="back_complete"):
                st.session_state["lp_active_unit"] = None
                st.session_state["lp_quiz_state"] = None
                st.rerun()

    # === ACTIVE QUESTION ===
    else:
        current_term, current_meaning = terms[q_idx]

        st.markdown(
            f'<div style="font-size:13px;color:#6c7590;margin-bottom:8px">'
            f'Question {q_idx + 1} of {total_q}</div>',
            unsafe_allow_html=True,
        )

        # Generate MCQ options if needed
        if qs["mcq_options"] is None or qs.get("mcq_for_idx") != q_idx:
            wrong_meanings = [m for m in ALL_MEANINGS if m != current_meaning]
            distractors = random.sample(wrong_meanings, min(3, len(wrong_meanings)))
            options = [(current_meaning, True)] + [(d, False) for d in distractors]
            random.shuffle(options)
            qs["mcq_options"] = options
            qs["mcq_for_idx"] = q_idx
            qs["answered"] = False
            qs["answer_correct"] = None
            qs["selected"] = None

        # Show flashcard
        st.markdown(
            f'<div class="lp-quiz-card">'
            f'<div class="lp-quiz-label">What does this mean?</div>'
            f'<div class="lp-quiz-term">{current_term}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("")

        # MCQ options
        answered = qs["answered"]
        options = qs["mcq_options"]

        for i, (opt_text, is_correct) in enumerate(options):
            if not answered:
                if st.button(opt_text, key=f"lp_mcq_{q_idx}_{i}", use_container_width=True):
                    qs["answered"] = True
                    qs["selected"] = i
                    was_correct = is_correct
                    qs["answer_correct"] = was_correct
                    if was_correct:
                        qs["correct"] += 1
                        qs["mastered"].append(current_term)
                    else:
                        qs["wrong"] += 1
                    st.rerun()
            else:
                selected = qs["selected"]
                if i == selected and is_correct:
                    st.markdown(f'<div class="lp-correct">✅ {opt_text}</div>', unsafe_allow_html=True)
                elif i == selected and not is_correct:
                    st.markdown(f'<div class="lp-wrong">❌ {opt_text}</div>', unsafe_allow_html=True)
                elif is_correct:
                    st.markdown(f'<div class="lp-correct">✅ {opt_text}</div>', unsafe_allow_html=True)
                else:
                    st.button(opt_text, key=f"lp_mcq_{q_idx}_{i}", use_container_width=True, disabled=True)

        if answered:
            if qs["answer_correct"]:
                st.success("Correct! 🔥")
            else:
                st.error(f"The answer: **{current_meaning}**")

            # Usage tip
            st.markdown(
                f'<div style="background:rgba(50,98,240,0.06);border:1px solid rgba(50,98,240,0.15);'
                f'border-radius:12px;padding:12px 16px;margin:8px 0">'
                f'<div style="font-size:11px;font-weight:600;text-transform:uppercase;'
                f'letter-spacing:0.8px;color:#7ba4f7;margin-bottom:4px">💬 Remember it</div>'
                f'<div style="font-size:14px;color:#9ca3b4">'
                f'<b>{current_term}</b> = {current_meaning}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if st.button("Next →", use_container_width=True, key=f"lp_next_{q_idx}"):
                qs["index"] += 1
                qs["answered"] = False
                qs["answer_correct"] = None
                qs["selected"] = None
                qs["mcq_options"] = None
                st.rerun()


# =====================================================================
#  PATH VIEW (unit list)
# =====================================================================
else:
    for i, unit in enumerate(UNITS):
        status = get_unit_status(i)
        progress = st.session_state["lp_progress"].get(unit["id"], {})

        # Connector line between units
        if i > 0:
            connector_class = "done" if status in ("completed", "available") else "locked"
            st.markdown(
                f'<div class="lp-connector {connector_class}"></div>',
                unsafe_allow_html=True,
            )

        # Unit card
        card_class = status
        icon_class = "completed" if status == "completed" else ("available" if status == "available" else "locked")

        # Build terms preview
        mastered_terms = progress.get("mastered_terms", [])
        terms_html = ""
        for term in unit["terms"]:
            term_class = "mastered" if term in mastered_terms else ""
            terms_html += f'<span class="lp-unit-term {term_class}">{term}</span>'

        # Unit progress
        if status == "completed":
            unit_pct = 100
            score = progress.get("score", 100)
            progress_text = f"✅ Completed — {score:.0f}% score"
            fill_class = "complete"
        elif status == "available":
            unit_pct = 0
            progress_text = f"📖 {len(unit['terms'])} terms to learn — {unit['xp']} XP"
            fill_class = ""
        else:
            unit_pct = 0
            progress_text = "🔒 Complete the previous unit to unlock"
            fill_class = ""

        st.markdown(
            f'<div class="lp-unit {card_class}">'
            f'<div class="lp-unit-header">'
            f'<div class="lp-unit-icon {icon_class}">{unit["icon"]}</div>'
            f'<div>'
            f'<div class="lp-unit-title">Unit {i + 1}: {unit["title"]}</div>'
            f'<div class="lp-unit-subtitle">{unit["desc"]}</div>'
            f'</div></div>'
            f'<div class="lp-unit-terms">{terms_html}</div>'
            f'<div class="lp-unit-progress"><div class="lp-unit-progress-fill {fill_class}" style="width:{unit_pct}%"></div></div>'
            f'<div class="lp-unit-progress-text">{progress_text}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Start button for available units
        if status == "available":
            if st.button(
                f"▶️ Start Unit {i + 1}",
                key=f"start_unit_{i}",
                use_container_width=True,
            ):
                st.session_state["lp_active_unit"] = i
                st.session_state["lp_quiz_state"] = None
                st.rerun()
        elif status == "completed":
            if st.button(
                f"🔄 Review Unit {i + 1}",
                key=f"review_unit_{i}",
                use_container_width=True,
            ):
                st.session_state["lp_active_unit"] = i
                st.session_state["lp_quiz_state"] = None
                st.rerun()


# --- Footer ---
render_footer()
