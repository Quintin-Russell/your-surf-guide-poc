from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

def create_embedding_model(model_name, url):
    return OllamaEmbeddingFunction(
        model_name=model_name,
        url=url
    )
