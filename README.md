# INTELLIMESH - LLM App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://intelli-mesh.streamlit.app/)

A comprehensive multi-feature LLM application built with **Streamlit** and powered by **Google Generative AI (Gemini)**. This project demonstrates practical implementation of advanced LLM capabilities for real-world applications.

## 🌟 Features

### Core Modules

1. **Text Generation** - Generate creative and contextual text content
2. **Image Analysis** - Analyze and understand images using vision capabilities
3. **Code Generation** - Generate code snippets based on natural language descriptions
4. **Document Summarization** - Summarize large documents into concise summaries
5. **Chat Assistant** - Interactive conversational AI assistant
6. **Translation Tool** - Multi-language translation capabilities
7. **Calorie Counter** - AI-powered nutritional analysis
8. **Multi-Language Invoice Extraction** - Extract information from invoices in multiple languages
9. **PDF Chat** - Chat with PDF documents and extract information
10. **Natural Language SQL Query** - Convert natural language to SQL queries

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Google Generative AI (Gemini API)
- **Backend**: Python
- **Database**: SQLite
- **Additional Libraries**:
  - `google-generativeai` - Google Generative AI API
  - `python-dotenv` - Environment variable management
  - `langchain` - LLM framework
  - `langchain-community` - Community integrations
  - `langchain-google-genai` - Google AI integration
  - `PyPDF2` - PDF processing
  - `chromadb` - Vector database for embeddings
  - `faiss-cpu` - Similarity search
  - `pandas` - Data manipulation
  - `Pillow` - Image processing

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini API
- Git (for cloning)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/pranjaysaxena007/LLM-App.git
cd LLM-App
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the project root directory:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 📖 Usage

### Run the Application

```bash
streamlit run main.py
```

The app will open in your default web browser at `http://localhost:8501`

### Navigation

Use the sidebar to navigate between different features:
- Each feature is a separate page
- Select from the dropdown or click on a feature
- Follow the on-screen instructions for each module

## 📂 Project Structure

```
LLM-App/
├── main.py                          # Main Streamlit app entry point
├── requirements.txt                 # Python dependencies
├── student.db                       # SQLite database
├── .env                             # Environment variables (create this)
├── .gitignore                       # Git ignore file
├── .streamlit/                      # Streamlit configuration
│   └── config.toml                 # Streamlit settings
├── .devcontainer/                   # Dev container setup
└── pages/                           # Multi-page app features
    ├── 1_text_generation.py         # Text generation module
    ├── 2_image_analysis.py          # Image analysis module
    ├── 3_code_generator.py          # Code generation module
    ├── 4_document_summarizer.py     # Document summarization
    ├── 5_chat_assistant.py          # Chat assistant
    ├── 6_translation_tool.py        # Translation tool
    ├── 7_calorie_counter.py         # Calorie counter
    ├── 8_multi_lang_invoice_extract.py  # Multi-language invoice extraction
    ├── 9_chat_with_pdf.py           # PDF chat interface
    └── 10_natural_lang_sql_query.py # Natural language to SQL
```

## 🔑 API Configuration

This application uses the **Google Generative AI API** (Gemini). You need to:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GOOGLE_API_KEY`

## 📝 Example Usage

### Text Generation
```
Prompt: "Write a short story about a robot learning to paint"
Output: [Generated story]
```

### Image Analysis
```
Upload Image → AI analyzes and describes content
```

### Code Generation
```
Description: "Create a function to reverse a string"
Output: Generated Python code
```

## 🌐 Live Demo

The application is deployed and live at: [https://intelli-mesh.streamlit.app/](https://intelli-mesh.streamlit.app/)

## 📚 Dependencies

See `requirements.txt` for all dependencies. Key packages:

```
streamlit>=1.0.0
google-generativeai
python-dotenv
langchain
langchain-google-genai
PyPDF2
chromadb
faiss-cpu
pandas
Pillow
```

## 🔒 Security

- Never commit `.env` files with real API keys
- API keys are stored in environment variables
- User data is processed locally by default

## 🐛 Troubleshooting

### Issue: "API Key not found"
- Ensure `.env` file exists in the project root
- Verify `GOOGLE_API_KEY` is set correctly
- Restart the Streamlit app

### Issue: Dependencies not installing
```bash
# Upgrade pip
pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

### Issue: Port 8501 already in use
```bash
streamlit run main.py --logger.level=debug --server.port=8502
```

## 📈 Future Enhancements

- [ ] User authentication
- [ ] History and saved sessions
- [ ] Advanced caching for better performance
- [ ] Integration with more LLM providers
- [ ] Custom model fine-tuning
- [ ] Real-time collaboration features
- [ ] Multi-language UI support
- [ ] Advanced analytics and logging

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Pranjay Saxena**
- GitHub: [@pranjaysaxena007](https://github.com/pranjaysaxena007)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you have any questions or need help:
- Open an Issue on GitHub
- Check existing documentation
- Review the code comments

## ⭐ Show Your Support

If this project helped you, please consider giving it a star! It motivates continuous improvement.

---

**Built with ❤️ using Streamlit and Google Generative AI**
