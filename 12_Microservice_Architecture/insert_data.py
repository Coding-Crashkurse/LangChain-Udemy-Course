from dotenv import find_dotenv, load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import os
import requests

load_dotenv(find_dotenv())

embeddings = OpenAIEmbeddings()

italian_loader = TextLoader("./FAQ/italian.txt")
italian_docs = italian_loader.load()
korean_loader = TextLoader("./FAQ/korean.txt")
korean_docs = korean_loader.load()
all_docs = italian_docs + korean_docs

for doc in all_docs:
    doc.metadata["source"] = os.path.splitext(os.path.basename(doc.metadata["source"]))[
        0
    ]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20,
)

documents = text_splitter.split_documents(all_docs)
docs_data = [doc.dict() for doc in documents]

url = "http://localhost:8000/ai_service/index"
response = requests.post(url, json=docs_data)
print(response.json())
