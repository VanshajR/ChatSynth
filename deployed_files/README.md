# 🤖 Your Personalized Chatbot
Now that you have the files for the chatbot ready, it's time to deploy it online, for free!

## 🚀 Quick Deployment Guide

1. **Fork this Repository**  
   [Click here to fork](https://github.com/VanshajR/ChatSynth/fork) → Select your account

2. **Get API Keys**  
   - [Groq Cloud API Key](https://console.groq.com/keys) (Free tier available)
   - [HuggingFace Token](https://huggingface.co/settings/tokens) (Use write token)

3. **Deploy on Streamlit**  
   [![Deploy](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
   - Create new app → Connect your forked repo
   - Set main file to `rag_chatbot.py`
   - Add secrets in Advanced Settings:
     ```toml
     GROQ_API_KEY = "your_groq_key"
     HF_TOKEN = "your_hf_token"
     ```

   **Alternatively**
   To run the app locally, just clone the repository or download the code, and add a `.streamlit` directory in the repository, and a `secrets.toml` file in that directory with the same content as above, and run the code:
   ```sh
   pip install -r requirements.txt
   streamlit run rag_chatbot.py
   ```

4. **Launch Your Chatbot**  
   Click "Deploy" - your AI assistant will be live in minutes!

## 📂 Project Structure
This is what the structure of the repositiry should look like:
```
<Name>/
├── faiss_index/
│   ├── index.faiss
│   └── index.pkl
├── README.md
├── rag_chatbot.py
├── requirements.txt
└── user_profile.json
```

## 🔧 Maintenance Tips
- Update `user_profile.json` to modify your information
- Regenerate FAISS index after profile changes
- Keep API keys secure - never commit them directly

## 💖 Support the Project
If you find this useful, please:
⭐ Star [ChatSynth Repository](https://github.com/VanshajR/ChatSynth)  
👤 Follow [Vanshaj on GitHub](https://github.com/VanshajR)