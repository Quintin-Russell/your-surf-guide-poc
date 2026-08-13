from dotenv import load_dotenv
import os
from database_utils.client import create_client
from database_utils.get_context import get_context
from ollama_utils.create_embedding_model import create_embedding_model
from ollama_utils.get_augmented_response import get_augmented_response
from helpers.chunk_text_from_file import chunk_text_from_file
from fastapi import FastAPI
from chromadb.config import Settings


load_dotenv()
app = FastAPI()

client = create_client()
client.reset()
ef = create_embedding_model(os.getenv("TEXT_PROCESSING_MODEL"), os.getenv("OLLAMA_URL"))
collection = client.get_or_create_collection(
    name=os.getenv("CHROMADB_COLLECTION_NAME"),
    embedding_function=ef,
)
for spot_file in os.listdir("info"):
    file_name = f"info/{spot_file}"

    if os.path.isfile(file_name):
        chunks = chunk_text_from_file(file_name)
        spot_name = spot_file[:-4]

        collection.add(
            ids= [f"{spot_name}chunk{i}" for i in range(len(chunks))],
            documents=chunks,
            metadatas=[{"source": spot_name, "chunk_index": i} for i in range(len(chunks))],
        )
        print(f"{spot_name} processed: {len(chunks)} processed")
    else:
        print(f"Error reading: {file_name}; it is not a file")

@app.get("/ask")
def ask(question):
    context = get_context(question, collection)
    return get_augmented_response(question, context)
