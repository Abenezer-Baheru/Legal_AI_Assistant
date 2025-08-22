import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from app.config import API_URL  # Configurable endpoint


st.set_page_config(page_title="Ethiopian Legal Assistant", page_icon="⚖️")
st.title("⚖️ Ethiopian Legal Assistant")

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# Input field
query = st.chat_input("Ask a legal question...")

if query and query.strip():
    st.session_state.history.append({"role": "user", "text": query})
    with st.chat_message("user"):
        st.markdown(query)

    try:
        with st.spinner("🔍 Searching legal documents..."):
            res = requests.post(API_URL, json={"query": query})
            data = res.json()
            response = data.get("response", "⚠️ No response received.")
            refs = data.get("references", [])
    except Exception as e:
        response = f"⚠️ Backend error: {e}"
        refs = []

    full = response
    if refs:
        full += "\n\n📖 You're referencing the following articles:\n"
        full += "\n".join(f"• {r}" for r in refs)

    st.session_state.history.append({"role": "ai", "text": full})
    with st.chat_message("ai"):
        st.markdown(full)

# Redisplay full history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])