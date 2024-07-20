import streamlit as st
import os
import pandas as pd
from PyPDF2 import PdfReader
from src.retriever.initialise import vector_db
from src.utils.documentInfo import documentInfo
from src.retriever.create_retriever import CreateRetriever

st.set_page_config(layout="wide")

retriever_instance = CreateRetriever(vector_db)
retriever = retriever_instance.get_retriever()

def invoke_retriever(query):
    if query:
        return retriever.invoke(query)
    else:
        return "Please enter a valid query to retrieve documents."

def read_csv_document(doc_name):
    doc_path = os.path.join(doc_name)
    return pd.read_csv(doc_path)

def read_pdf_document(doc_name):
    doc_path = os.path.join(doc_name)
    reader = PdfReader(doc_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def display_document_info(doc_info):
    relevant_document_info = next((info for info in documentInfo if info['filename'] == doc_info['source']), None)
    keywords = ", ".join(relevant_document_info['keywords']) if relevant_document_info else ""
    classification = relevant_document_info['classification'] if relevant_document_info else ""
    card_html = f"""
    <a href="?page=details&doc={doc_info['source']}" style="text-decoration: none; color: inherit;">
        <div style="width: 400px; border: 1px solid #ddd; padding: 15px; margin-bottom: 1px; border-radius: 10px; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); transition: transform 0.2s;"
            onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            <h4 style="font-size: 1.5em; margin: 0;">{doc_info['source']}</h4>
            <h5 style="font-size: 1.2em; color: #666; margin: 0;">Keywords: {keywords}</h5>
            <h5 style="font-size: 1.2em; color: #666; margin: 0;">Tag: {classification}</h5>
            <p style="font-size: 1em; color: #444;">Relevance: {doc_info['relevance_score']:.2f}</p>
        </div>
    </a>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def display_document_details(doc_name):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Document Content")
        if doc_name.endswith('.csv'):
            doc_content = read_csv_document(doc_name)
            st.dataframe(doc_content, height=600)
        elif doc_name.endswith('.pdf'):
            doc_content = read_pdf_document(doc_name)
            st.markdown(
                f"<div style='height: 600px; width: 100%; overflow-y: auto; border: 1px solid #ddd; padding: 10px;'>{doc_content}</div>",
                unsafe_allow_html=True
            )
        else:
            st.error("Unsupported file format")
    
    with col2:
        display_chatbot(doc_name)


def display_chatbot(doc_name):
    st.subheader("Document Information")
    doc_info = f"**Document Name:** {doc_name}<br>**Document Summary:** Short summary here."
    st.markdown(doc_info, unsafe_allow_html=True)
    
    st.subheader("Chatbot")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    display_chat_messages()

    key = "user_input_" + str(len(st.session_state.chat_history))
    user_message = st.text_input("Your message:", key=key)

    if st.button("Send", key="send_button"):
        if user_message.strip():
            add_message_to_chat_history(user_message)
            display_chat_messages()
            st.rerun()

def display_chat_messages():
    chat_display = "<div id='chat-area' style='height: 350px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; background-color: #f4f4f4;'>"
    for message in st.session_state.chat_history:
        chat_display += f"<div style='margin: 5px; padding: 5px;'>{message}</div>"
    chat_display += "</div>"
    st.markdown(chat_display, unsafe_allow_html=True)
    scroll_to_latest()

def add_message_to_chat_history(user_message):
    user_message_formatted = f"""
    <div style='display: flex; justify-content: flex-end; width: 100%; margin-bottom: 5px;'>
        <div style='color: blue; background-color: #e6e6ff; border-radius: 10px; padding: 5px; max-width: 200px;'>
            {user_message}
        </div>
    </div>"""
    
    st.session_state.chat_history.append(user_message_formatted)

    ai_response_text = "I have noted your message."
    ai_response = f"""
    <div style='display: flex; justify-content: flex-start; width: 100%; margin-bottom: 5px;'>
        <div style='color: green; background-color: #ccffcc; border-radius: 10px; padding: 5px; max-width: 200px;'>
            {ai_response_text}
        </div>
    </div>"""
    st.session_state.chat_history.append(ai_response)

def scroll_to_latest():
    st.markdown("""
    <script>
    setTimeout(function() {
        const chatArea = document.getElementById('chat-area');
        if(chatArea) {
            chatArea.scrollTop = chatArea.scrollHeight;
        }
    }, 500); // Delay to ensure the page has loaded
    </script>
    """, unsafe_allow_html=True)

def main():
    st.markdown("""
        <style>
        .reportview-container .main .block-container {
            max-width: 100%;
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("Document Search and Summary Interface")
    
    params = st.query_params
    if params and 'page' in params and params["page"] == "details" and 'doc' in params:
        doc_name = params["doc"]
        display_document_details(doc_name)
    else:
        query_input = st.text_input("Enter your search query here:", "")
        if query_input:
            response = invoke_retriever(query_input)
            if isinstance(response, str):
                st.error(response)
            else:
                response_message = response[0].page_content
                documents = [res.metadata for res in response]

                st.subheader("Query Response")
                st.write(response_message)

                st.subheader("Relevant Documents")
                cols_per_row = 4
                rows = [st.columns(cols_per_row) for _ in range((len(documents) + cols_per_row - 1) // cols_per_row)]
                index = 0
                for doc_info in documents:
                    col = rows[index // cols_per_row][index % cols_per_row]
                    with col:
                        display_document_info(doc_info)
                    index += 1

if __name__ == "__main__":
    main()
