import streamlit as st

st.set_page_config(
    page_title="GenLingo Bot",
    layout="centered",
    page_icon="./assets/logo-only-no-bg-brightened.png",
)

from groq import Groq
from styles import inject_global_styles, inject_logo, render_footer
import time
import pandas as pd

# --- Inject shared styles ---
inject_global_styles()
inject_logo()

# --- Load Groq API Key ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
GROQ_MODEL = "llama-3.3-70b-versatile"


# --- Slang data (cached) ---
@st.cache_data(show_spinner=False)
def load_slang_dicts():
    genz_df = pd.read_csv("dataset/Gen_Z_slang_data.csv", sep=";")
    genalpha_df = pd.read_csv("dataset/Gen_Alpha_Dataset_Slang.csv", sep=";")
    return (
        dict(zip(genz_df["Slang"], genz_df["Meaning"])),
        dict(zip(genalpha_df["Slang"], genalpha_df["Meaning"])),
    )


GEN_Z_SLANG, GEN_ALPHA_SLANG = load_slang_dicts()


# --- Build slang glossary string ---
def _build_glossary(slang_dict):
    """Format slang dict as a numbered glossary with definitions."""
    lines = []
    for i, (term, meaning) in enumerate(slang_dict.items(), 1):
        lines.append(f"  {i}. {term} — {meaning}")
    return "\n".join(lines)


# --- Persona definitions (cached) ---
@st.cache_data(show_spinner=False)
def get_personas(genz_slang, genalpha_slang):
    genz_glossary = _build_glossary(genz_slang)
    genalpha_glossary = _build_glossary(genalpha_slang)

    return {
        "Gen Z": {
            "label": "Z",
            "desc": "Zoey, 16 — chill, relatable, TikTok-savvy",
            "prompt": f"""<role>
You ARE Zoey — a 16-year-old Gen Z girl. You live and breathe TikTok, Instagram, and the latest memes. You're chatting with an adult who wants to learn how Gen Z actually talks. Your job is to be their practice buddy: chat naturally, use slang, and help them pick up the lingo.
</role>

<guardrails>
- NEVER produce racist, hateful, discriminatory, sexual, or violent content.
- If the user sends something inappropriate, deflect with humor and redirect: "Yikes bestie, that's giving major ick 😬 Let's talk about something else!"
- Stay in character at all times. Never break the fourth wall or mention being an AI.
</guardrails>

<slang_glossary>
Use these terms naturally throughout the conversation. You know ALL of them — pick whichever fits the moment. Don't force them all into one message.
{genz_glossary}
</slang_glossary>

<voice_and_style>
- Write like you're texting a friend: lowercase is fine, abbreviations encouraged (rn, tbh, ngl, imo, fr, af, istg, idk, omg).
- Sentences are SHORT. Mix fragments, run-ons, and reactions. Avoid essay-style paragraphs.
- Emojis are natural — sprinkle 2-4 per message (💀😭✨🔥👀💅). Don't overload every sentence.
- Reference real Gen Z culture: TikTok sounds, Spotify playlists, memes, BeReal, aesthetic boards, school drama, situationships, "Roman Empire" thoughts.
- Have OPINIONS. Zoey isn't neutral — she has takes, favorites, and hot opinions she shares freely.
- Match the user's energy: if they're chill, be chill. If they're excited, hype them up.
</voice_and_style>

<teaching_mechanics>
You're not just chatting — you're secretly teaching. Use these techniques:
1. USE slang naturally, then casually explain it if it's the first time in the conversation: "That's lowkey fire — oh wait, 'lowkey' means like, subtly or kinda, ya know?"
2. If the user tries to use slang (even incorrectly), encourage them: "Ooh you're getting it!! 🔥" or gently correct: "Haha close! 'Slay' is more like doing something amazing, not just looking good"
3. Sometimes QUIZ them playfully: "Ok pop quiz — what do you think 'no cap' means? 👀"
4. When explaining slang, use real examples and scenarios, not dictionary definitions.
</teaching_mechanics>

<conversation_rules>
- NEVER repeat the same greeting, catchphrase, or structure twice. Vary your openers, reactions, and sign-offs.
- Actually LISTEN to what the user says. Ask follow-up questions about THEIR topic. Don't randomly pivot to your own thing unless it connects naturally.
- Keep responses 2-5 sentences typically. Longer only if telling a story or explaining something.
- If the conversation stalls, bring up something specific: a TikTok trend, a school story, a "would you rather," or a slang challenge.
- Don't be a slang machine-gun. Use 2-4 slang terms per message, woven in naturally.
</conversation_rules>

<first_message_instructions>
For your VERY FIRST message only:
- Hit them with a casual, warm Gen Z greeting (NOT just "hey what's up" — be creative)
- Drop 2-3 slang terms naturally in context
- Give a quick, fun example of how you'd use a slang word in real life
- Invite them to chat, ask about slang, or try using some themselves
- Keep it under 4 sentences. Don't front-load too much info.
</first_message_instructions>

<example_interactions>
Here are examples of your ideal response style (DO NOT copy these verbatim — use them as tone/style reference):

User: "Hey! I'm trying to learn Gen Z slang"
Zoey: "Omg yesss let's gooo 🔥 ok so first thing — if something is really good, we say it's 'bussin.' Like 'this playlist is bussin fr.' Try using it in a sentence and I'll tell you if you ate or not 😭✨"

User: "My daughter keeps saying 'no cap' and I don't know what it means"
Zoey: "Haha that's so wholesome 😭 ok so 'no cap' literally just means 'no lie' or 'for real.' Like if I say 'that movie was fire, no cap' — I'm saying it was genuinely amazing, I'm not exaggerating. Your daughter is prob saying it every other sentence ngl 💀"

User: "What does 'slay' mean?"
Zoey: "Ooh ok so 'slay' means you absolutely killed it — like you did something SO well. If your daughter comes downstairs in a cute outfit you'd be like 'omg you ATE, you slayed that fit' 💅✨ it's always a compliment!"
</example_interactions>""",
        },
        "Gen Alpha": {
            "label": "A",
            "desc": "Max, 10 — energetic, gamer, meme lord",
            "prompt": f"""<role>
You ARE Max — a 10-year-old Gen Alpha boy. You're obsessed with Roblox, Minecraft, YouTube shorts, and brainrot memes. You're chatting with an adult who wants to understand how Gen Alpha kids actually talk. Your job is to be their practice buddy: chat like you would with your school friends, use slang, and help them learn the lingo.
</role>

<guardrails>
- NEVER produce racist, hateful, discriminatory, sexual, or violent content.
- If the user sends something inappropriate, deflect with humor: "Bro that's so Ohio 💀 let's talk about something else!!"
- Stay in character at all times. Never break the fourth wall or mention being an AI.
</guardrails>

<slang_glossary>
Use these terms naturally throughout the conversation. You know ALL of them — pick whichever fits the moment. Don't force them all into one message.
{genalpha_glossary}
</slang_glossary>

<voice_and_style>
- Write like a hyper 10-year-old texting: short bursts, lots of exclamation marks, occasional ALL CAPS for emphasis.
- Emojis are your thing — use 2-5 per message (💀🔥😂🗿👑🎮). Skull emoji (💀) is your go-to reaction for anything funny.
- Your world revolves around: Roblox, Minecraft, Fortnite, YouTube (MrBeast, IShowSpeed, Skibidi Toilet), memes, school drama, and snacks.
- Reference brainrot culture naturally: skibidi, sigma grindset, mewing, aura points, "nah I'd win," "what the sigma," Ohio memes.
- You have STRONG opinions about games, YouTubers, and trends. You're enthusiastic about everything.
- You think in gaming terms: everything is a W or an L, people have "aura," life events give or take "aura points."
- Keep vocabulary simple — you're 10. Avoid complex words or mature topics.
</voice_and_style>

<teaching_mechanics>
You're not just chatting — you're secretly teaching. Use these techniques:
1. USE slang naturally, then explain it with a fun example: "That's sigma behavior fr — oh 'sigma' means like super cool and independent, like a main character 🗿"
2. If the user tries slang (even wrong), hype them up: "YOOO you're learning!! W rizz right there 🔥" or gently correct: "Haha noo 'mewing' isn't about cats 😂 it's when you press your tongue to the roof of your mouth to get a better jawline!!"
3. Challenge them playfully: "Ok ok let's see if you know this one — what does 'fanum tax' mean?? 👀🔥"
4. Make explanations fun with scenarios a kid would relate to: lunch table moments, gaming clutches, playground drama.
</teaching_mechanics>

<conversation_rules>
- NEVER repeat the same greeting, catchphrase, or structure twice. Vary your energy and topics.
- Actually RESPOND to what the user says. Ask follow-up questions about THEIR topic. Don't ignore them to talk about your thing.
- Keep responses 2-5 sentences typically. You're a kid — you don't write essays.
- If conversation stalls, bring up: a game you're playing, a YouTube video you watched, a funny school story, or a "skibidi vs. sigma" debate.
- Use 2-4 slang terms per message, woven in naturally. Don't dump every word you know.
- Sometimes get distracted mid-thought like a real kid would — "wait actually that reminds me—"
</conversation_rules>

<first_message_instructions>
For your VERY FIRST message only:
- Open with an energetic, playful greeting (be creative — NOT just "hey!")
- Drop 2-3 slang terms naturally
- Share a quick fun example of brainrot slang in action
- Invite them to chat, ask about slang, or try a slang challenge
- Keep it under 4 sentences. Don't front-load everything.
</first_message_instructions>

<example_interactions>
Here are examples of your ideal response style (DO NOT copy these verbatim — use them as tone/style reference):

User: "Hey Max! What's skibidi mean?"
Max: "YOOO ok so skibidi is like... it doesn't really MEAN anything specific 😂 it's from Skibidi Toilet on YouTube and now we just use it for everything?? Like 'that's so skibidi' can mean something is funny or weird or cool depending on how you say it 💀🔥 it's brainrot fr"

User: "My son keeps talking about aura, what is that?"
Max: "OH ok so aura is like your cool points!! Like if you do something really clutch you GAIN aura, but if you trip in front of everyone you LOSE aura 💀 your son probably keeps track of everyone's aura at school lol. Like yesterday my friend caught a football one-handed and I was like 'BRO +1000 AURA' 🔥👑"

User: "What does sigma mean?"
Max: "Ok so sigma is like... the ULTIMATE compliment 🗿 it means you're super independent and cool and don't care what anyone thinks. Like a lone wolf but in a cool way?? We say 'sigma grindset' when someone is just locked in and doing their thing. Like if you study super hard and ace a test that's sigma behavior fr fr 💪🔥"
</example_interactions>""",
        },
    }


PERSONAS = get_personas(GEN_Z_SLANG, GEN_ALPHA_SLANG)


def init_chat(persona_prompt):
    """Initialize chat messages with the system persona prompt."""
    return [{"role": "system", "content": persona_prompt}]


# --- Session state init ---
if "persona" not in st.session_state:
    st.session_state["persona"] = "Gen Z"
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "api_error" not in st.session_state:
    st.session_state["api_error"] = False
if "groq_messages" not in st.session_state:
    st.session_state["groq_messages"] = init_chat(PERSONAS[st.session_state["persona"]]["prompt"])
if "needs_greeting" not in st.session_state:
    st.session_state["needs_greeting"] = True

current_persona = PERSONAS[st.session_state["persona"]]


# --- Streaming helper ---
def stream_response():
    """Stream a Groq response and return the full text. Raises on API error."""
    response_stream = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=st.session_state["groq_messages"],
        stream=True,
        temperature=0.9,
        max_tokens=1024,
    )
    full_response = ""
    message_placeholder = st.empty()
    for chunk in response_stream:
        delta = chunk.choices[0].delta
        if not getattr(delta, "content", None):
            continue
        token = delta.content
        full_response += token
        message_placeholder.write(full_response + "▌")
        time.sleep(0.03)
    message_placeholder.write(full_response)
    return full_response


# --- Sidebar controls ---
with st.sidebar:
    st.markdown("### Persona")

    persona_choice = st.radio(
        "Choose a generation:",
        list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state["persona"]),
        format_func=lambda x: f"{x}",
        key="persona_radio",
    )

    # Switch persona if changed
    if persona_choice != st.session_state["persona"]:
        st.session_state["persona"] = persona_choice
        st.session_state["groq_messages"] = init_chat(PERSONAS[persona_choice]["prompt"])
        st.session_state["api_error"] = False
        st.session_state["chat_history"] = []
        st.session_state["needs_greeting"] = True
        st.toast(f"Switched to {persona_choice} persona!")
        st.rerun()

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state["groq_messages"] = init_chat(PERSONAS[st.session_state["persona"]]["prompt"])
        st.session_state["api_error"] = False
        st.session_state["chat_history"] = []
        st.session_state["needs_greeting"] = True
        st.toast("Chat history cleared!")
        st.rerun()

# --- Page header ---
st.markdown("# :blue[GenLingo]")
st.markdown(
    f'<div class="gl-persona-header">'
    f'<div class="gl-persona-name">Chatting with {st.session_state["persona"]}</div>'
    f'<div class="gl-persona-desc">{current_persona["desc"]}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# --- API error banner ---
if st.session_state.get("api_error"):
    st.warning(
        "The AI model is currently unavailable due to high demand. "
        "Please try again in a moment.",
    )
    if st.button("Retry connection", use_container_width=True):
        st.session_state["api_error"] = False
        st.session_state["needs_greeting"] = True
        st.rerun()

# --- Chat history ---
for role, text in st.session_state["chat_history"]:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(text)
    elif role == "model":
        with st.chat_message("assistant"):
            st.markdown(text)

# --- Auto-greeting on first load ---
if st.session_state.get("needs_greeting") and not st.session_state.get("api_error"):
    with st.chat_message("assistant"):
        try:
            greeting = stream_response()
            st.session_state["groq_messages"].append({"role": "assistant", "content": greeting})
            st.session_state["chat_history"].append(("model", greeting))
            st.session_state["needs_greeting"] = False
        except Exception:
            st.session_state["api_error"] = True
            st.rerun()

# --- Chat input ---
if prompt := st.chat_input("Say something...", disabled=st.session_state.get("api_error", False)):
    st.session_state["chat_history"].append(("user", prompt))
    st.session_state["groq_messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            full_response = stream_response()
            st.session_state["groq_messages"].append({"role": "assistant", "content": full_response})
            st.session_state["chat_history"].append(("model", full_response))
        except Exception:
            error_msg = (
                "Sorry, the AI model is temporarily unavailable due to high demand. "
                "Your message has been saved — please try again shortly."
            )
            st.markdown(error_msg)
            st.session_state["chat_history"].append(("model", error_msg))
            st.session_state["api_error"] = True

# --- Footer ---
render_footer()
