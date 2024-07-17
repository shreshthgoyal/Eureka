from langchain_community.vectorstores import FAISS
from src.retriever.config import ANSWERS_CSV_PATH, EMBEDDINGS_MODEL
from langchain_core.documents.base import Document
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_nomic.embeddings import NomicEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_cohere import CohereEmbeddings
# from langchain_fireworks import FireworksEmbeddings


import dotenv

dotenv.load_dotenv()

def initialize_vector_db():
    loader = CSVLoader(file_path=ANSWERS_CSV_PATH, encoding="utf-8")
    raw_documents = loader.load()
    
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    for raw_doc in raw_documents:
        content_dict = parse_page_content(raw_doc.page_content)
        answer = content_dict.get('Answer', '')
        metadata = {
            'question': content_dict.get('Question', ''),
            'deep_link': content_dict.get('url', ''),
            'title': content_dict.get('Title', '')
        }

        chunks = text_splitter.split_text(answer)
        for chunk in chunks:
            documents.append(Document(page_content=chunk, metadata=metadata))

    # embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", dimensionality=512)
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
    # embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5")
    # embeddings = FireworksEmbeddings(model="nomic-ai/nomic-embed-text-v1.5")

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

vector_db = initialize_vector_db()
