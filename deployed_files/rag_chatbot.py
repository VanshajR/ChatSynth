import os
import json
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains.combine_documents.chain import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
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
        user_name = user_data["personal_info"]["name"]
    except Exception as e:
        st.error(f"Error loading user profile: {str(e)}")
        return
    
    # Load FAISS index only once and store it in session state
    if "faiss_vectors" not in st.session_state:
        try:
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            st.session_state.faiss_vectors = FAISS.load_local(
                "faiss_index", embeddings, allow_dangerous_deserialization=True
            )
        except Exception as e:
            st.error(f"Error loading FAISS index: {str(e)}")
            return
    
    # Set up UI
    st.set_page_config(page_title=f"{user_name}'s Chatbot", page_icon="🤖")
    st.title(f"Chat with {user_name}'s AI Assistant")

    # Sidebar settings
    with st.sidebar:
        st.header("⚙️ Settings")
        model_name = st.selectbox(
            "🤖 Choose LLM Model:", 
            ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "openai/gpt-oss-20b"] # <-- FIXED: Added missing closing bracket
        )
        st.write("Powered By ChatSynth")
        st.write("https://chatsynth.streamlit.app")

    # Initialize chat session
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat messages
    for msg in st.session_state.chat_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Create RAG chain
    retriever = ChatSynthRetriever(st.session_state.faiss_vectors).get_retriever()

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

    llm = ChatGroq(model_name=model_name, api_key=groq_key)
    
    # This document chain is correct. It expects 'context' and other keys.
    document_chain = create_stuff_documents_chain(llm, prompt_template)
    
    # This retrieval chain is also correct. It will take "input",
    # pass it to the retriever, get documents, and put them into
    # the "context" key for the document_chain.
    chain = create_retrieval_chain(retriever, document_chain)

    # Handle user input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        try:
            with st.spinner("Thinking..."):
                
                # --- REMOVED SECTION ---
                # We no longer need to retrieve documents manually.
                # The 'chain' does this for us.
                # 
                # retrieved_docs = retriever.get_relevant_documents(prompt)
                #
                # if not retrieved_docs:
                #    st.warning("No relevant context found in FAISS!...")
                # --- END REMOVED SECTION ---

                # Get conversation history (your string formatting is fine)
                history = "\n".join(
                    [f"{msg['role']}: {msg['content']}" 
                     for msg in st.session_state.chat_messages[-5:]]
                )

                # --- MODIFIED INVOKE CALL ---
                # We only need to pass the keys the prompt expects, *except* 'context'.
                # The retrieval_chain handles 'context' automatically.
                response = chain.invoke({
                    "input": prompt,
                    "history": history,
                    "name": user_name
                })
                # --- END MODIFIED INVOKE CALL ---

                answer = response.get("answer", "I don't have that information.")

                st.session_state.chat_messages.append({"role": "assistant", "content": answer})
                st.chat_message("assistant").write(answer)

        except Exception as e:
            st.error(f"Error: {str(e)}")

chat_assistant()
