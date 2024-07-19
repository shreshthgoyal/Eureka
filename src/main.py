from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.retriever.initialise import vector_db
from src.models.cult_rag_query import QueryInput, QueryOutput
from src.retriever.create_retriever import CreateRetriever
from src.utils.documentInfo import documentInfo
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever_instace = CreateRetriever(vector_db)
retriever = retriever_instace.get_retriever()

async def invokeRetreiver(query: str):
    if(query != None):
        return await retriever.ainvoke(query)
    else:
        return f"There seems to be some issue with this query, can you try this again?"

@app.get("/healthcheck")
async def get_status():
    return {"status": "running"}

@app.post("/search", response_model=QueryOutput)
async def searchDoc(query: QueryInput) -> QueryOutput:
    try:
        searchResponse = await invokeRetreiver(query.input)
        response_message = searchResponse[0].page_content
        
        doc_list = []
        for response in searchResponse:
            doc_list.append(response.metadata)
                    
        return QueryOutput(message=response_message, documents=doc_list, info= documentInfo)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app)

