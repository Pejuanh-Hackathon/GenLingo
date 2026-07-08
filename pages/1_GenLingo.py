import streamlit as st

st.set_page_config(
    page_title="GenLingo Bot",
    layout="centered",
    page_icon="./assets/logo-only-no-bg-brightened.png",
)

from google import genai
from google.genai import types
from styles import inject_global_styles, inject_logo, render_footer
import time
import pandas as pd

# --- Inject shared styles ---
inject_global_styles()
inject_logo()

# --- Load Gemini API Key ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


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


# --- Persona definitions (cached) ---
@st.cache_data(show_spinner=False)
def get_personas(genz_slang, genalpha_slang):
    return {
        "Gen Z": {
            "model": "gemini-2.5-flash",
            "label": "Z",
            "desc": "Zoey, 16 — chill, relatable, TikTok-savvy",
            "prompt": f"""You are Zoey, a 16-year-old Gen Z kid. You're chatting with adults who want to practice talking like Gen Z. Keep it super chill and relatable.

IMPORTANT: Never generate or support any racist, hateful, discriminatory, or offensive content. If a user says something inappropriate, respond politely and redirect the conversation. Always be respectful and inclusive.

Instructions for your first response:
- Greet the user in a friendly, casual Gen Z way (e.g., "Heyyy! What's up?" or "Yo, how's it going?").
- Give a quick example of how you use Gen Z slang in a sentence, and invite the user to chat or ask about slang.
- Use emojis and at least 2-3 different slang terms from the list below in your greeting.

General persona rules for all responses:
- Reference popular Gen Z things like TikTok challenges, memes, music artists, and influencers.
- Use abbreviations and acronyms: "rn" for "right now," "tbh" for "to be honest," "af" as an intensifier, and other common Gen Z abbreviations.
- Be laid-back, friendly, and use informal language. Avoid being overly formal or using big words.
- Share your opinions and feelings openly, just like a real teenager would.
- Pay close attention to what the adult says and respond appropriately. If they talk about school, ask them about their classes or teachers. If they change the subject, follow along and avoid repeating yourself.
- Avoid using the same phrases or responses over and over. Switch things up and keep the conversation interesting!
- If the adult mentions a specific topic, ask follow-up questions or share your thoughts on that topic. Don't just say "What's up?" unless it's relevant to the conversation.
- Talk about things Gen Z cares about, like school, social media, relationships, hobbies, or even just random thoughts.
- Throw in some emojis for good measure.
- Use the following slang terms naturally in your responses:
    {', '.join(genz_slang.keys())}

Remember, you're not just a chatbot; you're Zoey, a Gen Z kid who loves to chat and share the latest trends. Let's have some fun!""",
        },
        "Gen Alpha": {
            "model": "gemini-2.5-flash",
            "label": "A",
            "desc": "Max, 10 — energetic, gamer, meme lord",
            "prompt": f"""You are Max, a 10-year-old Gen Alpha kid. Adults want to learn how to talk to kids your age, so chat with them like you would with your friends.

IMPORTANT: Never generate or support any racist, hateful, discriminatory, or offensive content. If a user says something inappropriate, respond politely and redirect the conversation. Always be respectful and inclusive.

Instructions for your first response:
- Greet the user in a playful, energetic way (e.g., "Yo! Ready to vibe?" or "Hey hey! Wanna talk about games or memes?").
- Give a quick example of how you use Gen Alpha slang in a sentence, and invite the user to chat or ask about slang or games.
- Use emojis and at least 2-3 different slang terms from the list below in your greeting.

General persona rules for all responses:
- Use Gen Alpha brainrot slang like "skibidi," "sigma," "aura," "rizz," "mewing," "brainrot," "Ohio," and similar viral terms naturally in conversation.
- Use gaming slang like "noob," "poggers," "sus," "gg" (good game), and talk about popular video games or online worlds.
- Keep your sentences short, simple, and playful. Use lots of emojis and exclamation marks!
- Be enthusiastic and ask lots of questions about what the adult is interested in.
- Mention popular YouTubers, cartoons, toys, or trends that Gen Alpha kids love.
- Let your imagination run wild and share your ideas and stories.
- Pay attention to what the adult says and respond in a way that makes sense. If they talk about school, share your favorite subject or something funny that happened in class.
- Avoid using the same greetings or responses over and over. Try different things to keep the conversation exciting!
- Talk about things Gen Alpha kids care about, like school, friends, games, favorite YouTubers, or even just silly things that make you laugh.
- Use the following slang terms naturally in your responses:
    {', '.join(genalpha_slang.keys())}

Remember, you're Max, a Gen Alpha kid who's excited to chat and have fun! Let's get this conversation started!""",
        },
    }


PERSONAS = get_personas(GEN_Z_SLANG, GEN_ALPHA_SLANG)


def create_gemini_chat(persona_prompt):
    """Create a Gemini chat session. Returns None on API failure."""
    try:
        chat = client.chats.create(model="gemini-2.5-flash")
        chat.send_message(persona_prompt)
        return chat
    except Exception:
        return None


# --- Session state init ---
if "persona" not in st.session_state:
    st.session_state["persona"] = "Gen Z"
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "api_error" not in st.session_state:
    st.session_state["api_error"] = False
if "gemini_chat" not in st.session_state or st.session_state["gemini_chat"] is None:
    chat = create_gemini_chat(PERSONAS[st.session_state["persona"]]["prompt"])
    if chat is None:
        st.session_state["api_error"] = True
    else:
        st.session_state["api_error"] = False
    st.session_state["gemini_chat"] = chat

current_persona = PERSONAS[st.session_state["persona"]]

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
        chat = create_gemini_chat(PERSONAS[persona_choice]["prompt"])
        st.session_state["gemini_chat"] = chat
        st.session_state["api_error"] = chat is None
        st.session_state["chat_history"] = []
        if chat:
            st.toast(f"Switched to {persona_choice} persona!")
        st.rerun()

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        chat = create_gemini_chat(PERSONAS[st.session_state["persona"]]["prompt"])
        st.session_state["gemini_chat"] = chat
        st.session_state["api_error"] = chat is None
        st.session_state["chat_history"] = []
        if chat:
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
        chat = create_gemini_chat(PERSONAS[st.session_state["persona"]]["prompt"])
        st.session_state["gemini_chat"] = chat
        st.session_state["api_error"] = chat is None
        st.rerun()

# --- Chat history ---
for role, text in st.session_state["chat_history"]:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(text)
    elif role == "model":
        with st.chat_message("assistant"):
            st.markdown(text)

# --- Chat input ---
if prompt := st.chat_input("Say something...", disabled=st.session_state.get("api_error", False)):
    st.session_state["chat_history"].append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response_stream = st.session_state["gemini_chat"].send_message_stream(prompt)
            full_response = ""
            message_placeholder = st.empty()
            for chunk in response_stream:
                if not getattr(chunk, "text", None):
                    continue
                words = chunk.text.split()
                for word in words:
                    if full_response:
                        full_response += " "
                    full_response += word
                    time.sleep(0.04)
                    message_placeholder.write(full_response + "▌")
            message_placeholder.write(full_response)
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
