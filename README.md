## Overview

This repository contains a Streamlit application that integrates multiple components from the LangChain library and Google Generative AI to create an interactive, AI-powered chatbot. The chatbot can process, retrieve, and respond to user queries based on a pre-loaded PDF document. The system employs a vector database for efficient information retrieval and ensures responses are safe by leveraging Google's safety settings.

## Features

- **Google Generative AI Integration**: Utilizes the `ChatGoogleGenerativeAI` model for generating human-like responses.
- **PDF Document Processing**: Loads and processes PDF documents into chunks for efficient retrieval.
- **Vector Database**: Stores processed text chunks in a vector database using `Chroma`, allowing for fast and accurate query retrieval.
- **Streamlit Interface**: Provides a simple and interactive user interface for chat-based interaction.
- **Safety Settings**: Configured to block harmful content using Google's safety settings.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Google Generative AI](https://developers.generativeai.google)
- [LangChain](https://langchain.readthedocs.io/)
- [dotenv](https://pypi.org/project/python-dotenv/)

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables by creating a `.env` file in the root directory:
    ```
    GOOGLE_API_KEY=your_google_api_key
    ```

5. Place the PDF document in the `docs` directory:
    ```
    docs/Merged_Ayurbeat_Everyday_Ayurveda.pdf
    ```

## Usage

1. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

2. The application will start by checking if a vector database already exists. If not, it will process the provided PDF document, split it into chunks, and create a vector database.

3. Once the setup is complete, the application will load the vector database and present a chat interface.

4. Enter your query in the chat input, and the chatbot will respond based on the content of the processed PDF.

## File Structure

- **app.py**: Main script containing the logic for the Streamlit application.
- **docs/**: Directory containing the PDF document to be processed.
- **per_dir/**: Directory where the vector database will be persisted.
- **.env**: Environment variables, including the Google API key.

## Configuration

- **Google API Key**: Required for using Google Generative AI. Store it in the `.env` file.
- **PDF Loader**: Currently set to load a specific PDF document. Modify the path in the script to use a different document.
- **Safety Settings**: Configurable via the `HarmCategory` and `HarmBlockThreshold` parameters in the `ChatGoogleGenerativeAI` initialization.

## Dependencies

The project relies on the following Python packages:

- `langchain_chroma`
- `langchain_google_genai`
- `google-generativeai`
- `langchain_community`
- `dotenv`
- `streamlit`

Ensure all dependencies are installed using the provided `requirements.txt`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

By following the instructions in this README, you can set up and run the AI-powered chatbot that processes and responds to user queries based on the content of a PDF document. The chatbot is designed to provide safe, contextually relevant information while ensuring user interactions are positive and constructive.
