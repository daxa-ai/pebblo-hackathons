from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
import google.generativeai as genai
from langchain_community.document_loaders import  PyPDFLoader, PebbloSafeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import streamlit as st
import os


# Set the PWD environment variable to the current working directory
os.environ['PWD'] = os.getcwd()

# Load environment variables from .env file
load_dotenv()

# Define the persist directory for the vector database
persist_directory = os.path.join(os.environ['PWD'], 'per_dir')
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Initialize Google Generative AI
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize callback manager for streaming output
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Initialize the ChatGoogleGenerativeAI model with streaming output and safety settings
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
    },
    callback_manager=callback_manager
)

# Check if the persist directory exists
if not os.path.exists(persist_directory):
    with st.spinner('🚀 Starting your bot.  This might take a while'):
        # Data Pre-processing: Load and process PDF documents
        pdf_loader = PebbloSafeLoader(PyPDFLoader(os.path.join(os.environ['PWD'], 'docs', 'Merged_Ayurbeat_Everyday_Ayurveda.pdf')), name="Final")
        pdf_documents = pdf_loader.load()

        # Split the loaded text into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=50)
        pdf_context = "\n\n".join(str(p.page_content) for p in pdf_documents)
        pdfs = splitter.split_text(pdf_context)

        print("Data Processing Complete")

        # Create and persist the vector database from the processed text chunks
        vectordb = Chroma.from_texts(pdfs, embeddings, persist_directory=persist_directory)
        vectordb.persist()

        print("Vector DB Creating Complete\n")
else:
    # Load the existing vector database
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    print("Vector DB Loaded\n")

# Initialize the query chain for the model
query_chain = RetrievalQA.from_chain_type(
    llm=model,
    retriever=vectordb.as_retriever()
)

# Display the chat history
for msg in st.session_state.history:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# Handle user input
prompt = st.chat_input("Say something")
if prompt:
    # Append user message to session state history
    st.session_state.history.append({
        'role': 'user',
        'content': prompt + ". don't give harmful advice or anything that can hurt someone's feelings or emotions or anything outside of the context of this chat."
    })

    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant's response
    with st.spinner('💡Thinking'):
        response = query_chain.invoke({"query": prompt})

        st.session_state.history.append({
            'role': 'Assistant',
            'content': response['result']
        })

        with st.chat_message("Assistant"):
            st.markdown(response['result'])
