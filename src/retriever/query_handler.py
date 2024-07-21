from src.retriever.load_vectors import load_vector_db, load_single_document_vector_db

def query_all_documents(query, vector_db):
    docs = vector_db.similarity_search(query)
    return docs

def query_single_document(query, single_doc_embeddings):
    docs = single_doc_embeddings.similarity_search(query)
    return docs
