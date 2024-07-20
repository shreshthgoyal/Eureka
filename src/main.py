from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.retriever.initialise import vector_db
from src.models.cult_rag_query import QueryInput, QueryOutput, SelectInput, SelectOutput, MessageInput, MessageOutput
from src.retriever.create_retriever import CreateRetriever
from src.utils.documentInfo import documentInfo
from src.chains.cultFaqChain import DocumentFAQChain
import uvicorn
import uuid
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever_instance = CreateRetriever(vector_db)
retriever = retriever_instance.get_retriever()

chat_sessions = {}

PORT = 8000

async def invokeRetriever(query: str):
    if query is not None:
        return await retriever.ainvoke(query)
    else:
        return "There seems to be some issue with this query, can you try this again?"

@app.get("/healthcheck")
async def get_status():
    logging.info("Health check endpoint called")
    return {"status": "running"}

@app.post("/search", response_model=QueryOutput)
async def searchDoc(query: QueryInput) -> QueryOutput:
    try:
        searchResponse = await invokeRetriever(query.input)
        response_message = searchResponse[0].page_content
        
        doc_list = []
        for response in searchResponse:
            doc_list.append(response.metadata)
                    
        return QueryOutput(message=response_message, documents=doc_list, info=documentInfo)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#This endpoint is called when a user selects a document from the search results, and wishes to talk to that document. Creates a new session by creating a new instance of the chain, and stores it
@app.post("/select", response_model=SelectOutput)
async def selectDoc(query: SelectInput) -> SelectOutput:
    try:
        selected_doc_retriever = CreateRetriever(vector_db, query.document_title).get_retriever()
        doc_chain = DocumentFAQChain(selected_doc_retriever)
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = doc_chain

        return SelectOutput(message="Document selected successfully.", session_id=session_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#This endpoint is called when user sends a message in the chatbox. Request object contains the session_id and the message; session_id was returned when instance was created. The chain instance corresponding to the session_id is retrieved and the message is passed to the chain instance
@app.post("/message", response_model=MessageOutput)
async def messageDoc(query: MessageInput) -> MessageOutput:
    try:
        if query.session_id not in chat_sessions:
            raise HTTPException(status_code=404, detail="Session ID not found")
        
        doc_chain = chat_sessions[query.session_id]
        response = doc_chain.invoke_chain(query.query)

        return MessageOutput(response=response, history=doc_chain.history)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == '__main__':
    
    logging.info(f"Starting server on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
