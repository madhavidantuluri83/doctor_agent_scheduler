from fastapi import FastAPI
from pydantic import BaseModel

from graph.workflow import graph

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")

def chat(req: ChatRequest):

    result = graph.invoke({
        "user_input": req.message
    })

    return {
        "response": result["response"]
    }