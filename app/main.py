
from fastapi import FastAPI
from pydantic import BaseModel
from .agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
import os
from .logger.logging import log_endpoint, logger

app=FastAPI()

from typing import List, Literal, Optional

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class QueryRequest(BaseModel):
    messages: List[Message]
    

@app.post("/query")
@log_endpoint
async def query_travel_agent(query: QueryRequest):
    logger.info(f"Received query: {query}")
    graph = GraphBuilder(model_provider="google")
    react_app = graph()

    png_graph = react_app.get_graph().draw_mermaid_png()
    with open("my_graph.png", "wb") as f:
        f.write(png_graph)

    logger.info(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

    # Pass the full conversation history to the agent
    messages = {"messages": [{"role": m.role, "content": m.content} for m in query.messages]}

    output = react_app.invoke(messages)

    # If result is dict with messages:
    if isinstance(output, dict) and "messages" in output:
        final_output = output["messages"][-1].content  # Last AI response
    else:
        final_output = str(output)

    logger.info(f"Returning answer: {final_output}")
    return {"answer": final_output}
