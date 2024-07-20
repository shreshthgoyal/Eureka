# query_handler.py

from load_vectors import load_vector_db, load_single_document_vector_db

def query_all_documents(query, vector_db):
    docs = vector_db.similarity_search(query)
    return docs

def query_single_document(query, single_doc_embeddings):
    docs = single_doc_embeddings.similarity_search(query)
    return docs

# Load the FAISS index and embeddings for all documents
faiss_index_path = 'faiss_index_store'
embeddings_path = 'embeddings_store.pkl'
single_doc_folder = 'single_docs'
vector_db, _ = load_vector_db(faiss_index_path, embeddings_path)

query = "What is the policy on data privacy?"
all_docs_results = query_all_documents(query, vector_db)
print(f"Results from all documents: {[doc.page_content for doc in all_docs_results]}")

# Load the FAISS index and embeddings for a single document
doc_base_name = 'example_document'  # Change this to the actual document base name
single_vector_db, _ = load_single_document_vector_db(doc_base_name, single_doc_folder)
single_doc_results = query_single_document(query, single_vector_db)
print(f"Results from single document: {[doc.page_content for doc in single_doc_results]}")
