import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_core.documents.base import Document
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
import dotenv

dotenv.load_dotenv()

def load_and_process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load_and_split()

def load_and_process_csv(file_path):
    loader = CSVLoader(file_path)
    return loader.load()

def parse_page_content(page_content):
    content_dict = {}
    lines = page_content.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            content_dict[key.strip()] = value.strip()
    return content_dict

def ingest_documents(data_folder, faiss_index_path, embeddings_path, single_doc_folder):
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
    
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        if filename.endswith('.pdf'):
            pages = load_and_process_pdf(file_path)
        elif filename.endswith('.csv'):
            pages = load_and_process_csv(file_path)
        else:
            continue
                
        
        single_doc = []
        for doc in pages:
            if filename.endswith('.csv'):
                content_dict = parse_page_content(doc.page_content)
                doc.page_content = content_dict.get('Answer', '')
            chunks = text_splitter.split_text(doc.page_content)
            for chunk in chunks:
                metadata_with_source = doc.metadata
                metadata_with_source['source'] = filename
                doc = Document(page_content=chunk, metadata=metadata_with_source)
                documents.append(doc)
                single_doc.append(doc)

        if single_doc:
            single_vector_db = FAISS.from_documents(single_doc, embeddings)
            single_doc_base = os.path.splitext(filename)[0]
            single_doc_index_path = os.path.join(single_doc_folder, f"{single_doc_base}_index")
            single_doc_embeddings_path = os.path.join(single_doc_folder, f"{single_doc_base}_embeddings.pkl")
            
            with open(single_doc_embeddings_path, 'wb') as f:
                pickle.dump(single_doc, f)
            single_vector_db.save_local(single_doc_index_path)

    vector_db = FAISS.from_documents(documents, embeddings)

    with open(embeddings_path, 'wb') as f:
        pickle.dump(documents, f)
    
    vector_db.save_local(faiss_index_path)
    
    return vector_db

faiss_index_path = 'faiss_index_store'
embeddings_path = 'embeddings_store.pkl'
single_doc_folder = 'single_docs'
os.makedirs(single_doc_folder, exist_ok=True)
vector_db = ingest_documents('data/', faiss_index_path, embeddings_path, single_doc_folder)
