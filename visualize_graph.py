import os
from dotenv import load_dotenv
from app.agent.agentic_workflow import GraphBuilder
from langgraph.studio import visualize

# Load environment variables from .env if present
load_dotenv()

def main():
    # You can change the provider if needed ("groq" or "openai")
    graph = GraphBuilder(model_provider=os.getenv("MODEL_PROVIDER", "groq"))()
    print("Launching LangGraph Studio for visualization...")
    visualize(graph)

if __name__ == "__main__":
    main()
