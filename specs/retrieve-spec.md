# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
[your answer here]
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
[your answer here]
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
[your answer here]
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
We will return all results up to `n_results` without hard-filtering them via a strict distance threshold in the retriever itself.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
(a) Empty Collection: We will wrap the query logic in a try/except block or check `_collection.count()`. If empty, it gracefully returns `[]`, bypassing the LLM entirely.
(b) Poor Matches: It will still return the closest chunks available. Because their distance scores will be exceptionally high (e.g., > 0.8), the LLM's system instructions will dictate it to say "I don't know based on the loaded rules."
(c) Multi-game Chunks: The returned list will transparently mix chunks from different games, ordered strictly by distance. The downstream generator will receive chunks labeled with their respective games and can disambiguate (e.g., "In Catan you do X, but in Risk you do Y").
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: How many cards do you start with in your hand?
Top result game: Ticket to Ride
Distance score: 0.2841
Does it make sense? Yes, the text chunk explicitly outlines initial setup and deal mechanics.
```

**One thing about the query results that surprised you:**

```
I was surprised by how much semantic weight shorter common words carried. Queries containing the word "die" occasionally pulled up rules regarding player elimination (dying) instead of actual 6-sided dice results if the surrounding context wasn't explicitly structured.
```
