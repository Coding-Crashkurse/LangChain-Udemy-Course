from typing import Union, List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis
import requests
import json
import logging
from fastapi import Header, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

r = redis.Redis(host="redis", port=6379, db=0)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: Optional[str]
    content: Optional[str]


class Conversation(BaseModel):
    conversation: List[Message]


@app.get("/conversation_service/{conversation_id}")
async def get_conversation(conversation_id: str):
    logger.info(f"Retrieving initial id {conversation_id}")
    existing_conversation_json = r.get(conversation_id)
    if existing_conversation_json:
        existing_conversation = json.loads(existing_conversation_json)
        return existing_conversation
    else:
        return {"error": "Conversation not found"}


@app.post("/conversation_service/{conversation_id}")
async def conversation_service(
    conversation_id: str, conversation: Conversation, store: str = Header(None)
):
    if not store:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="store header is required"
        )

    logger.info(f"Sending Conversation with ID {conversation_id} to OpenAI")
    existing_conversation_json = r.get(conversation_id)
    if not existing_conversation_json:
        existing_conversation = {"conversation": []}
    else:
        existing_conversation = json.loads(existing_conversation_json)

    if conversation.model_dump()["conversation"]:
        existing_conversation["conversation"].append(
            conversation.model_dump()["conversation"][-1]
        )

    response = requests.post(
        f"http://ai_service:8000/ai_service/{conversation_id}",
        json=existing_conversation,
        headers={"store": store},
    )
    response.raise_for_status()
    assistant_message = response.json()["reply"]

    existing_conversation["conversation"].append(
        {"role": "assistant", "content": assistant_message}
    )

    r.set(conversation_id, json.dumps(existing_conversation))

    return existing_conversation
