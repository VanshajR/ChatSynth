import os
import json
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from chatsynth_vanshajr.retriever import ChatSynthRetriever

def chat_assistant():
    # Load secrets
    try:
        groq_key = st.secrets["GROQ_API_KEY"]
        hf_token = st.secrets["HF_TOKEN"]
    except KeyError:
        st.error("Missing API keys in secrets! Please add them in `.streamlit/secrets.toml`.")
        return
    
    # Load user profile
    try:
        with open("user_profile.json") as f:
            user_data = json.load(f)
        # Robustly extract name to prevent type errors
        user_name = str(user_data.get("personal_info", {}).get("name", "User"))
    except Exception as e:
        st.error(f"Error loading user profile: {str(e)}")
        return
    
    # Load FAISS index only once and store it in session state
    if "faiss_vectors" not in st.session_state:
        try:
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            if os.path.exists("faiss_index"):
                st.session_state.faiss_vectors = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            else:
                st.error("FAISS index not found.")
                return
        except Exception as e:
            st.error(f"Error loading FAISS index: {str(e)}")
            return
    
    # Set up UI
    st.set_page_config(page_title=f"{user_name}'s Chatbot", page_icon="🤖")
    st.title(f"Chat with {user_name}'s AI Assistant")

    # Sidebar settings
    with st.sidebar:
        st.header("⚙️ Settings")
        # Updated model list
        model_name = st.selectbox("🤖 Choose LLM Model:", ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
        st.write("Powered By ChatSynth")
        st.write("https://chatsynth.streamlit.app")

    # Initialize chat session
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat messages
    for msg in st.session_state.chat_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Create RAG components
    retriever = ChatSynthRetriever(st.session_state.faiss_vectors).get_retriever()
    llm = ChatGroq(model_name=model_name, api_key=groq_key)

    prompt_template = ChatPromptTemplate.from_template("""
        You are an AI assistant created to answer questions about {name}. You are **not** {name}, but you use the provided context to give accurate responses.

        Context about {name}:
        {context}

        Conversation History:
        {history}

        **Rules:**
        1. Be respectful and professional.
        2. Answer only using the given context.
        3. If unsure, say "I don't have that information."
        4. Keep responses professional and concise.

        **User's Question:** {input}
    """)

    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])

    # MODERN LCEL CHAIN (Fixes Dictionary Error & Deprecation)
    chain = (
        {
            # Fix 1: Explicitly extract 'input' string for retriever to avoid 'dict has no replace' error
            "context": (lambda x: x["input"]) | retriever | format_docs,
            # Fix 2: Pass 'input' string to prompt
            "input": lambda x: x["input"],
            "history": lambda x: x.get("history", ""),
            "name": lambda x: x.get("name", user_name)
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )

    # Handle user input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        try:
            with st.spinner("Thinking..."):
                # Get conversation history
                history = "\n".join(
                    [f"{msg['role']}: {msg['content']}" 
                     for msg in st.session_state.chat_messages[-5:]]
                )

                # Invoke chain (No manual retrieval needed)
                answer = chain.invoke({
                    "input": prompt,
                    "history": history,
                    "name": user_name,
                })

                if not answer:
                    answer = "I don't have that information."

                st.session_state.chat_messages.append({"role": "assistant", "content": answer})
                st.chat_message("assistant").write(answer)

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    chat_assistant()
