import streamlit as st
from chatbot import get_response
import datetime
import pandas as pd

st.set_page_config(page_title="ChatGPT external API", page_icon="🧠")

# Language
language = st.selectbox("🌐 Vyber jazyk / Select language", ["Čeština", "English"])

# Dictionary pro rozdělení jazyků
texts = {
    "Čeština": {
        "title": "💡 Objevuj, ověřuj, uč se... ",
        "description": "Aplikace je zpracována v rámci projektu v kurzu programování v Python. "
                       "Aplikace bude fungovat jako klasický ChatGPT, jen není možné se přihlásit a plně navázat na předchozí chaty.",
        "caption": "🛠️ Pracovní verze",
        "placeholder": "✍️ Zadejte svou zprávu:",
        "send": "Odeslat",
        "clear": "🗑️ Smazat konverzaci",
        "user": "👤 **Vy:**",
        "bot": "🤖 **Chat:**"
    },
    "English": {
        "title": "💡 Discover, verify, learn... ",
        "description": "This app is part of a project in a Python programming course. "
                       "It works like ChatGPT, but login and chat history are not supported.",
        "caption": "🛠️ Work in progress",
        "placeholder": "✍️ Enter your message:",
        "send": "Send",
        "clear": "🗑️ Clear conversation",
        "user": "👤 **You:**",
        "bot": "🤖 **Chat:**"
    }
}
t = texts[language]

# UI texty podle jazyka
st.title(t["title"])
st.markdown(t["description"])
st.caption(t["caption"])

# Ukládání dotazů na stránce
if "messages" not in st.session_state:
    st.session_state.messages = []

# Smazání
if st.button(t["clear"]):
    st.session_state.messages = []

# Input
with st.form("user_input_form", clear_on_submit=True):
    user_input = st.text_input(t["placeholder"])
    submitted = st.form_submit_button(t["send"])

# Zpracování zprávy a odpovědi
if submitted and user_input:
    # Uložení uživatelské zprávy
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Získání odpovědi z OpenAI
    with st.spinner("💬 Chat přemýšlí..."):
        response = get_response(st.session_state.messages, language=language)

    # Uložení odpovědi od AI
    st.session_state.messages.append({"role": "assistant", "content": response})

# Zobrazení historie konverzace
st.write("---")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"{t['user']} {msg['content']}", unsafe_allow_html=True)
    else:
        st.markdown(f"{t['bot']} {msg['content']}", unsafe_allow_html=True)

# Funkce pro uložení jako TXT
def save_chat_as_txt(messages):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_{timestamp}.txt"
    lines = []
    for msg in messages:
        role = "Ty" if msg["role"] == "user" else "AI"
        lines.append(f"{role}: {msg['content']}\n")
    return filename, "\n".join(lines)

# Funkce pro uložení jako CSV
def save_chat_as_csv(messages):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_{timestamp}.csv"
    df = pd.DataFrame([
        {"role": "Vy" if msg["role"] == "user" else "Chat", "message": msg["content"]}
        for msg in messages
    ])
    return filename, df.to_csv(index=False).encode("utf-8")

# Nabídka uložení
if st.session_state.messages:
    format_choice = st.radio("📥 Vyber formát pro uložení konverzace:", ["TXT", "CSV"], horizontal=True)

    if format_choice == "TXT":
        filename, content = save_chat_as_txt(st.session_state.messages)
        st.download_button("💾 Uložit jako TXT", content, file_name=filename, mime="text/plain")

    elif format_choice == "CSV":
        filename, content = save_chat_as_csv(st.session_state.messages)
        st.download_button("💾 Uložit jako CSV", content, file_name=filename, mime="text/csv")