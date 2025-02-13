import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
import dotenv

dotenv.load_dotenv()

def load_vector_db(faiss_index_path, embeddings_path):
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
    
    # Load embeddings and metadata
    with open(embeddings_path, 'rb') as f:
        documents = pickle.load(f)
    
    # Load FAISS vector store from local storage
    vector_db = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
    
    return vector_db, documents

def load_single_document_vector_db(doc_base_name, single_doc_folder):
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
    single_doc_index_path = os.path.join(single_doc_folder, f"{doc_base_name}_index")
    single_doc_embeddings_path = os.path.join(single_doc_folder, f"{doc_base_name}_embeddings.pkl")

    with open(single_doc_embeddings_path, 'rb') as f:
        single_doc = pickle.load(f)

    # Load FAISS vector store from local storage
    single_vector_db = FAISS.load_local(single_doc_index_path, embeddings, allow_dangerous_deserialization=True)

    return single_vector_db, single_doc
