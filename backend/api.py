from fastapi import FastAPI
from typing import Dict
from handleQuery import query_rag
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example function that performs an operation on the input string
def process_string(input_string: str) -> str:
    # Example: Reverse the string and convert to uppercase
   return query_rag(input_string)

# Define the GET endpoint
@app.get("/process")
async def process(input_string: str):
    if not input_string:
        raise HTTPException(status_code=400, detail="Input string cannot be empty")
    
    # Call the processing function
    processed_string = process_string(input_string)
    
    # Return the result
    return {"response": processed_string[0],"sources":processed_string[1]}