import streamlit as st
from openai import OpenAI
from spellchecker import SpellChecker
import time

# Initialize OpenAI client with your secret API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Spell checker
spell = SpellChecker()

# Fix typos
def correct_spelling(text):
    words = text.split()
    corrected = [spell.correction(w) or w for w in words]
    return " ".join(corrected)

# Typing effect
def typing_effect(message, speed=0.05):
    placeholder = st.empty()
    for i in range(len(message) + 1):
        placeholder.markdown(message[:i])
        time.sleep(speed)

# Get GPT response with basic error handling
def get_gpt_reply(user_input, messages):
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply

    except:
        return "⚠️ Sorry, I'm having trouble responding right now. Please try again later."

# Streamlit page config
st.set_page_config(page_title="AI ChatBot", page_icon="🤖")
st.markdown("<h1 style='text-align: center;'>🤖 AI ChatBot</h1>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Say something...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # Fix spelling
    fixed_input = correct_spelling(user_input)

    # Get bot response
    bot_response = get_gpt_reply(fixed_input, st.session_state.messages)

    # Show bot response
    with st.chat_message("assistant"):
        typing_effect(bot_response)
