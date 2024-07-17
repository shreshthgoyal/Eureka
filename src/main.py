from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.retriever.initialise import vector_db
from src.agents.cultRagAgent import CultAgentExecutor
from src.models.cult_rag_query import CultQueryInput, CultQueryOutput
from src.utils.async_util import async_retry
from src.apiResponse.actions import apiAction
from src.apiResponse.message import apiMessage
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
cult_agent_executor = CultAgentExecutor(retriever).get_executor()

async def invoke_agent_with_retry(query: str):
    if(query != None):
        return await cult_agent_executor.ainvoke({"input": query})
    else:
        return f"There seems to be some issue with this query, can you try this again?"

@app.get("/healthcheck")
async def get_status():
    return {"status": "running"}

@app.post("/cult-rag-agent", response_model=CultQueryOutput)
async def query_cult_agent(query: CultQueryInput) -> CultQueryOutput:
    try:
        query_response = await invoke_agent_with_retry(query.input)
        query_type = query_response['intermediate_steps'][0][0].__dict__['tool']

        # print(query_response)
        
        actions = apiAction(query.input, query_type, retriever_instace)
        if not isinstance(actions, list) or not all(isinstance(action, dict) for action in actions):
            actions = []
        
        query_response["message"] = apiMessage(query_type, query_response['output'])
        query_response["actions"] = actions

        return query_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app)

