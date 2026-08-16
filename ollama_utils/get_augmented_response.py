import os
import ollama

def get_augmented_response(question, context: str, matching_spots, swell_direction, wind_direction, tide):
    # Step 2: AUGMENT - build a prompt that includes the retrieved context
    augmented_prompt = f"""You are a surf guide in Krui, South Sumatra, Indonesia. You only guide surfers who ride shortboards.
Your job is to recommend a surf spot given the real-world conditions below. Be concise with your answer, but give reasons for your choice.

Current conditions:
- Swell direction: {swell_direction} degrees
- Wind direction: {wind_direction} degrees
- Tide: {tide}

These spots already passed a hard filter and are known to accept the current conditions: {", ".join(matching_spots)}
Use the spot descriptions below (retrieved for relevance to the question) to explain why the spot is good right now and what to expect. Do not ask the user for more information - you already have everything you need.

Spot descriptions:
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
        "matching_spots": matching_spots,
        "context_used": context,
    }
