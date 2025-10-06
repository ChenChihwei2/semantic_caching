# Semantic Caching System

## Overview
This project implements a semantic caching mechanism designed to reduce redundant large language model (LLM) calls by reusing semantically similar past responses.  
The goal is to lower both latency and API costs by retrieving cached responses whenever a new query is sufficiently similar to an earlier one, avoiding unnecessary LLM inference.

This prototype demonstrates how caching can accelerate repeated user interactions, but it also exposes several technical challenges, especially with context handling, prompt contamination, and cache reliability.

---

## System Architecture
The program consists of three primary modules:

1. **`main.py`** handles user input, cache search, and LLM invocation.  
2. **`cache.py`** performs semantic similarity checks and manages vector-based storage and retrieval.  
3. **`session_manager.py`** manages session state and user context for multi-turn conversations.

The system uses:
- **Language:** Python  
- **Vector Store:** [ChromaDB](https://www.trychroma.com/) for simplicity and local deployment  
- **Embedding Model:** Google Gemini `text-embedding-004`  
- **Similarity Metric:** Cosine distance, with `1 - cosine_distance` used for similarity comparison  

A similarity threshold of **0.78** was chosen after reviewing semantic search literature. Queries above this threshold are considered similar enough to reuse cached responses.

---

## Methodology

### Embedding and Context Construction
The system tries to create context-aware embeddings by including the last two conversation turns in the embedding process.  
This helps preserve some dialogue continuity but introduces a key flaw called **prompt contamination**, where irrelevant parts of previous turns dominate the embedding vector and lead to incorrect cache hits.

Longer or context-heavy prompts amplify this issue because added noise shifts the embedding away from the user’s actual intent.

### Similarity Search
The cache performs a nearest-neighbor lookup using Chroma’s cosine similarity with `n_results=1`.  
This design trusts Chroma to rank results correctly, but in practice it often favors verbose or context-rich prompts over truly relevant ones.

### Cache Insertion
When no match exceeds the threshold:

1. The query is sent to the LLM for a new response.  
2. The response and its embedding are stored in the cache for future reuse.

Currently, the system:

- Does not check for duplicates before insertion.  
- Lacks a selection policy to decide which of multiple near-duplicate prompts to keep.  
- Does not handle cache staleness or expiration of outdated information.

---

## Observations

### Performance
- Cached responses are returned almost instantly.  
- LLM-generated responses have noticeable delay, especially for long answers.  
- For short or repeated prompts, the cache consistently saves time and cost.

### Relevance vs. Precision
- The 0.78 threshold balances recall and precision but is imperfect.  
  - Lower thresholds increase false positives with irrelevant responses.  
  - Higher thresholds increase false negatives and miss usable cache hits.  
- For longer or multi-turn queries, similarity scores become less reliable due to embedding drift caused by mixed context.

---

## Known Limitations and Pitfalls

1. **Context Contamination:**  
   Including full conversation history pollutes embeddings and produces irrelevant cache matches. A more selective or weighted approach is needed.  

2. **Duplicate and Conflicting Entries:**  
   Similar prompts with different detail levels can create contradictory responses. There is no deduplication or conflict resolution.  

3. **Trust in Chroma’s Retrieval Heuristic:**  
   Using only one top result assumes the highest-ranked entry is always correct, which is not true when embeddings are dominated by context length or verbosity.  

4. **Scaling and Latency:**  
   As the cache grows, embedding time and retrieval cost increase. Chroma’s local storage also limits scalability for larger deployments.  

5. **Undefined Cache Aging:**  
   The system cannot invalidate or down-rank outdated cache entries. Old responses may continue to appear even when they are no longer correct.  

6. **Semantic Ambiguity in Long Queries:**  
   Long prompts can partially overlap with unrelated topics, creating misleadingly high similarity scores and incorrect cache hits.

---

## Planned Improvements

- **Sliding Context Window:** Use a dynamic memory window that adjusts based on conversation depth to minimize contamination.  
- **Similarity Decay:** Introduce a decay function where older embeddings gradually lose relevance.  
- **Duplicate Filtering:** Detect near-duplicates before insertion to prevent cache bloat and fragmentation.  
- **Logging System:** Add module-level logging for error tracking and debugging.  
- **Scalability Upgrade:** Replace ChromaDB with Redis or FAISS for better performance and scale.  
- **Embedding Benchmarking:** Compare Gemini embeddings with OpenAI `text-embedding-3-large` to evaluate precision and resistance to contamination.

---

## Evaluation and Reflections

- **Speed:** Clear latency improvement for repeated prompts.  
- **Reliability:** Highlighted meaningful flaws in naive context inclusion.  
- **Scalability:** Works for prototypes but not ready for production-level caching.  
- **Awareness:** Each identified failure mode, from contamination to duplicate handling, informs how to design a more intelligent caching layer.

---

## Conclusion
This project explores the strengths and weaknesses of semantic caching in LLM-driven systems.  
It shows that caching can significantly reduce cost and latency, but it also proves how sensitive retrieval accuracy is to embedding design, context inclusion, and similarity thresholds.  

The system functions as both a working proof of concept and a technical study in the complexity of building scalable, context-aware semantic caching mechanisms.

---
## Running the Program

To run the program, follow these steps:

1. Create a `.env` file in the project root directory and add your API key:
   ```bash
   GEMINI_API_KEY="your_api_key"
    ````

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the program:

Make sure you are in the dsrs folder. Then proceed to type the following command:
   ```bash
   python -m src.main
   ```

5. Closing the program:

To simply close the prompt terminal type: "quit", "exit"

After completing these steps, you can interact with the program directly through the command line.

```
```
