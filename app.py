from modules.json_creator import json_creator
from modules.faiss_creator import faiss_creator
from modules.chat_preview import chat_preview
from modules.github_deploy import github_deploy
import streamlit as st

def main():
    st.sidebar.title("ChatBot Factory")
    step = st.sidebar.radio("Steps", [
        "1. Create Profile",
        "2. Build Knowledge Base",
        "3. Preview Chat",
        "4. Deploy to GitHub"
    ])
    
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