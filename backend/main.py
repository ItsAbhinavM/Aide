from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent import agent

app= FastAPI()

# pydantic model schemas
class Prompt(BaseModel):
    question:str

class Response(BaseModel):
    response:str

@app.get("/health")
async def health_check():
    return {"Status":"OK","message":"Backend Running"}

@app.exception_handler(Exception)
async def global_exception_handler(request,exc):
    return JSONResponse(status_code=500,content={"error":str(exc)})

@app.get("/")
async def root():
    return {"message":"Hello"}

@app.post("/ask",response_model=Response)
async def ask_agent(query:Prompt):
    response=agent.invoke(query.question)
    return {"answer":response}