import os
import json
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
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
    
    # Ensure FAISS index exists
    if not os.path.exists("faiss_index"):
        st.error("FAISS index not found! Please generate the FAISS index first.")
        return
    
    
    # Set up UI
    st.set_page_config(page_title=f"{user_name}'s Chatbot", page_icon="🤖")
    st.title(f"Chat with {user_name}'s AI Assistant")

    # Sidebar settings
    with st.sidebar:
        st.header("⚙️ Settings")
        model_name = st.selectbox("🤖 Choose LLM Model:", ["Llama3-70b-8192", "mixtral-8x7b-32768"])
        st.write("Powered By ChatSynth")
        st.write("https://chatsynth.streamlit.app")

    # Initialize chat session
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat messages
    for msg in st.session_state.chat_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Create RAG chain
    retriever = ChatSynthRetriever().get_retriever()

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
    chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt_template))

    # Handle user input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        try:
            with st.spinner("Thinking..."):
                # Retrieve relevant documents from FAISS
                retrieved_docs = retriever.get_relevant_documents(prompt)

                # Check if context exists
                if not retrieved_docs:
                    st.warning("No relevant context found in FAISS! The chatbot may not provide a good answer.")

                # Get conversation history
                history = "\n".join(
                    [f"{msg['role']}: {msg['content']}" 
                     for msg in st.session_state.chat_messages[-5:]]
                )

                response = chain.invoke({
                    "input": prompt,
                    "history": history,
                    "name": user_name,
                    "context": "\n\n".join([doc.page_content for doc in retrieved_docs])
                })

                answer = response.get("answer", "I don't have that information.")

                st.session_state.chat_messages.append({"role": "assistant", "content": answer})
                st.chat_message("assistant").write(answer)

        except Exception as e:
            st.error(f"Error: {str(e)}")

chat_assistant()
