from chatsynth_vanshajr.json_creator import json_creator
from chatsynth_vanshajr.faiss_creator import faiss_creator
from chatsynth_vanshajr.chat_preview import chat_preview
from chatsynth_vanshajr.github_deploy import github_deploy
import streamlit as st

def main():
    st.set_page_config(
        page_title="ChatSynth",
        page_icon="logo.ico",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.sidebar.title("🤖 ChatSynth")
    step = st.sidebar.radio("Steps", [
        "1. Create Profile",
        "2. Build Knowledge Base",
        "3. Preview Chat",
        "4. Deploy to GitHub"
    ])
    
    st.sidebar.write("Do remember to provide any links as proper URLs (e.g., https://www.google.com)!")
    st.sidebar.write("If you find this useful, do star the repo and drop a follow!")
    st.sidebar.write("https://github.com/VanshajR")
    if step == "1. Create Profile":
        json_creator()
    elif step == "2. Build Knowledge Base":
        faiss_creator()
    elif step == "3. Preview Chat":
        chat_preview()
    elif step == "4. Deploy to GitHub":
        github_deploy()


if __name__ == "__main__":
    main()