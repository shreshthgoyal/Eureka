import streamlit as st
from src.retriever.initialise import vector_db
from src.retriever.create_retriever import CreateRetriever
from src.utils.documentInfo import documentInfo

# Initialize the document retriever
retriever_instance = CreateRetriever(vector_db)
retriever = retriever_instance.get_retriever()

def invoke_retriever(query):
    if query:
        return retriever.invoke(query)
    else:
        return "Please enter a valid query to retrieve documents."

st.title("Document Search and Summary Interface")
query_input = st.text_input("Enter your search query here:", "")

if query_input:
    response = invoke_retriever(query_input)
    if isinstance(response, str):
        st.error(response)
    else:
        response_message = response[0].page_content
        documents = [res.metadata for res in response]
        info = documentInfo  # Assuming documentInfo is a list of dicts with details

        st.subheader("Query Response")
        st.write(response_message)

        st.subheader("Relevant Documents")
        # Create a grid of cards for documents
        cols_per_row = 3
        rows = [st.columns(cols_per_row) for _ in range((len(documents) + cols_per_row - 1) // cols_per_row)]
        index = 0
        for doc_info in documents:
            col = rows[index // cols_per_row][index % cols_per_row]
            with col:
                doc_summary = next((item for item in info if item['filename'] == doc_info['source']), None)
                st.markdown(f"**{doc_info['source']}**")
                st.text(f"Relevance: {doc_info['relevance_score']:.2f}")
                if doc_summary:
                    st.text(f"Summary: {doc_summary['summary']}")
                    st.text(f"Keywords: {', '.join(doc_summary['keywords'])}")
                    st.text(f"Classification: {doc_summary['classification']}")
                st.write("---")
            index += 1
