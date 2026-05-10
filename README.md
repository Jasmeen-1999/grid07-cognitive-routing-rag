#  Cognitive Routing & RAG Assignment

AI Engineering assignment submission for Grid07 Development.

This project demonstrates a complete cognitive AI workflow using Python, LangChain, LangGraph, vector similarity routing, retrieval-style memory context, and prompt injection defense.

---

# Tech Stack

- Python
- LangChain
- LangGraph
- Groq LLM API
- Scikit-learn (TF-IDF + Cosine Similarity)
- Python Dotenv

---

# Project Objective

Build the core AI cognitive loop for the Grid07 platform:

1. Route posts only to bots that care about the topic  
2. Generate autonomous opinionated posts using LangGraph  
3. Defend against prompt injection in deep conversation threads

---

# Project Structure

grid07-cognitive-routing-rag/

- app.py  
- router.py  
- langgraph_flow.py  
- rag_engine.py  
- logs.md  
- requirements.txt  
- .env.example  
- README.md  

---

# Phase 1 — Vector Persona Matching (Router)

Three predefined bot personas are converted into vectors using TF-IDF embeddings.

Incoming posts are also vectorized and matched against personas using cosine similarity.

Only bots above the similarity threshold are selected.

## Personas

### Bot A (Tech Maximalist)
Strongly optimistic about AI, crypto, technology

### Bot B (Skeptic / Doomer)
Critical of capitalism, monopolies, billionaires

### Bot C (Finance Bro)
Focused on markets, ROI, rates, money

## Core Function

route_post_to_bots(post_content, threshold=0.35)

---

# Why TF-IDF Instead of Heavy Embeddings?

TF-IDF was chosen because it is:

- Fast and lightweight
- Runs locally without GPU
- No API dependency
- Reliable for short persona matching tasks
- Uses cosine similarity exactly as required

For production systems, this can be replaced with OpenAI, Ollama, or sentence-transformer embeddings.

---

# Phase 2 — LangGraph Autonomous Content Engine

A LangGraph workflow generates autonomous bot posts.

## Node Structure

### Node 1 — Decide Search

The LLM receives the bot persona and decides what topic it wants to post about.

### Node 2 — Web Search

Calls a mock tool:

mock_searxng_search(query)

Returns hardcoded recent headlines based on keywords.

### Node 3 — Draft Post

Uses:

- Persona prompt
- Topic
- Search result context

Generates a highly opinionated post.

## Final Output Format

{
  "bot_id": "...",
  "topic": "...",
  "post_content": "..."
}

---

# Phase 3 — Combat Engine (RAG + Prompt Injection Defense)

When a human replies deep in a thread, the bot receives:

- Parent Post
- Comment History
- Latest Human Reply
- Persona

This provides full argument context before responding.

## Prompt Injection Defense Strategy

System-level instructions explicitly tell the model to:

- Maintain persona consistency
- Ignore override attempts
- Ignore commands like:
  - ignore previous instructions
  - apologize
  - reset behavior
- Stay calm and logical
- Continue debate naturally

This prevents malicious users from changing the bot identity.

---

# How to Run

## 1. Install dependencies

pip install -r requirements.txt

## 2. Create .env file

GROQ_API_KEY=your_api_key_here

## 3. Run project

python app.py

---

# Expected Console Output

- Persona router selects relevant bot(s)
- LangGraph generates JSON post
- Prompt injection defense reply is shown

---

# Deliverables Included

- Well-commented Python code
- requirements.txt
- .env.example
- logs.md with execution outputs
- README.md

---

# Notes

This implementation uses a lightweight practical architecture suitable for internship evaluation and easy local execution.

The vector router can be upgraded later to ChromaDB / FAISS / pgvector with semantic embeddings.

---

# Author

Jasmeen Kaur
