import chromadb
from chromadb.config import Settings


def create_client(path="./chroma_db"):
    return chromadb.PersistentClient(path=path, settings=Settings(allow_reset=True))
