from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    # 1. Format the retrieved chunks into a structured context block
    # Optional: You can filter out weak matches here (e.g., if item["distance"] > 0.7)
    context_entries = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        entry = f"Source {i} [Game: {chunk['game']}]:\n{chunk['text']}"
        context_entries.append(entry)
    
    context_block = "\n\n---\n\n".join(context_entries)

    # 2. Craft a strict system prompt to enforce grounding
    system_prompt = (
        "You are a strict rules assistant for board games. Your job is to answer the user's "
        "question using ONLY the provided Context below. \n\n"
        "CRITICAL RULES:\n"
        "1. Rely only on the clear facts directly mentioned in the Context. Do not use outside knowledge "
        "or assume/extrapolate rules not explicitly stated.\n"
        "2. Always explicitly mention which game(s) the rules and answers are coming from based on the metadata provided.\n"
        "3. If the Context does not contain the answer to the question, state clearly and honestly that "
        "the answer is not in the loaded rules. Do not make up an answer."
    )

    user_prompt = f"Context:\n{context_block}\n\nQuestion: {query}"

    # Call the Groq API
    try:
        completion = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,  # Low temperature reduces creativity and ensures factual consistency
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating the response: {str(e)}"