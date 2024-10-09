import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import PyPDF2
import hashlib
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import concurrent.futures
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(page_title="ChatWithPDF", page_icon="📄", layout="wide")

# Initialize Groq client
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {e}")
    st.error("Failed to initialize the AI model. Please check your API key.")

# List of available models
MODELS = [
    "llama3-70b-8192",
    "llama3-8b-8192",
    "gemma-7b-it",
    "gemma2-9b-it",
    "mixtral-8x7b-32768"
]

@st.cache_data
def process_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_page = {executor.submit(extract_text, page): page for page in pdf_reader.pages}
            for future in concurrent.futures.as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    text += future.result() + "\n"
                except Exception as e:
                    logger.warning(f"Skipped page {pdf_reader.pages.index(page)} due to: {str(e)}")
        return text
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        st.error("Failed to process the PDF. Please try again with a different file.")
        return ""

def extract_text(page):
    try:
        return page.extract_text()
    except Exception as e:
        logger.warning(f"Error extracting text from page: {e}")
        return ""

@st.cache_data
def split_into_chunks(text, chunk_size=1500, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

@st.cache_data
def get_or_create_chunks(file):
    try:
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)

        cache_file = f"cache/{file_hash}_chunks.pkl"
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        text = process_pdf(file)
        chunks = split_into_chunks(text)

        os.makedirs('cache', exist_ok=True)
        with open(cache_file, 'wb') as f:
            pickle.dump(chunks, f)

        return chunks
    except Exception as e:
        logger.error(f"Error in get_or_create_chunks: {e}")
        st.error("Failed to process the PDF chunks. Please try again.")
        return []

@st.cache_resource
def get_vectorizer(chunks):
    try:
        return TfidfVectorizer().fit(chunks)
    except Exception as e:
        logger.error(f"Error creating vectorizer: {e}")
        st.error("Failed to create text vectorizer. Please try again.")
        return None

def find_most_relevant_chunks(query, chunks, vectorizer, top_k=2):
    try:
        chunk_vectors = vectorizer.transform(chunks)
        query_vector = vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, chunk_vectors)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [chunks[i] for i in top_indices]
    except Exception as e:
        logger.error(f"Error finding relevant chunks: {e}")
        st.error("Failed to find relevant information. Please try a different query.")
        return []

def get_ai_response(messages, context, model):
    try:
        system_message = {"role": "system", "content": "You are a helpful assistant for answering questions about the given PDF content. Use the provided context to answer questions, but also consider the conversation history."}

        # Combine system message, conversation history, and the new query with context
        all_messages = [system_message] + messages[:-1] + [{"role": "user", "content": f"Context: {context}\n\nBased on this context and our previous conversation, please answer the following question: {messages[-1]['content']}"}]

        chat_completion = client.chat.completions.create(
            messages=all_messages,
            model=model,
            max_tokens=2048,
            temperature=0.7
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "I'm sorry, but I encountered an error while processing your request. Please try again."

def main():
    st.title("ChatWithPDF")

    # Initialize session state variables
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'model' not in st.session_state:
        st.session_state.model = MODELS[0]
    if 'chunks' not in st.session_state:
        st.session_state.chunks = []
    if 'vectorizer' not in st.session_state:
        st.session_state.vectorizer = None

    st.sidebar.header("Upload PDF")
    pdf_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")

    if pdf_file:
        with st.spinner("Processing PDF..."):
            st.session_state.chunks = get_or_create_chunks(pdf_file)
            st.session_state.vectorizer = get_vectorizer(st.session_state.chunks)
        if st.session_state.chunks and st.session_state.vectorizer:
            st.sidebar.success("PDF processed successfully!")
        else:
            st.sidebar.error("Failed to process PDF. Please try again.")

    selected_model = st.selectbox("Select Model", MODELS, index=MODELS.index(st.session_state.model))
    if selected_model != st.session_state.model:
        st.session_state.model = selected_model

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your PDF"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            relevant_chunks = find_most_relevant_chunks(prompt, st.session_state.chunks, st.session_state.vectorizer) if st.session_state.chunks else []
            context = "\n\n".join(relevant_chunks)

            full_response = get_ai_response(st.session_state.messages, context, st.session_state.model)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Add a button to clear the conversation
   # if st.button("Clear Conversation"):
    #    st.session_state.messages = []
     #   st.experimental_rerun()

if __name__ == "__main__":
    main()
