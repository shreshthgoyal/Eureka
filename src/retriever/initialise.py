from langchain_community.vectorstores import FAISS
import os
from src.retriever.config import ANSWERS_CSV_PATH, EMBEDDINGS_MODEL
from langchain_core.documents.base import Document
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_nomic.embeddings import NomicEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_cohere import CohereEmbeddings
# from langchain_fireworks import FireworksEmbeddings


import dotenv

dotenv.load_dotenv()

def load_and_process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load_and_split()

def load_and_process_csv(file_path):
    loader = CSVLoader(file_path=file_path)
    return loader.load()

def initialize_vector_db(data_folder):
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    
    # embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", dimensionality=512)
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
    # embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5")
    # embeddings = FireworksEmbeddings(model="nomic-ai/nomic-embed-text-v1.5")
    
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        if filename.endswith('.pdf'):
            pages = load_and_process_pdf(file_path)
        elif filename.endswith('.csv'):
            pages = load_and_process_csv(file_path)
        else:
            continue

        for doc in pages:
            content_dict = parse_page_content(doc.page_content)
            doc.page_content = content_dict.get('Answer', '')
            chunks = text_splitter.split_text(doc.page_content)
            for chunk in chunks:
                doc = Document(page_content=chunk, metadata=doc.metadata)
                documents.append(doc)

    vector_db = FAISS.from_documents(
        documents,
        embeddings,
    )
    return vector_db

def parse_page_content(page_content):
    content_dict = {}
    lines = page_content.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            content_dict[key.strip()] = value.strip()
    return content_dict


vector_db = initialize_vector_db('data/')
