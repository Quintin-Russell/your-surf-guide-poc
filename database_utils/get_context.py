def get_context(question, collection):
    results = collection.query(
        query_texts=[question],
        n_results=2,
    )

    return "\n\n".join(results["documents"][0])
