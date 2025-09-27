# api.py
import asyncio
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from RAG import agent  # import your configured FunctionAgent
import os

# Load API key from environment variable (or hardcode for quick testing)
API_KEY = "lets-get-it-done"
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI(
    title="RAG API",
    description="Query UBS advisor knowledge base",
    version="1.0"
)

# Dependency to check API key
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate API KEY")


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_docs(request: QueryRequest, api_key: str = Depends(get_api_key)):
    """Endpoint to query the RAG system (API Key protected)."""
    response = await agent.run(request.query)
    return {"response": str(response)}
