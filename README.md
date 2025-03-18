# ChatSynth - AI Chatbot Builder 🤖
Check out the ChatSynth github account where all the generated repositories are hosted: [ChatSynth](https://github.com/ChatSynth)

Check out the deployed app here:

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatsynth.streamlit.app)

And a demo chatbot here:

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://demo-chatsynth.streamlit.app)


Create personalized Q&A AI chatbots in 3 easy steps:

1. **Build Profile**: Create structured JSON with user information
2. **Generate Knowledge**: Create FAISS vector database
3. **Deploy**: Push to GitHub with one-click Streamlit deployment

## ✨ Features
- Dynamic form builder with validation
- Option to add personal information, skills, education, work experience, socials and projects 
- FAISS vector store integration
- GitHub deployment for the created chatbot
- Support for multiple LLM models

## 🔑 Get API Keys  
   - [Groq Cloud API Key](https://console.groq.com/keys) (Free tier available)
   - [HuggingFace Token](https://huggingface.co/settings/tokens) (Use write token)

## 🏗️ Steps
1. **Step 1**: Fill in the details on the page to generate a json with the entered details, use the `Generate JSON` button.
2. **Step 2**: Enter your HuggingFace token and then use the `Create FAISS Index` button to then generate the FAISS store vector embeddings, be patient as it can take some time depending on the amount of data.
3. **Step 3**: Provide Groq API Key and HuggingFace token and then chat with your bot to verify that it works as you expect. If you wish to change anything, repeat steps 1 and 2.
4. **Step 4**: Provide a name for the resultant repository that will host the code for your chatbot, click `Deploy to Github` and wait for the success message which will contain the link to the created GitHub repository.

## ↗️ Next Steps
The created GitHub repository will contain further instructions, but basically you have to fork the repository or download the code to then deploy it online, and provide streamlit secrets when you do.

## 🤝 Contributing
Contributions are welcome, open an issue on the repository or get in contact through any socials.

## 📄 License
BSD License © [Vanshaj Raghuvanshi](https://github.com/VanshajR)
Please refrain from copying without accrediting.