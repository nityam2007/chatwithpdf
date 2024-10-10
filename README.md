# ChatWithPDF

ChatWithPDF is an advanced Streamlit application that enables users to engage in interactive conversations with the content of uploaded PDF documents using Groq's AI models. This tool simplifies the process of extracting information, generating insightful responses, and enhancing your overall PDF reading experience.

## Features

- 📤 Easy PDF document upload
- 📄 Automatic text extraction from PDFs
- 💬 Intuitive chat interface
- 🤖 AI-powered responses based on PDF content
- 🎨 User-friendly Streamlit interface
- 📱 Responsive design for desktop and mobile devices
- 🔄 Multiple AI model options
- 🔍 Context-aware responses using TF-IDF and cosine similarity
  <br><br>

# Our site or setup manually

## 🌐 **[chatwithpdf.nsheth.in](https://chatwithpdf.nsheth.in)**

## Installation

1. Clone the repository:

```

git clone https://github.com/nityam2007/chatwithpdf.git
cd chatwithpdf

```

2. Install the required dependencies:

```

pip install -r requirements.txt

```

3. Set up your API keys:
   Create a `.env` file in the project root and add your Groq API key:

```

GROQ_API_KEY=your_groq_api_key

```

## Usage

1. Run the Streamlit app:

```

streamlit run app.py

```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).

3. Upload a PDF document using the file uploader in the sidebar.

4. Select an AI model from the dropdown menu.

5. Start chatting with the AI about the content of your PDF!

## How It Works

1. **PDF Upload**: Users upload their PDF documents through the Streamlit interface.
2. **Text Extraction**: The application extracts text content from the uploaded PDF using [PyPDF2](https://pypdf2.readthedocs.io/).
3. **Text Chunking**: The extracted text is split into manageable chunks for processing.
4. **Vectorization**: TF-IDF vectorization is applied to the text chunks for efficient similarity comparison.
5. **Query Processing**: User queries are analyzed to find the most relevant text chunks.
6. **AI Processing**: The relevant chunks and query are sent to the selected Groq AI model for processing.
7. **Interactive Chat**: Users can ask questions or request information about the PDF content through the chat interface.
8. **AI Responses**: The AI generates contextual responses based on the PDF content and user queries.

## Dependencies

- [Streamlit](https://streamlit.io/): For creating the web application interface
- [PyPDF2](https://pypdf2.readthedocs.io/): For extracting text from PDF files
- [Groq](https://groq.com/): For powering the AI models and generating responses
- [python-dotenv](https://github.com/theskumar/python-dotenv): For managing environment variables
- [scikit-learn](https://scikit-learn.org/): For TF-IDF vectorization and cosine similarity calculations

## AI Models

The application supports multiple AI models from Groq:

- llama3-70b-8192
- llama3-8b-8192
- gemma-7b-it
- gemma2-9b-it
- mixtral-8x7b-32768

Users can select their preferred model from the dropdown menu in the application.

## Features

- **PDF Processing**: Efficiently extracts text from PDF files using multithreading.
- **Text Chunking**: Splits large texts into manageable chunks with customizable size and overlap.
- **Caching**: Implements caching mechanisms to improve performance for repeated queries on the same PDF.
- **Context-Aware Responses**: Uses TF-IDF and cosine similarity to find the most relevant text chunks for each query.
- **Conversation History**: Maintains chat history for context-aware responses throughout the conversation.
- **Error Handling**: Implements comprehensive error handling and logging for improved reliability.

## Contributing

We welcome contributions to improve ChatWithPDF! If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for providing an excellent framework for building data applications
- [Groq](https://groq.com/) for their powerful language models and API
- All open-source contributors whose libraries and tools made this project possible

## Contact and Support

For any questions, feedback, or issues, please:

- Open an issue on this GitHub repository
- Contact the maintainer at [support@nsheth.in](mailto:support@nsheth.in)

## Roadmap

- [ ] Implement multi-language support
- [ ] Add support for more document formats (e.g., DOCX, TXT)
- [ ] Improve text extraction accuracy for complex PDF layouts
- [ ] Implement user authentication and document saving features
- [ ] Enhance AI model selection with performance metrics and recommendations

---

Made with ❤️ by Nityam A Sheth (Nityam2007 / NSheth.in)
