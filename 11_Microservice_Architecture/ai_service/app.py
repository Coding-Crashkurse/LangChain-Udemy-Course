from typing import Union, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
import openai
from langchain.prompts import PromptTemplate
import logging
from dotenv import find_dotenv, load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from fastapi import Header, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from langchain.schema import Document
from langchain.indexes import SQLRecordManager, index

ROLE_CLASS_MAP = {"assistant": AIMessage, "user": HumanMessage, "system": SystemMessage}

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = "postgresql+psycopg2://admin:admin@postgres:5432/vectordb"
COLLECTION_NAME = "vectordb"

namespace = f"pgvector/{COLLECTION_NAME}"
record_manager = SQLRecordManager(namespace, db_url=CONNECTION_STRING)
record_manager.create_schema()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Message(BaseModel):
    role: Optional[str]
    content: Optional[str]


class Conversation(BaseModel):
    conversation: List[Message]


class DocumentRequest(BaseModel):
    page_content: str
    metadata: dict


embeddings = OpenAIEmbeddings()
chat = ChatOpenAI(temperature=0)
vectorstore = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
)


prompt_template = """As a FAQ Bot for our restaurant, you have the following information about our restaurant:

{context}

Please provide the most suitable response for the users question.
Answer:"""

prompt = PromptTemplate(template=prompt_template, input_variables=["context"])
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)


def create_messages(conversation):
    return [
        ROLE_CLASS_MAP[message.role](content=message.content)
        for message in conversation
    ]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI, Header, HTTPException

app = FastAPI()


@app.post("/ai_service/index")
async def index_documents(docs_request: List[DocumentRequest]):
    documents = [
        Document(page_content=doc.page_content, metadata=doc.metadata)
        for doc in docs_request
    ]
    result = index(
        documents,
        record_manager,
        vectorstore,
        cleanup="incremental",
        source_id_key="source",
    )
    return result


@app.post("/ai_service/{conversation_id}")
async def ai_service(
    conversation_id: str, conversation: Conversation, store: str = Header(None)
):
    if not store:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="store header is required"
        )
    logger.info(f"Received store header: {store}")

    query = conversation.conversation[-1].content
    context = vectorstore.similarity_search(query=query, filter={"source": store})

    prompt = system_message_prompt.format(context=context)
    messages = [prompt] + create_messages(conversation=conversation.conversation)

    print(messages)
    result = chat(messages)
    print("RESULT: ", result)
    return {"id": conversation_id, "reply": result.content}
