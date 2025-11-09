from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uuid
import httpx
from typing import Dict, Any

app = FastAPI()

# ...existing code...
@app.get("/")
async def root():
    return {"message": "Welcome to Git-Ops-Bot-Backend"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
# ...existing code...

class WebhookRequest(BaseModel):
    branch: str
    commit_message: str
    author: str | None = None
    files: Dict[str, str] | None = None

# simple in-memory state store
IN_MEMORY_STATE: Dict[str, Dict[str, Any]] = {}

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/git-ops")

@app.post("/webhook")
async def post_to_n8n(payload: WebhookRequest):
    commit_id = str(uuid.uuid4())
    state = {
        "id": commit_id,
        "branch": payload.branch,
        "commit_message": payload.commit_message,
        "author": payload.author,
        "files": payload.files,
        "status": "pending",
        "n8n_response": None,
        "error": None,
    }
    IN_MEMORY_STATE[commit_id] = state

    # Mock mode short-circuits external call for tests
    if os.getenv("N8N_WEBHOOK_URL", "").lower() == "mock":
        state["status"] = "processed"
        state["n8n_response"] = {"mock": True, "payload": payload.dict(), "commit_id": commit_id}
        return {"commit_id": commit_id, "status": state["status"]}

    async with httpx.AsyncClient(timeout=10.0) as client:
        # ...existing code...
        try:
            # include commit_id so n8n can correlate responses
            resp = await client.post(N8N_WEBHOOK_URL, json={"commit_id": commit_id, **payload.dict()})
            resp.raise_for_status()
            state["status"] = "processed"
            try:
                state["n8n_response"] = resp.json()
            except Exception:
                state["n8n_response"] = {"text": resp.text}
        except httpx.RequestError as e:
            state["status"] = "error"
            state["error"] = f"request_error: {str(e)}"
        except httpx.HTTPStatusError as e:
            state["status"] = "error"
            state["error"] = f"http_error: {str(e)}"

    return {"commit_id": commit_id, "status": state["status"]}

@app.get("/state/{commit_id}")
async def get_state(commit_id: str):
    state = IN_MEMORY_STATE.get(commit_id)
    if not state:
        raise HTTPException(status_code=404, detail="commit_id not found")
    return state

@app.get("/state")
async def list_state():
    return {"count": len(IN_MEMORY_STATE), "items": list(IN_MEMORY_STATE.values())}