from fastapi import FastAPI
from typing import Dict
from scripts import query_rag
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    response: str
    sources: str

# Define the GET endpoint
@app.post("/query_llm")
def process_text(request: TextRequest) -> Dict[str, str]:
    print(request.text)
    if not request.text:
        raise HTTPException(status_code=400, detail="Input string cannot be empty")

    # Call the processing function
    res = query_rag(request.text)

    if not res or len(res) < 2:
        raise HTTPException(status_code=500, detail="Processing error")

    # Return the result
    return QueryResponse(response=res['response'], sources=res['sources']).dict()