import os
import ollama

def get_augmented_response(question, context: str):  # FastAPI automatically reads "question" from the URL query string
    # Step 2: AUGMENT - build a prompt that includes the retrieved context
    augmented_prompt = f"""Use the following context to answer the question.
If the context doesn't contain relevant information, say so.

Context:
Assume that you are a surf guide in krui, south sumatra, indonesia. ypu only guide surfers that surf shortboards.
{context}

Question: {question}"""

    # Step 3: GENERATE - send the augmented prompt to the local LLM
    response = ollama.chat(
        model=os.getenv("OLLAMA_MODEL_NAME"),
        messages=[{"role": "user", "content": augmented_prompt}],
    )

    # Return the answer along with the context so users can verify the source
    return {
        "question": question,
        "answer": response["message"]["content"],
        "context_used": context,
    }
