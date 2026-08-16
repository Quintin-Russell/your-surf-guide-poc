def get_context(question, collection, candidate_spot_names=None, n_results=2):
    query_kwargs = {"query_texts": [question], "n_results": n_results}

    if candidate_spot_names is not None:
        query_kwargs["where"] = {"source": {"$in": candidate_spot_names}}

    results = collection.query(**query_kwargs)

    return "\n\n".join(results["documents"][0])
