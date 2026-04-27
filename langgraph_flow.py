# langgraph_flow.py

from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.tools import tool
import json

# --------------------------------------------------
# Load environment variables from .env
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Initialize Groq LLM
# --------------------------------------------------
llm = ChatGroq(model="llama-3.1-8b-instant")


# --------------------------------------------------
# TOOL: Mock Search Engine
# Simulates recent web headlines based on keywords
# --------------------------------------------------
@tool
def mock_searxng_search(query: str):
    """Simulates a search engine and returns recent headlines."""

    query = query.lower()

    if "crypto" in query or "web3" in query or "defi" in query:
        return "Bitcoin hits new all-time high amid ETF approvals."

    elif "ai" in query:
        return "AI models are rapidly replacing junior developers in tech industry."

    elif "finance" in query or "market" in query:
        return "Global markets rally as interest rates stabilize."

    return "Latest global tech trends are evolving rapidly."


# --------------------------------------------------
# LangGraph State Schema
# Stores data passed between nodes
# --------------------------------------------------
class GraphState(TypedDict):
    bot_id: str
    persona: str
    topic: str
    search_result: str
    post_content: dict


# --------------------------------------------------
# NODE 1: Decide Topic
# LLM chooses one trending topic based on persona
# --------------------------------------------------
def decide_topic(state):

    prompt = f"""
Persona:
{state['persona']}

Suggest ONE trending topic this persona would post about.

Respond with ONLY the topic name.
"""

    response = llm.invoke(prompt)

    # Clean topic text
    topic = response.content.strip().replace('"', "")

    return {"topic": topic}


# --------------------------------------------------
# NODE 2: Search Tool
# Uses topic as search query
# --------------------------------------------------
def search(state):

    result = mock_searxng_search.invoke(state["topic"])

    return {"search_result": result}


# --------------------------------------------------
# NODE 3: Generate Post
# Uses persona + topic + search context
# Returns strict JSON output
# --------------------------------------------------
def generate_post(state):

    prompt = f"""
Persona:
{state['persona']}

Topic:
{state['topic']}

Context:
{state['search_result']}

Write a highly opinionated social media post (max 280 characters).

Return ONLY valid JSON in this format:

{{
  "bot_id": "{state['bot_id']}",
  "topic": "{state['topic']}",
  "post_content": "your post here"
}}

Do not include markdown.
Do not include explanation.
Do not nest JSON.
"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    # ----------------------------------------------
    # Try parsing model response as JSON
    # ----------------------------------------------
    try:
        parsed = json.loads(raw)

    except:
        # If parsing fails, fallback clean structure
        parsed = {
            "bot_id": state["bot_id"],
            "topic": state["topic"],
            "post_content": raw
        }

    # ----------------------------------------------
    # Clean topic field
    # ----------------------------------------------
    topic = str(parsed.get("topic", state["topic"])).replace('"', "").strip()

    # ----------------------------------------------
    # Clean post_content field
    # ----------------------------------------------
    post = str(parsed.get("post_content", "")).strip()

    # If model nested JSON inside post_content
    if post.startswith("{") and post.endswith("}"):

        try:
            inner = json.loads(post)

            if isinstance(inner, dict):
                post = inner.get("post_content", post)

        except:
            pass

    # Remove line breaks / extra spaces
    post = post.replace("\n", " ").strip()

    # Final guaranteed structure
    final_output = {
        "bot_id": state["bot_id"],
        "topic": topic,
        "post_content": post
    }

    return {"post_content": final_output}


# --------------------------------------------------
# Build LangGraph Workflow
# decide -> search -> generate
# --------------------------------------------------
builder = StateGraph(GraphState)

builder.add_node("decide", decide_topic)
builder.add_node("search", search)
builder.add_node("generate", generate_post)

builder.set_entry_point("decide")

builder.add_edge("decide", "search")
builder.add_edge("search", "generate")

graph = builder.compile()


# --------------------------------------------------
# Main Runner Function
# Runs full graph for one bot
# --------------------------------------------------
def run_agent(bot_id, persona):

    result = graph.invoke({
        "bot_id": bot_id,
        "persona": persona
    })

    return result["post_content"]