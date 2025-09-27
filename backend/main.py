from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent

app= FastAPI()
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:1420",
    "http://127.0.0.1:1420",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://tauri.localhost",
    "tauri://localhost", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # origins - need to change it on prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

@app.post("/ask", response_model=Response)
async def ask_agent(query: Prompt):
    try:
        print("Received:", query.question)
        response = agent.invoke(query.question)
        print("Agent replied:", response)
        
        # Extract the actual text response from the agent response
        if isinstance(response, dict) and 'output' in response:
            response_text = response['output']
        elif hasattr(response, 'content'):
            response_text = response.content
        else:
            response_text = str(response)
            
        return {"response": response_text}
    except Exception as e:
        print("Error in /ask:", str(e))
        return {"response": f"Error: {str(e)}"}