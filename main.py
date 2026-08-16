from dotenv import load_dotenv
import os
from database_utils.client import create_client
from database_utils.postgres_client import create_postgres_client
from database_utils.get_context import get_context
from database_utils.get_matching_spots import get_matching_spots
from database_utils.seed_descriptions import seed_descriptions
from ollama_utils.create_embedding_model import create_embedding_model
from ollama_utils.get_augmented_response import get_augmented_response
from fastapi import FastAPI
from chromadb.config import Settings


load_dotenv()
app = FastAPI()

pg_conn = create_postgres_client()

client = create_client()
client.reset()
ef = create_embedding_model(os.getenv("TEXT_PROCESSING_MODEL"), os.getenv("OLLAMA_URL"))
collection = client.get_or_create_collection(
    name=os.getenv("CHROMADB_COLLECTION_NAME"),
    embedding_function=ef,
)
seed_descriptions(collection)

@app.get("/ask")
def ask(swell_direction: float, wind_direction: float, tide: str, question: str = "Where should I surf right now?"):
    # HARD FILTER: real-world numbers against each spot's acceptable window (Postgres, plain math).
    matching_slugs = get_matching_spots(pg_conn, swell_direction, wind_direction, tide)

    if not matching_slugs:
        return {
            "question": question,
            "answer": "No spots match those conditions right now.",
            "context_used": "",
        }

    # SEMANTIC LAYER: only search description chunks belonging to spots that already passed the filter.
    context = get_context(question, collection, candidate_spot_names=matching_slugs)
    return get_augmented_response(question, context, matching_slugs, swell_direction, wind_direction, tide)
