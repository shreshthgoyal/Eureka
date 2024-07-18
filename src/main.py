from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.retriever.initialise import vector_db
from src.models.cult_rag_query import CultQueryInput, CultQueryOutput
from src.retriever.create_retriever import CreateRetriever
import uvicorn


app = FastAPI(
    title="AI Chatbot",
    description="Endpoints for a cult RAG chatbot",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever_instace = CreateRetriever(vector_db)
retriever = retriever_instace.get_retriever()

#here to call query through llm import and call from src/chainns -> cultFaqchain

async def invokeRetreiver(query: str):
    if(query != None):
        return await retriever.ainvoke(query)
    else:
        return f"There seems to be some issue with this query, can you try this again?"

@app.get("/healthcheck")
async def get_status():
    return {"status": "running"}

@app.post("/cult-rag-agent", response_model=CultQueryOutput)
async def query_cult_agent(query: CultQueryInput) -> CultQueryOutput:
    try:
        query_response = await invokeRetreiver(query.input)
        print("----------------------------------------------")
        print(query_response[0].page_content)
        print("----------------------------------------------")
        response_message = query_response[0].page_content
        return CultQueryOutput(message=response_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app)

